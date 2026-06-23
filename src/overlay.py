"""Optional real-time debug overlay using OpenCV."""

from __future__ import annotations

from typing import List
import numpy as np


class Overlay:
    """Renders detection bounding boxes and FOV circle in a debug window."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        if enabled:
            import cv2
            self._cv2 = cv2
            cv2.namedWindow("AI Aim Assist - Debug", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("AI Aim Assist - Debug", 640, 640)

    def render(
        self,
        frame: np.ndarray,
        detections: List[dict],
        active: bool,
    ) -> None:
        """Draw detections onto the frame and display it."""
        if not self.enabled:
            return

        vis = frame.copy()
        h, w = vis.shape[:2]
        cx, cy = w // 2, h // 2

        # Status indicator
        status_text = "ACTIVE" if active else "INACTIVE"
        status_color = (0, 255, 80) if active else (0, 80, 255)
        self._cv2.putText(
            vis, status_text, (10, 30),
            self._cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2
        )

        # FOV circle
        self._cv2.circle(vis, (cx, cy), 200, (100, 100, 255), 1)

        # Crosshair
        self._cv2.line(vis, (cx - 12, cy), (cx + 12, cy), (255, 255, 255), 1)
        self._cv2.line(vis, (cx, cy - 12), (cx, cy + 12), (255, 255, 255), 1)

        # Bounding boxes
        for det in detections:
            x1 = int(det["cx"] - det["w"] / 2)
            y1 = int(det["cy"] - det["h"] / 2)
            x2 = int(det["cx"] + det["w"] / 2)
            y2 = int(det["cy"] + det["h"] / 2)
            self._cv2.rectangle(vis, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{det['conf']:.2f}"
            self._cv2.putText(
                vis, label, (x1, y1 - 6),
                self._cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1
            )

        self._cv2.imshow("AI Aim Assist - Debug", vis)
        self._cv2.waitKey(1)

    def close(self) -> None:
        if self.enabled:
            self._cv2.destroyAllWindows()
