import cv2

def process_video(input_path, callback):
    cap = cv2.VideoCapture(input_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        callback(frame)

    cap.release()
