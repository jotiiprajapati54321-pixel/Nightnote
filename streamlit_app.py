import streamlit as st
from google import genai

st.set_page_config(page_title="Night Note", page_icon="🌙")

def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None

st.title("🌙 Night Note")
st.write("Turn your study notes into clearer revision material.")

notes = st.text_area(
    "Paste your study notes here",
    height=240,
    placeholder="Paste your notes here...",
)

task = st.selectbox(
    "Choose what you want to make",
    [
        "Simplify these notes",
        "Write a short summary",
        "List key topics and terms",
        "Make bullet-point revision notes",
        "Create quiz questions with answers",
    ],
)

if st.button("Generate study help", type="primary"):
    api_key = get_api_key()

    if not notes.strip():
        st.warning("Paste your notes first.")
    elif not api_key:
        st.error("The Gemini key still needs to be added in Streamlit Secrets.")
    else:
        prompt = f"""
You are Night Note, a careful study assistant.
Task: {task}

Explain clearly for a student. Use the notes provided and do not invent facts.
If the notes do not contain enough information, say so.

STUDENT NOTES:
{notes}
"""
        try:
            client = genai.Client(api_key=api_key)
            with st.spinner("Making your study help..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                )
            st.session_state["study_result"] = (
                response.text or "No text response was returned."
            )
        except Exception:
            st.error("Gemini could not answer. We’ll check the key and app settings.")

if st.session_state.get("study_result"):
    st.subheader("Your study help")
    st.markdown(st.session_state["study_result"])
    st.download_button(
        "Download these notes",
        data=st.session_state["study_result"],
        file_name="night_note_study_notes.txt",
        mime="text/plain",
    )

st.divider()
st.subheader("Ask a question about your notes")

question = st.text_input("What are you unsure about?")

if st.button("Answer my question"):
    api_key = get_api_key()

    if not notes.strip():
        st.warning("Paste the notes you want to ask about first.")
    elif not question.strip():
        st.warning("Type your question first.")
    elif not api_key:
        st.error("The Gemini key still needs to be added in Streamlit Secrets.")
    else:
        prompt = f"""
You are Night Note, a careful study tutor.
Answer the student using the notes. Explain simply.
If the notes do not contain enough information, say so.

NOTES:
{notes}

QUESTION:
{question}
"""
        try:
            client = genai.Client(api_key=api_key)
            with st.spinner("Thinking..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                )
            st.markdown(response.text or "No text response was returned.")
        except Exception:
            st.error("Gemini could not answer. We’ll check the key and app settings.")