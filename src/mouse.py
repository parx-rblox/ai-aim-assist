"""Smooth mouse movement controller."""

from __future__ import annotations

import sys
import math


class MouseController:
    """Moves the mouse smoothly toward a target position."""

    def __init__(
        self,
        smoothing: float = 6.0,
        trigger_enabled: bool = False,
        trigger_fov: int = 10,
    ):
        self.smoothing = max(1.0, smoothing)
        self.trigger_enabled = trigger_enabled
        self.trigger_fov = trigger_fov

        # Prefer win32api on Windows for lower latency
        self._use_win32 = False
        if sys.platform == "win32":
            try:
                import win32api
                import win32con
                self._win32api = win32api
                self._win32con = win32con
                self._use_win32 = True
                print("[Mouse] Using win32api")
            except ImportError:
                pass

        if not self._use_win32:
            from pynput.mouse import Controller, Button
            self._pynput = Controller()
            self._Button = Button
            print("[Mouse] Using pynput")

    def move_toward(self, tx: int, ty: int, cx: int, cy: int) -> None:
        """Move mouse from current center (cx, cy) toward target (tx, ty)."""
        dx = (tx - cx) / self.smoothing
        dy = (ty - cy) / self.smoothing

        # Skip tiny movements to avoid jitter
        if abs(dx) < 0.5 and abs(dy) < 0.5:
            return

        if self._use_win32:
            import win32api
            cur_x, cur_y = win32api.GetCursorPos()
            new_x = int(cur_x + dx)
            new_y = int(cur_y + dy)
            win32api.mouse_event(
                self._win32con.MOUSEEVENTF_MOVE,
                int(dx),
                int(dy),
                0,
                0,
            )
        else:
            self._pynput.move(int(dx), int(dy))

        # Trigger bot
        if self.trigger_enabled:
            dist = math.sqrt(dx ** 2 + dy ** 2)
            if dist <= self.trigger_fov:
                self._click()

    def _click(self) -> None:
        """Perform a left-click."""
        if self._use_win32:
            self._win32api.mouse_event(self._win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            self._win32api.mouse_event(self._win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        else:
            self._pynput.press(self._Button.left)
            self._pynput.release(self._Button.left)
