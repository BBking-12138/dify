from ctypes import Union
from typing import List


class MockMilvusClass(object):

    @staticmethod
    def insert() -> List[Union[str, int]]:
        result = [447829498067199697]
        return result

    @staticmethod
    def delete() -> List[Union[str, int]]:
        result = [447829498067199697]
        return result

    @staticmethod
    def search() -> List[dict]:
        result = [
            {
                'id': 447829498067199697,
                'distance': 0.8776655793190002,
                'entity': {
                    'page_content': 'Dify is a company that provides a platform for the development of AI models.',
                    'metadata':
                        {
                            'doc_id': '327d1cb8-15ce-4934-bede-936a13c19ace',
                            'doc_hash': '7ee3cf010e606bb768c3bca7b1397ff651fd008ef10e56a646c537d2c8afb319',
                            'document_id': '6c4619dd-2169-4879-b05a-b8937c98c80c',
                            'dataset_id': 'a2f4f4eb-75eb-4432-8c5f-788100533454'
                        }
                }
            }
        ]
        return result

    @staticmethod
    def query() -> List[dict]:
        result = [
            {
                'id': 447829498067199697,
                'distance': 0.8776655793190002,
                'entity': {
                    'page_content': 'Dify is a company that provides a platform for the development of AI models.',
                    'metadata':
                        {
                            'doc_id': '327d1cb8-15ce-4934-bede-936a13c19ace',
                            'doc_hash': '7ee3cf010e606bb768c3bca7b1397ff651fd008ef10e56a646c537d2c8afb319',
                            'document_id': '6c4619dd-2169-4879-b05a-b8937c98c80c',
                            'dataset_id': 'a2f4f4eb-75eb-4432-8c5f-788100533454'
                        }
                }
            }
        ]
        return result

    @staticmethod
    def create_collection_with_schema():
        pass

    @staticmethod
    def has_collection() -> bool:
        return True

