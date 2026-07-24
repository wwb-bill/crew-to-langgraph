# crew-to-langgraph

Auto-migrate CrewAI crews to LangGraph. State schemas, graph definitions, tool integrations.

```python
from crew_to_langgraph import migrate, Agent, Task
agents = [Agent("researcher", "Research", "Find info")]
tasks = [Task("research", "Research AI", "researcher")]
report = migrate(agents, tasks)
```

MIT
