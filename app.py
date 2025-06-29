import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyC4nD33wVtoclwz0JDSvRGmQeCg-aHq6xc")

st.title("Model Selector and Text Generator")

# List all models without filtering
all_models = genai.list_models()

if not all_models:
    st.error("No models found from the API. Check your API key and internet connection.")
else:
    # Show model names and their generation methods
    for m in all_models:
        st.write(f"Model: {m.display_name}, Methods: {m.supported_generation_methods}")

    # Now let user select any model from the list
    model_names = [m.display_name for m in all_models]
    selected_name = st.selectbox("Choose a model:", model_names)

    selected_model = next(m for m in all_models if m.display_name == selected_name)
    st.write(f"Selected Model ID: {selected_model.name}")

    model = genai.GenerativeModel(selected_model.name)

    user_prompt = st.text_area("Enter your prompt:", "Write a startup plan for a tourist guide app.")

    if st.button("Generate Text"):
        with st.spinner("Generating..."):
            # Check if model supports generateText method
            if 'generateText' in selected_model.supported_generation_methods:
                response = model.generate_text(prompt=user_prompt)
                generated_text = response.candidates[0].output
                st.subheader("Generated Text:")
                st.write(generated_text)
            else:
                st.error(f"Model {selected_model.display_name} does not support text generation.")
