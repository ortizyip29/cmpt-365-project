from tkinter import *
from tkinter.filedialog import askopenfilename
import numpy as np
import cv2
import math
from PIL import Image, ImageTk


file_name = ['']


def openvideo():
    name = askopenfilename(filetypes=(("Video files", "*.mp4;*.mpg;*.avi;.mov;.flv"), ("All files", "*.*")))

    if name == "":
        return
    file_name[0] = name

    cap = cv2.VideoCapture(file_name[0])

    width, height = 400, 300
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def on_closing():
        root.destroy()

    root = Toplevel()
    root.wm_title("Video Selected")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    lmain = Label(root)
    lmain.pack()

    def show_frame():
        ret, frame = cap.read()
        if not ret:
            return
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame)

    show_frame()
    root.mainloop()


# Replace the colour RGB by the chromaticity
def replaceByChromaticity(frame):
    result = frame
    for i in range(len(result)):
        for j in range(len(result[0])):
            r, g, b = result[i][j][0], result[i][j][1], result[i][j][2]
            if not (r == 0 and g == 0 and b == 0):
                result[i][j][0] = int(round((((result[i][j][0] + 0.0) / ((r + 0.0) + g + b)) * 255)))
                result[i][j][1] = int(round((((result[i][j][1] + 0.0) / ((r + 0.0) + g + b)) * 255)))
                result[i][j][2] = int(round((((result[i][j][2] + 0.0) / ((r + 0.0) + g + b)) * 255)))
    return result


# Convert array to
def hist(arr):
    # Generate chromaticity 2D array, with r along on axis and g along another
    tmp = [[], []]
    for i in range(len(arr)):
        tmp[0].append(arr[i][0])
        tmp[1].append(arr[i][1])
    rgArr = np.asarray(tmp, np.dtype('uint8'))

    # Get number of bins using Sturges's Rule
    binCount = int(1 + math.log(len(arr), 2))
    result = cv2.calcHist(rgArr, [0, 1], None, [binCount, binCount], [0, 256, 0, 256])
    return result


# Convert image to list of histograms
def arr2histList(img):
    result = []
    for i in range(len(img)):
        result.append(hist(img[i]))
    return result


# Histogram intersection
def histIntersec(l):
    result = []
    for i in range(len(l) - 1):
        result.append(cv2.compareHist(l[i], l[i+1], 2))
    return result


# Histogram Difference
def histdiff():
    if file_name[0] == "":
        return

    root = Toplevel()
    root.wm_title("Histogram Difference")

    def on_closing():
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    label1 = Label(root, text="Row")
    label2 = Label(root, text="Column")
    label1.pack()
    label2.pack()

    cap = cv2.VideoCapture(file_name[0])
    mat = []

    # Loop through each frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Resize input frame to 32 x 32
        frame = cv2.resize(frame, (32, 32))

        # Store each column of each frame
        if not mat:
            mat = [replaceByChromaticity([frame[i]]) for i in range(32)]
        else:
            for i in range(32):
                mat[i].append(frame[i])

    # Replace by chromaticity
    for i in range(len(mat)):
        mat[i] = replaceByChromaticity(mat[i])

    colMat = np.transpose(mat, (2, 1, 0, 3))

    # Make histograms for the original image.
    histRow = []
    histCol = []
    for i in range(len(mat)):
        # Row
        STIRow = np.asarray(mat[i], np.dtype('uint8'))
        l1row = arr2histList(STIRow)
        l2row = histIntersec(l1row)
        histRow.append(l2row)
        # Column
        STICol = np.asarray(colMat[0], np.dtype('uint8'))
        l1col = arr2histList(STICol)
        l2col = histIntersec(l1col)
        histCol.append(l2col)
    histRow = np.dot(histRow, (1.0/32))
    histRow = np.dot(histRow, 255)
    histCol = np.dot(histCol, (1.0/32))
    histCol = np.dot(histCol, 255)
    imageRow = Image.fromarray(np.asarray(histRow, np.dtype('uint8')), "L")
    imageCol = Image.fromarray(np.asarray(histCol, np.dtype('uint8')), "L")

    # Display Histograms
    imgTkRow = ImageTk.PhotoImage(imageRow)
    label1.configure(image=imgTkRow)
    label1.image = imgTkRow
    imgTkCol = ImageTk.PhotoImage(imageCol)
    label2.configure(image=imgTkCol)
    label2.image = imgTkCol
    label1.pack()
    label2.pack()
    root.update()


# Copy column
def cpycol():
    if file_name[0] == "":
        return

    def on_closing():
        root.destroy()
    root = Toplevel()
    root.wm_title("Copy Column")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    lmain = Label(root)

    cap = cv2.VideoCapture(file_name[0])
    mat = []

    # Loop through each frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Resize input frame to 32 x 32
        frame = cv2.resize(frame, (32, 32))

        # Store each column of each frame
        if not mat:
            mat = [replaceByChromaticity([frame[i]]) for i in range(32)]
        else:
            for i in range(32):
                mat[i].append(frame[i])

    # Replace by chromaticity
    for i in range(len(mat)):
        mat[i] = replaceByChromaticity(mat[i])

    # STI copy by the center column from each frame
    colMat = np.transpose(mat, (2, 1, 0, 3))
    STICol = np.asarray(colMat[len(colMat) / 2], np.dtype('uint8'))
    imgCol = Image.fromarray(STICol.transpose(1, 0, 2))
    img = ImageTk.PhotoImage(imgCol)

    lmain.configure(image=img)
    lmain.image = img
    lmain.pack()
    root.update()


# Copy row
def cpyrow():
    if file_name[0] == "":
        return

    def on_closing():
        root.destroy()

    root = Toplevel()
    root.wm_title("Copy Row")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    lmain = Label(root)

    cap = cv2.VideoCapture(file_name[0])
    mat = []

    # Loop through each frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Resize input frame to 32 x 32
        frame = cv2.resize(frame, (32, 32))

        # Store each column of each frame
        if not mat:
            mat = [replaceByChromaticity([frame[i]]) for i in range(32)]
        else:
            for i in range(32):
                mat[i].append(frame[i])

    # Replace by chromaticity
    for i in range(len(mat)):
        mat[i] = replaceByChromaticity(mat[i])

    # STI copy by the center row from each frame
    STIRow = np.asarray(mat[len(mat)/2], np.dtype('uint8'))
    imgRow = Image.fromarray(STIRow.transpose(1, 0, 2))
    img = ImageTk.PhotoImage(imgRow)

    lmain.configure(image=img)
    lmain.image = img
    lmain.pack()
    root.update()


ui = Tk()
setRow = IntVar()
setRow.set(0)
ui.title("CMPT 365 Final Project")
Label(ui, text="Choose your video and which STI you want to work with:", justify = LEFT, padx = 20).pack()
Button(text="Choose Video", width = 50, command=lambda : openvideo()).pack()
Button(text="Copy Columns", width = 50, command=lambda : cpycol()).pack()
Button(text="Copy Rows", width = 50, command=lambda : cpyrow()).pack()
Button(text="Histogram Difference", width = 50, command=lambda : histdiff()).pack()
ui.mainloop()
