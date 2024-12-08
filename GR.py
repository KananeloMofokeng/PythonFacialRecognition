import cv2
import mediapipe as mp
import math

# Initialize face mesh model
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

# Set up FaceMesh
with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        # Flip the image horizontally for a selfie-view display
        frame = cv2.flip(frame, 1)
        
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Perform face mesh
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for landmarks in results.multi_face_landmarks:
                # Get the coordinates of key points for the calculations (Nose to Chin, Eye to Eye, etc.)
                
                # Landmarks for the nose (nose tip) and chin
                nose = landmarks.landmark[1]  # Landmark 1: Nose tip
                chin = landmarks.landmark[152]  # Landmark 152: Chin

                # Landmarks for the eyes (left and right)
                left_eye = landmarks.landmark[33]  # Landmark 33: Left eye
                right_eye = landmarks.landmark[133]  # Landmark 133: Right eye

                # Calculate Euclidean distance between points using the formula:
                # sqrt((x2 - x1)^2 + (y2 - y1)^2 + (z2 - z1)^2)
                def distance(point1, point2):
                    return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2 + (point2.z - point1.z) ** 2)
                
                # Calculate the distances for the measurements
                nose_chin_distance = distance(nose, chin)  # Nose to Chin
                eye_to_eye_distance = distance(left_eye, right_eye)  # Eye to Eye
                face_height = distance(nose, chin)  # Could also use forehead to chin, but this works as a start

                # Golden Ratio calculation
                golden_ratio = 1.618
                ratio = nose_chin_distance / eye_to_eye_distance

                # Display the Golden Ratio result on the image
                if ratio >= golden_ratio:
                    cv2.putText(frame, f"Golden Ratio: {ratio:.2f} (Good)", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                else:
                    cv2.putText(frame, f"Golden Ratio: {ratio:.2f} (Not Ideal)", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                # Draw landmarks on the face
                mp_drawing.draw_landmarks(frame, landmarks, mp_face_mesh.FACEMESH_TESSELATION)

        # Show the result
        cv2.imshow('Face Mesh with Golden Ratio', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
