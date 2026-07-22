import streamlit as st
import streamlit_image_coordinates
import ultivio
import av
from pathlib import Path
import time
import cv2

st.set_page_config(layout="wide")
st.title("Ultivio")

#build setup
session_state_false_list = ["uploaded_video", "get_coordinates", "run_model_check", "run_model", "run_live"]
session_state_none_list = ["coor1", "coor2", "coor3", "coor4", "video_x", "video_y", "video_fps", "run_length", "video_duration"]
session_state_list_builder = ["coor_store"]

#initial setup: too add, if false, add to false list, if none, add to none list
for initialize in session_state_false_list:
      if not initialize in st.session_state:
            st.session_state[initialize] = False

for initialize in session_state_none_list:
      if not initialize in st.session_state:
            st.session_state[initialize] = None

for list in session_state_list_builder:
      if not list in st.session_state:
            st.session_state[list] = []


file = st.file_uploader("Import your video", ".mp4", accept_multiple_files=False, max_upload_size=10000000)

if file:
      st.session_state["uploaded_video"] = True

#main loop
if st.session_state["uploaded_video"]:
      
      st.video(file, format="video/mp4", start_time=0, width="stretch")
      
      if not st.session_state["get_coordinates"] and not st.session_state["run_model_check"]:
            set_up_court = st.button("Set up court points")
      
      if not st.session_state["get_coordinates"] and not st.session_state["run_model_check"] and set_up_court:
            st.session_state["get_coordinates"] = True
      
      #grab video data
      container = av.open(file)
      stream = container.streams.video[0]
      st.session_state["video_x"]  = stream.width
      st.session_state["video_y"] = stream.height
      st.session_state["video_fps"] = float(stream.average_rate)
      st.session_state["video_duration"] = round(container.duration / 1000000)
      print(st.session_state["video_duration"])

      if st.session_state["get_coordinates"]: 
            container = av.open(file)
            run_once = True
            
            #grab one frame and display
            cursor_style = "crosshair"
            frame_gen = container.decode(video=0) #type: ignore
            frame1_img = next(frame_gen).to_ndarray(format="bgr24")
            frame1_rgb = cv2.cvtColor(frame1_img, cv2.COLOR_BGR2RGB)

            col1, col2, col3, col4 = st.columns(4, border=True)
            
            

            coord_grab = streamlit_image_coordinates.streamlit_image_coordinates(
                  frame1_rgb,
                  key=f"cursor_{cursor_style}",
                  width= None,
                  cursor= cursor_style,
            )

            if coord_grab:
                  #look through already initialized
                  if st.session_state["coor1"] == None:
                        st.session_state["coor1"] = [coord_grab['x'], coord_grab['y']]
                  elif st.session_state["coor2"] == None:
                        st.session_state["coor2"] = [coord_grab['x'], coord_grab['y']]
                  elif st.session_state["coor3"] == None:
                        st.session_state["coor3"] = [coord_grab['x'], coord_grab['y']]
                  elif st.session_state["coor4"] == None:
                        st.session_state["coor4"] = [coord_grab['x'], coord_grab['y']]
                        st.session_state["run_model_check"] = True

            if st.session_state["coor1"]:
                  with col1:
                        st.write(st.session_state["coor1"])
            if st.session_state["coor2"]:
                  with col2:
                        st.write(st.session_state["coor2"])
            if st.session_state["coor3"]:
                  with col3:
                        st.write(st.session_state["coor3"])
            if st.session_state["coor4"]:
                  with col4:
                        st.write(st.session_state["coor4"])

      if st.session_state["run_model_check"]:
            
            st.session_state["get_coordinates"] = False
            st.write("Court initialized successfully!")
            run_live = st.checkbox("Run live")
            run_duration = st.number_input("Duration in seconds: Leave 0 for max.", min_value=0, max_value=st.session_state["video_duration"])
            run_model = st.button("Run model")

      if st.session_state["run_model_check"] and run_model:
            st.session_state["run_model"] = True

      if st.session_state["run_model"]: #main loop
            container = av.open(file)
            
            if run_duration == 0:
                  run_duration = st.session_state["video_duration"]
            
            frames_to_process = run_duration * st.session_state["video_fps"]

            for i, frame in enumerate(container.decode(video=0)): #type: ignore
                  if i >= frames_to_process:
                        pass
                  else:
                        img = frame.to_ndarray(format="bgr24")
                        ultivio.process_frame(img, i)

                              




            




