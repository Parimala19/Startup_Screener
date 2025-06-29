import streamlit as st
import google.generativeai as genai

# Page config
st.set_page_config(page_title="🚀 Startup Screener", page_icon="🚀")

st.title("🚀 Startup Screener – Idea Evaluator")
st.markdown("Give me your startup idea and I’ll evaluate its potential!")

# Configure API key securely from Streamlit secrets
genai.configure(api_key="AIzaSyC4nD33wVtoclwz0JDSvRGmQeCg-aHq6xc")

# List available models once on first run and let user pick
if "models_list" not in st.session_state:
    try:
        models = genai.list_models()
        st.session_state.models_list = models
    except Exception as e:
        st.error(f"Error listing models: {e}")
        st.stop()

model_names = [model.name for model in st.session_state.models_list]
selected_model = st.selectbox("Select model to use", model_names)

model = genai.GenerativeModel(selected_model)

# Keep chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input form
with st.form("idea_form"):
    user_idea = st.text_area("💡 Describe your startup idea:", height=150)
    submitted = st.form_submit_button("Analyze Idea")

# On submit
if submitted and user_idea:
    with st.spinner("Thinking..."):
        prompt = f"""
You are a professional startup mentor. A student has an idea:

\"{user_idea}\"

Please evaluate this idea and respond with:
1. 🧠 Summary of the idea
2. 📈 Potential market and competition
3. 🔍 Possible challenges
4. ✅ Suggest improvements
5. 🏁 Final verdict (Promising / Needs work / Unclear)
"""
        try:
            response = model.generate_content(prompt)
            reply = response.text
            st.session_state.chat_history.append((user_idea, reply))
        except Exception as e:
            st.error(f"API call failed: {e}")

# Show chat history
if st.session_state.chat_history:
    st.markdown("---")
    for idea, reply in reversed(st.session_state.chat_history):
        st.markdown(f"🧍 **You:** {idea}")
        st.markdown(f"🤖 **Startup Screener:** {reply}")
        st.markdown("---")
