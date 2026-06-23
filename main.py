"""AI Aim Assist - Main entry point."""

import time
import threading
import yaml
from pathlib import Path

from src.detector import Detector
from src.capture import ScreenCapture
from src.mouse import MouseController
from src.overlay import Overlay
from src.utils import load_config, get_screen_center, closest_target


def main():
    config = load_config("config.yaml")

    print("\n🎯 AI Aim Assist — Starting...")
    print(f"   Model : {config['model_path']}")
    print(f"   Device: {config['device']}")
    print(f"   Toggle: {config['toggle_key']} to enable/disable\n")

    detector = Detector(
        model_path=config["model_path"],
        confidence=config["confidence"],
        target_class=config["target_class"],
        device=config["device"],
    )

    capture = ScreenCapture(
        width=config["capture_width"],
        height=config["capture_height"],
    )

    mouse = MouseController(
        smoothing=config["smoothing"],
        trigger_enabled=config["trigger_enabled"],
        trigger_fov=config["trigger_fov"],
    )

    overlay = Overlay(enabled=config["overlay"])

    # Toggle state
    active = threading.Event()
    stop_event = threading.Event()

    def hotkey_listener():
        """Listen for toggle hotkey in a background thread."""
        try:
            from pynput import keyboard

            toggle_key = getattr(keyboard.Key, config["toggle_key"].lower(), None)
            if toggle_key is None:
                toggle_key = keyboard.KeyCode.from_char(config["toggle_key"].lower())

            def on_press(key):
                if key == toggle_key:
                    if active.is_set():
                        active.clear()
                        print("[AIM] Disabled")
                    else:
                        active.set()
                        print("[AIM] Enabled")

            with keyboard.Listener(on_press=on_press) as listener:
                while not stop_event.is_set():
                    time.sleep(0.05)
                listener.stop()
        except Exception as e:
            print(f"[WARN] Hotkey listener error: {e}")

    hotkey_thread = threading.Thread(target=hotkey_listener, daemon=True)
    hotkey_thread.start()

    screen_cx, screen_cy = get_screen_center()
    aim_offset_x = config.get("aim_offset_x", 0)
    aim_offset_y = config.get("aim_offset_y", 0)
    fov_radius = config.get("fov_radius", 0)

    print(f"[INFO] Screen center: ({screen_cx}, {screen_cy})")
    print("[INFO] Press the toggle key to activate. Ctrl+C to quit.\n")

    try:
        while True:
            frame = capture.grab()
            if frame is None:
                time.sleep(0.001)
                continue

            detections = detector.detect(frame)

            if active.is_set() and detections:
                # Convert detections from capture-space to screen-space
                cap_w = config["capture_width"]
                cap_h = config["capture_height"]
                offset_x = screen_cx - cap_w // 2
                offset_y = screen_cy - cap_h // 2

                screen_targets = []
                for det in detections:
                    tx = int(det["cx"] + offset_x + aim_offset_x)
                    ty = int(det["cy"] + offset_y + aim_offset_y)
                    screen_targets.append({"x": tx, "y": ty, "w": det["w"], "h": det["h"]})

                target = closest_target(screen_targets, screen_cx, screen_cy, fov_radius)

                if target:
                    mouse.move_toward(target["x"], target["y"], screen_cx, screen_cy)

            if overlay.enabled:
                overlay.render(frame, detections, active.is_set())

            time.sleep(0.001)

    except KeyboardInterrupt:
        print("\n[INFO] Stopping...")
        stop_event.set()
        overlay.close()


if __name__ == "__main__":
    main()
