import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY =st.secrets['secret_key']

def check_api_key():
    api_key = GOOGLE_API_KEY
    if not api_key:
        st.error("❌ Google API Key not found. Please set the GOOGLE_API_KEY environment variable.")
        st.info("💡 You can set it by adding GOOGLE_API_KEY=your_api_key to your .env file.")
        return False
    return True

def main():
    st.set_page_config(page_title="EVALPDF", page_icon="📚", layout="wide")

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

    .main-header {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }

    .feature-card {
        background-color: var(--card-background);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        margin-bottom: 1rem;
    }

    .stButton > button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }

    .nav-button {
        background-color: var(--card-background);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        text-decoration: none;
        color: var(--text-color);
        transition: all 0.2s;
    }

    .nav-button:hover {
        background-color: rgba(59, 130, 246, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    if not check_api_key():
        st.stop()

    st.markdown('''
        <div class="main-header">
            <h1>📚 EVALPDF</h1>
            <p style="font-size: 1.2rem; opacity: 0.9;">Transform your PDF documents into interactive questions with automated assessment and feedback. </p>
        </div>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('''
            <div class="feature-card">
                <h3>📝 Question Generator</h3>
                <p>Upload PDFs and generate custom questions that has MCQ's and short answer questions.</p>
            </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
            <div class="feature-card">
                <h3>✍️ Assessment</h3>
                <p>Take the Test with a modern interface and get instant feedback on your answers.</p>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown('''
        <div class="feature-card">
            <h2>🚀 Getting Started</h2>
            <p>1. Navigate to the Question Generator to create questions.</p>
            <p>2. Upload your pdf file and choose Difficulty level along with No of Questions to Generate.</p>
            <p>3. Take the test in the Take Test interface and submit it to get feedback.</p>
        </div>
    ''', unsafe_allow_html=True)

    # Add a status indicator
    # state = load_state()
    # if state['questions_generated']:
    #     st.success("Questions have been generated. You can now take the test!")
    # else:
    #     st.warning("No questions have been generated yet. Please go to the Question Generator page to create questions.")

    # st.markdown('''
    #     <div style="display: flex; justify-content: space-around; margin-top: 2rem;">
    #         <a href="/Question_Generator" class="nav-button">Go to Question Generator</a>
    #         <a href="/Take_Test" class="nav-button">Take the Test</a>
    #     </div>
    # ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

