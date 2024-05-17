from guizero import App, Box, Text
from PROMU.Promu_2024.pantallas.funciones_globales import center_window

def show_main_screen():
    app = App(title="Pantalla de Inicio", width=800, height=600)
    center_window(app, 800, 600)

    sidebar = Box(app, align="left", width=150, height="fill", border=True)
    Text(sidebar, text="Barra Lateral", align="top")

    right_container = Box(app, align="left", width="fill", height="fill")

    top_bar = Box(right_container, align="top", width="fill", height=50, border=True)
    Text(top_bar, text="Barra Superior", align="left")

    main_content = Box(right_container, align="top", width="fill", height="fill", border=True)
    Text(main_content, text="Área de Contenido Principal", align="top")

    app.display()


if __name__ == "__main__":
    show_main_screen()
