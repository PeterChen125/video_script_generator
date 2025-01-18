import streamlit as st
from utils import generate_script

st.title("🎬 Video Script Generator 🎬")

with st.sidebar:
    openai_api_key = st.text_input("Please type in your OpenAI API key：", type="password")
    st.markdown("[How to get access to OpenAI API key](https://platform.openai.com/account/api-keys)")

subject = st.text_input("💡 Please input the theme/subject of this video")
video_length = st.number_input("⏱️ Please input approximate length of this video, in minutes ", min_value=0.1, step=0.1)
creativity = st.slider("✨ Please input the creativity level for the script (a lower number indicates more strictness, and a higher number indicates more creativity)", min_value=0.0,
                       max_value=1.0, value=0.2, step=0.1)
submit = st.button("Generate Script")

if submit and not openai_api_key:
    st.info("Please input your OpenAI API key")
    st.stop()
if submit and not subject:
    st.info("Please input a subject for this video")
    st.stop()
if submit and not video_length >= 0.1:
    st.info("Please make sure your video length value is greater or equal to 0.1 min")
    st.stop()
if submit:
    with st.spinner("AI is thinking right now，please wait a second..."):
        search_result, title, script = generate_script(subject, video_length, creativity, openai_api_key)

    st.success("The video script has been successfully generated!")
    st.subheader("🔥 Title: ")
    st.write(title)
    st.subheader("📝 Video Script: ")
    st.write(script)
    with st.expander("Wikipedia Search Results 👀"):
     st.info(search_result)
