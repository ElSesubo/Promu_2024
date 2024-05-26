import os
import tkinter as tk
from PIL import ImageTk, Image


def center_window(app, width, height):
    screen_width = app.tk.winfo_screenwidth()
    screen_height = app.tk.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    app.tk.geometry(f'{width}x{height}+{x}+{y}')

def load_image(canvas, path, dimensiones):
    image = Image.open(path)
    image = image.resize((dimensiones[0], dimensiones[1]), Image.LANCZOS)
    photo_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)
    canvas.image = photo_image  # Necesario para evitar que la imagen sea recolectada por el garbage collector

def clear_box(box):
    while box.children:
        for widget in box.children:
            widget.destroy()
