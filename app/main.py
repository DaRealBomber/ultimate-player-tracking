import streamlit as st
import ultivio
from io import BytesIO
import av
from pathlib import Path
import cv2
import time


save_frame_directory = Path(r"C:\Users\Jairus\Desktop\ultimate-player-tracking\app\frames")

st.title("Ultivio")

file = st.file_uploader("Import your video", ".mp4", accept_multiple_files=False, max_upload_size=10000000)

if file:
      st.video(file, format="video/mp4", start_time=0, width="stretch")

      run_model = st.button("Run Model")

      if run_model: 
            container = av.open(file)
            
            start = time.perf_counter()
            
            for i, frame in enumerate(container.decode(video=0)): #type: ignore
                  img = frame.to_ndarray(format="bgr24")
                  ultivio.process_frame(img, i)

                  if i == 100:
                        ultivio.close
                        break
            
            stop = time.perf_counter()
            print(stop - start)


            




