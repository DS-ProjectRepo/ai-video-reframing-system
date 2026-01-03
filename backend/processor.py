from ultralytics import YOLO

from backend.tracker import LockedPersonTracker
from backend.video_io import open_video, create_writer, merge_audio


class AutoShortsProcessor:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)

    def process_video(self, input_path, output_path, selected_box):
        """
        Parameters
        ----------
        input_path : str
            Path to input video
        output_path : str
            Path to output video
        selected_box : tuple (x1, y1, x2, y2)
            Initial bounding box of the selected subject
        """
        cap, props = open_video(input_path)

        orig_width = props["width"]
        orig_height = props["height"]
        fps = props["fps"]
        total_frames = props["total_frames"]

        # Target vertical crop (9:16)
        target_height = orig_height
        target_width = int(target_height * 9 / 16)

        temp_video_path = "temp_video.mp4"
        out = create_writer(
            temp_video_path,
            fps,
            target_width,
            target_height,
        )

        tracker = LockedPersonTracker(
            model=self.model,
            target_box=selected_box,
        )

        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            center = tracker.get_target_center(frame)

            x_start = int(center - target_width / 2)
            x_start = max(0, min(x_start, orig_width - target_width))

            cropped = frame[:, x_start : x_start + target_width]
            out.write(cropped)

            frame_count += 1
            yield frame_count / total_frames

        cap.release()
        out.release()

        merge_audio(input_path, temp_video_path, output_path)
