# AI Video Reframing System – Detailed Project Explanation

## 1. Problem Statement

Short-form video platforms (Instagram Reels, YouTube Shorts, TikTok) require
vertical (9:16) videos. However, most videos are recorded in landscape format.
Naively cropping the center of the frame often results in:

- important subjects being cut off
- unstable camera motion
- frequent subject switching
- visible flickering

This project aims to design a **robust, stable, and user-controllable**
AI-based video reframing system that converts landscape videos into
vertical shorts while maintaining subject focus and temporal smoothness.

---

## 2. Design Philosophy

Instead of treating the problem as a purely automatic detection task,
this project models video reframing as a **temporal tracking problem**
with **human-in-the-loop control**.

Key principles:

- Temporal stability is more important than frame-wise accuracy
- Identity consistency is critical to avoid flicker
- User guidance is preferable to unreliable automation
- Classical CV methods are favored where deep models are unnecessary

---

## 3. High-Level System Pipeline

1. Video upload via Streamlit UI
2. Subject discovery using YOLO on sampled frames
3. Temporal aggregation of detected subjects
4. Enhanced subject thumbnail generation
5. User selects the main subject to track
6. Subject-locked tracking throughout the video
7. Dead-zone motion control to suppress jitter
8. Vertical cropping to 9:16 aspect ratio
9. Audio reattachment and final rendering

---

## 4. Technologies and Libraries Used

### 4.1 Streamlit
Used for building an interactive web-based UI.
Chosen for rapid prototyping, clean state handling, and ease of deployment.

### 4.2 OpenCV (cv2)
Used for:
- video frame reading and writing
- image resizing and filtering
- color-space conversion
- classical image processing operations

### 4.3 Ultralytics YOLOv8
Used for person detection.
The lightweight `yolov8n` model was chosen for:
- fast inference
- acceptable accuracy
- low resource usage

YOLO is used **only for detection**, not tracking.

### 4.4 MoviePy
Used to:
- extract audio from original video
- reattach audio to processed video
- ensure output video preserves sound

### 4.5 NumPy
Used for:
- numerical computations
- bounding box geometry
- filter kernels

---

## 5. Subject Discovery Algorithm

### 5.1 Frame Sampling

Instead of processing every frame, frames are sampled at a fixed interval
(e.g., every 20 frames) to reduce computation while preserving coverage.

### 5.2 Person Detection

YOLO is applied to sampled frames to detect bounding boxes for class `person`.

Low-confidence detections are discarded using a confidence threshold.

---

## 6. Temporal Aggregation & Importance Scoring

Detected persons across frames are grouped using **IoU-based association**.

Each subject track maintains:
- latest bounding box
- detection count
- cumulative bounding box area

### Importance Score:
importance = detection_count × average_area


This prioritizes subjects that:
- appear consistently
- occupy meaningful screen space

---

## 7. Human-in-the-Loop Subject Selection

Instead of automatically choosing the largest or most confident detection,
the system displays enhanced thumbnails and allows the user to explicitly
select the subject to track.

Benefits:
- eliminates identity switching
- prevents incorrect subject focus
- mirrors professional video-editing tools

---

## 8. Thumbnail Enhancement Pipeline

Detected subject crops are often small and blurry.
A classical image enhancement pipeline is applied:

### 8.1 Color Correction
- Convert from OpenCV BGR to RGB

### 8.2 High-Quality Upscaling
- Resize using `INTER_LANCZOS4` interpolation

### 8.3 Edge-Preserving Denoising
- Bilateral filter reduces noise while preserving edges

### 8.4 Unsharp Masking
- Enhances edges without over-sharpening

This improves UX without using heavy deep-learning super-resolution models.

---

## 9. Subject-Locked Tracking Algorithm

Once a subject is selected, tracking is **locked** to that subject.

### 9.1 IoU-Based Association
For each frame:
- detect persons
- compute IoU with the last known bounding box
- select the best match

If no match is found, the previous position is retained temporarily.

---

## 10. Dead-Zone Motion Control (Jitter Suppression)

YOLO bounding boxes fluctuate slightly frame-to-frame, causing micro-jitter.

To suppress this:
dead_zone = dead_zone_ratio × frame_width


If the subject center moves less than the dead-zone threshold,
the camera position is not updated.

This prevents unnecessary camera movement while allowing real motion.

---

## 11. Vertical Cropping Strategy

- Target aspect ratio: 9:16
- Crop width computed from original height
- Crop center determined by tracked subject
- Boundary checks ensure crop stays within frame

---

## 12. Audio Preservation

Since OpenCV does not handle audio:
- MoviePy extracts audio from the original video
- Audio is attached to the processed video
- Final output preserves original sound

---

## 13. User Experience Safeguards

The UI explicitly warns users:
- to select subjects visible for most of the video
- that long subject disappearance may cause tracking degradation

This sets correct expectations and improves perceived system reliability.

---

## 14. Failure Cases & Limitations

- Subject leaves frame for extended duration
- Heavy occlusion or extreme motion blur
- Very small or distant subjects
- Rapid camera motion causing smoothing lag

These are partially mitigated but not fully eliminated.

---

## 15. Why Human-in-the-Loop Was Chosen

Fully automatic tracking suffers from:
- identity instability
- unreliable importance estimation
- flicker in complex scenes

Human-in-the-loop selection guarantees:
- identity consistency
- predictable behavior
- professional-grade output

---

## 16. Future Work

- Automatic subject importance modeling
- Identity-aware tracking (DeepSORT / ReID)
- Optical-flow-based refinement
- Batch video processing
- Quantitative jitter evaluation metrics

---

## 17. Academic Context

This project was developed as a **Master’s-level Data Science project**,
emphasizing:

- system robustness
- explainable design decisions
- real-world deployment constraints
- engineering trade-offs over raw accuracy
