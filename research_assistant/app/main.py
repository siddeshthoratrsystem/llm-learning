from research_assistant.app.graph.edges import build_graph

graph = build_graph()
result = graph.invoke({"user_input": "hello"})
print(result)
