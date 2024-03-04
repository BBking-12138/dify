import os
from typing import Callable, List, Literal

import pytest
# import monkeypatch
from _pytest.monkeypatch import MonkeyPatch
from pymilvus import Connections, MilvusClient
from pymilvus.orm import utility
from qdrant_client import QdrantClient
from unstructured.chunking.title import chunk_by_title
from unstructured.partition.md import partition_md
from tests.integration_tests.model_runtime.__mock.openai_completion import MockCompletionsClass
from tests.integration_tests.rag.__mock.milvus_function import MockMilvusClass
from tests.integration_tests.rag.__mock.qdrant_function import MockQdrantClass
from tests.integration_tests.rag.__mock.unstructured_function import MockUnstructuredClass


def mock_milvus(monkeypatch: MonkeyPatch, methods: List[Literal["get_collections", "delete", "recreate_collection", "create_payload_index", "upsert", "scroll", "search"]]) -> Callable[[], None]:
    """
        mock unstructured module

        :param monkeypatch: pytest monkeypatch fixture
        :return: unpatch function
    """
    def unpatch() -> None:
        monkeypatch.undo()

    if "connect" in methods:
        monkeypatch.setattr(Connections, "connect", MockMilvusClass.delete())
    if "get_collections" in methods:
        monkeypatch.setattr(utility, "has_collection", MockMilvusClass.get_collections())
    if "insert" in methods:
        monkeypatch.setattr(MilvusClient, "insert", MockMilvusClass.insert())
    if "create_payload_index" in methods:
        monkeypatch.setattr(QdrantClient, "create_payload_index", MockMilvusClass.create_payload_index())
    if "upsert" in methods:
        monkeypatch.setattr(QdrantClient, "upsert", MockMilvusClass.upsert())
    if "scroll" in methods:
        monkeypatch.setattr(QdrantClient, "scroll", MockMilvusClass.scroll())
    if "search" in methods:
        monkeypatch.setattr(QdrantClient, "search", MockMilvusClass.search())

    return unpatch


MOCK = os.getenv('MOCK_SWITCH', 'false').lower() == 'true'

@pytest.fixture
def setup_milvus_mock(request, monkeypatch):
    methods = request.param if hasattr(request, 'param') else []
    if MOCK:
        unpatch = mock_milvus(monkeypatch, methods=methods)
    
    yield

    if MOCK:
        unpatch()

