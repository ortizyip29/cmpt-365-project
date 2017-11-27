from tkinter import *
from tkinter.filedialog import askopenfilename
import numpy as np
import cv2
import PIL
from PIL import Image, ImageTk


file_name = ""

def openvideo():
    name = askopenfilename(filetypes=(("Video files", "*.mp4"), ("All files", "*.*")))
    #name = askopenfilename(filetypes=(("Video files", "*.mp4;*.mpg;*.avi;.mov;.flv"), ("All files", "*.*")))
    if name == "":
        return
    file_name = name

    cap = cv2.VideoCapture(name)

    width, height = 400, 300
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    root = Toplevel()
    root.wm_title("Video Selected")
    lmain = Label(root)
    lmain.pack()

    def on_closing():
        root.destroy()

    def show_frame():
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame)

    show_frame()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

    '''
    rval, frame = cap.read()

    if rval:
        key = cv2.waitKey(1000)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    '''

    '''
    totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    x_center = frameWidth / 2
    y_center = frameHeight / 2

    STI_col = np.matrix(cap)
    STI_row = np.matrix(cap)
    STI_his = np.matrix(cap)
    '''

#def hisdiff():
    #histogram difference (part 1)

#def cpypix():
    #copy pixel method(part 2)

ui = Tk()
setRow = IntVar()
setRow.set(0)
ui.title("CMPT 365 Final Project")
Label(ui, text="Choose your video and which STI you want to work with:", justify = LEFT, padx = 20).pack()
Button(text="Choose Video", width = 50, command=lambda : openvideo()).pack()
Button(text="Copy Columns", width = 50, command=lambda : cpycol()).pack()
Button(text="Copy Rows", width = 50, command=lambda : cpyrow()).pack()
Button(text="Histogram Difference", width = 50, command=lambda : hisdiff()).pack()
ui.mainloop()