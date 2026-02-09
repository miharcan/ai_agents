from core.agent_kernel import AgentKernel
from execution.llm_runtime import run_llm


class ReActAgent(AgentKernel):
    def __init__(self, llm_backend: str):
        self.llm_backend = llm_backend
        super().__init__()

    def route_tools(self, thought):
        domain = self.state.get("domain", "runtime")
        compare = self.state.get("compare")

        # Comparison mode takes priority
        if domain == "runtime" and compare:
            # ensure comparison happens once
            if not self.state.get("_did_compare"):
                self.state["_did_compare"] = True
                return ("compare_openstack", {"query": thought})

        # Normal runtime retrieval
        if domain == "runtime":
            return ("search_runtime_evidence", {"query": thought})

        if domain == "knowledge":
            return ("search_arxiv", {"query": thought})

        return None

    def run(self, query):
        self.state.pop("_did_compare", None)
        steps = []

        for _ in range(3):
            thought = self.think(query)
            tool_call = self.route_tools(thought)

            if not tool_call:
                break  # no more evidence needed

            name, args = tool_call
            result = self.tools.call(name, **args)
            self.observe(result)
            steps.append((thought, name, args, result))

        return self.final_answer(query, steps)

    def _render_openstack_comparison(self, result: dict) -> str:
        normal = result.get("normal", [])
        abnormal = result.get("abnormal", [])

        def flatten(nodes):
            texts = []
            for n in nodes:
                if hasattr(n, "node") and hasattr(n.node, "text"):
                    texts.append(n.node.text)
                elif hasattr(n, "text"):
                    texts.append(n.text)
            return texts

        normal_text = flatten(normal)
        abnormal_text = flatten(abnormal)

        return (
            "\n--- Normal baseline evidence ---\n"
            + "\n".join(normal_text[:5]) +
            "\n\n--- Abnormal baseline evidence ---\n"
            + "\n".join(abnormal_text[:5])
        )

    def final_answer(self, query, steps):
        def pretty_subsystem(name: str) -> str:
            return name.replace("_", " ").replace("openstack", "OpenStack").title()

        def infer_subsystem(query: str) -> str | None:
            q = query.lower()
            # Linux (existing)
            if "wifi" in q or "wireless" in q or "wlan" in q:
                return "wireless"
            if "network" in q or "ethernet" in q:
                return "network"
            if "disk" in q or "filesystem" in q:
                return "storage"

            # --- OpenStack ---
            if "api" in q or "keystone" in q or "endpoint" in q:
                return "openstack_api"
            if "nova" in q or "compute" in q or "vm" in q:
                return "openstack_compute"
            if "rabbit" in q or "mq" in q or "queue" in q:
                return "openstack_mq"
            if "database" in q or "mysql" in q or "mariadb" in q:
                return "openstack_db"

            # Generic OpenStack fallback
            if "openstack" in q:
                return "openstack_control"

            return None

        domain = self.state.get("domain", "runtime")

        # Collect retrieved evidence text (if any)
        evidence_text = ""
        for step in steps:
            if len(step) == 4:
                _, _, _, result = step
                if isinstance(result, str):
                    # In compare mode, suppress generic runtime evidence
                    if not self.state.get("compare"):
                        evidence_text += " " + result

                elif isinstance(result, dict) and "normal" in result and "abnormal" in result:
                    comparison_text = self._render_openstack_comparison(result)
                    evidence_text += " " + comparison_text

        subsystem_coverage = {
            # Linux
            "wireless": ["wifi", "wireless", "wlan", "802.11"],
            "network": ["eth", "ethernet", "network interface"],
            "storage": ["ext", "fs", "disk", "scsi"],
            # OpenStack
            "openstack_api": ["keystone", "api", "endpoint", "http"],
            "openstack_compute": ["nova", "compute", "instance", "scheduler"],
            "openstack_mq": ["rabbit", "amqp", "queue", "message"],
            "openstack_db": ["mysql", "mariadb", "database", "sql"],
            "openstack_control": ["openstack", "nova", "keystone", "glance"],
        }

        subsystem = infer_subsystem(query)

        if not subsystem:
            for name, indicators in subsystem_coverage.items():
                if any(i in evidence_text for i in indicators):
                    subsystem = name
                    break

        next_evidence = {
            # Linux
            "wireless": [
                "Wireless hardware detection during boot",
                "Wireless network interface initialization events",
                "Network management service logs related to Wi-Fi",
            ],
            "network": [
                "Network interface configuration events",
                "Link status or connection negotiation logs",
                "Firewall or packet filtering logs",
            ],
            "storage": [
                "Disk or block device detection events",
                "Filesystem mount and error logs",
                "I/O error or timeout messages",
            ],
            # OpenStack
            "openstack_api": [
                "Keystone API logs",
                "HTTP request/response error logs",
                "Authentication failure events",
            ],
            "openstack_compute": [
                "Nova compute service logs",
                "Scheduler decision logs",
                "Instance lifecycle state transitions",
            ],
            "openstack_mq": [
                "RabbitMQ connection logs",
                "Message retry or backlog metrics",
                "AMQP heartbeat failures",
            ],
            "openstack_db": [
                "Database connection errors",
                "Slow query logs",
                "Transaction timeout events",
            ],
            "openstack_control": [
                "Service health summaries",
                "Inter-service communication logs",
            ],
        }

        scope_note = ""
        gap_note = ""
        next_evidence_note = ""

        if domain == "runtime":
            scope_note = (
                "Note: The following answer is based solely on the available "
                "runtime system logs and observed behavior. "
                "If relevant events are not present in these logs, "
                "they cannot be assessed.\n\n"
            )

            indicators = subsystem_coverage.get(subsystem, [])
            if indicators and not any(i in evidence_text for i in indicators):
                gap_note = (
                    f"Evidence gap detected: The available runtime logs do not "
                    f"contain information related to the {pretty_subsystem(subsystem)} subsystem."
                    f"No initialization, errors, or events for this subsystem "
                    f"are present in the provided evidence.\n\n"
                )
                
                if subsystem in next_evidence:
                    needed = next_evidence[subsystem]
                    bullets = "\n".join(f"- {item}" for item in needed)

                    next_evidence_note = (
                        "To investigate this issue further, additional runtime evidence "
                        "would be required, such as:\n"
                        f"{bullets}\n\n"
                    )

        reasoning = "\n".join(str(step) for step in steps)

        evidence_block = ""
        if evidence_text:
            evidence_block = f"""
        Retrieved runtime evidence:
        {evidence_text}
        """
            
        if self.state.get("compare"):
            evidence_block = (
                "IMPORTANT:\n"
                "Only differences between NORMAL and ABNORMAL baselines "
                "should be considered causal.\n"
                "Environmental conditions present in BOTH baselines "
                "(e.g., old kernel, low memory) MUST NOT be treated as root causes.\n\n"
                + evidence_block
            )

        prompt = f"""
You are a reasoning agent.

{scope_note}{gap_note}
Original question:
{query}

{evidence_block}

Reasoning trace:
{reasoning}

Based strictly on the retrieved evidence above,
provide a clear, concise final answer.
"""

        # return run_llm(prompt, backend=self.llm_backend)
        llm_answer = run_llm(prompt, backend=self.llm_backend)

        final = ""
        if scope_note:
            final += scope_note
        if gap_note:
            final += gap_note
        if next_evidence_note:
            final += next_evidence_note

        final += llm_answer
        return final

    