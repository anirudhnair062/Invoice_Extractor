from dotenv import load_dotenv
import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai
from pyngrok import ngrok  # Add this import for tunneling

# Load environment variables
load_dotenv()

# Set up Ngrok token
ngrok.set_auth_token(os.environ.get('NGROK_AUTH_TOKEN'))

# Configure the Google Gemini API
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

# Function to load OpenAI model and get responses
def get_gemini_response(input, image, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input, image[0], prompt])
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize our Streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Application")

input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the image")

input_prompt = """
    You are an expert in understanding invoices.
    You will receive input images as invoices &
    you will have to answer questions based on the input image.
"""

if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input)
        if response:
            st.subheader("The Response is:")
            st.write(response)
    except FileNotFoundError as e:
        st.error(f"Error: {e}")