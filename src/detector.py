"""YOLOv8 inference wrapper."""

from __future__ import annotations

from typing import Optional
import numpy as np


class Detector:
    """Wraps Ultralytics YOLOv8 for real-time object detection."""

    def __init__(
        self,
        model_path: str,
        confidence: float = 0.5,
        target_class: int = -1,
        device: str = "auto",
    ):
        from ultralytics import YOLO
        import torch

        if device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        print(f"[Detector] Loading model: {model_path} on {self.device}")
        self.model = YOLO(model_path)
        self.model.to(self.device)
        self.confidence = confidence
        self.target_class = target_class

        # Warm-up pass
        dummy = np.zeros((640, 640, 3), dtype=np.uint8)
        self.model(dummy, verbose=False)
        print("[Detector] Model ready.")

    def detect(self, frame: np.ndarray) -> list[dict]:
        """Run inference and return list of target dicts.

        Each dict has keys: cx, cy, w, h, conf, cls
        """
        results = self.model(
            frame,
            verbose=False,
            conf=self.confidence,
            device=self.device,
        )

        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue
            for box in boxes:
                cls = int(box.cls[0])
                if self.target_class != -1 and cls != self.target_class:
                    continue

                x1, y1, x2, y2 = map(float, box.xyxy[0])
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                w = x2 - x1
                h = y2 - y1
                conf = float(box.conf[0])

                detections.append(
                    {"cx": cx, "cy": cy, "w": w, "h": h, "conf": conf, "cls": cls}
                )

        return detections
