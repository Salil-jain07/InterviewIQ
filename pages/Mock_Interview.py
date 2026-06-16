import streamlit as st
from utils.question_loader import load_questions
from models.scorer import calculate_similarity
from utils.database import save_interview

# -------------------------
# LOGIN CHECK
# -------------------------
if "logged_in" not in st.session_state:
    st.error("Please login first.")
    st.stop()


st.title("🎤 Mock Interview")

# -------------------------
# SUBJECT SELECT
# -------------------------
subject = st.selectbox(
    "Select Subject",
    ["DSA", "DBMS", "OOP", "OS", "CN", "ML"]
)

questions = load_questions(subject).reset_index(drop=True)

# -------------------------
# SESSION STATE INIT
# -------------------------
if "session_answers" not in st.session_state:
    st.session_state.session_answers = []

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "step" not in st.session_state:
    st.session_state.step = "ASK"

if "current_subject" not in st.session_state:
    st.session_state.current_subject = subject

if "temp_result" not in st.session_state:
    st.session_state.temp_result = None

# -------------------------
# EMPTY CHECK
# -------------------------
if questions.empty:
    st.warning("No questions available")
    st.stop()

# -------------------------
# SUBJECT CHANGE RESET
# -------------------------
if st.session_state.current_subject != subject:
    st.session_state.current_subject = subject
    st.session_state.question_index = 0
    st.session_state.session_answers = []
    st.session_state.step = "ASK"
    st.session_state.temp_result = None
    st.rerun()

# -------------------------
# QUESTION SAFETY
# -------------------------
if st.session_state.question_index < len(questions):
    question = questions.iloc[st.session_state.question_index]
else:
    st.session_state.step = "END"
    question = None

# -------------------------
# SHOW QUESTION
# -------------------------
if st.session_state.step != "END" and question is not None:
    st.subheader("Question")
    st.write(question["question"])

# -------------------------
# STEP 1: ASK
# -------------------------
if st.session_state.step == "ASK" and question is not None:

    answer = st.text_area("Your Answer")

    if st.button("Submit Answer"):

        if not answer.strip():
            st.error("Answer cannot be empty")

        elif len(answer.strip()) < 10:
            st.error("Answer is too short. Please explain in more detail.")

        else:
            score = calculate_similarity(
                question["ideal_answer"],
                answer
            )

            if score >= 80:
                grade = "Excellent"
            elif score >= 60:
                grade = "Good"
            elif score >= 40:
                grade = "Average"
            else:
                grade = "Needs Improvement"

            save_interview(
                st.session_state.user_email,
                subject,
                question["question"],
                answer,
                score,
                grade
            )

            st.session_state.temp_result = {
                "answer": answer,
                "score": score,
                "grade": grade
            }

            st.session_state.step = "RESULT"
            st.rerun()

# -------------------------
# STEP 2: RESULT
# -------------------------
elif st.session_state.step == "RESULT" and st.session_state.temp_result is not None:

    st.metric("🎯 Score", f"{st.session_state.temp_result['score']:.2f}/100")
    st.metric("🏆 Grade", st.session_state.temp_result['grade'])

    st.progress(min(int(st.session_state.temp_result["score"]), 100))

    with st.expander("📝 Your Submitted Answer", expanded=True):
        st.write(st.session_state.temp_result["answer"])

    with st.expander("✅ Ideal Answer"):
        st.write(question["ideal_answer"])

    if st.button("Next Question"):

        st.session_state.session_answers.append({
            "question": question["question"],
            "answer": st.session_state.temp_result["answer"],
            "score": st.session_state.temp_result["score"],
            "grade": st.session_state.temp_result["grade"]
        })

        st.session_state.question_index += 1
        st.session_state.temp_result = None

        if st.session_state.question_index >= len(questions):
            st.session_state.step = "END"
        else:
            st.session_state.step = "ASK"

        st.rerun()

# -------------------------
# STEP 3: END
# -------------------------
elif st.session_state.step == "END":

    st.success("🎉 Interview Completed")

    if st.button("Start New Interview"):


        st.success("Saved successfully!")

        # RESET EVERYTHING
        st.session_state.session_answers = []
        st.session_state.question_index = 0
        st.session_state.step = "ASK"
        st.session_state.temp_result = None

        st.rerun()