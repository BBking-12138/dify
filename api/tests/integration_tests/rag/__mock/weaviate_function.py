from typing import List, Optional, Tuple
from qdrant_client.conversions import common_types as types


class MockWeaviateClass(object):

    @staticmethod
    def contains() -> bool:
        return True

    @staticmethod
    def add_data_object() -> str:
        return 'd48632d7-c972-484a-8ed9-262490919c79'

    @staticmethod
    def delete_class() -> None:
        return None

    @staticmethod
    def do() -> dict:
        record = {
            'Get': {
                'Vector_index_a5f66ab4_cc83_4061_85a5_cb775933d52a_Node': [
                    {
                        '_additional': {
                            'distance': 0.10660946,
                            'vector': [0.23333 for _ in range(233)]
                        },
                        'dataset_id': 'a5f66ab4-cc83-4061-85a5-cb775933d52a',
                        'doc_hash': '52c3c8889c34d2d7b50bb04ca4d77081b1b4b625bc69c82294abfbdf7e918c21',
                        'doc_id': 'b3fdec03-99ad-4a7c-a565-94d02dcde05e',
                        'document_id': '71ec7e68-c45a-4d8b-886b-6077730a83ee',
                        'text': '1、你知道孙悟空是从哪里生出来的吗？'
                    }
                ]
            }
        }
        return record

