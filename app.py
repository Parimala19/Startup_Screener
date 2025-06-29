import streamlit as st
import google.generativeai as genai

# Configure your API key here
genai.configure(api_key="AIzaSyC4nD33wVtoclwz0JDSvRGmQeCg-aHq6xc")

st.title("Model Selector and Text Generator")

# Fetch the list of models from the API
models = list(genai.list_models())

# Extract display names for dropdown
model_display_names = [model.display_name for model in models]

# Dropdown for selecting the model
selected_display_name = st.selectbox("Choose a model:", model_display_names)

# Find the selected model object based on display name
selected_model = next(m for m in models if m.display_name == selected_display_name)

st.write(f"Selected Model ID: `{selected_model.name}`")

# Create a GenerativeModel instance with the selected model
model = genai.GenerativeModel(selected_model.name)

# Text input for user prompt
user_prompt = st.text_area("Enter your prompt:", "Write a short poem about startups.")

# Button to trigger text generation
if st.button("Generate Text"):
    with st.spinner("Generating..."):
        response = model.generate_text(prompt=user_prompt)
        st.subheader("Generated Text:")
        st.write(response.text)
