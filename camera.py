import cv2

class Camera:
    def __init__(self, device_index=0, width=640, height=480):
        """
        Initialize the camera.
        device_index: 0 for laptop webcam, 1 for external camera.
        width, height: camera resolution.
        """
        self.cap = cv2.VideoCapture(device_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def get_frame(self):
        """
        Reads a frame from the camera.
        Returns (frame_bgr, frame_rgb).
        """
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        # Flip for natural mirror-like view
        frame = cv2.flip(frame, 1)

        # Convert BGR → RGB for MediaPipe
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return frame, rgb

    def release(self):
        """
        Releases camera safely.
        """
        self.cap.release()
        cv2.destroyAllWindows()
