import streamlit as st
import ztp



st.title("Ultivio")

file = st.file_uploader("Import your video", ".mp4", accept_multiple_files=False, max_upload_size=10000000)

if file:
      st.video(file, format="video/mp4", start_time=0, width="stretch")
      run_model = st.button("Run Model")

