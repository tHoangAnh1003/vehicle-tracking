from deep_sort_realtime.deepsort_tracker import DeepSort

def init_tracker():
    return DeepSort(max_age=30)

def update_tracker(tracker, detections):
    tracks = tracker.update_tracks(detections, frame=None)
    return tracks
