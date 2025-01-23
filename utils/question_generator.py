import pdfplumber
import streamlit as st
import json
from fpdf import FPDF
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = st.secrets['secret_key']

class QuestionGenerator:
    def __init__(self):
        api_key = GOOGLE_API_KEY
        if not api_key:
            raise ValueError("Google API Key not found. Please set the GOOGLE_API_KEY environment variable.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def extract_text_from_pdfs(self, pdf_files):
        all_texts = []
        for pdf_file in pdf_files:
            try:
                pdf = pdfplumber.open(pdf_file)
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                all_texts.append({"filename": pdf_file.name, "text": text, "pages": len(pdf.pages)})
            except Exception as e:
                st.error(f"Error extracting text from {pdf_file.name}: {str(e)}")
        return all_texts

    def generate_questions(self, pdf_texts, difficulty, num_mcqs, num_answers):
        total_questions = num_mcqs + num_answers
        all_questions = {"mcq": [], "short_answer": []}
        
        total_pages = sum(pdf["pages"] for pdf in pdf_texts)
        
        for pdf in pdf_texts:
            pdf_ratio = pdf["pages"] / total_pages
            pdf_mcqs = max(1, round(num_mcqs * pdf_ratio))
            pdf_answers = max(1, round(num_answers * pdf_ratio))
            
            prompt = f"""Generate questions based on the following text with:
                    - {pdf_mcqs} Multiple Choice Questions (MCQs)
                    - {pdf_answers} Short Answer Questions
                    All questions should be {difficulty} level.
                    Format the response as a JSON string with the following structure:
                    {{
                        "mcq": [
                            {{
                                "question": "question text",
                                "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                                "correct_answer": "A"
                            }}
                        ],
                        "short_answer": [
                            {{
                                "question": "question text",
                                "answer": "brief answer (2-3 sentences)"
                            }}
                        ]
                    }}
                    Source: {pdf['filename']}"""
            
            response = self.model.generate_content(pdf["text"] + "\n" + prompt)
            questions = self._parse_response(response.text)
            
            if questions:
                for q in questions["mcq"]:
                    q["source"] = pdf["filename"]
                for q in questions["short_answer"]:
                    q["source"] = pdf["filename"]
                
                all_questions["mcq"].extend(questions["mcq"])
                all_questions["short_answer"].extend(questions["short_answer"])
        
        return all_questions
    
    def _parse_response(self, response_text):
        try:
            cleaned_text = response_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:-3]
            return json.loads(cleaned_text)
        except json.JSONDecodeError as e:
            st.error(f"Error parsing response: {str(e)}")
            return None

def create_pdf(questions):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    
    # Add MCQs
    pdf.cell(0, 10, "Multiple Choice Questions", ln=True)
    pdf.set_font("Arial", size=12)
    
    for i, q in enumerate(questions['mcq'], 1):
        pdf.multi_cell(0, 10, f"{i}. {q['question']} (Source: {q['source']})")
        for option in q['options']:
            pdf.multi_cell(0, 10, f"   {option}")
        pdf.ln(5)
    
    # Add Short Answer Questions
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Short Answer Questions", ln=True)
    pdf.set_font("Arial", size=12)
    
    for i, q in enumerate(questions['short_answer'], 1):
        pdf.multi_cell(0, 10, f"{i}. {q['question']} (Source: {q['source']})")
        pdf.ln(5)
    
    return pdf.output(dest='S').encode('latin-1')

