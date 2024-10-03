from configs import dify_config

HIDDEN_VALUE = "[__HIDDEN__]"
UUID_NIL = "00000000-0000-0000-0000-000000000000"

IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp", "gif", "svg"]
IMAGE_EXTENSIONS.extend([ext.upper() for ext in IMAGE_EXTENSIONS])

VIDEO_EXTENSIONS = ["mp4", "mov", "mpeg", "mpga"]
VIDEO_EXTENSIONS.extend([ext.upper() for ext in VIDEO_EXTENSIONS])

AUDIO_EXTENSIONS = ["mp3", "m4a", "wav", "webm", "amr"]
AUDIO_EXTENSIONS.extend([ext.upper() for ext in AUDIO_EXTENSIONS])

DOCUMENT_EXTENSIONS = ["txt", "markdown", "md", "html", "htm", "xml", "pdf", "xlsx", "xls", "docx", "doc", "csv", "pptx", "ppt", "epub", "eml", "msg"]  # noqa: E501
DOCUMENT_EXTENSIONS.extend([ext.upper() for ext in DOCUMENT_EXTENSIONS])
