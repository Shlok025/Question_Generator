import json
import streamlit as st
import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = st.secrets['secret_key']

def load_questions():
    try:
        with open('generated_questions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("No generated questions found. Please generate questions first.")
        return None

def compare_answers(question, correct_answer, user_answer):
    api_key = GOOGLE_API_KEY
    if not api_key:
        raise ValueError("Google API Key not found. Please set the GOOGLE_API_KEY environment variable.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Question: {question}
    Correct Answer: {correct_answer}
    User Answer: {user_answer}
    
    Compare the user's answer to the correct answer. Provide:
    1. A score out of 10
    2. Feedback on what the user got right
    3. Feedback on what the user got wrong or missed
    4. Suggestions for improvement

    Also if the user has not provided any answer to a specific question give them zero marks in that specific question.

    Format your response as follows:
    Score: [score]
    Correct: [what the user got right]
    Incorrect: [what the user got wrong or missed]
    Suggestions: [suggestions for improvement]
    """
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Parse the response text
        score_match = re.search(r'Score:\s*(\d+)', response_text)
        correct_match = re.search(r'Correct:\s*(.*?)(?:\n|$)', response_text, re.DOTALL)
        incorrect_match = re.search(r'Incorrect:\s*(.*?)(?:\n|$)', response_text, re.DOTALL)
        suggestions_match = re.search(r'Suggestions:\s*(.*?)(?:\n|$)', response_text, re.DOTALL)

        result = {
            "score": int(score_match.group(1)) if score_match else 5,
            "feedback": {
                "correct": correct_match.group(1).strip() if correct_match else "Unable to determine specific correct aspects.",
                "incorrect": incorrect_match.group(1).strip() if incorrect_match else "Unable to determine specific incorrect aspects.",
                "suggestions": suggestions_match.group(1).strip() if suggestions_match else "Please review the correct answer and compare it with your response."
            }
        }
        
        return result
    except Exception as e:
        st.error(f"An error occurred while evaluating the answer: {str(e)}")
        return fallback_response()

def fallback_response():
    return {
        "score": 5,
        "feedback": {
            "correct": "Unable to determine specific correct aspects.",
            "incorrect": "Unable to determine specific incorrect aspects.",
            "suggestions": "Please review the correct answer and compare it with your response."
        }
    }

