import pytest

from core.rag.datasource.vdb.qdrant.qdrant_vector import QdrantVector, QdrantConfig
from core.rag.models.document import Document


@pytest.mark.parametrize('setup_qdrant_mock',
                         [['get_collections', 'recreate_collection',
                           'create_payload_index', 'upsert', 'scroll',
                           'search']],
                         indirect=True)
def test_qdrant(setup_qdrant_mock):
    document = Document(page_content="test", metadata={"test": "test"})
    qdrant_vector = QdrantVector(
        collection_name="test",
        group_id='test',
        config=QdrantConfig(
            endpoint="http://localhost:6333",
            api_key="test",
            root_path="test",
            timeout=10
        )
    )
    # create
    qdrant_vector.create(texts=[document], embeddings=[[0.23333 for _ in range(233)]])
    # search
    result = qdrant_vector.search_by_vector(query_vector=[0.23333 for _ in range(233)])
    for item in result:
        assert isinstance(item, Document)
    # delete
    qdrant_vector.delete()

