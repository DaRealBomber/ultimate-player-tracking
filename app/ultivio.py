import cv2
from ultralytics import YOLO
import csv

model = YOLO(r"..\Models\ultiV1.pt")
csv_file = open(r"test_tracking.csv", "w", newline="")
writer = csv.writer(csv_file)

writer.writerow([
    "frame",
    "track_id",
    "class",
    "confidence",
    "x1",
    "y1",
    "x2",
    "y2"
])

def process_frame(frame, frame_num):
    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml"
    )
    result = results[0]
    boxs = result.boxes
    
    for box in boxs: #type: ignore
        track_id = int(box.id.item()) #type:ignore
        cls = int(box.cls.item())
        conf = float(box.conf.item())
        x1, y1, x2, y2 = box.xyxy[0].tolist()

        writer.writerow([
            frame_num,
            track_id,
            cls,
            conf,
            x1,
            y1,
            x2,
            y2
        ])

def close():
    csv_file.close()


        



