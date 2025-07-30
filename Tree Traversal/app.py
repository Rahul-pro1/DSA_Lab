import streamlit as st
import time
import graphviz

tree_size = 15 
tree_structure = {i: "" for i in range(tree_size)}

def render_binary_tree(tree_structure, highlighted_nodes):
    dot = graphviz.Digraph()

    for index, value in tree_structure.items():
        if value != "":
            label = f"{value}\n({index})"
            if index in highlighted_nodes:
                dot.node(str(index), label, style="filled", fillcolor="lightblue")
            else:
                dot.node(str(index), label)
        else:
            dot.node(str(index), " ", style="invis")

        left = 2 * index + 1
        right = 2 * index + 2

        if left < tree_size and tree_structure[left] != "":
            dot.edge(str(index), str(left))
        if right < tree_size and tree_structure[right] != "":
            dot.edge(str(index), str(right))

    return dot

def generate_inorder_traversal_steps(tree_structure):
    steps, descriptions, highlighted, traversal_result, traversal_path = [], [], [], [], []
    stack = []
    current_node = 0

    if 0 not in tree_structure or tree_structure[0] == "":
        steps.append(tree_structure.copy())
        descriptions.append("Root node is empty. Please provide a value for the root (Node 0).")
        highlighted.append([])
        return steps, descriptions, highlighted, traversal_result, []

    while stack or (current_node is not None and tree_structure.get(current_node, "") != ""):
        while current_node is not None and tree_structure.get(current_node, "") != "":
            stack.append(current_node)
            steps.append(tree_structure.copy())
            descriptions.append(f"Push node {tree_structure[current_node]} (index {current_node}) to stack")
            highlighted.append([current_node])
            traversal_path.append(current_node)
            current_node = 2 * current_node + 1

        current_node = stack.pop()
        traversal_result.append(tree_structure[current_node])
        steps.append(tree_structure.copy())
        descriptions.append(f"Visit node {tree_structure[current_node]} (index {current_node})")
        highlighted.append([current_node])
        traversal_path.append(current_node)

        current_node = 2 * current_node + 2

    return steps, descriptions, highlighted, traversal_result, traversal_path

def generate_preorder_traversal_steps(tree_structure):
    steps, descriptions, highlighted, traversal_result, traversal_path = [], [], [], [], []

    if 0 not in tree_structure or tree_structure[0] == "":
        steps.append(tree_structure.copy())
        descriptions.append("Root node is empty. Please provide a value for the root (Node 0).")
        highlighted.append([])
        return steps, descriptions, highlighted, traversal_result, []

    stack = [0]

    while stack:
        current = stack.pop()
        if current >= tree_size or tree_structure.get(current, "") == "":
            continue

        traversal_result.append(tree_structure[current])
        steps.append(tree_structure.copy())
        descriptions.append(f"Visit node {tree_structure[current]} (index {current})")
        highlighted.append([current])
        traversal_path.append(current)

        right = 2 * current + 2
        left = 2 * current + 1
        if right < tree_size:
            stack.append(right)
        if left < tree_size:
            stack.append(left)

    return steps, descriptions, highlighted, traversal_result, traversal_path

def generate_postorder_traversal_steps(tree_structure):
    steps, descriptions, highlighted, traversal_result, traversal_path = [], [], [], [], []

    if 0 not in tree_structure or tree_structure[0] == "":
        steps.append(tree_structure.copy())
        descriptions.append("Root node is empty. Please provide a value for the root (Node 0).")
        highlighted.append([])
        return steps, descriptions, highlighted, traversal_result, []

    stack1 = [0]
    stack2 = []

    while stack1:
        current = stack1.pop()
        if current >= tree_size or tree_structure.get(current, "") == "":
            continue
        stack2.append(current)

        left = 2 * current + 1
        right = 2 * current + 2
        if left < tree_size:
            stack1.append(left)
        if right < tree_size:
            stack1.append(right)

    while stack2:
        node = stack2.pop()
        traversal_result.append(tree_structure[node])
        steps.append(tree_structure.copy())
        descriptions.append(f"Visit node {tree_structure[node]} (index {node})")
        highlighted.append([node])
        traversal_path.append(node)

    return steps, descriptions, highlighted, traversal_result, traversal_path

st.set_page_config(page_title="Binary Tree Traversal Visualizer", layout="wide")
st.title("Binary Tree Traversal Visualizer")
if st.button("Back to Home"):
    st.markdown('<meta http-equiv="refresh" content="0; URL=/">', unsafe_allow_html=True)

st.sidebar.header("Binary Tree Input")
for i in range(tree_size):
    tree_structure[i] = st.sidebar.text_input(f"Node {i} (Index {i})", value=tree_structure[i])

traversal_type = st.sidebar.selectbox("Choose Traversal Type", ["Inorder", "Preorder", "Postorder"])

if st.sidebar.button("Generate Traversal"):
    if traversal_type == "Inorder":
        steps, descriptions, highlights, traversal_result, traversal_path = generate_inorder_traversal_steps(tree_structure)
    elif traversal_type == "Preorder":
        steps, descriptions, highlights, traversal_result, traversal_path = generate_preorder_traversal_steps(tree_structure)
    else:
        steps, descriptions, highlights, traversal_result, traversal_path = generate_postorder_traversal_steps(tree_structure)

    st.session_state.steps = steps
    st.session_state.descriptions = descriptions
    st.session_state.highlights = highlights
    st.session_state.traversal_result = traversal_result
    st.session_state.traversal_path = traversal_path
    st.session_state.current_step = 0
    st.session_state.traversal_type = traversal_type

if "traversal_result" in st.session_state:
    st.subheader(f"{st.session_state.traversal_type} Traversal Result:")
    st.write(" → ".join(st.session_state.traversal_result))

    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("⏮️ Previous") and st.session_state.current_step > 0:
            st.session_state.current_step -= 1
    with col3:
        if st.button("Next ⏭️") and st.session_state.current_step < len(st.session_state.steps) - 1:
            st.session_state.current_step += 1

    step_index = st.session_state.current_step
    st.markdown(f"### Step {step_index + 1} of {len(st.session_state.steps)}")
    st.info(st.session_state.descriptions[step_index])
    st.graphviz_chart(render_binary_tree(st.session_state.steps[step_index], st.session_state.highlights[step_index]))
