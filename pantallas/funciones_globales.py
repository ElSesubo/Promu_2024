import os

def center_window(app, width, height):
    screen_width = app.tk.winfo_screenwidth()
    screen_height = app.tk.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    app.tk.geometry(f'{width}x{height}+{x}+{y}')

def load_image(picture,ruta):
    image_path = os.path.join(os.getcwd(), ruta)
    if os.path.exists(image_path):
        picture.image = image_path
    else:
        print(f"Image not found at {image_path}")
