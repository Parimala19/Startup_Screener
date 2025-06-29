import streamlit as st
import google.generativeai as genai

# Set your API key here (replace with your actual key)
genai.configure(api_key="AIzaSyC4nD33wVtoclwz0JDSvRGmQeCg-aHq6xc")

st.title("Startup Idea Validator and Enhancer")
st.markdown("Enter your startup idea below, and I'll help you assess its novelty and potential for growth!")

# Fetch available models
try:
    # It's good practice to filter for 'gemini-pro' or 'gemini-1.5-flash' for general text tasks,
    # as 1.5-pro might be overkill and has lower free-tier limits.
    # We'll prioritize models suitable for text generation.
    all_models = [m for m in genai.list_models() if "generateContent" in m.supported_generation_methods]
except Exception as e:
    st.error(f"Failed to fetch models: {e}")
    st.stop()

# Filter for models that are good for text
text_models = [m for m in all_models if "text" in m.name or "gemini" in m.name] # Add more specific filtering if needed

model_names = [model.display_name for model in text_models]

selected_name = st.selectbox("Choose a model for analysis:", model_names, index=model_names.index("Gemini 1.5 Flash (Latest)") if "Gemini 1.5 Flash (Latest)" in model_names else 0)


# Find the selected model object
try:
    selected_model = next(m for m in text_models if m.display_name == selected_name)
except StopIteration:
    st.error("Selected model not found.")
    st.stop()

st.write(f"Using Model: {selected_model.name}")

# Instantiate generative model
model = genai.GenerativeModel(selected_model.name)

# Idea input
user_idea = st.text_area("Describe your startup idea (be as detailed as possible):", height=200)

if st.button("Analyze Idea"):
    if not user_idea.strip():
        st.warning("Please enter your startup idea to analyze.")
    else:
        with st.spinner("Analyzing your idea..."):
            try:
                # --- CORE LOGIC FOR IDEA ANALYSIS ---
                analysis_prompt = f"""You are an AI-powered Startup Idea Analyst for an entrepreneurship cell. Your goal is to evaluate user-submitted startup ideas for their novelty, market potential, and provide actionable feedback.

                Analyze the following startup idea: "{user_idea}"

                Based on your analysis, provide feedback in the following structured format:

                **1. Idea Overview:**
                [A brief re-statement/summary of the user's idea.]

                **2. Novelty Assessment:**
                * Is this idea entirely new or does it have similar existing solutions/competitors?
                * If similar solutions exist, briefly describe them.

                **3. Strategic Recommendations:**
                * **If Existing/Similar:** Suggest specific ways to differentiate this idea. How can it be innovated, niche-targeted, or improved to stand out in the market? Think about unique value propositions, technology integration, target audience refinement, or business model innovation.
                * **If New/Novel:** Propose strategies for broadening its reach or enhancing its implementation. What are potential growth avenues, new markets to explore, or features to consider for wider appeal?

                **4. Implementation Considerations:**
                * What are 2-3 key challenges or considerations for implementing this idea (e.g., technical hurdles, regulatory issues, market adoption, funding)?
                * Suggest initial steps or resources for an entrepreneurship cell to further explore or support this idea.

                **5. Next Steps for Entrepreneur:**
                [Provide 1-2 actionable next steps for the user to take after reading this analysis.]

                Keep the language professional, encouraging, and focused on practical advice for a startup founder.
                """

                response = model.generate_content(analysis_prompt)
                
                if response.candidates:
                    # Extract generated text from first candidate
                    analysis_output = response.candidates[0].content.parts[0].text
                    
                    st.subheader("💡 Idea Analysis:")
                    st.markdown(analysis_output) # Use markdown to render the structured response

                    # Optional: Add a section for further questions/refinements
                    st.markdown("---")
                    st.subheader("Refine your idea or ask follow-up questions:")
                    follow_up_prompt = st.text_area("How can I help you further with this idea?", height=100)
                    if st.button("Get Follow-up Advice"):
                        if follow_up_prompt.strip():
                            with st.spinner("Getting follow-up advice..."):
                                follow_up_response = model.generate_content(f"Regarding the idea '{user_idea}' and the previous analysis, {follow_up_prompt}")
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
