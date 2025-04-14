import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Graph Traversal Visualizer", layout="wide")
st.title("Graph Traversal Visualizer")

st.sidebar.header("Graph Builder")
nodes_input = st.sidebar.text_input("Enter nodes (comma-separated)", value="A,B,C,D,E")
nodes = [node.strip() for node in nodes_input.split(",") if node.strip()]

edges = []
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        if st.sidebar.checkbox(f"Edge between {nodes[i]} and {nodes[j]}", key=f"{i}-{j}"):
            edges.append((nodes[i], nodes[j]))

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

def draw_graph(G, highlight_node=None):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    node_colors = ["lightblue" if node == highlight_node else "lightgrey" for node in G.nodes]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1000, font_weight='bold')
    st.pyplot(plt)

def bfs_steps(graph, start_node):
    visited = set()
    queue = [start_node]
    order = []
    steps = []

    while queue:
        current = queue.pop(0)
        if current not in visited:
            visited.add(current)
            order.append(current)
            steps.append((current, list(queue), list(order)))
            for neighbor in graph.neighbors(current):
                if neighbor not in visited and neighbor not in queue:
                    queue.append(neighbor)
    return steps

def dfs_steps(graph, start_node):
    visited = set()
    stack = [start_node]
    order = []
    steps = []

    while stack:
        current = stack.pop()
        if current not in visited:
            visited.add(current)
            order.append(current)
            steps.append((current, list(stack), list(order)))
            neighbors = list(graph.neighbors(current))
            neighbors.reverse()
            for neighbor in neighbors:
                if neighbor not in visited and neighbor not in stack:
                    stack.append(neighbor)
    return steps

traversal_type = st.selectbox("Traversal Type", ["BFS", "DFS"])
start_node = st.selectbox("Start Node", nodes)

if st.button("Generate Traversal Steps"):
    if traversal_type == "BFS":
        steps = bfs_steps(G, start_node)
    else:
        steps = dfs_steps(G, start_node)

    st.session_state.steps = steps
    st.session_state.step_index = 0
    st.session_state.traversal_type = traversal_type

if "steps" in st.session_state:
    steps = st.session_state.steps
    index = st.session_state.step_index
    traversal_type = st.session_state.traversal_type

    current_node, queue_or_stack, traversal_result = steps[index]

    st.subheader(f"Step {index + 1} of {len(steps)}")
    st.markdown(f"**Visiting Node:** {current_node}")
    draw_graph(G, highlight_node=current_node)

    if traversal_type == "BFS":
        st.info(f"Queue: {queue_or_stack}")
    else:
        st.info(f"Stack: {queue_or_stack}")

    st.success(f"Traversal Order: {' → '.join(traversal_result)}")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Previous") and st.session_state.step_index > 0:
            st.session_state.step_index -= 1
    with col3:
        if st.button("Next ➡️") and st.session_state.step_index < len(steps) - 1:
            st.session_state.step_index += 1
