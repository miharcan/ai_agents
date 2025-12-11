from core.agent_kernel import AgentKernel

def test_kernel_runs():
    agent = AgentKernel()
    result = agent.run("hello")
    assert "Final answer" in result
