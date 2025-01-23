import pdfplumber
import os
import streamlit as st
import json
from fpdf import FPDF
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = st.secrets['secret_key']
# Configure generative AI
genai.configure(api_key=os.GOOGLE_API_KEY)

class QuestionGenerator:
    # Original QuestionGenerator class remains exactly the same
    def __init__(self):
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
        try:
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
            
            with open('generated_questions.json', 'w') as f:
                json.dump(all_questions, f)

            return all_questions
            
        except Exception as e:
            st.error(f"Error generating questions: {str(e)}")
            return None

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

def main():
    st.set_page_config(page_title="Question Generator", page_icon="📝", layout="wide")

    # Custom CSS for dark theme
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

    .main > div:first-child {
        padding-top: 0 !important;
    }

    .generator-header {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }

    # .settings-card {
    #     background-color: var(--card-background);
    #     padding: 1.5rem;
    #     border-radius: 12px;
    #     border: 1px solid var(--border-color);
    #     margin-bottom: 1rem;
    # }

    # .upload-section {
    #     background-color: var(--card-background);
    #     border: 2px dashed var(--border-color);
    #     border-radius: 12px;
    #     padding: 1.5rem;
    #     text-align: center;
    #     margin: 1rem 0;
    # }

    .stFileUploader > div:first-child {
        padding: 1rem !important;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
    }

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

    .generated-questions {
        background-color: var(--card-background);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        margin-top: 2rem;
    }

    .question-card {
        padding: 1rem;
        border-left: 3px solid var(--primary-color);
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('''
        <div class="generator-header">
            <h2 style="margin:0">📝 Question Generator</h2>
            <p style="margin:0.5rem 0 0 0;font-size:1rem;opacity:0.9">Generate custom questions from your PDF documents</p>
        </div>
    ''', unsafe_allow_html=True)

    # Sidebar settings
    with st.sidebar:
        st.markdown('<div class="settings-card">', unsafe_allow_html=True)
        st.title("📊 Question Settings")
        
        difficulty = st.selectbox("Select difficulty", ["Simple", "Medium", "Hard"], key="difficulty_select")
        num_mcqs = st.number_input("Number of MCQs", min_value=1, max_value=10, value=1, key="mcq_input")
        num_answers = st.number_input("Number of short answers", min_value=1, max_value=10, value=1, key="answer_input")
        
        st.markdown(f'''
            <div style="text-align: center; padding: 1rem; background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%); border-radius: 8px; margin-top: 1rem;">
                <h3 style="margin:0">Total Questions</h3>
                <h2 style="margin:0.5rem 0 0 0">{num_mcqs + num_answers}</h2>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Main content
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("📁 Upload your PDF files", type="pdf", accept_multiple_files=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_files:
        st.write(f"📚 Uploaded {len(uploaded_files)} PDF(s)")
        
        if st.button("🚀 Generate Questions"):
            with st.spinner("Generating questions..."):
                generator = QuestionGenerator()
                pdf_texts = generator.extract_text_from_pdfs(uploaded_files)
                
                if pdf_texts:
                    questions = generator.generate_questions(pdf_texts, difficulty, num_mcqs, num_answers)
                    
                    if questions:
                        st.markdown('<div class="generated-questions">', unsafe_allow_html=True)
                        st.subheader("📝 Generated Questions")
                        
                        # MCQs section
                        st.write("### Multiple Choice Questions")
                        for i, q in enumerate(questions['mcq'], 1):
                            st.markdown(f'''
                                <div class="question-card">
                                    <p><strong>Q{i}.</strong> {q['question']}</p>
                                    <p><em>Source: {q['source']}</em></p>
                                </div>
                            ''', unsafe_allow_html=True)
                        
                        # Short Answer section
                        st.write("### Short Answer Questions")
                        for i, q in enumerate(questions['short_answer'], 1):
                            st.markdown(f'''
                                <div class="question-card">
                                    <p><strong>Q{i}.</strong> {q['question']}</p>
                                    <p><em>Source: {q['source']}</em></p>
                                </div>
                            ''', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Download button
                        try:
                            pdf_bytes = create_pdf(questions)
                            st.download_button(
                                label="📥 Download Questions PDF",
                                data=pdf_bytes,
                                file_name="generated_questions.pdf",
                                mime="application/pdf",
                                key="download_pdf",
                                help="Download the generated questions as a PDF file"
                            )
                        except Exception as e:
                            st.error(f"Error creating PDF: {str(e)}")
    else:
        st.info("👆 Please upload one or more PDF files to begin.")

if __name__ == "__main__":
    main()
