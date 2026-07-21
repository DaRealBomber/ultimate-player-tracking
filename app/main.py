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
session_state_false_list = ["uploaded_video", "get_coordinates", "run_model_check", "run_model"]
session_state_none_list = ["coor1", "coor2", "coor3", "coor4"]
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

if st.session_state["uploaded_video"]:
      
      st.video(file, format="video/mp4", start_time=0, width="stretch")
      
      if not st.session_state["get_coordinates"] and not st.session_state["run_model_check"]:
            set_up_court = st.button("Set up court points")
      
      if not st.session_state["get_coordinates"] and not st.session_state["run_model_check"] and set_up_court:
            st.session_state["get_coordinates"] = True
      
      

      if st.session_state["get_coordinates"]: 
            container = av.open(file)
            run_once = True
            
            #grab one frame and display
            cursor_style = "crosshair"
            frame_gen = container.decode(video=0) #type: ignore
            frame1_img = next(frame_gen).to_ndarray(format="bgr24")
            frame1_rgb = cv2.cvtColor(frame1_img, cv2.COLOR_BGR2RGB)

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

      if st.session_state["run_model_check"]:
            #mini print check
            for i in range(1, 5):
                  print(st.session_state[f"coor{i}"])



            st.session_state["get_coordinates"] = False
            st.write("Court initialized successfully!")
            run_model = st.button("Run model")

      if st.session_state["run_model_check"] and run_model:
            st.session_state["run_model"] = True

      if st.session_state["run_model"]: #main loop
            container = av.open(file)
           
            break_state = False
            for i, frame in enumerate(container.decode(video=0)): #type: ignore
                  if not break_state:
                        img = frame.to_ndarray(format="bgr24")
                        ultivio.process_frame(img, i)

                        if i == 10:
                              ultivio.close()
                              break_state = True
                  else:
                        break




            




