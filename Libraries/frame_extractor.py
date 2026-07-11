import cv2
import os

def run_extractor(original_folder_path:str, destination_folder:str, interval_frames:int):

    video_folder = original_folder_path #use r"C:.... to avoid formatting issues
    output_folder = destination_folder
    interval = interval_frames #number of frasmes passed before a frame extraction



    
    if interval <= 0:
        raise ValueError("interval_frames must be greater than 0")

    os.makedirs(output_folder, exist_ok=True)
    
    total_saved = 0

    for video_name in os.listdir(video_folder):
        if not video_name.lower().endswith(".mp4"):
            continue

        path = os.path.join(video_folder, video_name)
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            print(f"Couldn't open {path}")
            continue

        #progress bar settings
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        total_frames_for_review = total_frames // interval

        count = 0
        saved = 0

        try:
            while True:
                ret, frame = cap.read() #returns tuple, first value is state of video to check if video next frame exist, second is array containing the image pixels
                if not ret: #if video ends
                    break

                if count % interval == 0: #only save on the interval
                    filename = f"{video_name[:-4]}_{saved:05d}.jpg"
                    cv2.imwrite(os.path.join(output_folder, filename), frame)
                    saved += 1
                    print(f"Completed: {saved} images in current file: {video_name}")
                    print(f"Progress: {round((saved / total_frames_for_review * 100), None)}%")
                    print(saved / total_frames * 100)

                count += 1
                
        finally:
            total_saved += saved
            cap.release()

    return f"Frame extraction completed for: {total_saved} number of frames."