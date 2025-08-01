import streamlit as st

st.set_page_config(page_title="DSA_Lab", layout="centered")

st.title("DSA Lab: Algorithm Visualizer & Problem Solving Hub")
st.write("Select a module below to get started:")

pages = {
    "Problem Repository": "http://repo.dsa.lab.local/",
    "Tree Traversals": "http://tree.dsa.lab.local/",
    "Sorting Visualizer": "http://sort.dsa.lab.local/",
    "BFS & DFS": "http://bfs.dsa.lab.local/",
    "Dijkstra / Floyd-Warshall": "http://dij.dsa.lab.local/",
}

for label, path in pages.items():
    if st.button(label):
        st.markdown(f'<meta http-equiv="refresh" content="0; URL={path}">', unsafe_allow_html=True)
