import mediapipe as mp

class FaceMeshDetector:
    def __init__(self, max_faces=1):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=max_faces,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def detect(self, rgb_frame):
        """
        Takes RGB frame and returns face landmarks.
        """
        results = self.face_mesh.process(rgb_frame)
        if not results.multi_face_landmarks:
            return None

        return results.multi_face_landmarks[0]   # we use only first face

    def get_landmark(self, landmarks, idx, w, h):
        """
        Returns pixel coordinates of a specific landmark index.
        """
        lm = landmarks.landmark[idx]
        x, y = int(lm.x * w), int(lm.y * h)
        return x, y
