import streamlit as st
import tempfile
import os
import time

from ultralytics import YOLO
from backend.processor import AutoShortsProcessor
from backend.subject_discovery import discover_subjects

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Video Reframing", layout="centered")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0f1117;
    color: #e6e6e6;
}
.subject-card {
    border-radius: 14px;
    padding: 10px;
    background: #1a1d29;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.subject-card:hover {
    transform: scale(1.03);
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}
.warning-box {
    background-color: #2a1f1f;
    border-left: 4px solid #ff6b6b;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

st.title("🎯 AI Video Reframing")
st.caption("Select a subject once. Get stable, vertical framing.")

@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()
processor = AutoShortsProcessor()

if "selected_idx" not in st.session_state:
    st.session_state.selected_idx = None

uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    tfile.close()

    st.video(uploaded_file)

    st.subheader("Detected Subjects")
    subjects = discover_subjects(model, tfile.name)

    if len(subjects) == 0:
        st.warning("No stable subjects detected in the sampled frames.")
        os.remove(tfile.name)
        st.stop()

    # ---------------- USER WARNING ----------------
    st.markdown("""
    <div class="warning-box">
        <strong>Important:</strong><br>
        Please select a subject that is visible for most of the video duration.
        If the selected subject disappears for long periods, the system may lose
        tracking and minor flickering can occur.
    </div>
    """, unsafe_allow_html=True)
    # ------------------------------------------------

    cols = st.columns(len(subjects))

    for i, subj in enumerate(subjects):
        with cols[i]:
            st.markdown('<div class="subject-card">', unsafe_allow_html=True)
            st.image(subj["thumbnail"], width=220)
            if st.button("Select", key=f"select_{i}"):
                st.session_state.selected_idx = i
            st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.selected_idx is not None:
        st.success(f"Subject {st.session_state.selected_idx} selected")

        if st.button("Generate Vertical Short"):
            output_path = "output_short.mp4"
            progress = st.progress(0)

            for p in processor.process_video(
                tfile.name,
                output_path,
                subjects[st.session_state.selected_idx]["box"],
            ):
                progress.progress(p)

            st.video(output_path)

            with open(output_path, "rb") as f:
                st.download_button(
                    "Download Video",
                    f,
                    file_name="ai_short.mp4",
                )

    time.sleep(0.5)
    os.remove(tfile.name)
