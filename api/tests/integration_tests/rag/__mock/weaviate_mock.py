import os
from typing import Callable, List, Literal

import pytest
# import monkeypatch
from _pytest.monkeypatch import MonkeyPatch
from qdrant_client import QdrantClient
from unstructured.chunking.title import chunk_by_title
from unstructured.partition.md import partition_md
from weaviate.batch import Batch
from weaviate.gql.get import GetBuilder
from weaviate.schema import Schema

from tests.integration_tests.model_runtime.__mock.openai_completion import MockCompletionsClass
from tests.integration_tests.rag.__mock.qdrant_function import MockQdrantClass
from tests.integration_tests.rag.__mock.weaviate_function import MockWeaviateClass


def mock_weaviate(monkeypatch: MonkeyPatch, methods: List[Literal["get_collections", "delete", "recreate_collection", "create_payload_index", "upsert", "scroll", "search"]]) -> Callable[[], None]:
    """
        mock unstructured module

        :param monkeypatch: pytest monkeypatch fixture
        :return: unpatch function
    """
    def unpatch() -> None:
        monkeypatch.undo()

    if "delete" in methods:
        monkeypatch.setattr(Schema, "delete", MockWeaviateClass.delete_class())
    if "contains" in methods:
        monkeypatch.setattr(Schema, "contains", MockWeaviateClass.contains())
    if "add_data_object" in methods:
        monkeypatch.setattr(Batch, "add_data_object", MockWeaviateClass.add_data_object())
    if "do" in methods:
        monkeypatch.setattr(GetBuilder, "do", MockWeaviateClass.do())

    return unpatch


MOCK = os.getenv('MOCK_SWITCH', 'false').lower() == 'true'

@pytest.fixture
def setup_weaviate_mock(request, monkeypatch):
    methods = request.param if hasattr(request, 'param') else []
    if MOCK:
        unpatch = mock_weaviate(monkeypatch, methods=methods)
    
    yield

    if MOCK:
        unpatch()

