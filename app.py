import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyC4nD33wVtoclwz0JDSvRGmQeCg-aHq6xc")

st.title("Model Selector and Text Generator")

models = list(genai.list_models())

# Filter models to only those that support generateContent
text_models = [m for m in models if "generateContent" in m.supported_generation_methods]

model_display_names = [m.display_name for m in text_models]

selected_display_name = st.selectbox("Choose a model:", model_display_names)

selected_model = next(m for m in text_models if m.display_name == selected_display_name)

st.write(f"Selected Model ID: `{selected_model.name}`")

model = genai.GenerativeModel(selected_model.name)

user_prompt = st.text_area("Enter your prompt:", "Write a short poem about startups.")

if st.button("Generate Text"):
    with st.spinner("Generating..."):
        response = model.generate_text(prompt=user_prompt)
        st.subheader("Generated Text:")
        st.write(response.text)
