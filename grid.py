import cv2
import os
import time
import threading
import tkinter as tk
from tkinter import messagebox

# Specify the folder path where you want to save the images
save_folder = 'C:/CS PROJECT/saved_faces'

# Ensure the folder exists
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

def draw_center_rectangle(frame, width_ratio=3, height_ratio=4):
    height, width, _ = frame.shape
    rect_width = width // 2
    rect_height = int(rect_width * (height_ratio / width_ratio))
    x1 = (width - rect_width) // 2
    y1 = (height - rect_height) // 2
    x2 = x1 + rect_width
    y2 = y1 + rect_height

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return frame, (x1, y1, x2, y2)

def detect_and_save_face(frame, rect_coords, face_cascade, padding=20):
    x1, y1, x2, y2 = rect_coords
    roi = frame[y1:y2, x1:x2]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (fx, fy, fw, fh) in faces:
        # Calculate padding
        x_padding = padding
        y_padding = padding
        fx_padded = max(fx - x_padding, 0)
        fy_padded = max(fy - y_padding, 0)
        fw_padded = min(fw + 2 * x_padding, roi.shape[1] - fx_padded)
        fh_padded = min(fh + 2 * y_padding, roi.shape[0] - fy_padded)

        face_padded = roi[fy_padded:fy_padded + fh_padded, fx_padded:fx_padded + fw_padded]
        
        # Generate a unique filename
        filename = os.path.join(save_folder, 'detected_face_{}.jpg'.format(time.strftime("%Y%m%d-%H%M%S")))
        
        # Save the image
        cv2.imwrite(filename, face_padded)
        print(f"Face detected and saved with padding! Saved as {filename}")
        break  # Save only the first detected face

def capture_photo():
    global frame, rect_coords
    detect_and_save_face(frame, rect_coords, face_cascade, padding=20)
    messagebox.showinfo("Info", "Photo captured and saved!")

def start_camera():
    global cap, frame, rect_coords, running
    cap = cv2.VideoCapture(0)  # Use the default webcam

    # Allow the camera feed to stabilize
    time.sleep(2)

    while running:
        ret, frame = cap.read()
        if not ret:
            break
        frame, rect_coords = draw_center_rectangle(frame)
        cv2.imshow('Webcam with Center Rectangle', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

def start_camera_thread():
    global running
    running = True
    camera_thread = threading.Thread(target=start_camera)
    camera_thread.start()

def stop_camera():
    global running
    running = False

# Initialize the face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Create the main window
root = tk.Tk()
root.title("Photo Capture")

# Create and place the buttons
start_button = tk.Button(root, text="Start Camera", command=start_camera_thread)
start_button.pack(pady=10)

capture_button = tk.Button(root, text="Capture Photo", command=capture_photo)
capture_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Camera", command=stop_camera)
stop_button.pack(pady=10)

# Run the GUI main loop
root.mainloop()
