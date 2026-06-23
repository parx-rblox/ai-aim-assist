"""High-speed screen capture using mss."""

from __future__ import annotations

import numpy as np


class ScreenCapture:
    """Captures a centered region of the primary monitor."""

    def __init__(self, width: int = 640, height: int = 640):
        import mss
        import ctypes

        self.width = width
        self.height = height
        self.sct = mss.mss()

        # Get real screen resolution (handles DPI scaling on Windows)
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            pass

        monitor_info = self.sct.monitors[1]  # Primary monitor
        self.screen_w = monitor_info["width"]
        self.screen_h = monitor_info["height"]

        # Centered capture region
        self.region = {
            "top": (self.screen_h - height) // 2,
            "left": (self.screen_w - width) // 2,
            "width": width,
            "height": height,
        }
        print(
            f"[Capture] Region: {self.region['left']},{self.region['top']} "
            f"{width}x{height} (screen {self.screen_w}x{self.screen_h})"
        )

    def grab(self) -> np.ndarray | None:
        """Capture and return BGR numpy array, or None on failure."""
        try:
            screenshot = self.sct.grab(self.region)
            # mss returns BGRA, convert to BGR for OpenCV/YOLO
            frame = np.array(screenshot, dtype=np.uint8)[:, :, :3]
            return frame
        except Exception as e:
            print(f"[Capture] Error: {e}")
            return None
