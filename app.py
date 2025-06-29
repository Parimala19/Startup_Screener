import streamlit as st
import google.generativeai as genai

# Page config
st.set_page_config(page_title="🚀 Startup Screener", page_icon="🚀")
st.title("🚀 Startup Screener – Idea Evaluator")
st.markdown("Give me your startup idea and I’ll evaluate its potential!")

# Get API key from secrets.toml
genai.configure(api_key="AIzaSyCG5gZbNfzYlHLw1qQww_5N6CY5r7Y5jJ0")

# Initialize Gemini model
model = genai.GenerativeModel('text-bison-001')


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

        response = model.generate_content(prompt)
        reply = response.text

        # Save in history
        st.session_state.chat_history.append((user_idea, reply))

# Show chat history
if st.session_state.chat_history:
    st.markdown("---")
    for idx, (idea, reply) in enumerate(reversed(st.session_state.chat_history)):
        st.markdown(f"🧍 **You:** {idea}")
        st.markdown(f"🤖 **Startup Screener:** {reply}")
        st.markdown("---")
