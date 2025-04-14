import streamlit as st

st.set_page_config(page_title="AlgoLand", layout="centered")

st.title("🚀 Algorithm Visualizer & Code Execution Hub")
st.write("Select a module below to get started:")

pages = {
    "🧠 Problem Repository": "http://localhost:8501",
    "🌲 Tree Traversals": "http://localhost:8506",
    "📊 Sorting Visualizer": "http://localhost:8505",
    "🔁 BFS & DFS": "http://localhost:8503",
    "📍 Dijkstra / Floyd-Warshall": "http://localhost:8504"
}

for label, url in pages.items():
    if st.button(label):
        st.markdown(f'<meta http-equiv="refresh" content="0; URL={url}">', unsafe_allow_html=True)
