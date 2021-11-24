from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab
import numpy as np

letter_model = load_model('letter_model.h5')
digit_model=load_model('digit_model.h5')
def predict_digit(img):
    img = img.resize((28,28))
    img = img.convert('L')
    img = np.array(img)
    img = img.reshape(1,28,28,1)
    img = img/255.0
    op=digit_model.predict([img])[0]
    return np.argmax(op), max(op)
    
def predict_letter(img):
    img = img.resize((28,28))
    img = img.convert('L')
    img = np.array(img)
    img = img.reshape(1,28,28,1)
    word_dict = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X', 24:'Y',25:'Z'}
    img_pred=word_dict[np.argmax(letter_model.predict(img))]
    return img_pred

class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        self.title("Character Guesser")
        self.canvas=tk.Canvas(self,width=300,height=300, bg="light pink", cursor="cross")
        self.label=tk.Label(self,text="Write the digit/alphabet ..\nChoose appropriate button", font=("Times New Roman",40))
        self.guess_btn1=tk.Button(self,text="Guess Digit",command=self.classify_digit)
        self.guess_btn2=tk.Button(self,text="Guess Alphabet",command=self.classify_letter)
        self.clr_btn=tk.Button(self,text="clear",command=self.clear_all)

        self.canvas.grid(row=0,column=0,pady=2,sticky=W,)
        self.label.grid(row=0,column=1,pady=2,padx=2)
        self.guess_btn1.grid(row=1,column=1,pady=2,padx=2)
        self.guess_btn2.grid(row=1,column=2,pady=2,padx=2)
        self.clr_btn.grid(row=1,column=0,pady=2)
        self.canvas.bind("<B1-Motion>",self.draw_lines)
    
    def clear_all(self):
        self.canvas.delete("all")
    
    def classify_digit(self):
        HWND=self.canvas.winfo_id()
        rect=win32gui.GetWindowRect(HWND)
        a,b,c,d = rect
        rect = (a+4,b+4,c-4,d-4)
        im=ImageGrab.grab(rect)

        digit,acc=predict_digit(im)
        self.label.configure(text='Guessed No. '+str(digit)+'\nAccuracy '+str(int(acc*100))+'%')
    
    def classify_letter(self):
        HWND=self.canvas.winfo_id()
        rect=win32gui.GetWindowRect(HWND)
        a,b,c,d = rect
        rect = (a+4,b+4,c-4,d-4)
        im=ImageGrab.grab(rect)

        letter=predict_letter(im)
        self.label.configure(text='Guessed Alphabet '+str(letter))
    

    def draw_lines(self,event):
        self.x=event.x
        self.y=event.y
        r=8
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='gray')

app = GUI()
mainloop()