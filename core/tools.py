class RuntimeEvidenceTool:
    name = "search_runtime_evidence"
    description = (
        "Search runtime evidence including Linux and OpenStack logs "
        "for observed system behavior, errors, or anomalies."
    )

    def __init__(self, linux_retriever=None, openstack_retriever=None):
        self.linux = linux_retriever
        self.openstack = openstack_retriever

    def __call__(self, query: str):
        results = []

        if self.linux:
            results.extend(self.linux.retrieve(query))

        if self.openstack:
            results.extend(self.openstack.retrieve(query))

        return "\n".join(n.node.text for n in results)

    def compare_openstack(self, query: str):
        """
        Retrieve and compare normal vs abnormal OpenStack runtime evidence.
        """
        normal = self.openstack.search(
            query, corpus="normal", k=5
        )
        abnormal = self.openstack.search(
            query, corpus="abnormal", k=5
        )

        return {
            "normal": normal,
            "abnormal": abnormal,
        }



class LinuxLogSearchTool:
    name = "search_linux_logs"
    description = "Search Linux boot logs for relevant context"

    def __init__(self, retriever):
        self.retriever = retriever

    def __call__(self, query: str):
        nodes = self.retriever.retrieve(query)
        return "\n".join(n.text for n in nodes)


class ArxivSearchTool:
    name = "search_arxiv"
    description = (
        "Search academic and research literature for theoretical explanations,"
        "background knowledge, or known system design patterns."
    )

    def __init__(self, retriever):
        self.retriever = retriever

    def __call__(self, query: str):
        nodes = self.retriever.retrieve(query)
        return "\n".join(n.text for n in nodes)


class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, tool):
        self.tools[tool.name] = tool

    def call(self, name, **kwargs):
        return self.tools[name](**kwargs)


class OpenStackCompareTool:
    name = "compare_openstack"
    description = "Compare normal vs abnormal OpenStack runtime behavior"

    def __init__(self, runtime_tool: RuntimeEvidenceTool):
        self.runtime_tool = runtime_tool

    def __call__(self, query: str):
        return self.runtime_tool.compare_openstack(query)
