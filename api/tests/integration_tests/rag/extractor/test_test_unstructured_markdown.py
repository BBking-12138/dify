import os
import pytest
from core.rag.extractor.unstructured.unstructured_markdown_extractor import UnstructuredMarkdownExtractor
from core.rag.models.document import Document
from tests.integration_tests.rag.__mock.unstructured_mock import setup_unstructured_mock

@pytest.mark.parametrize('setup_unstructured_mock', [['partition_md', 'chunk_by_title']], indirect=True)
def test_extract_unstructured_markdown(setup_unstructured_mock):
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get assets directory
    assets_dir = os.path.join(os.path.dirname(current_dir), 'assets')

    # Construct the path to the markdown file
    test_file_path = os.path.join(assets_dir, 'test.md')

    unstructured_api_url = os.getenv('UNSTRUCTURED_API_URL')

    extractor = UnstructuredMarkdownExtractor(test_file_path, unstructured_api_url)
    result = extractor.extract()

    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, Document)
