from dotenv import load_dotenv
load_dotenv() # loading all env varibales


import os
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


# function to load Gemini Pro model and get response
model = genai.GenerativeModel("gemini-pro")
def get_gemini_response(question):
    response = model.generate_content(question)
    print(response.text)
    return response.text

st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM application")
input = st.text_input("Input: ", key="input")

submit =st.button("Ask the question: ")
if submit:
    response = get_gemini_response(input)
    st.subheader("The Response is ")
    st.write(response)