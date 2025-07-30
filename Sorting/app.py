import streamlit as st
import numpy as np

st.set_page_config(page_title="Sorting Algorithm Visualizer")
st.title("🔢 Sorting Algorithm Visualizer")
if st.button("Back to Home"):
    st.markdown('<meta http-equiv="refresh" content="0; URL=/">', unsafe_allow_html=True)

if 'array' not in st.session_state:
    st.session_state.array = []
if 'step_history' not in st.session_state:
    st.session_state.step_history = []
if 'step_descriptions' not in st.session_state:
    st.session_state.step_descriptions = []
if 'highlighted_indices' not in st.session_state:
    st.session_state.highlighted_indices = []
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'sorting_complete' not in st.session_state:
    st.session_state.sorting_complete = False
if 'array_initialized' not in st.session_state:
    st.session_state.array_initialized = False
if 'algorithm' not in st.session_state:
    st.session_state.algorithm = "Bubble Sort"
if 'merge_sort_visualization' not in st.session_state:
    st.session_state.merge_sort_visualization = []

def reset_app():
    st.session_state.array = []
    st.session_state.step_history = []
    st.session_state.step_descriptions = []
    st.session_state.highlighted_indices = []
    st.session_state.current_step = 0
    st.session_state.sorting_complete = False
    st.session_state.array_initialized = False
    st.session_state.merge_sort_visualization = []

array_size = st.number_input("Enter the size of the array", 
                             min_value=3, 
                             max_value=15, 
                             value=8, 
                             step=1,
                             key="array_size")

if st.button("Reset"):
    reset_app()

if not st.session_state.array_initialized or len(st.session_state.array) != array_size:
    st.session_state.array = [0] * array_size
    st.session_state.array_initialized = True
    st.session_state.step_history = []
    st.session_state.step_descriptions = []
    st.session_state.highlighted_indices = []
    st.session_state.current_step = 0
    st.session_state.sorting_complete = False
    st.session_state.merge_sort_visualization = []

st.subheader("Enter Array Values")
cols = st.columns(array_size)
for i in range(array_size):
    with cols[i]:
        val = st.text_input(f"Index {i}", key=f"val_{i}", label_visibility="collapsed")
        st.session_state.array[i] = int(val) if val.strip() and val.strip().isdigit() else 0

def generate_bubble_sort_steps(arr):
    steps = [arr.copy()]
    descriptions = ["Initial array"]
    highlighted = [[-1, -1]]  
    
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            highlighted.append([j, j+1])
            steps.append(arr.copy())
            descriptions.append(f"Comparing elements at indices {j} ({arr[j]}) and {j+1} ({arr[j+1]})")
            
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                steps.append(arr.copy())
                descriptions.append(f"Swapped elements at indices {j} and {j+1}")
                highlighted.append([j, j+1])
    
    steps.append(arr.copy())
    descriptions.append("Array is sorted")
    highlighted.append([-1, -1])
    
    return steps, descriptions, highlighted

def generate_insertion_sort_steps(arr):
    steps = [arr.copy()]
    descriptions = ["Initial array"]
    highlighted_indices = [[-1]]  
    
    arr_copy = arr.copy()  
    
    for i in range(1, len(arr_copy)):
        key = arr_copy[i]
        j = i - 1
        
        steps.append(arr_copy.copy())
        descriptions.append(f"Selected key element {key} at index {i} for insertion")
        highlighted_indices.append([i])  
        
        while j >= 0 and arr_copy[j] > key:
            steps.append(arr_copy.copy())
            descriptions.append(f"Element {arr_copy[j]} at index {j} > key {key}, needs shifting")
            highlighted_indices.append([i, j]) 
            
            arr_copy[j+1] = arr_copy[j]
            
            steps.append(arr_copy.copy())
            descriptions.append(f"Shifted element from index {j} to {j+1}")
            highlighted_indices.append([j+1]) 
            
            j -= 1
        
        arr_copy[j+1] = key
        
        steps.append(arr_copy.copy())
        descriptions.append(f"Inserted key {key} at position {j+1}")
        highlighted_indices.append([j+1])  
    
    steps.append(arr_copy.copy())
    descriptions.append("Array is sorted")
    highlighted_indices.append([-1])
    
    return steps, descriptions, highlighted_indices

def generate_selection_sort_steps(arr):
    steps = [arr.copy()]
    descriptions = ["Initial array"]
    highlighted = [[-1, -1]]  
    
    n = len(arr)
    for i in range(n):
        min_idx = i
        
        steps.append(arr.copy())
        descriptions.append(f"Finding minimum element for position {i}")
        highlighted.append([i, -1])
        
        for j in range(i + 1, n):
            steps.append(arr.copy())
            descriptions.append(f"Comparing current minimum {arr[min_idx]} at index {min_idx} with {arr[j]} at index {j}")
            highlighted.append([min_idx, j])
            
            if arr[j] < arr[min_idx]:
                min_idx = j
                steps.append(arr.copy())
                descriptions.append(f"New minimum found: {arr[min_idx]} at index {min_idx}")
                highlighted.append([min_idx, -1])
        
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            steps.append(arr.copy())
            descriptions.append(f"Swapped elements at indices {i} and {min_idx}")
            highlighted.append([i, min_idx])
    
    steps.append(arr.copy())
    descriptions.append("Array is sorted")
    highlighted.append([-1, -1])
    
    return steps, descriptions, highlighted

