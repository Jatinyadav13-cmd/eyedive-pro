import time
import pyautogui


class DragDetector:
    def __init__(self):
        self.drag_threshold = 1.2   # improved tolerance
        self.open_threshold = 4.5   # eye must be fully open to stop
        self.hold_time = 0.40       # hold duration to start drag
        self.release_delay = 0.15   # stable open before releasing

        self.dragging = False
        self.close_start = None
        self.open_start = None

    def eye_ratio(self, top, bottom, h):
        return abs((top.y - bottom.y) * h)

    def update(self, landmarks, w, h):
        right_top = landmarks.landmark[386]
        right_bottom = landmarks.landmark[374]
        left_top = landmarks.landmark[159]
        left_bottom = landmarks.landmark[145]

        right_ratio = self.eye_ratio(right_top, right_bottom, h)
        left_ratio = self.eye_ratio(left_top, left_bottom, h)

        now = time.time()

        # ------------------------------------
        # START DRAG → right eye long close
        # ------------------------------------
        if right_ratio < self.drag_threshold and left_ratio > 4.0:
            if self.close_start is None:
                self.close_start = now
            elif not self.dragging and (now - self.close_start) > self.hold_time:
                pyautogui.mouseDown(button="left")
                self.dragging = True
                print("🟣 DRAG START")
        else:
            self.close_start = None

        # ------------------------------------
        # STOP DRAG → right eye fully open
        # ------------------------------------
        if self.dragging:
            if right_ratio > self.open_threshold:
                if self.open_start is None:
                    self.open_start = now
                elif (now - self.open_start) > self.release_delay:
                    pyautogui.mouseUp(button="left")
                    self.dragging = False
                    print("🟠 DRAG STOP")
            else:
                self.open_start = None
