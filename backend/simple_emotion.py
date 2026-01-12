import cv2
from rmn import RMN

# 1. Initialize the Emotion Detector (PyTorch based)
print("Loading AI model... (This might take a moment)")
m = RMN()

# 2. Start the Camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("✅ Camera started! Press 'q' to quit.")

while True:
    # Read a frame
    ret, frame = cap.read()
    if not ret:
        break

    # 3. Detect Emotion
    # RMN detects faces AND emotions in one go
    results = m.detect_emotion_for_single_frame(frame)

    # results is a list of dictionaries, e.g.:
    # [{'xmin': 100, 'ymin': 200, 'xmax': 300, 'ymax': 400, 'emo_label': 'happy', 'emo_proba': 0.9}]
    
    # If we found a face
    if results:
        # Get the first face found
        face = results[0]
        emotion = face['emo_label']
        confidence = face['emo_proba'] * 100
        
        # Coordinates for the box
        x, y, w, h = face['xmin'], face['ymin'], face['xmax'] - face['xmin'], face['ymax'] - face['ymin']

        # 4. Draw the Box and Text
        cv2.rectangle(frame, (face['xmin'], face['ymin']), (face['xmax'], face['ymax']), (0, 255, 0), 2)
        
        label = f"{emotion.upper()} ({int(confidence)}%)"
        cv2.putText(frame, label, (face['xmin'], face['ymin'] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Print to terminal too
        print(f"User is: {emotion}")

    # Show the video
    cv2.imshow('Antigravity Emotion Test', frame)

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()