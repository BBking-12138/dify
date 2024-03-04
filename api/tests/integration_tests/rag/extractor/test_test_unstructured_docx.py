import os

from core.rag.extractor.markdown_extractor import MarkdownExtractor
from core.rag.extractor.text_extractor import TextExtractor
from core.rag.extractor.unstructured.unstructured_doc_extractor import UnstructuredWordExtractor
from core.rag.extractor.unstructured.unstructured_markdown_extractor import UnstructuredMarkdownExtractor
from core.rag.models.document import Document


def test_extract_unstructured_docx():
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get assets directory
    assets_dir = os.path.join(os.path.dirname(current_dir), 'assets')

    # Construct the path to the docx file
    test_file_path = os.path.join(assets_dir, 'test.docx')

    unstructured_api_url = os.getenv('UNSTRUCTURED_API_URL')

    extractor = UnstructuredWordExtractor(test_file_path, unstructured_api_url)
    result = extractor.extract()

    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, Document)
