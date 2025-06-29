import streamlit as st
import google.generativeai as genai

# Configure API key here
genai.configure(api_key="AIzaSyC4nD33wVtoclwz0JDSvRGmQeCg-aHq6xc")

st.title("Model Selector and Text Generator")

try:
    # Fetch models once
    all_models = genai.list_models()

    if not all_models:
        st.error("No models found from the API. Please check your API key and network.")
        st.stop()

    # Prepare model names for dropdown
    model_names = [m.display_name for m in all_models]

    # Model selection dropdown by index for safety
    selected_index = st.selectbox("Choose a model:", range(len(model_names)), format_func=lambda i: model_names[i])
    selected_model = all_models[selected_index]

    st.write(f"Selected Model ID: {selected_model.name}")

    model = genai.GenerativeModel(selected_model.name)

    # Prompt input
    user_prompt = st.text_area("Enter your prompt:", "Write a startup plan for a tourist guide app.")

    if st.button("Generate Text"):
        with st.spinner("Generating..."):
            # Check if model supports generate_text method
            if 'generateText' in selected_model.supported_generation_methods:
                response = model.generate_text(prompt=user_prompt)
                generated_text = response.candidates[0].output
                st.subheader("Generated Text:")
                st.write(generated_text)
            else:
                st.error(f"The selected model does not support text generation.")

except Exception as e:
    st.error(f"An error occurred: {e}")
