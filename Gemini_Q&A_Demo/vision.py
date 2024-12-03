from dotenv import load_dotenv
from PIL import Image
import os
import streamlit as st
import google.generativeai as genai
import io

# Load environment variables
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Function to convert image to bytes
def image_to_bytes(image, format="PNG"):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=format)
    img_byte_arr.seek(0)
    return img_byte_arr.read()

# Load the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get a response from the Gemini model
def get_gemini_response(input_text, image):
    # Prepare the parts list for text and image
    parts = []
    if input_text:
        parts.append({"text": input_text})
    if image:
        image_bytes = image_to_bytes(image)
        parts.append({
            "mime_type": "image/png",  # Adjust MIME type based on your image format
            "data": image_bytes
        })
    
    # Generate content using Gemini model
    response = model.generate_content({"parts": parts})
    return response.text if response else "No content provided."

# Streamlit UI setup for file upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)

# Submit button to process the request
submit = st.button("Tell me about the image")

if submit:
    input_text = "Describe the image content"  # Replace with desired input text
    response = get_gemini_response(input_text, image)
    st.subheader("The Response is")
    st.write(response)
