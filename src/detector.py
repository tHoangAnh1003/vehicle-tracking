from ultralytics import YOLO

def load_model(weights_path):
    return YOLO(weights_path)

def detect(model, frame):
    results = model(frame, verbose=False)[0]
    return results.boxes