import time
import pyautogui


class BlinkDetector:
    def __init__(self):
        # thresholds from your eyelid ratios
        self.left_threshold = 2.5
        self.right_threshold = 2.0

        # timings
        self.blink_gap = 0.28      # time allowed for double blink
        self.cooldown = 0.20       # global cooldown

        # timestamps
        self.last_left_blink = 0
        self.last_right_blink = 0
        self.last_action = time.time()

    def eye_ratio(self, top, bottom, h):
        return abs((top.y - bottom.y) * h)

    def detect(self, landmarks, w, h):
        now = time.time()

        # Prevent spam
        if now - self.last_action < self.cooldown:
            return

        left_top = landmarks.landmark[159]
        left_bottom = landmarks.landmark[145]
        right_top = landmarks.landmark[386]
        right_bottom = landmarks.landmark[374]

        left_ratio = self.eye_ratio(left_top, left_bottom, h)
        right_ratio = self.eye_ratio(right_top, right_bottom, h)

        # ---------------------------------
        # LEFT EYE ACTION (Left click / double click)
        # ---------------------------------
        if left_ratio < self.left_threshold and right_ratio > 4.0:
            if now - self.last_left_blink < self.blink_gap:
                pyautogui.doubleClick(button="left")
                print("🟢 LEFT DOUBLE CLICK")
            else:
                pyautogui.click(button="left")
                print("🟢 LEFT CLICK")

            self.last_left_blink = now
            self.last_action = now
            return

        # ---------------------------------
        # RIGHT EYE ACTION (Right click / double click)
        # ---------------------------------
        if right_ratio < self.right_threshold and left_ratio > 4.0:
            if now - self.last_right_blink < self.blink_gap:
                pyautogui.doubleClick(button="right")
                print("🔵 RIGHT DOUBLE CLICK")
            else:
                pyautogui.click(button="right")
                print("🔵 RIGHT CLICK")

            self.last_right_blink = now
            self.last_action = now
            return
