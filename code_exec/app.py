import streamlit as st
import subprocess
import tempfile
import os
import time
import uuid
import warnings

from db_config import problems_collection

warnings.filterwarnings("ignore", category=FutureWarning)

LANGUAGES = {
    "python": "Python",
    "c": "C",
    "cpp": "C++",
    "java": "Java",
    "js": "JavaScript"
}

EXTENSIONS = {
    "python": "py",
    "c": "c",
    "cpp": "cpp",
    "java": "java",
    "js": "js"
}

def run_code(code, lang_key, inputs):
    ext = EXTENSIONS[lang_key]

    with tempfile.TemporaryDirectory() as tmpdir:
        if lang_key == "java":
            filename = "Main.java"
        else:
            filename = f"Main_{uuid.uuid4().hex[:8]}.{ext}"

        filepath = os.path.join(tmpdir, filename)
        with open(filepath, "w") as f:
            f.write(code)

        results = []
        for input_data in inputs:
            try:
                if lang_key == "python":
                    start = time.time()
                    result = subprocess.run(["python", filepath], input=input_data.encode(), capture_output=True, timeout=2)

                elif lang_key == "java":
                    compile_result = subprocess.run(["javac", filename], capture_output=True, cwd=tmpdir, timeout=2)
                    if compile_result.returncode != 0:
                        output = ""
                        error = compile_result.stderr.decode().strip()
                        results.append((output, error, None))
                        continue
                    start = time.time()
                    result = subprocess.run(["java", "Main"], input=input_data.encode(), capture_output=True, cwd=tmpdir, timeout=2)

                elif lang_key == "c":
                    exe_file = os.path.join(tmpdir, "a.out")
                    compile_result = subprocess.run(["gcc", filepath, "-o", exe_file], capture_output=True, timeout=2)
                    if compile_result.returncode != 0:
                        output = ""
                        error = compile_result.stderr.decode().strip()
                        results.append((output, error, None))
                        continue
                    start = time.time()
                    result = subprocess.run([exe_file], input=input_data.encode(), capture_output=True, timeout=2)

                elif lang_key == "cpp":
                    exe_file = os.path.join(tmpdir, "a.out")
                    compile_result = subprocess.run(["g++", filepath, "-o", exe_file], capture_output=True, timeout=2)
                    if compile_result.returncode != 0:
                        output = ""
                        error = compile_result.stderr.decode().strip()
                        results.append((output, error, None))
                        continue
                    start = time.time()
                    result = subprocess.run([exe_file], input=input_data.encode(), capture_output=True, timeout=2)

                elif lang_key == "js":
                    start = time.time()
                    result = subprocess.run(["node", filepath], input=input_data.encode(), capture_output=True, timeout=2)

                end = time.time()
                output = result.stdout.decode().strip()
                error = result.stderr.decode().strip()
                results.append((output, error, round((end - start) * 1000, 2)))

            except subprocess.TimeoutExpired:
                results.append(("Timeout", "", None))
            except Exception as e:
                results.append((f"Error: {str(e)}", "", None))

    return results

def fetch_all_problems():
    return list(problems_collection.find({}, {"_id": 0}))

st.set_page_config(page_title="Code Execution Platform", layout="wide")
st.title("Code Execution & Validation App")
if st.button("Back to Home"):
    st.markdown('<meta http-equiv="refresh" content="0; URL=/">', unsafe_allow_html=True)
if st.button("Back to Problem Repository"):
    st.markdown('<meta http-equiv="refresh" content="0; URL=/problem-repo">', unsafe_allow_html=True)

all_problems = fetch_all_problems()
problem_titles = [p["title"] for p in all_problems]

if all_problems:
    query_params = st.experimental_get_query_params()
    selected_title = query_params.get("title", [None])[0]
    selected_problem = next((p for p in all_problems if p["title"] == selected_title), None)

    if selected_problem:
        st.markdown(f"**Problem:** {selected_problem['description']}")
        st.markdown(f"**Input Format:** {selected_problem['input_format']}")
        st.markdown(f"**Output Format:** {selected_problem['output_format']}")

        lang_options = selected_problem["language"]
        lang_title_map = {lang: LANGUAGES[lang] for lang in lang_options}
        lang_title_to_key = {v: k for k, v in lang_title_map.items()}

        selected_lang_title = st.selectbox("Choose language", list(lang_title_to_key.keys()))
        selected_lang_key = lang_title_to_key[selected_lang_title]

        code = st.text_area("Write your code here", height=300)

        if st.button("Run Code"):
            test_inputs = [tc["input"] for tc in selected_problem["test_cases"]]
            expected_outputs = [tc["output"] for tc in selected_problem["test_cases"]]
            outputs = run_code(code, selected_lang_key, test_inputs)

            st.write("### Results")
            for i, (user_out, err, exec_time) in enumerate(outputs):
                st.markdown(f"**Test Case {i + 1}**")
                st.write(f"**Input:** {test_inputs[i]}")
                st.write(f"**Expected Output:** {expected_outputs[i]}")
                st.write(f"**Your Output:** {user_out}")
                st.write(f"**Correct:** {'✅' if user_out.strip() == expected_outputs[i].strip() else '❌'}")
                if exec_time is not None:
                    st.write(f"**Execution Time:** {exec_time} ms")
                if err:
                    st.warning(f"**Error:** {err}")
                st.write("---")
    else:
        st.warning("No valid problem selected via query parameters.")
else:
    st.warning("No problems found. Please add one from the Problem Repository.")
