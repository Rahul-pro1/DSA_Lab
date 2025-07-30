import streamlit as st

st.set_page_config(page_title="DSA_Lab", layout="centered")

st.title("DSA Lab: Algorithm Visualizer & Problem Solving Hub")
st.write("Select a module below to get started:")

pages = {
    "Problem Repository": "/problem-repo",
    "Tree Traversals": "/tree-traversal",
    "Sorting Visualizer": "/sorting",
    "BFS & DFS": "/bfs-dfs",
    "Dijkstra / Floyd-Warshall": "/dijkstra-floyd",
    "Code Execution": "/code-exec"
}

for label, path in pages.items():
    if st.button(label):
        st.markdown(f'<meta http-equiv="refresh" content="0; URL={path}">', unsafe_allow_html=True)
