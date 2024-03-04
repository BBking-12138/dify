import os
from typing import Callable, List, Literal

import pytest
# import monkeypatch
from _pytest.monkeypatch import MonkeyPatch
from unstructured.chunking import title
from unstructured.partition import md, text
from tests.integration_tests.rag.__mock.unstructured_function import MockUnstructuredClass


def mock_unstructured(monkeypatch: MonkeyPatch, methods: List[Literal["partition_md", "chunk_by_title"]]) -> Callable[[], None]:
    """
        mock unstructured module

        :param monkeypatch: pytest monkeypatch fixture
        :return: unpatch function
    """
    def unpatch() -> None:
        monkeypatch.undo()

    if "partition_md" in methods:
        monkeypatch.setattr(md, "partition_md", MockUnstructuredClass.partition_md())
    if "partition_text" in methods:
        monkeypatch.setattr(text, "partition_text", MockUnstructuredClass.partition_text())
    if "chunk_by_title" in methods:
        monkeypatch.setattr(title, "chunk_by_title", MockUnstructuredClass.chunk_by_title())

    return unpatch


MOCK = os.getenv('MOCK_SWITCH', 'false').lower() == 'true'


@pytest.fixture
def setup_unstructured_mock(request, monkeypatch):
    methods = request.param if hasattr(request, 'param') else []
    if MOCK:
        unpatch = mock_unstructured(monkeypatch, methods=methods)
    
    yield

    if MOCK:
        unpatch()

