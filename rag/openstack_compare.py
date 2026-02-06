from llama_index.core import Document
from llama_index.core.schema import NodeWithScore
from rag.openstack_index import load_openstack_retriever


def load_openstack_comparison_retriever(
    normal_path: str,
    abnormal_path: str,
):
    """
    Build a contrastive OpenStack retriever by comparing
    normal vs abnormal runtime narratives.
    """

    normal = load_openstack_retriever(normal_path)
    abnormal = load_openstack_retriever(abnormal_path)

    class ComparisonRetriever:
        def retrieve(self, query: str):
            normal_nodes = normal.retrieve(query)
            abnormal_nodes = abnormal.retrieve(query)

            normal_text = "\n".join(
                n.node.text for n in normal_nodes
            )
            abnormal_text = "\n".join(
                n.node.text for n in abnormal_nodes
            )

            comparison = (
                "Baseline OpenStack behavior:\n"
                f"{normal_text}\n\n"
                "Observed OpenStack behavior:\n"
                f"{abnormal_text}"
            )

            doc = Document(
                text=comparison,
                metadata={
                    "source": "openstack",
                    "comparison": True,
                },
            )

            # Wrap back into a NodeWithScore-like structure
            return [
                NodeWithScore(
                    node=doc,
                    score=1.0,
                )
            ]

    return ComparisonRetriever()
