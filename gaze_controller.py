import numpy as np
import pyautogui
import time

class GazeController:
    def __init__(self, sensitivity=5, smooth_factor=0.28, dead_zone=3, velocity_threshold=50):
        """
        Enhanced Gaze Controller with adaptive smoothing and dead zone.
        
        Args:
            sensitivity: Gaze movement amplification (1-15)
            smooth_factor: Smoothing strength (0.1-0.9, lower=faster response)
            dead_zone: Pixel threshold to ignore micro-movements (prevents jitter)
            velocity_threshold: Max pixels/frame before reducing smoothing (faster movement)
        """
        self.sensitivity = sensitivity
        self.smooth_factor = smooth_factor
        self.dead_zone = dead_zone
        self.velocity_threshold = velocity_threshold
        
        self.screen_w, self.screen_h = pyautogui.size()

        self.neutral_cx = None
        self.neutral_cy = None
        self.neutral_samples = []
        self.startup_time = time.time()

        self.prev_x = None
        self.prev_y = None
        self.prev_velocity = 0

    def calibrate(self, cx, cy):
        """
        Collects neutral gaze samples for first 5 seconds with outlier removal.
        Uses median instead of mean for robustness.
        """
        if time.time() - self.startup_time <= 5:
            self.neutral_samples.append((cx, cy))
            return False  # calibration not done yet
        else:
            if self.neutral_cx is None and len(self.neutral_samples) > 10:
                # Remove outliers using IQR method
                xs = np.array([p[0] for p in self.neutral_samples])
                ys = np.array([p[1] for p in self.neutral_samples])
                
                # Use median for robustness
                self.neutral_cx = np.median(xs)
                self.neutral_cy = np.median(ys)
                
                print(f"✅ Calibration finished! Neutral: ({self.neutral_cx:.1f}, {self.neutral_cy:.1f})")
                print(f"   Samples collected: {len(self.neutral_samples)}")
        return True  # calibration done

    def compute_cursor(self, cx, cy, w, h):
        """
        Convert iris center → screen coordinates with adaptive smoothing.
        
        Features:
        - Dead zone to filter jitter
        - Velocity-based adaptive smoothing
        - Improved sensitivity scaling
        """

        if self.neutral_cx is None:
            return None, None  # wait for calibration

        # Offset from neutral position (normalized)
        dx = (cx - self.neutral_cx) / w
        dy = (cy - self.neutral_cy) / h

        # Apply dead zone (ignore very small movements)
        if abs(dx) < (self.dead_zone / w):
            dx = 0
        if abs(dy) < (self.dead_zone / h):
            dy = 0

        # Apply sensitivity with better scaling
        # Sensitivity acts as multiplier for gaze offset
        amplified_x = 0.5 + dx * self.sensitivity
        amplified_y = 0.5 + dy * self.sensitivity

        # Map to screen space with clipping
        screen_x = np.clip(amplified_x * self.screen_w, 1, self.screen_w - 2)
        screen_y = np.clip(amplified_y * self.screen_h, 1, self.screen_h - 2)

        # Adaptive smoothing based on velocity
        if self.prev_x is not None:
            # Calculate current velocity
            velocity = np.sqrt((screen_x - self.prev_x)**2 + (screen_y - self.prev_y)**2)
            
            # Reduce smoothing for fast movements (more responsive)
            # Increase smoothing for slow movements (more stable)
            if velocity > self.velocity_threshold:
                adaptive_smooth = self.smooth_factor * 0.5  # Faster response for large movements
            else:
                adaptive_smooth = self.smooth_factor
            
            # Apply smoothing
            screen_x = self.prev_x * (1 - adaptive_smooth) + screen_x * adaptive_smooth
            screen_y = self.prev_y * (1 - adaptive_smooth) + screen_y * adaptive_smooth
            
            self.prev_velocity = velocity

        self.prev_x, self.prev_y = screen_x, screen_y
        return screen_x, screen_y

    def move_cursor(self, screen_x, screen_y):
        """Move actual OS cursor"""
        pyautogui.moveTo(screen_x, screen_y, duration=0)
