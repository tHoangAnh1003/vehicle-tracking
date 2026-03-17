import cv2

class LineCounter:
    def __init__(self, y):
        self.y = y
        self.count = 0
        self.prev_positions = {}

    def update(self, tracks):
        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            x1, y1, x2, y2 = track.to_ltrb()
            cy = int((y1 + y2) / 2)

            if track_id in self.prev_positions:
                prev_y = self.prev_positions[track_id]

                if prev_y < self.y and cy >= self.y:
                    self.count += 1

            self.prev_positions[track_id] = cy

    def draw(self, frame):
        h, w, _ = frame.shape

        cv2.line(frame, (0, self.y), (w, self.y), (0, 0, 255), 2)
        cv2.putText(frame, f"Count: {self.count}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)