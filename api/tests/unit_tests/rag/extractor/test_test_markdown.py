import os

from core.rag.extractor.markdown_extractor import MarkdownExtractor
from core.rag.extractor.text_extractor import TextExtractor
from core.rag.models.document import Document


def test_extract_markdown():
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get assets directory
    assets_dir = os.path.join(os.path.dirname(current_dir), 'assets')

    # Construct the path to the markdown file
    test_file_path = os.path.join(assets_dir, 'test.md')

    extractor = MarkdownExtractor(test_file_path, autodetect_encoding=True)
    result = extractor.extract()

    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, Document)
