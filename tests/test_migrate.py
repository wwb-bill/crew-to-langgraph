from crew_to_langgraph import migrate, Agent, Task

def test_basic():
    r = migrate([Agent("r","Research","Find")], [Task("t","Research AI","r")])
    assert r.agent_count == 1 and r.task_count == 1
def test_multi_agent():
    r = migrate([Agent("r","R","F"),Agent("w","W","C")], [Task("t1","d","r"),Task("t2","d","w",["t1"])])
    assert r.agent_count == 2 and len(r.langgraph.nodes) == 2
def test_warns_unknown():
    assert len(migrate([Agent("a","r","g")],[Task("t","d","x")]).warnings) == 1
def test_warns_missing_dep():
    assert len(migrate([Agent("a","r","g")],[Task("t","d","a",["x"])]).warnings) == 1
def test_state_schema():
    r = migrate([Agent("x","r","g")],[Task("t","d","x")])
    assert "class AgentState" in r.langgraph.state_schema
def test_empty():
    assert migrate([],[]).agent_count == 0