import cv2
import time
import config

# Eye-tracking modules only
from utils.camera import Camera
from utils.facemesh_detector import FaceMeshDetector
from utils.gaze_controller import GazeController
from utils.Drag_detector import DragDetector
from utils.blink_detector import BlinkDetector


# ---------------------------------------------------------
# INITIALIZATION
# ---------------------------------------------------------

# Eye tracking
camera = Camera(
    device_index=config.CAMERA_DEVICE,
    width=config.CAMERA_WIDTH,
    height=config.CAMERA_HEIGHT
)
detector = FaceMeshDetector()
gaze = GazeController(
    sensitivity=config.GAZE_SENSITIVITY,
    smooth_factor=config.GAZE_SMOOTH_FACTOR,
    dead_zone=config.GAZE_DEAD_ZONE,
    velocity_threshold=config.GAZE_VELOCITY_THRESHOLD
)
blink = BlinkDetector()
drag = DragDetector()

LEFT_IRIS = 468
RIGHT_IRIS = 473


# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------

print("\n" + "="*60)
print("SCREEN EYE CONTROLLER - SIMPLIFIED MODE")
print("="*60)
print("Features: Eye Tracking + Click + Drag")
print("Press 'q' to quit")
print("="*60 + "\n")

while True:
    frame_start = time.time()
    frame, rgb = camera.get_frame()
    if frame is None:
        break

    h, w, _ = frame.shape

    # --------- FACE DETECTION ---------
    landmarks = detector.detect(rgb)
    if landmarks is None:
        cv2.putText(frame, "No face detected", (40, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.imshow("Eye Controller", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    # --------- IRIS DETECTION ---------
    left_x, left_y = detector.get_landmark(landmarks, LEFT_IRIS, w, h)
    right_x, right_y = detector.get_landmark(landmarks, RIGHT_IRIS, w, h)

    cx = (left_x + right_x) // 2
    cy = (left_y + right_y) // 2

    # --------- GAZE CONTROL ---------
    screen_x, screen_y = None, None

    if not gaze.calibrate(cx, cy):
        cv2.putText(frame, "Calibrating... Look straight (5 sec)", (40, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    else:
        screen_x, screen_y = gaze.compute_cursor(cx, cy, w, h)
        if screen_x is not None:
            gaze.move_cursor(screen_x, screen_y)
            # Draw gaze point on frame
            cv2.circle(frame, (int(cx), int(cy)), 5, (0, 255, 0), -1)
            cv2.putText(frame, f"Gaze: ({int(screen_x)}, {int(screen_y)})", (40, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

    # --------- BLINK DETECTION (CLICKING) ---------
    blink.detect(landmarks, w, h)

    # --------- DRAG DETECTION ---------
    drag.update(landmarks, w, h)

    # --------- DISPLAY INFO ---------
    frame_time = time.time() - frame_start
    fps = 1.0 / frame_time if frame_time > 0 else 0
    
    cv2.putText(frame, f"FPS: {fps:.1f}", (w-200, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
    cv2.putText(frame, "Left blink=Click | Right blink=Right-click | Hold right=Drag", (10, h-20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 0), 1)

    # Show window
    cv2.imshow("Eye Controller", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\nExiting...")
        break

camera.release()
cv2.destroyAllWindows()
print("✅ Application closed")
