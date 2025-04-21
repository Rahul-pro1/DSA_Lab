import streamlit as st
from db_config import problems_collection
import urllib.parse
import bson
import requests
from datetime import datetime

FEEDBACK_API_URL = "http://student_feedback_service:8000/mentor/feedback/create"  
NOTIFICATION_URL = "http://notification_service:5000/send_notification" 

st.set_page_config(page_title="Problem Repository", layout="wide")
st.title("🧠 Problem Repository")

problems = list(problems_collection.find({}))

st.subheader("📋 Existing Problems")
if problems:
    for p in problems:
        with st.expander(p["title"]):
            st.markdown(f"**Description:** {p['description']}")
            st.markdown(f"**Input Format:** {p['input_format']}")
            st.markdown(f"**Output Format:** {p['output_format']}")
            st.markdown(f"**Supported Languages:** {', '.join(p['language'])}")
            st.markdown(f"**Test Cases:**")
            solve_url = f"http://localhost:8502/?title={urllib.parse.quote(p['title'])}"
            st.markdown(f"[🛠 Solve Now]({solve_url})", unsafe_allow_html=True)

            for i, tc in enumerate(p["test_cases"]):
                st.code(f"Input {i+1}: {tc['input']}\nOutput {i+1}: {tc['output']}")

            col1, col2 = st.columns([1, 1])
            if col1.button("✏️ Edit", key=f"edit_{str(p['_id'])}"):
                st.session_state["editing"] = str(p["_id"])
            if col2.button("🗑️ Delete", key=f"delete_{str(p['_id'])}"):
                problems_collection.delete_one({"_id": p["_id"]})
                st.success(f"Deleted problem: {p['title']}")
                st.rerun()

            st.markdown("---")
            st.markdown("### ✍️ Provide Feedback")

            with st.form(key=f"feedback_form_{str(p['_id'])}"):
                student_id = st.text_input("Student ID", key=f"student_{p['_id']}")
                mentor_id = st.text_input("Mentor ID", key=f"mentor_{p['_id']}")
                feedback_text = st.text_area("Feedback", key=f"fb_{p['_id']}")
                highlights = st.text_area("Highlights (comma-separated)", key=f"hl_{p['_id']}")
                submitted = st.form_submit_button("Submit Feedback")

                if submitted:
                    if not all([student_id, mentor_id, feedback_text]):
                        st.warning("Please fill all required fields.")
                    else:
                        payload = {
                            "student_id": student_id.strip(),
                            "mentor_id": mentor_id.strip(),
                            "feedback": feedback_text.strip(),
                            "date": datetime.utcnow().isoformat(),
                            "highlights": [h.strip() for h in highlights.split(",") if h.strip()]
                        }

                        try:
                            res = requests.post(FEEDBACK_API_URL, json=payload)
                            if res.status_code == 200:
                                st.success("✅ Feedback submitted successfully!")
                            else:
                                st.error(f"Failed to submit feedback: {res.json().get('message')}")
                        except Exception as e:
                            st.error(f"Error: {e}")
else:
    st.info("No problems found.")

is_editing = st.session_state.get("editing", None)
editing_data = None

if is_editing:
    editing_data = problems_collection.find_one({"_id": bson.ObjectId(is_editing)})
    st.subheader(f"✏️ Edit Problem: {editing_data['title']}")
else:
    st.subheader("➕ Add New Problem")

title = st.text_input("Title", value=editing_data["title"] if editing_data else "")
description = st.text_area("Description", value=editing_data["description"] if editing_data else "")
input_format = st.text_input("Input Format", value=editing_data["input_format"] if editing_data else "")
output_format = st.text_input("Output Format", value=editing_data["output_format"] if editing_data else "")
selected_langs = st.multiselect(
    "Supported Languages", ["python", "c", "cpp", "java", "js"],
    default=editing_data["language"] if editing_data else []
)

test_inputs = st.text_area(
    "Test Inputs (one per line)",
    value="\n".join(tc["input"] for tc in editing_data["test_cases"]) if editing_data else ""
).splitlines()

test_outputs = st.text_area(
    "Expected Outputs (one per line)",
    value="\n".join(tc["output"] for tc in editing_data["test_cases"]) if editing_data else ""
).splitlines()

if st.button("💾 Save"):
    if title and description and input_format and output_format and len(test_inputs) == len(test_outputs):
        problem_doc = {
            "title": title,
            "description": description,
            "input_format": input_format,
            "output_format": output_format,
            "language": selected_langs,
            "test_cases": [{"input": i, "output": o} for i, o in zip(test_inputs, test_outputs)]
        }

        if editing_data:
            problems_collection.update_one({"_id": editing_data["_id"]}, {"$set": problem_doc})
            st.success("✅ Problem updated!")
            del st.session_state["editing"]
        else:
            problems_collection.insert_one(problem_doc)
            st.success("✅ Problem added!")

            try:
                notif_payload = {
                    "student_name": "All Students",
                    "student_email": "rahulsiv2108@gmail.com",  
                    "email_subject": "🆕 New DSA Problem Added!",
                    "email_body": f"A new problem titled '{title}' has been added. Check it out in the Problem Repository!",
                    "reminder_datetime": "",
                    "reminder_subject": "",
                    "reminder_message": ""
                }

                notif_response = requests.post(NOTIFICATION_URL, data=notif_payload)
                if notif_response.status_code == 200:
                    st.success("📧 Notification sent!")
                else:
                    st.warning("⚠️ Failed to send notification.")
            except Exception as e:
                st.warning(f"⚠️ Notification error: {e}")

        st.rerun()
    else:
        st.error("Please complete all fields and match number of test inputs/outputs.")
