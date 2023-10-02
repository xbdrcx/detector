import cv2, os
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

# Haar Cascades (https://github.com/opencv/opencv/tree/master/data/haarcascades)

class GUI():
    def __init__(self):
        # MAIN CONFIG
        self.root = tk.Tk()
        self.root.title("Detector")            
        self.root.geometry("430x180")
        self.root.resizable(0,0)
        # FRAMES
        self.haar_frame = tk.Frame(self.root)
        self.source_frame = tk.Frame(self.root)
        self.bottom_frame = tk.Frame(self.root)
        self.haar_frame.rowconfigure(0, weight=4)
        self.source_frame.rowconfigure(0, weight=4)
        self.bottom_frame.rowconfigure(0, weight=4)
        self.haar_frame.grid(row=0, column=0, sticky="W", padx=10, pady=10)
        self.source_frame.grid(row=1, column=0, sticky="W", padx=10, pady=10)
        self.bottom_frame.grid(row=2, column=0, sticky="W", padx=10, pady=10)
        # ELEMENTS
        self.haar_btn = tk.Button(self.haar_frame, text="Choose HaarCascade", command=lambda:choose_haarcascade(self))
        self.haar_btn.grid(row=0, column=0, padx=10, pady=10)
        self.haar_file = tk.Label(self.haar_frame, text="None")
        self.haar_file.grid(row=0, column=1, padx=10, pady=10, sticky="W", columnspan=1)
        tk.Label(self.source_frame, text="Choose source:").grid(row=1, column=1)
        self.image_btn = tk.Button(self.source_frame, text="Image", command=lambda:read_img(self), state="disabled")
        self.image_btn.grid(row=1, column=2, padx=10, pady=10)
        self.video_btn = tk.Button(self.source_frame, text="Video", command=lambda:read_vid_source(self, 0), state="disabled")
        self.video_btn.grid(row=1, column=3, padx=10, pady=10)
        self.cam_btn = tk.Button(self.source_frame, text="Camera", command=lambda:read_vid_source(self, 1), state="disabled")
        self.cam_btn.grid(row=1, column=4, padx=10, pady=10)
        tk.Label(self.bottom_frame, text="When Detection is Running, Press Q to Quit").grid(row=0, column=0, padx=10, pady=10)
        # INIT
        self.root.mainloop()

# State
# Tkinter Button States (normal, disabled, active)
def change_button_state(gui, state: str):
    gui.haar_btn.config(state=state)
    gui.image_btn.config(state=state)
    gui.video_btn.config(state=state)
    gui.cam_btn.config(state=state)

def choose_haarcascade(gui):
    haarCascadeFile = askopenfilename(initialdir="./haarcascades/", filetypes=[("XML", ".xml")])
    global trained_data
    trained_data = cv2.CascadeClassifier(haarCascadeFile)
    gui.haar_file.config(text=os.path.basename(haarCascadeFile))
    gui.video_btn.config(state="normal")
    gui.image_btn.config(state="normal")
    gui.cam_btn.config(state="normal")

# Source
# 0 = Video Source
# 1 - Camera Source
def read_vid_source(gui, source: int):
    change_button_state(gui, "disabled")
    try:
        tk.Tk().withdraw()
        if source == 0:
            filename = askopenfilename(initialdir="./examples/", filetypes=[("Videos", ".mp4 .mov .webm .gif")])     
            vid_source = cv2.VideoCapture(filename)
        elif source == 1:
            vid_source = cv2.VideoCapture(0)
        while True:
            successful_frame_read, frame = vid_source.read()
            grayscaled_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            coordinates = trained_data.detectMultiScale(grayscaled_img)
            for(x, y, w, h) in coordinates:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
            cv2.imshow('Detector', frame)
            key = cv2.waitKey(1)
            if key == 81 or key == 113:
                break
        cv2.destroyWindow("Detector")
    except:
        messagebox.showerror(title="Error", message="Something went wrong reading video source.")
    change_button_state(gui, "normal")

def read_img(gui):
    change_button_state(gui, "disabled")
    try:
        tk.Tk().withdraw()
        filename = askopenfilename(initialdir="./examples/", filetypes=[("Images", ".jpg .png")])
        img = cv2.imread(filename)
        grayscaled_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        coordinates = trained_data.detectMultiScale(grayscaled_img)
        for (x, y, w, h) in coordinates:
            cv2.rectangle(img , (x, y), (x+w, y+h), (0, 255, 0), 1)
        cv2.imshow('Detector', img)
        cv2.waitKey()
        cv2.destroyWindow("Detector")
    except:
        messagebox.showerror(title="Error", message="Something went wrong reading image source.")
    change_button_state(gui, "normal")

if __name__ == "__main__":
    gui = GUI()
