import cv2

from configs.config import *
from src.detector import load_model, detect
from src.tracker import init_tracker, update_tracker
from src.visualize import draw_tracks
from src.counter import LineCounter

def main():
    # Load model
    model = load_model(MODEL_PATH)

    # Get class mapping
    class_names = model.model.names
    selected_ids = [
        k for k, v in class_names.items()
        if v in SELECTED_CLASS_NAMES
    ]

    # Init tracker
    tracker = init_tracker()

    # Open video
    cap = cv2.VideoCapture(INPUT_VIDEO)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    out = cv2.VideoWriter(
        OUTPUT_VIDEO,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    # Init counter
    line_y = int(height * LINE_Y_RATIO)
    counter = LineCounter(line_y)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        boxes = detect(model, frame)

        detections = []
        for box in boxes:
            class_id = int(box.cls[0])

            if class_id not in selected_ids:
                continue

            x1, y1, x2, y2 = box.xyxy[0]
            conf = float(box.conf[0])
            class_name = class_names[class_id]

            detections.append((
                [float(x1), float(y1), float(x2 - x1), float(y2 - y1)],
                conf,
                class_name
            ))

        tracks = update_tracker(tracker, detections, frame)

        counter.update(tracks)

        frame = draw_tracks(frame, tracks)
        counter.draw(frame)

        out.write(frame)

    cap.release()
    out.release()

if __name__ == "__main__":
    main()