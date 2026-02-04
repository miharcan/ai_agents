import json
from llama_index.core import Document

def load_arxiv_documents(json_path, limit=1000):
    docs = []
    with open(json_path, "r") as f:
        for i, line in enumerate(f):
            if limit and i >= limit:
                break

            record = json.loads(line)
            text = f"""
Title: {record.get("title")}
Authors: {record.get("authors")}
Categories: {record.get("categories")}

Abstract:
{record.get("abstract")}
"""
            docs.append(
                Document(
                    text=text,
                    metadata={
                        "id": record.get("id"),
                        "categories": record.get("categories"),
                    },
                )
            )
    return docs
