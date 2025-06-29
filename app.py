import streamlit as st
import google.generativeai as genai

# Set your API key here
genai.configure(api_key="AIzaSyC4nD33wVtoclwz0JDSvRGmQeCg-aHq6xc")

st.title("Model Selector and Text Generator")

try:
    all_models = list(genai.list_models())
except Exception as e:
    st.error(f"Failed to fetch models: {e}")
    st.stop()

model_names = [model.display_name for model in all_models]

selected_name = st.selectbox("Choose a model:", model_names)

try:
    selected_model = next(m for m in all_models if m.display_name == selected_name)
except StopIteration:
    st.error("Selected model not found.")
    st.stop()

st.write(f"Selected Model ID: {selected_model.name}")

model = genai.GenerativeModel(selected_model.name)

user_prompt = st.text_area("Enter your prompt:")

if st.button("Generate Text"):
    if not user_prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating..."):
            try:
                response = model.generate(prompt=user_prompt)
                generated_text = next(response.candidates).output
                st.subheader("Generated Text:")
                st.write(generated_text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
