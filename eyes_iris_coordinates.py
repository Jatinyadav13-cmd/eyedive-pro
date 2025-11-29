from utils.camera import Camera
from utils.facemesh_detector import FaceMeshDetector
import cv2

# Initialize
camera = Camera()
detector = FaceMeshDetector()

# Iris landmark indices
LEFT_IRIS = 468
RIGHT_IRIS = 473

while True:
    frame, rgb = camera.get_frame()
    if frame is None:
        break

    h, w, _ = frame.shape

    # Detect face mesh landmarks
    landmarks = detector.detect(rgb)

    if landmarks:
        # Get left iris landmark center
        left_x, left_y = detector.get_landmark(landmarks, LEFT_IRIS, w, h)

        # Get right iris landmark center
        right_x, right_y = detector.get_landmark(landmarks, RIGHT_IRIS, w, h)

        # Draw points
        cv2.circle(frame, (left_x, left_y), 3, (0, 255, 0), -1)
        cv2.circle(frame, (right_x, right_y), 3, (0, 0, 255), -1)

        # Display coordinates
        cv2.putText(frame, f"L: {left_x},{left_y}", (left_x+10, left_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
        cv2.putText(frame, f"R: {right_x},{right_y}", (right_x+10, right_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

    cv2.imshow("Iris Landmarks", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