def generate_merge_sort_steps(arr):
    steps = []
    descriptions = []
    highlighted = []
    merge_visualization = []  
    
    steps.append(arr.copy())
    descriptions.append("Initial array")
    highlighted.append([-1, -1])
    merge_visualization.append([{"array": arr.copy(), "level": 0, "position": 0}])
    
    def merge_sort_recursive(arr, start, end, level):
        if end - start <= 1:
            return
        
        mid = (start + end) // 2
        
        current_subarrays = []
        left_half = arr[start:mid]
        right_half = arr[mid:end]
        
        current_subarrays.append({"array": left_half, "level": level+1, "position": start})
        current_subarrays.append({"array": right_half, "level": level+1, "position": mid})
        
        merge_visualization.append(current_subarrays.copy())
        steps.append(arr.copy())
        descriptions.append(f"Split array into {left_half} and {right_half}")
        highlighted.append([start, end-1])  
        
        merge_sort_recursive(arr, start, mid, level+1)
        merge_sort_recursive(arr, mid, end, level+1)
        
        merge(arr, start, mid, end, level)
    
    def merge(arr, start, mid, end, level):
        left = arr[start:mid].copy()
        right = arr[mid:end].copy()
        
        current_subarrays = []
        current_subarrays.append({"array": left, "level": level+1, "position": start})
        current_subarrays.append({"array": right, "level": level+1, "position": mid})
        
        merge_visualization.append(current_subarrays.copy())
        steps.append(arr.copy())
        descriptions.append(f"About to merge {left} and {right}")
        highlighted.append([start, end-1]) 
        
        i, j, k = 0, 0, start
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
        
        merged = arr[start:end]
        current_subarrays = []
        current_subarrays.append({"array": merged, "level": level, "position": start})
        
        merge_visualization.append(current_subarrays.copy())
        steps.append(arr.copy())
        descriptions.append(f"Merged into {merged}")
        highlighted.append([start, end-1]) 
    
    merge_sort_recursive(arr, 0, len(arr), 0)
    
    if steps[-1] != arr:
        steps.append(arr.copy())
        descriptions.append("Final sorted array")
        highlighted.append([-1, -1])
        merge_visualization.append([{"array": arr.copy(), "level": 0, "position": 0}])
    
    return steps, descriptions, highlighted, merge_visualization

algorithm = st.radio("Select Sorting Algorithm", 
                     ["Bubble Sort", "Insertion Sort", "Selection Sort", "Merge Sort"])
st.session_state.algorithm = algorithm

if st.button(f"Start {st.session_state.algorithm}"):
    if len(st.session_state.array) > 0:
        if any(val > 0 for val in st.session_state.array):
            if st.session_state.algorithm == "Bubble Sort":
                st.session_state.step_history, st.session_state.step_descriptions, st.session_state.highlighted_indices = generate_bubble_sort_steps(st.session_state.array.copy())
            elif st.session_state.algorithm == "Insertion Sort":
                st.session_state.step_history, st.session_state.step_descriptions, st.session_state.highlighted_indices = generate_insertion_sort_steps(st.session_state.array.copy())
            elif st.session_state.algorithm == "Selection Sort":
                st.session_state.step_history, st.session_state.step_descriptions, st.session_state.highlighted_indices = generate_selection_sort_steps(st.session_state.array.copy())
            elif st.session_state.algorithm == "Merge Sort":
                st.session_state.step_history, st.session_state.step_descriptions, st.session_state.highlighted_indices, st.session_state.merge_sort_visualization = generate_merge_sort_steps(st.session_state.array.copy())

            st.session_state.current_step = 0
            st.session_state.sorting_complete = True
        else:
            st.error("Please enter at least one value in the array")

