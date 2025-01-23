
# EVALPDF

## Overview

*EVALPDF* is an interactive Streamlit app designed to transform PDF documents into engaging and interactive questions. It utilizes advanced AI techniques to generate multiple-choice and short answer questions, providing users with an automated assessment and feedback system.

## Features

### Key Features
- *Question Generation*: Upload PDF files to create custom questions, including multiple-choice and short answer formats.
- *Instant Feedback*: Take tests and receive immediate feedback on your answers.
- *User-Friendly Interface*: Modern and intuitive design for easy navigation and interaction.
- *Getting Started Guide*: Step-by-step instructions to help users navigate the application.

### Visualizations and UI Components
1. *Main Header*: Displays the application title and a brief description.
2. *Feature Cards*: Highlights key functionalities such as the Question Generator and Assessment.
3. *Getting Started Section*: Provides users with a clear guide on how to use the application.

### Interactive Filters
- *Difficulty Level*: Choose the difficulty level for generated questions.
- *Number of Questions*: Specify how many questions to generate from the uploaded PDF.

## Requirements

To run this app, ensure the following:

1. *Streamlit*: Install the latest version of Streamlit with pip install streamlit.
2. *Python Environment*: Ensure you have Python installed (preferably version 3.9 or higher).
3. *dotenv*: Install the python-dotenv library to manage environment variables.

## Setup Instructions

1. Clone the repository to your local machine.
2. Install the necessary Python dependencies:
    bash
    pip install -r requirements.txt
    
3. Set up your environment variables in a .env file with the following content:
    bash
    GOOGLE_API_KEY=<your-google-api-key>
    
4. Run the Streamlit app:
    bash
    streamlit run Home.py
    

## Usage

1. Navigate to the Question Generator section to upload your PDF file.
2. Select the desired difficulty level and the number of questions to generate.
3. Click the "Generate Questions" button to process the PDF.
4. View the generated questions and take the test to receive feedback.
5. Optionally, navigate to the assessment section to take the test and submit your answers.

## Images

### Home:
![Home](https://github.com/user-attachments/assets/d2b66fc5-2bda-4114-b420-3b607df7db18)

### Question Generator:
![Question Generator](https://github.com/user-attachments/assets/76bccd58-53db-40af-b6ac-0b44b2907428)

### Assessment:
![Assessment](https://github.com/user-attachments/assets/346b0151-3a84-48f3-b421-fb71f435c4a9)

## Contribution

Contributions are welcome! If you have suggestions for improvement or encounter any issues, feel free to open an issue or submit a pull request.

## Footer

Developed with ❤ by [Shlok Gaikwad](https://github.com/shlok025/)

⚡ Features: Question Generation, Assessment, and Instant Feedback
