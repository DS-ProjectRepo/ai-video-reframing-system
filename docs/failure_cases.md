# Failure Cases & Limitations

This document lists known failure cases observed during testing.

---

## 1. Subject Disappearance

If the selected subject leaves the frame for extended durations,
the tracker may lose spatial context, causing minor jitter.

**Mitigation**
- User guidance during subject selection
- Dead-zone control to suppress sudden jumps

---

## 2. Heavy Occlusion

Severe occlusion or overlapping objects can degrade detection quality.

**Mitigation**
- IoU-based subject locking
- Temporal aggregation during discovery

---

## 3. Extremely Small or Distant Subjects

Very small subjects may appear blurred in thumbnails and be harder to track.

**Mitigation**
- Classical image enhancement pipeline
- Minimum size filtering during discovery

---

## 4. Rapid Camera Motion

Fast camera pans may introduce lag due to temporal smoothing.

**Mitigation**
- Tunable dead-zone and smoothing parameters
