from dotenv import load_dotenv
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
load_dotenv()
import google.generativeai as genai


#1.Configuring Google Gemini with our api key info
genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) #Setting Api_Key


#2. It takes the input_prompts,pdf(converted_file into bytes),
def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([prompt,pdf_content[0],input])
    return response.candidates
#3.Now Function for getting pdf input
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())
        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

#Streamlit App
st.set_page_config(page_title= "ATS Resume Expert With GEMINI PRO")
st.header("ATS Tracking System")
input_text=st.text_area("Enter Job Description here-->> ",key='input')
uploaded_file=st.file_uploader("Upload Resume/CV here....",type=['pdf'])

if uploaded_file is not None:
    st.write("Uploaded File Successfully")


submit1=st.button("Tell Me About My Resume")
submit2=st.button("Percentage Match")
submit3=st.button("How can i improve my skills?")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager in the field of Data Science and Full-Stack Web Developer , Cyber Security,Big Data,Engineering,DEVOPS,Data Analyst,your task is to review the provided resume against the job description for this profiles. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""
input_prompt2 = """
You are an Technical Human Resource Manager with expertise in  Data Science and Full-Stack Web Developer , Cyber Security,Big Data,Engineering,DEVOPS,Data Analyst,
your role is to scrutinize the resume in light of the job description provided.
Share your insights on the candidate's suitability for the role from an HR perspective.
Additionally, offer advice on enhancing the candidate's skills and identify areas.  Give a Score out of 100 for the resume.
"""
input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""
if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)#setting that "uploaded_file" into function which we made for converting pdf into bytes and bytes into image"
        response=get_gemini_response(input_prompt1,pdf_content,input_text)#here input prompts are we already defined,pdf_content,input_text as job description
        st.subheader("The Repsonse is:")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Repsonse is: ")
        st.write(response)
elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is: ")
        st.write(response)
    else:
        st.write("Please uplaod the resume")