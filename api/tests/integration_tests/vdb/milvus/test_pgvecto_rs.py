from core.rag.datasource.vdb.milvus.milvus_vector import MilvusConfig, MilvusVector
from core.rag.datasource.vdb.pgvecto_rs.pgvecto_rs import PgvectoRSConfig, PGVectoRS
from tests.integration_tests.vdb.test_vector_store import (
    AbstractTestVector,
    get_sample_text,
    setup_mock_redis,
)


class TestPgvectoRSVector(AbstractTestVector):
    def __init__(self):
        super().__init__()
        self.vector = PGVectoRS(
            collection_name=self.collection_name,
            config=PgvectoRSConfig(
                host='localhost',
                port=5432,
                user='postgres',
                password='dify123456',
                database='postgres',
            ),
            dim=3
        )

    def search_by_full_text(self):
        # pgvecto rs only support english text search, So it’s not open for now
        hits_by_full_text = self.vector.search_by_full_text(query=get_sample_text())
        assert len(hits_by_full_text) == 0


def test_milvus_vector(setup_mock_redis):
    TestPgvectoRSVector().run_all_test()
