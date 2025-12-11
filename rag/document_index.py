from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

def load_docs(path):
    docs = SimpleDirectoryReader(path).load_data()
    index = VectorStoreIndex.from_documents(docs)
    return index.as_query_engine()
