"""test paragraph index processor."""
import datetime
import uuid
from typing import Optional
import pytest
from core.rag.cleaner.clean_processor import CleanProcessor
from core.rag.datasource.keyword.keyword_factory import Keyword
from core.rag.datasource.retrieval_service import RetrievalService
from core.rag.datasource.vdb.vector_factory import Vector
from core.rag.extractor.entity.extract_setting import ExtractSetting
from core.rag.extractor.extract_processor import ExtractProcessor
from core.rag.index_processor.index_processor_factory import IndexProcessorFactory
from core.rag.models.document import Document
from libs import helper
from models.dataset import Dataset
from models.model import UploadFile


@pytest.mark.parametrize('setup_unstructured_mock', [['partition_md', 'chunk_by_title']], indirect=True)
def extract():

    index_processor = IndexProcessorFactory('text_model').init_index_processor()

    # extract
    file_detail = UploadFile(
        tenant_id='test',
        storage_type='local',
        key='test.txt',
        name='test.txt',
        size=1024,
        extension='txt',
        mime_type='text/plain',
        created_by='test',
        created_at=datetime.datetime.utcnow(),
        used=True,
        used_by='d48632d7-c972-484a-8ed9-262490919c79',
        used_at=datetime.datetime.utcnow()
    )
    extract_setting = ExtractSetting(
        datasource_type="upload_file",
        upload_file=file_detail,
        document_model='text_model'
    )

    text_docs = ExtractProcessor.extract(extract_setting=extract_setting,
                                         is_automatic=True)
    assert isinstance(text_docs, list)
    for text_doc in text_docs:
        assert isinstance(text_doc, Document)

    # transform
    process_rule = {
        'pre_processing_rules': [
            {'id': 'remove_extra_spaces', 'enabled': True},
            {'id': 'remove_urls_emails', 'enabled': False}
        ],
        'segmentation': {
            'delimiter': '\n',
            'max_tokens': 500,
            'chunk_overlap': 50
        }
    }
    documents = index_processor.transform(text_docs, embedding_model_instance=None,
                                          process_rule=process_rule)
    for document in documents:
        assert isinstance(document, Document)

    # load
    vector = Vector(dataset)
    vector.create(documents)


def clean(self, dataset: Dataset, node_ids: Optional[list[str]], with_keywords: bool = True):
    if dataset.indexing_technique == 'high_quality':
        vector = Vector(dataset)
        if node_ids:
            vector.delete_by_ids(node_ids)
        else:
            vector.delete()
    if with_keywords:
        keyword = Keyword(dataset)
        if node_ids:
            keyword.delete_by_ids(node_ids)
        else:
            keyword.delete()


def retrieve(self, retrival_method: str, query: str, dataset: Dataset, top_k: int,
             score_threshold: float, reranking_model: dict) -> list[Document]:
    # Set search parameters.
    results = RetrievalService.retrieve(retrival_method=retrival_method, dataset_id=dataset.id, query=query,
                                        top_k=top_k, score_threshold=score_threshold,
                                        reranking_model=reranking_model)
    # Organize results.
    docs = []
    for result in results:
        metadata = result.metadata
        metadata['score'] = result.score
        if result.score > score_threshold:
            doc = Document(page_content=result.page_content, metadata=metadata)
            docs.append(doc)
    return docs
