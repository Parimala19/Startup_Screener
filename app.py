import streamlit as st
import google.generativeai as genai

# Replace with your actual Google Generative AI API key
genai.configure(api_key="AIzaSyC4nD33wVtoclwz0JDSvRGmQeCg-aHq6xc")

st.title("Startup Idea Validator and Enhancer")
st.markdown("Enter your startup idea below, and I'll help you assess its novelty and potential for growth!")

try:
    # Filter only those models that support content generation
    all_models = [m for m in genai.list_models() if "generateContent" in m.supported_generation_methods]
except Exception as e:
    st.error(f"Failed to fetch models: {e}")
    st.stop()

# (This step ensures we only use models good at generating text.)
text_models = [m for m in all_models if "text" in m.name or "gemini" in m.name]

# Extract model display names for UI dropdown
model_names = [model.display_name for model in text_models]

# Create dropdown to select a model (default to Gemini 1.5 Flash if available)
selected_name = st.selectbox(
    "Choose a model for analysis:",
    model_names,
    index=model_names.index("Gemini 1.5 Flash (Latest)") if "Gemini 1.5 Flash (Latest)" in model_names else 0
)

try:
    selected_model = next(m for m in text_models if m.display_name == selected_name)
except StopIteration:
    st.error("Selected model not found.")
    st.stop()

# Show model ID
st.write(f"Using Model: {selected_model.name}")

# Instantiate the selected model
model = genai.GenerativeModel(selected_model.name)

user_idea = st.text_area("Describe your startup idea (be as detailed as possible):", height=200)

if st.button("Analyze Idea"):
    if not user_idea.strip():
        st.warning("Please enter your startup idea to analyze.")
    else:
        with st.spinner("Analyzing your idea..."):
            try:
                # Construct a structured analysis prompt
                analysis_prompt = f"""You are an AI-powered Startup Idea Analyst for an entrepreneurship cell. Your goal is to evaluate user-submitted startup ideas for their novelty, market potential, and provide actionable feedback.

                Analyze the following startup idea: "{user_idea}"

                Based on your analysis, provide feedback in the following structured format:

                **1. Idea Overview:**
                [A brief re-statement/summary of the user's idea.]

                **2. Novelty Assessment:**
                * Is this idea entirely new or does it have similar existing solutions/competitors?
                * If similar solutions exist, briefly describe them.

                **3. Strategic Recommendations:**
                * **If Existing/Similar:** Suggest specific ways to differentiate this idea. How can it be innovated, niche-targeted, or improved to stand out in the market?
                * **If New/Novel:** Propose strategies for broadening its reach or enhancing its implementation.

                **4. Implementation Considerations:**
                * What are 2-3 key challenges or considerations for implementing this idea (e.g., technical hurdles, regulations, funding)?
                * Suggest initial steps or resources to explore or support the idea.

                **5. Next Steps for Entrepreneur:**
                [Give 1-2 clear next steps for the user.]

                Keep the tone professional, encouraging, and practical.
                """

                # Generate content using the selected model
                response = model.generate_content(analysis_prompt)

                if response.candidates:
                    # Extract the generated analysis text
                    analysis_output = response.candidates[0].content.parts[0].text
                    
                    # ✅ Display result
                    st.subheader("💡 Idea Analysis:")
                    st.markdown(analysis_output)

                    # --- Optional: Follow-up Section ---
                    st.markdown("---")
                    st.subheader("Refine your idea or ask follow-up questions:")
                    follow_up_prompt = st.text_area("How can I help you further with this idea?", height=100)

                    if st.button("Get Follow-up Advice"):
                        if follow_up_prompt.strip():
                            with st.spinner("Getting follow-up advice..."):
                                follow_up_response = model.generate_content(
                                    f"Regarding the idea '{user_idea}' and the previous analysis, {follow_up_prompt}"
                                )
                                if follow_up_response.candidates:
                                    st.markdown(follow_up_response.candidates[0].content.parts[0].text)
                                else:
                                    st.warning("Could not generate follow-up advice.")
                        else:
                            st.warning("Please enter a follow-up question.")

                else:
                    st.warning("No analysis could be generated for your idea.")
                    if response.prompt_feedback and response.prompt_feedback.block_reason:
                        st.error(f"Analysis was blocked due to: {response.prompt_feedback.block_reason.name}")

            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
