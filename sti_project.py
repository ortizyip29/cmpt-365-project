from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from tkinter.filedialog import askopenfilename
def openvideo():
    name= askopenfilename(filetypes=(("Video files", "*.mp4;*.mpg;*.avi;.mov;.flv"),("All files", "*.*")))
    file_name[0] = name
def openpicture():
    name= askopenfilename(filetypes=(("Image files", "*.png;*.jpeg;*.gif;.tif;.jpg"),("All files", "*.*")))
    file_name[0] = name
ui = Tk()
setrow = IntVar()
setrow.set(0)
ui.title("CMPT 365 Final Project")
Label(ui, text="""Choose your video and which STI you want to work with:""", justify = LEFT, padx = 20).pack()
Button(text="Choose Video", width = 50, command=lambda : openvideo()).pack()
Button(text="Choose Picture", width = 50, command=lambda : openpicture()).pack()
Button(text="Histogram Difference", width = 50, command=lambda : hisint()).pack() 
Button(text="Copy Pixels", width = 50, command=lambda : cpypix()).pack()
ui.mainloop()
