from typing import List

from unstructured.documents.elements import Element


class MockUnstructuredClass(object):
    @staticmethod
    def partition_md() -> List[Element]:
        element = Element(
            category="title",
            embeddings=[],
            id="test",
            metadata={},
            text="test"
        )
        return [element]

    @staticmethod
    def partition_text() -> List[Element]:
        element = Element(
            category="title",
            embeddings=[],
            id="test",
            metadata={},
            text="test"
        )
        return [element]


    @staticmethod
    def chunk_by_title() -> List[Element]:
        element = Element(
            category="title",
            embeddings=[],
            id="test",
            metadata={},
            text="test"
        )
        return [element]
