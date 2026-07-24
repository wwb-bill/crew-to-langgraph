from dataclasses import dataclass

@dataclass
class Agent:
    name: str; role: str; goal: str; tools: list = None
    def __post_init__(self):
        if self.tools is None: self.tools = []

@dataclass
class Task:
    name: str; description: str; agent: str; depends_on: list = None
    def __post_init__(self):
        if self.depends_on is None: self.depends_on = []

@dataclass
class LangGraphDef:
    state_schema: str; nodes: list; edges: list; entry_point: str

@dataclass
class MigrationReport:
    langgraph: LangGraphDef; warnings: list; agent_count: int; task_count: int


def migrate(agents: list, tasks: list) -> MigrationReport:
    state_fields = ["messages: list", "next: str"]
    warnings = []
    nodes = []
    edges = []
    for agent in agents:
        state_fields.append(f"{agent.name}_output: str")
        nodes.append(f"  def {agent.name}_node(state): return {{{agent.name}_output: 'done'}}")
    for task in tasks:
        if task.agent not in [a.name for a in agents]:
            warnings.append(f"Task '{task.name}' references unknown agent '{task.agent}'")
    for task in tasks:
        if task.depends_on:
            for dep in task.depends_on:
                dep_task = next((t for t in tasks if t.name == dep), None)
                if dep_task:
                    edges.append(f'  workflow.add_edge("{dep_task.agent}_node", "{task.agent}_node")')
                else:
                    warnings.append(f"Dependency '{dep}' not found for '{task.name}'")
    state_schema = "class AgentState(TypedDict):\n" + "\n".join(f"  {f}" for f in state_fields)
    entry = tasks[0].agent + "_node" if tasks else "START"
    return MigrationReport(
        langgraph=LangGraphDef(state_schema=state_schema, nodes=nodes, edges=edges, entry_point=entry),
        warnings=warnings, agent_count=len(agents), task_count=len(tasks)
    )