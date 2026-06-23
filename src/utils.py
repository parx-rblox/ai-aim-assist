"""Utility functions."""

from __future__ import annotations

import math
from typing import Optional
import yaml


def load_config(path: str) -> dict:
    """Load YAML config file."""
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    print(f"[Config] Loaded: {path}")
    return config


def get_screen_center() -> tuple[int, int]:
    """Return the center pixel of the primary monitor."""
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        user32 = ctypes.windll.user32
        w = user32.GetSystemMetrics(0)
        h = user32.GetSystemMetrics(1)
        return w // 2, h // 2
    except Exception:
        pass

    try:
        import subprocess
        result = subprocess.run(
            ["xrandr"], capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if " connected" in line and "+0+0" in line:
                res = line.split()[2].split("+")[0]
                w, h = map(int, res.split("x"))
                return w // 2, h // 2
    except Exception:
        pass

    return 960, 540  # fallback 1920x1080 center


def closest_target(
    targets: list[dict],
    cx: int,
    cy: int,
    fov_radius: int = 0,
) -> Optional[dict]:
    """Return the target closest to (cx, cy), optionally limited to fov_radius."""
    best = None
    best_dist = float("inf")

    for t in targets:
        dist = math.sqrt((t["x"] - cx) ** 2 + (t["y"] - cy) ** 2)
        if fov_radius > 0 and dist > fov_radius:
            continue
        if dist < best_dist:
            best_dist = dist
            best = t

    return best
