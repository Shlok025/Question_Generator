import streamlit as st
from utils.test_utils import load_questions, compare_answers
import json

def main():
    st.set_page_config(page_title="Automated Assessment", page_icon="💡", layout="wide")

    # Custom CSS for dark theme and improved appearance
    st.markdown("""
    <style>
    /* Dark theme colors */
    :root {
        --background-color: #1a1a1a;
        --card-background: #2d2d2d;
        --primary-color: #3b82f6;
        --text-color: #ffffff;
        --border-color: #404040;
    }

    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }

    .quiz-header {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .quiz-header img {
        width: 40px;
        height: 40px;
    }

    .question-number {
        color: var(--primary-color);
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    /* Style radio buttons */
    .stRadio > label {
        background-color: var(--card-background);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.25rem 0;
        transition: all 0.2s;
    }

    .stRadio > label:hover {
        background-color: rgba(59, 130, 246, 0.1);
    }

    /* Style text areas */
    .stTextArea textarea {
        background-color: var(--card-background);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-color);
        padding: 0.75rem;
    }

    /* Style submit button */
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }

    .score-display {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .generator-header {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }

    .feedback-item {
        padding: 0.5rem;
        border-left: 3px solid var(--primary-color);
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header with icon
    st.markdown('''
        <div class="generator-header">
            <h2 style="margin:0">✍️ Assessment</h2>
            <p style="margin:0.5rem 0 0 0;font-size:1rem;opacity:0.9">Provide Answers to the following questions.</p>
        </div>
    ''', unsafe_allow_html=True)

    questions = load_questions()
    if not questions:
        st.error("No generated questions found. Please generate questions first.")
        return

    total_score = 0
    total_mcq_questions = len(questions['mcq'])
    total_sa_questions = len(questions['short_answer'])
    total_questions = total_mcq_questions + total_sa_questions

    # Ensure answers are initialized before accessing
    if "answers" not in st.session_state:
        st.session_state["answers"] = {
            "mcq": [None] * total_mcq_questions,
            "short_answer": [None] * total_sa_questions
        }

    # Main content and sidebar layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # MCQ Questions
        mcq_answers = [None] * total_mcq_questions
        for i, q in enumerate(questions['mcq'], 1):
            st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="question-number">Question {i}</div>', unsafe_allow_html=True)
            st.subheader(q['question'])
            mcq_answers[i - 1] = st.radio(
                "Select your answer:", q['options'], key=f"mcq_{i}"
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # Short Answer Questions
        sa_answers = [None] * total_sa_questions
        for i, q in enumerate(questions['short_answer'], 1):
            st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="question-number">Question {total_mcq_questions + i}</div>', unsafe_allow_html=True)
            st.subheader(q['question'])
            sa_answers[i - 1] = st.text_area(
                "Your answer:", key=f"sa_{i}", height=150
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # Update session state answers after all inputs are collected
        st.session_state["answers"]["mcq"] = mcq_answers
        st.session_state["answers"]["short_answer"] = sa_answers

        if st.button("Submit Quiz", help="Click to submit all your answers"):
            with st.spinner("Evaluating your answers..."):
                results = []
                
                # Evaluate all answers
                for i, q in enumerate(questions['mcq'], 1):
                    user_answer = st.session_state["answers"]["mcq"][i - 1]
                    result = compare_answers(q['question'], q['correct_answer'], user_answer)
                    total_score += result['score']
                    results.append(("MCQ", i, result))

                for i, q in enumerate(questions['short_answer'], 1):
                    user_answer = st.session_state["answers"]["short_answer"][i - 1]
                    result = compare_answers(q['question'], q['answer'], user_answer)
                    total_score += result['score']
                    results.append(("Short Answer", i, result))

                st.session_state["quiz_results"] = results
                st.session_state["total_score"] = total_score
                st.session_state["total_questions"] = total_questions

    with col2:
        st.sidebar.title("Test Results")
        
        if "quiz_results" in st.session_state:
            # Total score display
            st.sidebar.markdown(
                f'<div class="score-display">'
                f'<h2>Total Score</h2>'
                f'<h1>{st.session_state["total_score"]}/{st.session_state["total_questions"] * 10}</h1>'
                f'</div>',
                unsafe_allow_html=True
            )
            
            # Individual results
            for q_type, q_num, result in st.session_state["quiz_results"]:
                st.sidebar.markdown(f'<div class="result-card">', unsafe_allow_html=True)
                st.sidebar.subheader(f"{q_type} {q_num}")
                st.sidebar.markdown(f'<div class="score-display">Score: {result["score"]}/10</div>', unsafe_allow_html=True)
                
                st.sidebar.markdown('<div class="feedback-item">', unsafe_allow_html=True)
                st.sidebar.write("✅ Correct:")
                st.sidebar.write(result['feedback']['correct'])
                st.sidebar.markdown('</div>', unsafe_allow_html=True)
                
                st.sidebar.markdown('<div class="feedback-item">', unsafe_allow_html=True)
                st.sidebar.write("❌ Incorrect:")
                st.sidebar.write(result['feedback']['incorrect'])
                st.sidebar.markdown('</div>', unsafe_allow_html=True)
                
                st.sidebar.markdown('<div class="feedback-item">', unsafe_allow_html=True)
                st.sidebar.write("💡 Suggestions:")
                st.sidebar.write(result['feedback']['suggestions'])
                st.sidebar.markdown('</div>', unsafe_allow_html=True)
                
                st.sidebar.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()