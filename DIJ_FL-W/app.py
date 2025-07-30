import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import heapq

st.set_page_config(page_title="Graph Algorithm Visualizer", layout="wide")
st.title("Graph Algorithm Visualizer")
if st.button("Back to Home"):
    st.markdown('<meta http-equiv="refresh" content="0; URL=/">', unsafe_allow_html=True)

st.sidebar.header("Graph Builder")
nodes_input = st.sidebar.text_input("Enter nodes (comma-separated)", value="A,B,C,D")
nodes = [node.strip() for node in nodes_input.split(",") if node.strip()]

edges = []
st.sidebar.markdown("### Define Weighted Edges")
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        add_edge = st.sidebar.checkbox(f"Edge: {nodes[i]} ↔ {nodes[j]}", key=f"{i}-{j}")
        if add_edge:
            weight = st.sidebar.number_input(f"Weight for edge {nodes[i]}-{nodes[j]}", min_value=1, value=1, key=f"w-{i}-{j}")
            edges.append((nodes[i], nodes[j], weight))

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_weighted_edges_from(edges)

def draw_graph(G, path_nodes=[], current_node=None):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    node_colors = []
    for node in G.nodes:
        if node == current_node:
            node_colors.append("orange")
        elif node in path_nodes:
            node_colors.append("lightgreen")
        else:
            node_colors.append("lightgrey")

    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1000, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    st.pyplot(plt)

def dijkstra_steps(graph, start):
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    pq = [(0, start)]
    visited = set()
    prev = {}
    steps = []

    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_node in visited:
            continue
        visited.add(current_node)

        step_info = {
            "current": current_node,
            "distances": distances.copy(),
            "queue": list(pq),
            "visited": list(visited),
        }
        steps.append(step_info)

        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor]['weight']
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                prev[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    paths = {}
    for node in graph.nodes:
        if distances[node] == float('inf'):
            continue
        path = []
        curr = node
        while curr in prev:
            path.append(curr)
            curr = prev[curr]
        if curr == start:
            path.append(curr)
            paths[node] = list(reversed(path))

    return steps, paths

def floyd_warshall_steps(graph, nodes):
    dist = {u: {v: float('inf') for v in nodes} for u in nodes}
    for node in nodes:
        dist[node][node] = 0
    for u, v, w in graph.edges(data='weight'):
        dist[u][v] = w
        dist[v][u] = w 

    steps = []

    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
        snapshot = {i: dist[i].copy() for i in nodes}
        steps.append((k, snapshot))

    return steps

algo_choice = st.selectbox("Select Algorithm", ["Dijkstra", "Floyd-Warshall"])

if algo_choice == "Dijkstra":
    start_node = st.selectbox("Select Start Node", nodes)
    if st.button("Run Dijkstra"):
        d_steps, d_paths = dijkstra_steps(G, start_node)
        st.session_state.dijkstra_steps = d_steps
        st.session_state.dijkstra_paths = d_paths
        st.session_state.dijkstra_index = 0

    if "dijkstra_steps" in st.session_state:
        steps = st.session_state.dijkstra_steps
        index = st.session_state.dijkstra_index
        step = steps[index]

        st.subheader(f"Dijkstra Step {index + 1} / {len(steps)}")
        st.markdown(f"**Visiting Node:** {step['current']}")
        draw_graph(G, current_node=step['current'])

        st.info(f"Priority Queue: {step['queue']}")
        st.write("**Distance Table:**")
        st.table(step['distances'])

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("⬅️ Prev Step") and st.session_state.dijkstra_index > 0:
                st.session_state.dijkstra_index -= 1
        with col3:
            if st.button("Next Step ➡️") and st.session_state.dijkstra_index < len(steps) - 1:
                st.session_state.dijkstra_index += 1

        if st.session_state.dijkstra_index == len(steps) - 1:
            st.subheader("Final Shortest Paths")
            for dest, path in st.session_state.dijkstra_paths.items():
                if dest == start_node:
                    continue
                st.success(f"{start_node} → {dest}: {' → '.join(path)}")

elif algo_choice == "Floyd-Warshall":
    if st.button("Run Floyd-Warshall"):
        fw_steps = floyd_warshall_steps(G, nodes)
        st.session_state.fw_steps = fw_steps
        st.session_state.fw_index = 0

    if "fw_steps" in st.session_state:
        steps = st.session_state.fw_steps
        index = st.session_state.fw_index
        k_node, dist_snapshot = steps[index]

        st.subheader(f"Floyd-Warshall Step {index + 1} / {len(steps)}")
        st.markdown(f"**Considering Intermediate Node:** {k_node}")

        draw_graph(G, current_node=k_node)

        matrix_data = []
        for i in nodes:
            row = []
            for j in nodes:
                val = dist_snapshot[i][j]
                row.append("∞" if val == float('inf') else int(val))
            matrix_data.append(row)

        st.write("**Distance Matrix:**")
        st.table(pd.DataFrame(matrix_data, index=nodes, columns=nodes))

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("⬅️ Prev Step") and st.session_state.fw_index > 0:
                st.session_state.fw_index -= 1
        with col3:
            if st.button("Next Step ➡️") and st.session_state.fw_index < len(steps) - 1:
                st.session_state.fw_index += 1
