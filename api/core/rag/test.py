from llama_index.core import DocumentSummaryIndex

doc_summary_index = DocumentSummaryIndex.from_documents(
    city_docs,
    llm=chatgpt,
    transformations=[splitter],
    response_synthesizer=response_synthesizer,
    show_progress=True,
)