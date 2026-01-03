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


class LockedPersonTracker:
    """
    Subject-locked tracker with dead-zone control
    to suppress micro-jitter.
    """

    def __init__(
        self,
        model,
        target_box,
        conf_threshold=0.4,
        dead_zone_ratio=0.02,  # 2% of frame width
    ):
        self.model = model
        self.target_box = target_box
        self.conf_threshold = conf_threshold
        self.dead_zone_ratio = dead_zone_ratio

        self.prev_center = (target_box[0] + target_box[2]) / 2

    def get_target_center(self, frame):
        frame_width = frame.shape[1]
        dead_zone_px = frame_width * self.dead_zone_ratio

        results = self.model(frame, verbose=False, classes=[0])

        best_match = None
        best_iou = 0.0

        for result in results:
            for box in result.boxes:
                conf = float(box.conf[0])
                if conf < self.conf_threshold:
                    continue

                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                candidate = (x1, y1, x2, y2)

                score = iou(candidate, self.target_box)
                if score > best_iou:
                    best_iou = score
                    best_match = candidate

        if best_match is not None:
            self.target_box = best_match
            new_center = (best_match[0] + best_match[2]) / 2

            if abs(new_center - self.prev_center) < dead_zone_px:
                return self.prev_center

            self.prev_center = new_center
            return new_center

        return self.prev_center
