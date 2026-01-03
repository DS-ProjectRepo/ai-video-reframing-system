import cv2
import numpy as np


def iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    inter = max(0, xB - xA) * max(0, yB - yA)
    areaA = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    areaB = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    if areaA + areaB - inter == 0:
        return 0.0

    return inter / (areaA + areaB - inter)


# ----------------- IMAGE ENHANCEMENT PIPELINE -----------------

def enhance_thumbnail(crop, target_size=256):
    """
    Classical super-resolution + denoise + sharpening pipeline
    """
    # BGR → RGB
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)

    h, w, _ = crop.shape
    if h < 10 or w < 10:
        return crop  # avoid junk crops

    # --- 1. High-quality upscaling ---
    scale = target_size / max(h, w)
    new_w, new_h = int(w * scale), int(h * scale)

    crop = cv2.resize(
        crop,
        (new_w, new_h),
        interpolation=cv2.INTER_LANCZOS4
    )

    # --- 2. Edge-preserving denoise ---
    crop = cv2.bilateralFilter(
        crop,
        d=9,
        sigmaColor=75,
        sigmaSpace=75
    )

    # --- 3. Unsharp masking ---
    gaussian = cv2.GaussianBlur(crop, (0, 0), sigmaX=1.0)
    crop = cv2.addWeighted(crop, 1.5, gaussian, -0.5, 0)

    return crop


# ----------------- SUBJECT DISCOVERY -----------------

def discover_subjects(
    model,
    video_path,
    sample_rate=20,
    conf_threshold=0.35,
    max_subjects=5,
):
    cap = cv2.VideoCapture(video_path)

    tracks = []
    frame_id = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % sample_rate != 0:
            frame_id += 1
            continue

        results = model(frame, verbose=False, classes=[0])

        for result in results:
            for box in result.boxes:
                conf = float(box.conf[0])
                if conf < conf_threshold:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                area = (x2 - x1) * (y2 - y1)
                curr_box = (x1, y1, x2, y2)

                matched = False
                for track in tracks:
                    if iou(track["box"], curr_box) > 0.3:
                        track["box"] = curr_box
                        track["count"] += 1
                        track["area_sum"] += area
                        matched = True
                        break

                if not matched:
                    crop = frame[y1:y2, x1:x2]
                    thumb = enhance_thumbnail(crop)

                    tracks.append({
                        "box": curr_box,
                        "count": 1,
                        "area_sum": area,
                        "thumbnail": thumb,
                    })

        frame_id += 1
        if frame_id > sample_rate * 50:
            break

    cap.release()

    for t in tracks:
        t["score"] = t["count"] * (t["area_sum"] / t["count"])

    tracks.sort(key=lambda x: x["score"], reverse=True)

    return tracks[:max_subjects]
