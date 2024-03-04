from typing import List, Optional, Tuple
from qdrant_client.conversions import common_types as types


class MockQdrantClass(object):

    @staticmethod
    def get_collections() -> types.CollectionsResponse:
        collections_response = types.CollectionsResponse(
            collections=["test"]
        )
        return collections_response

    @staticmethod
    def recreate_collection() -> bool:
        return True

    @staticmethod
    def create_payload_index() -> types.UpdateResult:
        update_result = types.UpdateResult(
            updated=1
        )
        return update_result

    @staticmethod
    def upsert() -> types.UpdateResult:
        update_result = types.UpdateResult(
            updated=1
        )
        return update_result

    @staticmethod
    def delete() -> types.UpdateResult:
        update_result = types.UpdateResult(
            updated=1
        )
        return update_result

    @staticmethod
    def scroll() -> Tuple[List[types.Record], Optional[types.PointId]]:

        record = types.Record(
            id='d48632d7-c972-484a-8ed9-262490919c79',
            payload={'group_id': '06798db6-1f99-489a-b599-dd386a043f2d',
                     'metadata': {'dataset_id': '06798db6-1f99-489a-b599-dd386a043f2d',
                                  'doc_hash': '85197672a2c2b05d2c8690cb7f1eedc78fe5f0ca7b8ae8a301f64eb8d959b436',
                                  'doc_id': 'd48632d7-c972-484a-8ed9-262490919c79',
                                  'document_id': '1518a57d-9049-426e-99ae-5a6d479175c0'},
                     'page_content': 'Dify is a company that provides a platform for the development of AI models.'},
            vector=[0.23333 for _ in range(233)]
        )
        return [record], 'd48632d7-c972-484a-8ed9-262490919c79'

    @staticmethod
    def search() -> List[types.ScoredPoint]:
        result = types.ScoredPoint(
            id='d48632d7-c972-484a-8ed9-262490919c79',
            payload={'group_id': '06798db6-1f99-489a-b599-dd386a043f2d',
                     'metadata': {'dataset_id': '06798db6-1f99-489a-b599-dd386a043f2d',
                                  'doc_hash': '85197672a2c2b05d2c8690cb7f1eedc78fe5f0ca7b8ae8a301f64eb8d959b436',
                                  'doc_id': 'd48632d7-c972-484a-8ed9-262490919c79',
                                  'document_id': '1518a57d-9049-426e-99ae-5a6d479175c0'},
                     'page_content': 'Dify is a company that provides a platform for the development of AI models.'},
            vision=999,
            vector=[0.23333 for _ in range(233)],
            score=0.99
        )
        return [result]
