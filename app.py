from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(input_prompt, image, prompt):
    # Use correct model name
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response=model.generate_content([input, image[0],prompt])
    return response.text

# Function to prepare image data
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

# Prompt template
input_prompt = """
You are an expert nutritionist. From the image, identify all the food items and:
- Estimate total calories
- List each item with estimated calories in this format:

1. Item 1 - X calories  
2. Item 2 - Y calories  
...
"""

# Streamlit App UI
st.set_page_config(page_title="AI Nutritionist App")
st.header("AI Nutritionist App 🍱")

input = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Upload a food image (jpg/png)", type=["jpg", "jpeg", "png"])
image=""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
submit=st.button("Tell me the total calories")

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("Analysis Result")
    st.write(response)

