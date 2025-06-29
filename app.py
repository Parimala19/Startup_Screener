import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyC4nD33wVtoclwz0JDSvRGmQeCg-aHq6xc")

st.title("Model Selector and Text Generator")

# List models that support 'generateText'
models = [m for m in genai.list_models() if 'generateText' in m.supported_generation_methods]
model_names = [m.display_name for m in models]

selected_name = st.selectbox("Choose a model:", model_names)
selected_model = next(m for m in models if m.display_name == selected_name)

st.write(f"Selected Model ID: {selected_model.name}")

model = genai.GenerativeModel(selected_model.name)

user_prompt = st.text_area("Enter your prompt:", "Write a startup plan for a tourist guide app.")

if st.button("Generate Text"):
    with st.spinner("Generating..."):
        # Use generate_text, as .generate does NOT exist
        response = model.generate_text(prompt=user_prompt)
        generated_text = response.candidates[0].output
        st.subheader("Generated Text:")
        st.write(generated_text)
