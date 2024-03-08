import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import cv2
import numpy as np

# Global variables
panelA = None
panelB = None
eimg = None
key = None

# Function to open image file
def open_img():
    global panelA, panelB, eimg
    filename = filedialog.askopenfilename(title="Open")
    if filename:
        img = Image.open(filename)
        eimg = img.copy()
        img.thumbnail((400, 400))  # Resize image for display
        img = ImageTk.PhotoImage(img)
        if panelA is None:
            panelA = Label(image=img)
            panelA.image = img
            panelA.place(x=20, y=100)
        else:
            panelA.configure(image=img)
            panelA.image = img

# Function to encrypt image
def en_fun():
    global panelB, eimg, key
    if eimg is not None:
        image_input = cv2.cvtColor(np.array(eimg), cv2.COLOR_RGB2GRAY).astype(float) / 255.0
        mu, sigma = 0, 0.1
        key = np.random.normal(mu, sigma, image_input.shape) + np.finfo(float).eps
        image_encrypted = image_input / key
        image_encrypted = (image_encrypted * 255).astype(np.uint8)
        img = Image.fromarray(image_encrypted)
        img.thumbnail((400, 400))
        img = ImageTk.PhotoImage(img)
        if panelB is None:
            panelB = Label(image=img)
            panelB.image = img
            panelB.place(x=450, y=100)
        else:
            panelB.configure(image=img)
            panelB.image = img
    else:
        messagebox.showerror("Error", "No image loaded")

# Function to decrypt image
def de_fun():
    global panelB, eimg, key
    if eimg is not None and key is not None:
        image_output = cv2.cvtColor(np.array(eimg), cv2.COLOR_RGB2GRAY).astype(float) * key
        image_output *= 255.0
        image_output = image_output.astype(np.uint8)
        img = Image.fromarray(image_output)
        img.thumbnail((400, 400))
        img = ImageTk.PhotoImage(img)
        if panelB is None:
            panelB = Label(image=img)
            panelB.image = img
            panelB.place(x=450, y=100)
        else:
            panelB.configure(image=img)
            panelB.image = img
    else:
        messagebox.showerror("Error", "No image loaded or encrypted")

# Function to reset image
def reset():
    global panelB, eimg
    if eimg is not None:
        img = eimg.copy()
        img.thumbnail((400, 400))
        img = ImageTk.PhotoImage(img)
        if panelB is None:
            panelB = Label(image=img)
            panelB.image = img
            panelB.place(x=450, y=100)
        else:
            panelB.configure(image=img)
            panelB.image = img
    else:
        messagebox.showerror("Error", "No image loaded")

# Main window
window = Tk()
window.geometry("900x600")
window.title("Image Encryption Decryption")
window.configure(bg="lightgray")

# Buttons
open_button = Button(window, text="Open", command=open_img, bg="blue", fg="white", font=("Arial", 16), width=10)
open_button.place(x=20, y=50)

encrypt_button = Button(window, text="Encrypt", command=en_fun, bg="green", fg="white", font=("Arial", 16), width=10)
encrypt_button.place(x=150, y=50)

decrypt_button = Button(window, text="Decrypt", command=de_fun, bg="red", fg="white", font=("Arial", 16), width=10)
decrypt_button.place(x=280, y=50)

reset_button = Button(window, text="Reset", command=reset, bg="orange", fg="white", font=("Arial", 16), width=10)
reset_button.place(x=410, y=50)

exit_button = Button(window, text="Exit", command=window.quit, bg="gray", fg="white", font=("Arial", 16), width=10)
exit_button.place(x=540, y=50)

window.mainloop()
