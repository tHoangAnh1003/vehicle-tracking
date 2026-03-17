from ultralytics import YOLO

def load_model(weights_path):
    model = YOLO(weights_path)
    return model

def detect(model, frame):
    results = model(frame)[0]
    return results