import mimetypes
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any

from sqlalchemy import select

from constants import AUDIO_EXTENSIONS, DOCUMENT_EXTENSIONS, IMAGE_EXTENSIONS, VIDEO_EXTENSIONS
from core.file import File, FileBelongsTo, FileExtraConfig, FileTransferMethod, FileType
from core.helper import ssrf_proxy
from extensions.ext_database import db
from models import UploadFile

if TYPE_CHECKING:
    from enums import CreatedByRole
    from models import MessageFile


def build_from_message_files(
    *,
    message_files: Sequence["MessageFile"],
    tenant_id: str,
    config: FileExtraConfig,
) -> Sequence[File]:
    results = [
        build_from_message_file(message_file=file, tenant_id=tenant_id, config=config)
        for file in message_files
        if file.belongs_to != FileBelongsTo.ASSISTANT
    ]
    return results


def build_from_message_file(
    *,
    message_file: "MessageFile",
    tenant_id: str,
    config: FileExtraConfig,
):
    return File(
        id=message_file.id,
        tenant_id=tenant_id,
        type=FileType.value_of(message_file.type),
        transfer_method=FileTransferMethod.value_of(message_file.transfer_method),
        remote_url=message_file.url,
        related_id=message_file.upload_file_id or None,
        _extra_config=config,
    )


def build_from_mapping(
    *,
    mapping: Mapping[str, Any],
    tenant_id: str,
    user_id: str,
    role: "CreatedByRole",
    config: FileExtraConfig,
):
    transfer_method = FileTransferMethod.value_of(mapping.get("transfer_method"))
    match transfer_method:
        case FileTransferMethod.REMOTE_URL:
            file = _build_from_remote_url(
                mapping=mapping,
                tenant_id=tenant_id,
                config=config,
                transfer_method=transfer_method,
            )
        case FileTransferMethod.LOCAL_FILE:
            file = _build_from_local_file(
                mapping=mapping,
                tenant_id=tenant_id,
                user_id=user_id,
                role=role,
                config=config,
                transfer_method=transfer_method,
            )
        case FileTransferMethod.TOOL_FILE:
            file = File(
                tenant_id=tenant_id,
                type=FileType.value_of(mapping.get("type")),
                transfer_method=transfer_method,
                remote_url=None,
                related_id=mapping.get("tool_file_id"),
                _extra_config=config,
            )
        case _:
            raise ValueError(f"Invalid file transfer method: {transfer_method}")

    return file


def build_from_mappings(
    *,
    mappings: Sequence[Mapping[str, Any]],
    config: FileExtraConfig | None,
    tenant_id: str,
    user_id: str,
    role: "CreatedByRole",
) -> Sequence[File]:
    if not config:
        return []

    files = [
        build_from_mapping(
            mapping=mapping,
            tenant_id=tenant_id,
            user_id=user_id,
            role=role,
            config=config,
        )
        for mapping in mappings
    ]

    if (
        # If image config is set.
        config.image_config
        # And the number of image files exceeds the maximum limit
        and sum(1 for _ in (filter(lambda x: x.type == FileType.IMAGE, files))) > config.image_config.number_limits
    ):
        raise ValueError(f"Number of image files exceeds the maximum limit {config.image_config.number_limits}")
    if config.number_limits and len(files) > config.number_limits:
        raise ValueError(f"Number of files exceeds the maximum limit {config.number_limits}")

    return files


def _build_from_local_file(
    *,
    mapping: Mapping[str, Any],
    tenant_id: str,
    user_id: str,
    role: "CreatedByRole",
    config: FileExtraConfig,
    transfer_method: FileTransferMethod,
):
    # check if the upload file exists.
    file_type = FileType.value_of(mapping.get("type"))
    stmt = select(UploadFile).where(
        UploadFile.id == mapping.get("upload_file_id"),
        UploadFile.tenant_id == tenant_id,
        UploadFile.created_by == user_id,
        UploadFile.created_by_role == role,
    )
    if file_type == FileType.IMAGE:
        stmt = stmt.where(UploadFile.extension.in_(IMAGE_EXTENSIONS))
    elif file_type == FileType.VIDEO:
        stmt = stmt.where(UploadFile.extension.in_(VIDEO_EXTENSIONS))
    elif file_type == FileType.AUDIO:
        stmt = stmt.where(UploadFile.extension.in_(AUDIO_EXTENSIONS))
    elif file_type == FileType.DOCUMENT:
        stmt = stmt.where(UploadFile.extension.in_(DOCUMENT_EXTENSIONS))
    row = db.session.scalar(stmt)
    if row is None:
        raise ValueError("Invalid upload file")
    file = File(
        filename=row.name,
        extension=row.extension,
        mime_type=row.mime_type,
        tenant_id=tenant_id,
        type=file_type,
        transfer_method=transfer_method,
        remote_url=None,
        related_id=mapping.get("upload_file_id"),
        _extra_config=config,
        size=row.size,
    )
    return file


def _build_from_remote_url(
    *,
    mapping: Mapping[str, Any],
    tenant_id: str,
    config: FileExtraConfig,
    transfer_method: FileTransferMethod,
):
    url = mapping.get("url")
    if not url:
        raise ValueError("Invalid file url")
    resp = ssrf_proxy.head(url)
    resp.raise_for_status()
    file_size = int(resp.headers.get("Content-Length", 0))
    mime_type = str(resp.headers.get("Content-Type", ""))
    if not mime_type:
        mime_type, _ = mimetypes.guess_type(url)
    file = File(
        tenant_id=tenant_id,
        type=FileType.value_of(mapping.get("type")),
        transfer_method=transfer_method,
        remote_url=url,
        _extra_config=config,
        mime_type=mime_type,
        size=file_size,
    )
    return file
