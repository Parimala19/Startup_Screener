import streamlit as st
import google.generativeai as genai

# Set your API key here
genai.configure(api_key="AIzaSyC4nD33wVtoclwz0JDSvRGmQeCg-aHq6xc")

st.title("Conversational Model Selector and Text Generator")

# Fetch all models safely
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

# Initialize conversation in session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

def build_prompt_from_conversation(conversation):
    prompt = ""
    for msg in conversation:
        role = msg['role']
        content = msg['content']
        if role == 'user':
            prompt += f"User: {content}\n"
        else:
            prompt += f"Assistant: {content}\n"
    prompt += "Assistant:"  # So model knows to respond next
    return prompt

user_input = st.text_input("Your message:")

if st.button("Send"):
    if not user_input.strip():
        st.warning("Please enter a message.")
    else:
        # Append user message
        st.session_state.conversation.append({"role": "user", "content": user_input.strip()})

        # Build prompt with conversation history
        prompt_text = build_prompt_from_conversation(st.session_state.conversation)

        with st.spinner("Generating response..."):
            try:
                response = model.generate_content(
                    prompt_text,
                    temperature=0.7,
                    candidate_count=1,
                    max_output_tokens=300  # limit length, adjust as needed
                )
                if response.candidates:
                    generated_text = response.candidates[0].content.parts[0].text.strip()
                    # Append assistant response
                    st.session_state.conversation.append({"role": "assistant", "content": generated_text})
                else:
                    generated_text = "No response generated."
                    st.warning(generated_text)
            except Exception as e:
                st.error(f"Error generating response: {e}")

# Display conversation as chat
for msg in st.session_state.conversation:
    if msg['role'] == 'user':
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Assistant:** {msg['content']}")
