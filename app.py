import streamlit as st

st.set_page_config(
    page_title="InterviewIQ",
    page_icon="🎯",
    layout="wide"
)

# -------------------------
# SIDEBAR
# -------------------------
if "logged_in" in st.session_state and st.session_state.logged_in:

    st.sidebar.success(
        f"👤 {st.session_state.user_name}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.clear()

        st.success("Logged out successfully!")

        st.rerun()

# -------------------------
# HOME PAGE
# -------------------------
st.title("🎯 InterviewIQ")

st.subheader("AI-Based Mock Interview Performance Analyzer")

st.write("""
Welcome to InterviewIQ.

This platform helps students prepare for technical interviews by:

✅ Conducting mock interviews

✅ Evaluating answers using NLP

✅ Generating scores

✅ Identifying weak areas

✅ Providing personalized feedback
""")