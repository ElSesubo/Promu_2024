from guizero import App, Box, Text, PushButton
from PROMU.Promu_2024.pantallas.funciones_globales import center_window

def mostrar_pantalla_tutorial():
    pass

def mostrar_pantalla_realizarSalto():
    pass

def mostrar_pantalla_ranking():
    pass

def mostrar_pantalla_principal():
    app = App(title="Pantalla de Inicio", width=800, height=600)
    center_window(app, 800, 600)

    sidebar = Box(app, align="left", width=150, height="fill", border=True)
    Box(sidebar, width="fill", height=30, align="top")
    Text(sidebar, text="Menú", align="top")
    Box(sidebar, width="fill", height=40, align="top")

    instruccionesPB = PushButton(sidebar, text="Tutorial", align="top", width="fill")
    realizarsaltoPB = PushButton(sidebar, text="Realizar salto", align="top", width="fill")
    rankingPB = PushButton(sidebar, text="Ranking", align="top", width="fill")

    salirPB = PushButton(sidebar, text="Salir", align="bottom", width="fill")

    instruccionesPB.tk.config(borderwidth=0)
    realizarsaltoPB.tk.config(borderwidth=0)
    rankingPB.tk.config(borderwidth=0)
    salirPB.tk.config(borderwidth=0)

    right_container = Box(app, align="left", width="fill", height="fill")

    main_content = Box(right_container, align="top", width="fill", height="fill", border=True)
    Text(main_content, text="Área de Contenido Principal", align="top")

    app.display()


if __name__ == "__main__":
    mostrar_pantalla_principal()
