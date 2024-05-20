from guizero import App, Picture, Box, Text, TextBox, PushButton
import os
from PROMU.Promu_2024.pantallas.funciones_globales import center_window
from PROMU.Promu_2024.pantallas.inicio.funciones import *
from PROMU.Promu_2024.ClienteTCP import *
import tkinter as tk
from tkinter import font as tkfont
from PIL import ImageFont

def load_image():
    image_path = os.path.join(os.getcwd(), "../../PIKLEAPlogo2.png")
    if os.path.exists(image_path):
        picture.image = image_path
    else:
        print(f"Image not found at {image_path}")

def send_login_data():
    username = userTxTBox.value
    password = passTxTBox.value
    #login(username, password)

app = App(title="PikLeap", width=800, height=600, bg="#fff5a4")
center_window(app, 800, 600)

box = Box(app, align="top", width="fill", height="fill")

spacer_top = Box(box, width="fill", height=75, align="top")
picture = Picture(box, width=425, height=300, align="top")

# Añadir espacio entre la imagen y los campos de texto
spacer_between_image_and_fields = Box(box, width="fill", height=20, align="top")

form_container = Box(box, align="top", width="fill")
form_box = Box(form_container, layout="grid", align="top")

Text(form_box, text="Usuario: ", grid=[0,0], align="left")
userTxTBox = TextBox(form_box, text="", grid=[1,0], width=30)
userTxTBox.tk.config(bg="white")

Text(form_box, text="Contraseña: ", grid=[0,2], align="left")
passTxTBox = TextBox(form_box, text="", grid=[1,2], width=30)
passTxTBox.tk.config(bg="white")

spacer_between_fields_and_button = Box(form_box, grid=[0,3,2,1], height=30)

button_container = Box(form_box, grid=[0,4,2,1], align="top", width="fill")

sendPB = PushButton(button_container, text="Iniciar sesión", align="top")
sendPB.tk.config(bg="white")

spacer_bottom = Box(box, width="fill", height=100, align="top")

load_image()

app.display()
