import cv2
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pytesseract
import keras_ocr

# Initialize the OCR pipeline for Keras OCR (if you prefer to use it)
pipeline = keras_ocr.pipeline.Pipeline()

# Path to save the captured image
image_path = 'captured_id_card.png'

# Initialize the webcam
cap = cv2.VideoCapture(0)

def capture_image():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        # Save the captured frame as an image file
        cv2.imwrite(image_path, frame)
        messagebox.showinfo("Success", "Image captured and saved as 'captured_id_card.png'")
        
        # Extract text from the saved image
        extracted_text = extract_text_from_image(image_path)
        text_output.delete('1.0', END)
        text_output.insert(END, extracted_text)
    else:
        messagebox.showerror("Error", "Failed to capture image")

def extract_text_from_image(image_path):
    # Open the image using PIL
    img = Image.open(image_path)
    # Use Tesseract to extract text
    text = pytesseract.image_to_string(img)
    
    # Alternatively, use Keras OCR for text extraction (comment out the lines above and uncomment the lines below)
    # image = keras_ocr.tools.read(image_path)
    # predictions = pipeline.recognize([image])[0]
    # text = '\n'.join([text for text, _ in predictions])
    
    return text

def show_frame():
    ret, frame = cap.read()
    if ret:
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

# Create the main window
root = Tk()
root.title("ID Card Text Extraction")

# Create a label to display the webcam feed
lmain = Label(root)
lmain.pack()

# Create a button to capture the image and extract text
capture_button = Button(root, text="Capture Image and Extract Text", command=capture_image)
capture_button.pack()

# Create a Text widget to display the extracted text
text_output = Text(root, height=10, width=50)
text_output.pack()

# Start displaying the frames
show_frame()

# Start the GUI main loop
root.mainloop()

# Release the webcam
cap.release()
cv2.destroyAllWindows()
