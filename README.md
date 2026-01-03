# AI Video Reframing System (Auto-Shorts)

A **person-aware video reframing system** that converts landscape videos into
stable vertical shorts using computer vision and human-in-the-loop design.

This project emphasizes **temporal stability**, **robust tracking**, and
**practical system engineering**, rather than naive frame-by-frame detection.

---

## 🚀 Key Features

- Human-in-the-loop subject selection
- Subject-locked tracking (no identity switching)
- Temporal smoothing with dead-zone control
- Classical image enhancement for subject thumbnails
- Audio-preserving vertical video rendering
- Clean and interactive Streamlit UI

---

## 🧠 Motivation

Naive object-detection-based reframing often suffers from:

- identity flickering
- unstable camera motion
- false subject switching

This project treats video reframing as a **temporal tracking problem** and
introduces **explicit subject locking** to guarantee stability and predictability.

---

## 🏗️ System Architecture

flowchart TD
    A[User Uploads Video] --> B[Video Preprocessing]
    B --> C["Subject Discovery<br/>(YOLO + Temporal Aggregation)"]

    C --> D[Enhanced Subject Thumbnails]
    D --> E[User Selects Target Subject]

    E --> F["Subject-Locked Tracking<br/>(IoU Association)"]
    F --> G[Dead-Zone Motion Control]

    G --> H["Vertical Cropping<br/>(9:16 Aspect Ratio)"]
    H --> I[Audio Reattachment]
    I --> J[Final Vertical Short Output]



## ⚙️ Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


▶️ Usage
python -m streamlit run app.py