if st.session_state.sorting_complete:
    st.subheader(f"{st.session_state.algorithm} Visualization")

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("⬅️ Previous Step") and st.session_state.current_step > 0:
            st.session_state.current_step -= 1
    with col2:
        if st.button("Next Step ➡️") and st.session_state.current_step < len(st.session_state.step_history) - 1:
            st.session_state.current_step += 1
    with col3:
        st.write(f"Step {st.session_state.current_step + 1} of {len(st.session_state.step_history)}")

    current_array = st.session_state.step_history[st.session_state.current_step]
    
    st.info(st.session_state.step_descriptions[st.session_state.current_step])
    
    highlights = st.session_state.highlighted_indices[st.session_state.current_step] if st.session_state.current_step < len(st.session_state.highlighted_indices) else [-1, -1]
    
    if st.session_state.algorithm == "Insertion Sort":
        st.write("---")
        max_val = max(current_array) if current_array else 1
        cols = st.columns(len(current_array))
        
        sorted_boundary = 0
        if st.session_state.current_step > 0:
            for idx in range(st.session_state.current_step):
                highlight_indices = st.session_state.highlighted_indices[idx]
                sorted_boundary = max(sorted_boundary, max([i for i in highlight_indices if i != -1] or [0]))
            sorted_boundary = min(sorted_boundary + 1, len(current_array))
        
        for i, val in enumerate(current_array):
            with cols[i]:
                relative_height = val / max_val
                
                if i in highlights:
                    color = "coral" 
                elif i < sorted_boundary:
                    color = "lightgreen"  
                else:
                    color = "lightblue"  
                
                border_style = "1px solid black"
                if i == sorted_boundary - 1:
                    border_style = "2px solid black"
                
                st.markdown(
                    f"""
                    <div style="
                        background-color: {color};
                        width: 100%;
                        height: {200 * relative_height}px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: black;
                        font-weight: bold;
                        border: {border_style};
                        margin: 2px;
                    ">
                        {val}
                    </div>
                    <div style="
                        width: 100%;
                        text-align: center;
                        margin-top: 5px;
                        font-weight: {'bold' if i in highlights else 'normal'};
                    ">
                        {i}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        st.write("---")
        st.markdown("""
        <div style="display: flex; justify-content: center; gap: 20px;">
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: lightgreen; margin-right: 5px;"></div>
                <span>Sorted portion</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: lightblue; margin-right: 5px;"></div>
                <span>Unsorted portion</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: coral; margin-right: 5px;"></div>
                <span>Current key or comparing/moving element</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif st.session_state.algorithm != "Merge Sort":
        st.write("---")
        max_val = max(current_array) if current_array else 1
        cols = st.columns(len(current_array))
        for i, val in enumerate(current_array):
            with cols[i]:
                relative_height = val / max_val
                color = "lightblue"
                
                if i in highlights:
                    color = "coral"

                st.markdown(
                    f"""
                    <div style="
                        background-color: {color};
                        width: 100%;
                        height: {200 * relative_height}px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: black;
                        font-weight: bold;
                        border: 1px solid black;
                    ">
                        {val}
                    </div>
                    <div style="
                        width: 100%;
                        text-align: center;
                        margin-top: 5px;
                    ">
                        {i}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    if st.session_state.algorithm == "Merge Sort":
        st.write("---")
        max_val = max(current_array) if current_array else 1
        cols = st.columns(len(current_array))
        for i, val in enumerate(current_array):
            with cols[i]:
                relative_height = val / max_val
                color = "lightblue"
                
                if highlights[0] <= i <= highlights[1]:
                    color = "coral"

                st.markdown(
                    f"""
                    <div style="
                        background-color: {color};
                        width: 100%;
                        height: {200 * relative_height}px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: black;
                        font-weight: bold;
                        border: 1px solid black;
                    ">
                        {val}
                    </div>
                    <div style="
                        width: 100%;
                        text-align: center;
                        margin-top: 5px;
                    ">
                        {i}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        if 0 < st.session_state.current_step < len(st.session_state.step_history) - 1:
            st.write("---")
            st.write("Merge Sort Visualization (showing array partitioning):")
            
            viz_step = st.session_state.merge_sort_visualization[st.session_state.current_step]
            
            max_level = max(subarray["level"] for subarray in viz_step)
            
            for level in range(max_level + 1):
                level_subarrays = [sa for sa in viz_step if sa["level"] == level]
                if level_subarrays:
                    st.write(f"Level {level}:")
                    
                    spacer_cols = st.columns(len(st.session_state.array))
                    
                    for subarray in sorted(level_subarrays, key=lambda x: x["position"]):
                        pos = subarray["position"]
                        arr = subarray["array"]
                        
                        for i, val in enumerate(arr):
                            with spacer_cols[pos + i]:
                                max_val = max(current_array) if current_array else 1
                                relative_height = val / max_val
                                
                                st.markdown(
                                    f"""
                                    <div style="
                                        background-color: {'lightgreen' if level % 2 == 0 else 'lightblue'};
                                        width: 100%;
                                        height: {150 * relative_height}px;
                                        display: flex;
                                        align-items: center;
                                        justify-content: center;
                                        color: black;
                                        font-weight: bold;
                                        border: 1px solid black;
                                        margin: 2px;
                                    ">
                                        {val}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

    if st.session_state.current_step == len(st.session_state.step_history) - 1:
        st.write("---")
        st.subheader("Final Sorted Array")
        final_cols = st.columns(len(current_array))
        for i, val in enumerate(current_array):
            with final_cols[i]:
                st.markdown(
                    f"""
                    <div style="
                        background-color: #4CAF50;
                        color: white;
                        width: 100%;
                        height: 50px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: bold;
                        border-radius: 5px;
                        margin-bottom: 5px;
                    ">
                        {val}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.caption(f"Index {i}")