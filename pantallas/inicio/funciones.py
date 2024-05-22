from guizero import App, Box, Text, PushButton, TextBox, info
from PROMU.Promu_2024.pantallas.funciones_globales import center_window

color_fondo = "#fff5a4"
color_sidebar = "#fcef89"
def clear_box(box):
    for widget in box.children:
        widget.destroy()

def ajustar_texto(texto, max_length):
    if len(texto) > max_length:
        return texto[:max_length-3] + "..."
    return texto

def estilizar_boton(boton, colores):
    boton.tk.config(
        bg=colores[0],
        fg=colores[1],
        font=("Helvetica", 10),
        relief="flat",
        borderwidth=0,
        padx=10,
        pady=5,
    )
    boton.tk.bind("<Enter>", lambda e: on_hover(boton, colores[2]))
    boton.tk.bind("<Leave>", lambda e: on_leave(boton, colores[0]))

def on_hover(boton, color):
    boton.tk.config(cursor="hand2")
    boton.tk.config(bg=color)

def on_leave(boton, color):
    boton.tk.config(cursor="")
    boton.tk.config(bg=color)

def seleccionar_archivo(archivo_btn):
    archivo = app.select_file(filetypes=[["CSV files", "*.csv"], ["Excel files", "*.xlsx"]])
    if archivo:
        archivo_btn.text = f"Archivo: {ajustar_texto(archivo.split('/')[-1], 15)}"
        info("Archivo seleccionado", f"Has seleccionado: {archivo}")
    return archivo

def mostrar_pantalla_configuracion():
    pass

def mostrar_pantalla_inicio(main_content):
    clear_box(main_content)
    contenido = Box(main_content, align="top", width="fill", height="fill")
    contenido.tk.config(bg=color_fondo)
    Text(contenido, text="Salto", align="top")

def mostrar_pantalla_resultados():
    pass
def mostrar_pantalla_realizarSalto(main_content):
    clear_box(main_content)
    contenido = Box(main_content, align="top", width="fill", height="fill")
    contenido.tk.config(bg=color_fondo)

    top_box = Box(contenido, width="fill", height=40, align="top")
    top_box.tk.config(bg=color_fondo)

    titulo_box = Box(contenido, align="top", width="fill")
    titulo_box.tk.config(bg=color_fondo)
    Text(titulo_box, text="Realizar salto", align="top", size=20, color="black", bg=color_fondo, width="fill")

    top_box = Box(contenido, align="top", width="fill", height=30)
    top_box.tk.config(bg=color_fondo)

    centered_container = Box(contenido, align="top")

    form_container = Box(centered_container, align="top", width="fill")
    form_box = Box(form_container, layout="grid", align="top")
    form_container.tk.config(bg=color_fondo)
    form_box.tk.config(bg=color_fondo)

    archivoTXT = Text(form_box, text="Seleccionar datos del salto: ", grid=[0,0], align="left")
    archivoBTN = PushButton(form_box, text="Seleccionar Archivo", grid=[1,0], command=lambda: seleccionar_archivo(archivoBTN))
    colores = ["white", "black", "lightgrey"]
    estilizar_boton(archivoBTN, colores)
    archivoTXT.tk.config(bg=color_fondo)

    Box(form_box, grid=[0,1,2,1], height=20)

    masaTXT = Text(form_box, text="Masa del saltador: ", grid=[0,2], align="left")
    userTxTBox = TextBox(form_box, text="", grid=[1,2], width=30)
    userTxTBox.tk.config(bg="white")
    masaTXT.tk.config(bg=color_fondo)

    Box(form_box, grid=[0,3,2,1], height=20)

    nombreTXT = Text(form_box, text="Nombre saltador: ", grid=[0,4], align="left")
    userTxTBox = TextBox(form_box, text="", grid=[1,4], width=30)
    userTxTBox.tk.config(bg="white")
    nombreTXT.tk.config(bg=color_fondo)

    Box(form_box, grid=[0,5,2,1], height=20)

    grupoTXT = Text(form_box, text="Nombre grupo: ", grid=[0,6], align="left")
    passTxTBox = TextBox(form_box, text="", grid=[1,6], width=30)
    passTxTBox.tk.config(bg="white")
    grupoTXT.tk.config(bg=color_fondo)

    Box(form_box, grid=[0,7,2,1], height=40)

    enviarBTN = PushButton(contenido, text="Enviar datos")
    colores = ["white", "black", "lightgrey"]
    estilizar_boton(enviarBTN, colores)

