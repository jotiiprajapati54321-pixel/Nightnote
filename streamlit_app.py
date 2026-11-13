import streamlit as st

st.set_page_config(page_title="Night Note", page_icon="🌙")

st.title("🌙 Night Note")
st.write("Make your study notes easier to understand.")

notes = st.text_area(
    "Paste your study notes here",
    height=220,
    placeholder="Paste a paragraph from your notes..."
)

if st.button("Simplify my notes"):
    if notes.strip():
        st.info("Your notes are ready. We’ll connect the AI in a later step.")
    else:
        st.warning("Paste some notes first.")