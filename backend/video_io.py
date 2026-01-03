import cv2
from moviepy.editor import VideoFileClip

def open_video(path):
    cap = cv2.VideoCapture(path)

    props = {
        "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": int(cap.get(cv2.CAP_PROP_FPS)),
        "total_frames": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
    }
    return cap, props


def create_writer(path, fps, width, height):
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    return cv2.VideoWriter(path, fourcc, fps, (width, height))


def merge_audio(original_path, processed_path, output_path):
    original = VideoFileClip(original_path)
    processed = VideoFileClip(processed_path)

    final = processed.set_audio(original.audio)
    final.write_videofile(
        output_path, codec="libx264", audio_codec="aac"
    )

    original.close()
    processed.close()
    final.close()
