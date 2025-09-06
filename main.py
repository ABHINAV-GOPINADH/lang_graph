from graphs.maintenance_graph import build_graph

if __name__ == "__main__":
    graph = build_graph()
    app = graph.compile()
    result = app.invoke({})

    print("\n=== Final Result from Graph ===")
    print(result)  # Full state debug

    # Access structured decision output
    decision_output = result.get("decision", {})
    print("\n--- Decision Agent Output ---")
    print("Recommended Actions:", decision_output.get("decision"))
    print("Manual Context:", decision_output.get("manual_context"))

    # Access structured optimizer output
    optimizer_output = result.get("optimization", {})
    print("\n--- Optimizer Agent Output ---")
    print("Optimized Plan:", optimizer_output.get("optimization"))
