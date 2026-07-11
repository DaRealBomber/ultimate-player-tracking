from ultralytics import YOLO


def pre_label(model_name:str, img_size: int, frame_source:str, save_to_directory: str, folder_name:str):
    # Load pretrained model
    model = YOLO(model_name)

    # Run prediction on all images
    model.predict(
        source=frame_source,   # Folder containing images
        save=True,          # Save images with boxes drawn
        save_txt=True,      # Save YOLO labels (.txt)
        save_conf=True,     # Save confidence scores
        conf=0.25,          # Minimum confidence
        imgsz= img_size,         
        project= save_to_directory,
        name= folder_name,
        exist_ok=True
    )

    return f"Completed pre-labelling, results can be found in {save_to_directory}."