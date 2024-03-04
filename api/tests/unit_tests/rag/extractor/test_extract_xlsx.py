import os
from core.rag.extractor.excel_extractor import ExcelExtractor
from core.rag.models.document import Document


def test_extract_xlsx():
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get assets directory
    assets_dir = os.path.join(os.path.dirname(current_dir), 'assets')

    # Construct the path to the xlsx file
    test_file_path = os.path.join(assets_dir, 'test.xlsx')

    extractor = ExcelExtractor(test_file_path)
    result = extractor.extract()
    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, Document)
