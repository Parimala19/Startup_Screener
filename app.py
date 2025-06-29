import streamlit as st
from google.generativeai import client as genai

# Initialize the API client with your API key
genai.configure(api_key="AIzaSyC4nD33wVtoclwz0JDSvRGmQeCg-aHq6xc")

st.title("Model Selector and Text Generator")

# Fetch all available models
all_models = genai.list_models()

# Get display names for dropdown
model_names = [m.display_name for m in all_models]

# Model selection box
selected_name = st.selectbox("Choose a model:", model_names)

try:
    # Find the selected model object
    selected_model = next(m for m in all_models if m.display_name == selected_name)
except StopIteration:
    st.error("Selected model not found.")
    st.stop()

st.write(f"Selected Model ID: {selected_model.name}")

# Create the GenerativeModel instance
model = genai.GenerativeModel(selected_model.name)

# User input prompt
user_prompt = st.text_area("Enter your prompt:")

if st.button("Generate Text"):
    if not user_prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating..."):
            try:
                if 'generateContent' in selected_model.supported_generation_methods or 'generateText' in selected_model.supported_generation_methods:
                    # Use generate_text() method
                    response = model.generate_text(prompt=user_prompt)
                    # Get first candidate from generator
                    generated_text = next(response.candidates).output
                    st.subheader("Generated Text:")
                    st.write(generated_text)
                else:
                    st.error("Selected model does not support text generation.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
