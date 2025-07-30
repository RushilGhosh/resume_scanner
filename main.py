import google.generativeai as genai
import streamlit as st
import pypdf
import io
import os
from dotenv import load_dotenv

#Get API key
load_dotenv()

#Initialize model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

#Add title and subtitle text
st.set_page_config(page_title="Resume Scanner", page_icon=":file_folder:", layout="centered")
st.title("Resume Scanner")
st.write("Upload your resume and get feedback on what you can do to improve it!")
st.write("Using Gemini 1.5 Flash")

uploaded_file = st.file_uploader("Upload your resume in PDF or TXT format:", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you are applying for (optional):")

analyze = st.button("Analyze Resume")

#Gets text from uploaded PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = pypdf.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if(uploaded_file.type == "application/pdf"):
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8") #gets text from TXT file

#if the button has been pressed and a file has been uploaded
if analyze and uploaded_file:
    try: 
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip(): #if there is no text to strip
            st.error("File does not have any content!")
            st.stop()

        prompt = f"""Please analyze this resume and provide constructive feedback.
                    Focus on the following aspects: 
                    1. content clarity and impact
                    2. skills presentation
                    3. experience descriptions
                    4. specific improvements for {job_role if job_role else 'general job applications'}

                    Resume content: {file_content}

                    Please provide your analysis in a clear, structured format with specific recommendations."""
        response = model.generate_content(prompt)
        st.markdown("### Analysis Results")
        st.markdown(response.text)

    except Exception as e:
        st.error(f"An error occured: {str(e)}")