def mostrar_pantalla_ranking(main_content, datos_ranking):
    clear_box(main_content)

    contenido = Box(main_content, align="top", width="fill", height="fill")
    contenido.tk.config(bg=color_fondo)

    top_box = Box(contenido, align="top", width="fill", height=40)
    top_box.tk.config(bg=color_fondo)

    titulo_box = Box(contenido, align="top", width="fill")
    titulo_box.tk.config(bg=color_fondo)
    Text(titulo_box, text="Ranking", align="top", size=20, color="black", bg=color_fondo, width="fill")

    top_box = Box(contenido, align="top", width="fill", height=30)
    top_box.tk.config(bg=color_fondo)

    encabezados_box = Box(contenido, align="top", width="fill")
    encabezados = Box(encabezados_box, align="top")
    encabezados_box.tk.config(bg=color_fondo)
    encabezados.tk.config(bg=color_fondo)

    encabezadoTXT = Text(encabezados, text="Nombre", align="left", color="black", bg=color_fondo, width=15)
    encabezadoTXT.tk.config(font=("Helvetica", 12, "bold"))
    encabezadoTXT = Text(encabezados, text="Grupo", align="left", size=12, color="black", bg=color_fondo, width=10)
    encabezadoTXT.tk.config(font=("Helvetica", 12, "bold"))
    encabezadoTXT = Text(encabezados, text="Altura", align="left", size=12, color="black", bg=color_fondo, width=10)
    encabezadoTXT.tk.config(font=("Helvetica", 12, "bold"))
    encabezadoTXT = Text(encabezados, text="Fecha", align="left", size=12, color="black", bg=color_fondo, width=15)
    encabezadoTXT.tk.config(font=("Helvetica", 12, "bold"))

    try:
        top_box = Box(contenido, align="top", width="fill", height=20)
        top_box.tk.config(bg=color_fondo)
        for i in range(len(datos_ranking)):
            fila_box = Box(contenido, align="top", width="fill")
            fila = Box(fila_box, align="top")
            fila_box.tk.config(bg=color_fondo)

            Text(fila, text=datos_ranking[i]['nombre'], align="left", size=12, color="black", bg=color_fondo, width=15)
            Text(fila, text=datos_ranking[i]['grupo'], align="left", size=12, color="black", bg=color_fondo, width=10)
            Text(fila, text=datos_ranking[i]['altura'], align="left", size=12, color="black", bg=color_fondo, width=10)
            Text(fila, text=datos_ranking[i]['fecha'], align="left", size=12, color="black", bg=color_fondo, width=15)
    except IndexError:
        print("No quedan más registros")

datos_ranking = [
    {'nombre': 'Juan Pérez', 'grupo': 'A', 'promedio': '9.5', 'altura': '1.80m', 'fecha': '2024-05-22'},
    {'nombre': 'Ana López', 'grupo': 'B', 'promedio': '9.8', 'altura': '1.75m', 'fecha': '2024-05-21'},
    {'nombre': 'Carlos Gómez', 'grupo': 'A', 'promedio': '9.7', 'altura': '1.78m', 'fecha': '2024-05-20'},
]

def mostrar_pantalla_principal():
    center_window(app, 800, 600)

    sidebar = Box(app, align="left", width=150, height="fill")
    sidebar.tk.config(bg=color_sidebar)
    separador = Box(sidebar, width="fill", height=30, align="top")
    separador.tk.config(bg=color_sidebar)
    menuTXT = Text(sidebar, text="Menú", align="top")
    menuTXT.tk.config(bg=color_sidebar)
    separador = Box(sidebar, width="fill", height=40, align="top")
    separador.tk.config(bg=color_sidebar)

    right_container = Box(app, align="left", width="fill", height="fill")
    main_content = Box(right_container, align="top", width="fill", height="fill")
    mostrar_pantalla_inicio(main_content)

    def salir():
        app.destroy()

    instruccionesPB = PushButton(sidebar, text="Inicio", align="top", width="fill", height=3, command=lambda: mostrar_pantalla_inicio(main_content))
    instruccionesPB.tk.config(bg=color_sidebar)
    realizarsaltoPB = PushButton(sidebar, text="Realizar salto", align="top", width="fill", height=3, command=lambda: mostrar_pantalla_realizarSalto(main_content))
    realizarsaltoPB.tk.config(bg=color_sidebar)
    rankingPB = PushButton(sidebar, text="Ranking", align="top", width="fill", height=3, command=lambda: mostrar_pantalla_ranking(main_content, datos_ranking))
    rankingPB.tk.config(bg=color_sidebar)
    salirPB = PushButton(sidebar, text="Salir", align="bottom", width="fill", height=3, command=salir)
    salirPB.tk.config(bg=color_sidebar)

    colores = [color_sidebar, "black", color_fondo]

    estilizar_boton(instruccionesPB, colores)
    estilizar_boton(realizarsaltoPB, colores)
    estilizar_boton(rankingPB, colores)
    estilizar_boton(salirPB, colores)

    app.display()

if __name__ == "__main__":
    app = App(title="PikLeap", width=800, height=600)
    mostrar_pantalla_principal()
