import json
from tkinter import ttk
from PIL import ImageDraw, ImageFont
from guizero import App, Box, Text, PushButton, TextBox, info
from ClienteTCP import login, iniciar_conexion
from funciones_globales import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.integrate import cumtrapz
import pygame
from tkinter import font as tkFont

pygame.mixer.init()

colores_botones_inter = ["white", "black", "lightgrey"]
tema_actual = "Claro"
idioma_actual = "Español"
volumen_actual = 100
fuente_subtitulos = "../../fuentes/Nunito-Bold.ttf"
fuente_titulos = "../../fuentes/Nunito-ExtraBold.ttf"
fuente_texto = "../../fuentes/Nunito-Medium.ttf"
archivo_seleccionado = None

datos_ranking = [
    {'nombre': 'Juan Pérez', 'grupo': 'A', 'promedio': '9.5', 'altura': '1.80m', 'fecha': '2024-05-22'},
    {'nombre': 'Ana López', 'grupo': 'B', 'promedio': '9.8', 'altura': '1.75m', 'fecha': '2024-05-21'},
    {'nombre': 'Carlos Gómez', 'grupo': 'A', 'promedio': '9.7', 'altura': '1.78m', 'fecha': '2024-05-20'},
    {'nombre': 'Juan Pérez', 'grupo': 'A', 'promedio': '9.5', 'altura': '1.80m', 'fecha': '2024-05-22'},
    {'nombre': 'Ana López', 'grupo': 'B', 'promedio': '9.8', 'altura': '1.75m', 'fecha': '2024-05-21'},
    {'nombre': 'Carlos Gómez', 'grupo': 'A', 'promedio': '9.7', 'altura': '1.78m', 'fecha': '2024-05-20'},
    {'nombre': 'Juan Pérez', 'grupo': 'A', 'promedio': '9.5', 'altura': '1.80m', 'fecha': '2024-05-22'},
    {'nombre': 'Ana López', 'grupo': 'B', 'promedio': '9.8', 'altura': '1.75m', 'fecha': '2024-05-21'},
    {'nombre': 'Carlos Gómez', 'grupo': 'A', 'promedio': '9.7', 'altura': '1.78m', 'fecha': '2024-05-20'},
    {'nombre': 'Juan Pérez', 'grupo': 'A', 'promedio': '9.5', 'altura': '1.80m', 'fecha': '2024-05-22'},
    {'nombre': 'Ana López', 'grupo': 'B', 'promedio': '9.8', 'altura': '1.75m', 'fecha': '2024-05-21'},
    {'nombre': 'Carlos Gómez', 'grupo': 'A', 'promedio': '9.7', 'altura': '1.78m', 'fecha': '2024-05-20'},
]

temas = {
     "Claro": {
        "color_fondo": "#BDEAFA",
        "color_texto": "black",
        "color_titulos": "#31c816",
        "color_sidebar": "#fcef89",
        "colores_botones_sidebar": ["#fcef89", "#000000", "#fff5a4"],
        "colores_resultados": "white",
        "fondo_login": "../../imagenes/fondo_login.png",
        "fondo_inicio": "../../imagenes/fondo_inicio.png",
        "fondo_ranking": "../../imagenes/fondo_ranking.png",
        "fondo_realizar_salto": "../../imagenes/fondo_realizar_salto.png",
        "fondo_configuracion": "../../imagenes/fondo_configuracion.png",
        "fondos_resultados": ["../../imagenes/fondos_resultados/4.png","../../imagenes/fondos_resultados/5.png","../../imagenes/fondos_resultados/6.png",
                              "../../imagenes/fondos_resultados/7.png","../../imagenes/fondos_resultados/8.png","../../imagenes/fondos_resultados/9.png",
                              "../../imagenes/fondos_resultados/10.png","../../imagenes/fondos_resultados/11.png","../../imagenes/fondos_resultados/12.png"]
    },
    "Oscuro": {
        "color_fondo": "#361057",
        "color_texto": "white",
        "color_titulos": "#31c816",
        "color_sidebar": "#1E1E1E",
        "colores_botones_sidebar": ["#1E1E1E", "#FFFFFF", "#555555"],
        "colores_resultados": ["#270F26", "#0F2327", "#0F2327", "#262829", "#100F27", "#27110F", "#27240F", "#14270F", "#270F21"],
        "fondo_login": "../../imagenes/fondo_login_osc.png",
        "fondo_inicio": "../../imagenes/fondo_inicio_osc.png",
        "fondo_ranking": "../../imagenes/fondo_ranking_osc.png",
        "fondo_realizar_salto": "../../imagenes/fondo_realizar_salto_osc.png",
        "fondo_configuracion": "../../imagenes/fondo_configuracion_osc.png",
        "fondos_resultados": ["../../imagenes/fondos_resultados/17.png","../../imagenes/fondos_resultados/18.png","../../imagenes/fondos_resultados/19.png",
                              "../../imagenes/fondos_resultados/20.png","../../imagenes/fondos_resultados/21.png","../../imagenes/fondos_resultados/22.png",
                              "../../imagenes/fondos_resultados/23.png","../../imagenes/fondos_resultados/24.png","../../imagenes/fondos_resultados/25.png"]
    }
}

textos = {
    "English": {
        "pikmin_morado": ["Scientific Name: Pikminidae yokozunum. Its size is only slightly larger than other Pikmin species, but its density is so great that they weigh about ten times more, to the point that when thrown against the ground, they create intense gravitational waves capable of, incredibly, distorting space-time itself! Their muscle fibers are also ten times denser, allowing them to carry ten times more weight than their relatives. The intense purple color is due to powerful antioxidant polyphenols."],
        "pikmin_rojo": ["Scientific Name: Pikminidae rubrus. In addition to their color, they are identified by a pointed nasal protrusion and their especially aggressive behavior. They also possess peculiar qualities such as immunity to heat and fire, which is unheard of in living organisms but is explained by observing their epidermis and muscle fibers, which are composed of fire-resistant cellulose."],
        "pikmin_azul": ["Scientific Name: Pikminidae caerula. Blue Pikmin (who sprout leaves and flowers like any terrestrial Pikmin) breathe on land through the stomata in their epidermis and in water through a gill on their head that looks like a mouth; in short, they are perfectly amphibious. The proteins in their skin pigments perform a function analogous to the photosynthesis of cyanobacteria, which gives them their striking coloration."],
        "pikmin_amarillo": ["Scientific Name: Pikminidae auribus. The bodies of yellow Pikmin conduct electricity; what is dangerous to other living beings is enjoyable to them. Electricity even makes them bloom! This species has two lamellae on either side of their head, resembling ears, which help them dig quickly and reach great heights when thrown."],
        "pikmin_pétreo": ["Scientific Name: Pikminidae habisaxum. This species undoubtedly belongs to the Pikmin genus, but its body does not share any of the vegetative characteristics that distinguish them; rather, its composition is primarily mineral. There is a type of parasitic Pikmin called 'Ermikmin.' In this case, the parasite takes a stone as its host, and, similar to a seed taking root through the cracks in a rock, the Pikmin's roots penetrate the stone and house vital organs in an interior cavity similar to a crystal geode."],
        "pikmin_alado": ["Scientific Name: Pikminidae volarosa. Their wings resemble those of other native flying species. It is possible that a primitive winged Onion somehow absorbed the DNA of another creature, giving rise to the precursor of the winged Pikmin as we know them today."],
        "pikmin_blanco": ["Scientific Name: Pikminidae venalbius. The poison in their bodies is a diterpene alkaloid similar to a toxin present in some roots. Ingestion can cause nausea, lung problems, and even total organ collapse, leading to death by cardiorespiratory arrest. Despite the potency of this poison, it can be used to create a medicinal substance known as aconite."],
        "pikmin_gélido": ["Scientific Name: Pikminidae habiglacius. Icy Pikmin are parasitic in nature and use ice as a host. This ice is primarily composed of water, as expected, but resembles a saline solution with low concentrations of sodium, potassium, and calcium ions that act as neurotransmitters. Interestingly, the ice shows no signs of melting when exposed to direct sunlight. This is due to the low temperature of the core, which continuously generates ice to maintain a stable size."],
        "pikmin_luminoso": ["Scientific Name: Pikminidae supravelum. These creatures share essential traits with all Pikmin: they have a leaf on their head and fight, carry weights, and propagate in similar ways. However, they do not sprout from an Onion but from Glowcaps, and their activity is exclusively nocturnal or underground. During the day, they revert to seeds and enter a dormant state. Most surprisingly, luminous Pikmin show no signs of life or vital reactions. When one dies, it transforms into light and returns to the Glowcap."],
        "REALIZAR SALTO": "PERFORM JUMP",
        "Seleccionar datos del salto: ": "Select jump data: ",
        "Seleccionar Archivo": "Select File",
        "Masa del saltador: ": "Jumper's weight: ",
        "Nombre saltador: ": "Jumper's name: ",
        "Nombre grupo: ": "Group name: ",
        "Enviar datos": "Send data",
        "Realizar salto": "Perform jump",
        "BIENVENIDO A PEAKLEAP": "WELCOME TO PEAKLEAP",
        "Esta aplicación te permitirá registrar y analizar tus saltos.": "This app will allow you to record and analyze your jumps.",
        "Sigue este tutorial para familiarizarte con las funcionalidades.": "Follow this tutorial to familiarize yourself with the features.",
        "1. Realizar Salto": "1. Perform Jump",
        "En esta sección, puedes registrar los datos de tu salto": "In this section, you can record your jump data",
        "incluyendo masa y nombre del saltador, y grupo.": "including jumper's weight, name, and group.",
        "2. Ranking": "2. Ranking",
        "Consulta el ranking de los mejores saltos registrados, ordenados por altura.": "Check the ranking of the best recorded jumps, sorted by height.",
        "3. Configuración": "3. Settings",
        "Ajusta las configuraciones de la aplicación, como el tema y el idioma.": "Adjust the app settings, such as theme and language.",
        "¡Esperamos que disfrutes usando PeakLeap!": "We hope you enjoy using PeakLeap!",
        "CONFIGURACIÓN": "SETTINGS",
        "Tema:": "Theme:",
        "Volumen:": "Volume:",
        "Idioma:": "Language:",
        "RANKING": "RANKING",
        "Nombre": "Name",
        "Grupo": "Group",
        "Altura": "Height",
        "Fecha": "Date",
        "Inicio": "Home",
        "Realizar salto": "Perform Jump",
        "Configuración": "Settings",
        "Iniciar sesión": "Login",
        "Usuario: ": "Username:",
        "Contraseña: ": "Password:"
    },
    "Español":{
        "pikmin_morado": ["Nombre científico: Pikminidae yokozunum. Su tamaño es apenas algo mayor que el de otras especies de Pikmin, pero su densidad es tan grande que pesan alrededor de diez veces más, hasta el punto de que, al lanzarlos contra el suelo, crean intensas ondas gravitatorias capaces, por increíble que parezca, ¡de distorsionar el mismísimo espacio-tiempo! Sus fibras musculares también son diez veces más densas, lo que les permite transportar diez veces más peso que sus parientes. El intenso color morado se debe a unos potentes polifenoles antioxidantes."],
        "pikmin_rojo": ["Nombre científico: Pikminidae rubrus. Además de por su color, se les identifica por una puntiaguda protuberancia nasal y por su comportamiento especialmente agresivo. Además, posee ciertas cualidades peculiares, como la inmunidad al calor y al fuego, algo inaudito en organismos vivos, pero que se explica al observar su epidermis y las fibras musculares, que se componen de una celulosa ignífuga."],
        "pikmin_azul": ["Nombre científico: Pikminidae caerula. Los Pikmin azules (a quienes les brotan hojas y flores como a cualquier Pikmin terrestre) respiran en tierra mediante los estomas de la epidermis y en el agua mediante una branquia en la cabeza de aspecto similar a una boca; en definitiva: son perfectamente anfibios. Las proteínas de sus pigmentos dérmicos realizan una función análoga a la fotosíntesis de las cianobacterias, lo que les confiere esa coloración tan llamativa."],
        "pikmin_amarillo": ["Nombre científico: Pikminidae auribus. Los cuerpos de los pikmin amarillos conducen la electricidad; lo que para otros seres vivos es un peligro, para ellos es un disfrute. ¡La corriente eléctrica incluso los hace florecer! Esta especie posee dos lamelas a ambos lados de la cabeza, semejantes a orejas, que les ayudan a cavar con rapidez y alcanzar grandes alturas cuando son lanzados."],
        "pikmin_pétreo": ["Nombre científico: Pikminidae habisaxum. Esta especie pertenece sin duda al género de los Pikmin, pero su cuerpo no comparte ninguna de las características vegetales que los distinguen, sino que su composición es principalmente mineral. Existe un tipo de Pikmin parasitario llamado «Ermikmin». En este caso, el parásito toma como anfitrión una piedra y, de manera similar a una semilla que echa raíces a través de las grietas de una roca, las raíces del Pikmin se adentran en la piedra y alojan los órganos vitales en una cavidad interior similar a una geoda cristalizada."],
        "pikmin_alado": ["Nombre científico: Pikminidae volarosa. Sus alas se asemejan a las de otras especies voladoras autóctonas. Es posible que una cebolla alada primitiva absorbiese de algún modo el ADN de otra criatura y eso diese pie al precursor de los Pikmin alados tal y como los conocemos hoy."],
        "pikmin_blanco": ["Nombre científico: Pikminidae venalbius. El veneno de sus cuerpos es un diterpeno alcaloide similar a cierta toxina presente en algunas raíces. Su ingestión puede producir náuseas problemas pulmonares e incluso un colapso total de los órganos que podría dar pie a la muerte por paro cardiorrespiratorio. A pesar de la potencia de este veneno, se puede crear con él una sustancia medicinal conocida como acónito."],
        "pikmin_gélido": ["Nombre científico: Pikminidae habiglacius. Los Pikmin gélidos son de naturaleza parasítica y utilizan el hielo como anfitrión. Este hielo se compone principalmente de agua, como era de esperar, pero se asemeja a una solución salina con baja concentración de iones de sodio, de potasio y de calcio que actúan como transmisores neuronales. Curiosamente, el hielo no muestra señales de derretirse al exponerlo a la luz solar directa. Esto se debe a la baja temperatura del núcleo, que sigue generando hielo continuamente con el fin de mantener un tamaño estable."],
        "pikmin_luminoso": ["Nombre científico: Pikminidae supravelum. Estas criaturas comparten rasgos esenciales a todos los Pikmin: tienen una hoja sobre la cabeza y luchan, cargan pesos y se propagan de formas similares. Sin embargo, no brotan de una Cebolla, sino de Lumilomas, y su actividad es exclusivamente nocturna o subterránea. Durante el día, revierten a semillas y entran en letargo. Lo más sorprendente es que los Pikmin luminosos no muestran señales de vida ni reacciones vitales al uso. Cuando uno muere, se transforma en luz y regresa a la Lumiloma."],
        "REALIZAR SALTO": "REALIZAR SALTO",
        "Seleccionar datos del salto: ": "Seleccionar datos del salto: ",
        "Seleccionar Archivo": "Seleccionar Archivo",
        "Masa del saltador: ": "Masa del saltador: ",
        "Nombre saltador: ": "Nombre saltador: ",
        "Nombre grupo: ": "Nombre grupo: ",
        "Enviar datos": "Enviar datos",
        "Realizar salto": "Realizar salto",
        "BIENVENIDO A PEAKLEAP": "BIENVENIDO A PEAKLEAP",
        "Esta aplicación te permitirá registrar y analizar tus saltos.": "Esta aplicación te permitirá registrar y analizar tus saltos.",
        "Sigue este tutorial para familiarizarte con las funcionalidades.": "Sigue este tutorial para familiarizarte con las funcionalidades.",
        "1. Realizar Salto": "1. Realizar Salto",
        "En esta sección, puedes registrar los datos de tu salto": "En esta sección, puedes registrar los datos de tu salto",
        "incluyendo masa y nombre del saltador, y grupo.": "incluyendo masa y nombre del saltador, y grupo.",
        "2. Ranking": "2. Ranking",
        "Consulta el ranking de los mejores saltos registrados, ordenados por altura.": "Consulta el ranking de los mejores saltos registrados, ordenados por altura.",
        "3. Configuración": "3. Configuración",
        "Ajusta las configuraciones de la aplicación, como el tema y el idioma.": "Ajusta las configuraciones de la aplicación, como el tema y el idioma.",
        "¡Esperamos que disfrutes usando PeakLeap!": "¡Esperamos que disfrutes usando PeakLeap!",
        "CONFIGURACIÓN": "CONFIGURACIÓN",
        "Tema:": "Tema:",
        "Volumen:": "Volumen:",
        "Idioma:": "Idioma:",
        "RANKING": "RANKING",
        "Nombre": "Nombre",
        "Grupo": "Grupo",
        "Altura": "Altura",
        "Fecha": "Fecha",
        "Inicio": "Inicio",
        "Realizar salto": "Realizar salto",
        "Configuración": "Configuración",
        "Iniciar sesión": "Iniciar sesión",
        "Usuario: ": "Usuario:",
        "Contraseña: ": "Contraseña:"
    }
}

color_fondo = temas[tema_actual]["color_fondo"]
color_texto = temas[tema_actual]["color_texto"]
color_titulos = temas[tema_actual]["color_titulos"]
color_sidebar = temas[tema_actual]["color_sidebar"]
colores_botones_sidebar = temas[tema_actual]["colores_botones_sidebar"]
colores_resultados = temas[tema_actual]["colores_resultados"]
fondo_login = temas[tema_actual]["fondo_login"]
fondo_inicio = temas[tema_actual]["fondo_inicio"]
fondo_ranking = temas[tema_actual]["fondo_ranking"]
fondo_realizar_salto = temas[tema_actual]["fondo_realizar_salto"]
fondo_configuracion = temas[tema_actual]["fondo_configuracion"]
fondos_resultados = temas[tema_actual]["fondos_resultados"]

def aplicar_tema(tema):
    global color_fondo, color_texto, color_sidebar, color_titulos, colores_botones_sidebar, fondo_login, fondo_inicio, fondo_ranking, fondo_realizar_salto, fondo_configuracion, fondos_resultados, colores_resultados

    color_fondo = tema["color_fondo"]
    color_texto = tema["color_texto"]
    color_titulos = tema["color_titulos"]
    color_sidebar = tema["color_sidebar"]
    colores_botones_sidebar = tema["colores_botones_sidebar"]
    colores_resultados = tema["colores_resultados"]
    fondo_login = tema["fondo_login"]
    fondo_inicio = tema["fondo_inicio"]
    fondo_ranking = tema["fondo_ranking"]
    fondo_realizar_salto = tema["fondo_realizar_salto"]
    fondo_configuracion = tema["fondo_configuracion"]
    fondos_resultados = tema["fondos_resultados"]

def importar_datos(fichero):
    if fichero.endswith('.csv'):
        data = pd.read_csv(fichero, delimiter=';', skipinitialspace=True)
    elif fichero.endswith('.xlsx'):
        data = pd.read_excel(fichero, engine='openpyxl')
    else:
        raise ValueError("Formato de archivo no soportado. Por favor, selecciona un archivo CSV o Excel.")

    expected_columns = ['t', 'a', 'ax', 'ay', 'az']
    if not all(col in data.columns for col in expected_columns):
        raise ValueError(f"El archivo debe contener las siguientes columnas: {expected_columns}")

    # Convertir columnas a numéricas, reemplazando errores con NaN y eliminando filas con NaN
    data = data.apply(pd.to_numeric, errors='coerce').dropna()

    t = data['t'].astype(float)
    a = data['a'].astype(float)
    ax = data['ax'].astype(float)
    ay = data['ay'].astype(float)
    az = data['az'].astype(float)
    return t, a, ax, ay, az

def load_translations(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        translations = json.load(file)
    return translations

def get_translation(translations, lang, key):
    return translations[lang].get(key, key)

def representar_figuras(t, ax, ay, az, a):
    plt.figure()
    plt.plot(t, ax)
    plt.plot(t, ay)
    plt.plot(t, az)
    plt.plot(t, a)
    plt.grid('on')
    plt.xlabel('$t$ [s]')
    plt.ylabel('$a$ [m/s$^2$]')
    plt.title('Datos del acelerómetro')
    plt.legend(['$a_x$', '$a_y$', '$a_z$', '$||a||$'])
    plt.show()

def corregir_aceleracion(a, ay):
    return a * np.sign(ay)

def representar_aceleracion_corregida(t, a, a_fixed):
    plt.figure()
    plt.plot(t, a_fixed)
    plt.plot(t, a, '--')
    plt.grid('on')
    plt.xlabel('$t$ [s]')
    plt.ylabel('$a$ [m/s$^2$]')
    plt.title('Módulo de la aceleración medida')
    plt.legend(['$||a||$ Corregida', '$||a||$ Original'])
    plt.show()

def recortar_datos(t, a_fixed, start_time, end_time):
    start_index = np.searchsorted(t, start_time)
    end_index = np.searchsorted(t, end_time)
    t_recortada = t[start_index:end_index] - t[start_index]
    a_recortada = a_fixed[start_index:end_index]
    return t_recortada, a_recortada, start_index, end_index

def combinar_reposo(t, a_fixed, start_time):
    reposo_indice = np.searchsorted(t, start_time)
    t_reposo = t[:reposo_indice] - t[0]
    a_reposo = a_fixed[:reposo_indice]
    return t_reposo, a_reposo

def aplicar_filtro_savgol(t_combinada, a_combinada, window_length=11, polyorder=3):
    return savgol_filter(a_combinada, window_length=window_length, polyorder=polyorder)

def representar_señal_suavizada(t_combinada, a_combinada, a_filtrada):
    plt.figure()
    plt.plot(t_combinada, a_combinada, '-o', label='Corregida', markersize=4)
    plt.plot(t_combinada, a_filtrada, label='Corregida y Filtrada')
    plt.grid('on')
    plt.xlabel('$t$ [s]')
    plt.ylabel('$a$ [m/$s^2$]')
    plt.title('Señal suavizada (2)')
    plt.legend()
    plt.show()

def obtener_instantes_clave(t_combinada, a_filtrada):
    diff_a_filtrada = np.diff(a_filtrada)
    t1_index = np.argmax(diff_a_filtrada > 0.1) + 1
    t1 = t_combinada[t1_index]

    min_abs_a = np.argmin(np.abs(a_filtrada))
    t2_index = np.argmax(a_filtrada[:min_abs_a])
    t2 = t_combinada[t2_index]

    t3_index = min_abs_a + np.argmax(np.abs(np.gradient(a_filtrada[min_abs_a:])) > 0.1)
    t3 = t_combinada[t3_index]

    return t1, t2, t3, t1_index, t2_index, t3_index

def representar_instantes_clave(t_combinada, a_filtrada, t1, t2, t3, a_t1, a_t2, a_t3):
    plt.figure()
    plt.plot(t_combinada, a_filtrada, label='Corregida y Filtrada')
    plt.scatter(t1, a_t1, color='r', label='Inicio de impulso')
    plt.scatter(t2, a_t2, color='g', label='Máxima aceleración')
    plt.scatter(t3, a_t3, color='b', label='Impacto en el suelo')
    plt.grid('on')
    plt.xlabel('$t$ [s]')
    plt.ylabel('$a$ [m/$s^2$]')
    plt.title('Puntos de interés')
    plt.legend()
    plt.show()

def calcular_fuerza_salto(a_filtrada, g_medida, m=75):
    a_salt = a_filtrada - g_medida
    return m * (a_salt + 9.81)

def representar_fuerza_salto(t_combinada, a_filtrada, t2, a_t2):
    plt.figure()
    plt.plot(t_combinada, a_filtrada)
    plt.scatter(t2, a_t2, color='r', label='Maxima fuerza de salto')
    plt.grid('on')
    plt.xlabel('$t$ [s]')
    plt.ylabel('$F$(t) [N]')
    plt.legend()
    plt.show()

def calcular_velocidad_salto(t_combinada, a_filtrada, g_medida, start_index, end_index):
    a_nueva = a_filtrada - g_medida
    dt = t_combinada[1] - t_combinada[0]
    v = cumtrapz(a_nueva, dx=dt, initial=0) * dt
    v_recortada = v[start_index:end_index + 1]
    t_v_recortada = t_combinada[start_index:end_index + 1]
    v_max = np.max(v_recortada)
    ind_v_max = np.argmax(v_recortada)
    t_v_max = t_v_recortada[ind_v_max]
    return v_recortada, t_v_recortada, v_max, t_v_max

def representar_velocidad_salto(t_v_recortada, v_recortada, t_v_max, v_max, t_fin_impulso, t_fin_vuelo):
    plt.figure()
    plt.plot(t_v_recortada, v_recortada)
    plt.scatter(t_v_max, v_max, color='r', label='Velocidad máxima durante el despegue')
    plt.axvspan(t_fin_impulso, t_fin_vuelo, color='purple', alpha=0.3, label='Tiempo de vuelo')
    plt.grid('on')
    plt.xlabel('$t$ [s]')
    plt.ylabel('$v$ [m/s]')
    plt.title('Velocidad en función del tiempo')
    plt.show()

def calcular_potencia_salto(F, v, start_index, end_index):
    P = F[start_index:end_index + 1] * v[start_index:end_index + 1]
    return P

def representar_potencia_salto(t_recortado, P, t_p_max, p_max):
    plt.figure()
    plt.plot(t_recortado, P, label='potencia')
    plt.scatter(t_p_max, p_max, color='r', label='potencia maxima')
    plt.grid('on')
    plt.xlabel('$t$ [s]')
    plt.ylabel('$v$ [m/s]')
    plt.title('Potencia en función del tiempo')
    plt.show()

def calcular_altura_salto(v_max, g_medida, t_vuelo):
    H_a = (v_max ** 2) / (2 * g_medida)
    H_b = (g_medida * (t_vuelo / 2) ** 2) / 2
    return H_a, H_b

def calcular_datos_salto(fichero):
    print("Cargando datos del archivo...")
    t, a, ax, ay, az = importar_datos(fichero)
    print("Datos cargados correctamente.")

    representar_figuras(t, ax, ay, az, a)
    a_fixed = corregir_aceleracion(a, ay)
    representar_aceleracion_corregida(t, a, a_fixed)

    print("Recortando datos...")
    t_recortada, a_recortada, start_index, end_index = recortar_datos(t, a_fixed, 0.5, 3)
    print("Datos recortados.")

    t_reposo, a_reposo = combinar_reposo(t, a_fixed, 0.5)
    t_combinada = np.concatenate((t_reposo, t_recortada + t_reposo[-1] + (t[1] - t[0])))
    a_combinada = np.concatenate((a_reposo, a_recortada))
    a_filtrada = aplicar_filtro_savgol(t_combinada, a_combinada)
    representar_señal_suavizada(t_combinada, a_combinada, a_filtrada)

    print("Obteniendo instantes clave...")
    t1, t2, t3, t1_index, t2_index, t3_index = obtener_instantes_clave(t_combinada, a_filtrada)
    a_t1, a_t2, a_t3 = a_filtrada[t1_index], a_filtrada[t2_index], a_filtrada[t3_index]
    representar_instantes_clave(t_combinada, a_filtrada, t1, t2, t3, a_t1, a_t2, a_t3)

    g_medida = np.mean(a_filtrada[:t1_index])
    F = calcular_fuerza_salto(a_filtrada, g_medida)
    representar_fuerza_salto(t_combinada, a_filtrada, t2, a_t2)

    v_recortada, t_v_recortada, v_max, t_v_max = calcular_velocidad_salto(t_combinada, a_filtrada, g_medida, start_index, end_index)
    t_fin_impulso = t_v_max
    v_min = np.min(v_recortada)
    ind_v_min = np.argmin(v_recortada)
    t_v_min = t_v_recortada[ind_v_min]
    t_fin_vuelo = t_v_min
    t_vuelo = t_fin_vuelo - t_fin_impulso
    representar_velocidad_salto(t_v_recortada, v_recortada, t_v_max, v_max, t_fin_impulso, t_fin_vuelo)

    P = calcular_potencia_salto(F, v_recortada, start_index, end_index)
    t_recortado = t_combinada[start_index:end_index + 1]
    p_max = np.max(P)
    ind_p_max = np.argmax(P)
    t_p_max = t_recortado[ind_p_max]
    representar_potencia_salto(t_recortado, P, t_p_max, p_max)

    H_a, H_b = calcular_altura_salto(v_max, g_medida, t_vuelo)
    print(f'Altura del salto a partir de la velocidad de despegue: {H_a:.2f} m')
    print(f'Altura del salto a partir del tiempo de vuelo: {H_b:.2f} m')
    return H_a

def salir(app):
    mostrar_pantalla_login(app)

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
    boton.tk.bind("<ButtonPress-1>", ignore_event, add="+")
    boton.tk.bind("<ButtonRelease-1>", on_button_release)

def on_hover(boton, color='white'):
    boton.tk.config(cursor="hand2")
    boton.tk.config(bg=color)

def on_leave(boton, color):
    boton.tk.config(cursor="")
    boton.tk.config(bg=color)

def ignore_event(event):
    return "break"

def on_button_release(event):
    event.widget.config(bg=None)
    event.widget.invoke()

def seleccionar_archivo(archivo_btn):
    global archivo_seleccionado  # Declarar la variable global
    archivo = app.select_file(filetypes=[["CSV files", "*.csv"], ["Excel files", "*.xlsx"]])
    if archivo:
        archivo_btn.text = f"Archivo: {ajustar_texto(archivo.split('/')[-1], 15)}"
        info("Archivo seleccionado", f"Has seleccionado: {archivo}")
        archivo_seleccionado = archivo
    return archivo

def cambiar_tema(nuevo_tema):
    global tema_actual
    tema_actual = nuevo_tema
    aplicar_tema(temas[nuevo_tema])
    mostrar_pantalla_principal(app)

def cambiar_volumen(volumen):
    global volumen_actual
    volumen_actual = int(float(volumen))
    pygame.mixer.music.set_volume(volumen_actual / 100.0)

def reproducir_musica():
    pygame.mixer.music.load("../../audio/003 - Title.mp3")
    pygame.mixer.music.play(-1)

def detener_musica():
    pygame.mixer.music.stop()

def cambiar_idioma(idioma):
    global idioma_actual
    idioma_actual = idioma
    mostrar_pantalla_principal(app)

def recortar_datos(t, a, umbral, duracion_min):
    # Encontrar el índice donde la aceleración supera el umbral
    start_indices = np.where(a > umbral)[0]
    if len(start_indices) == 0:
        raise ValueError("No se encontraron datos que superen el umbral.")

    start_index = start_indices[0]

    # Encontrar el índice donde la duración es suficiente
    end_index = start_index + int(duracion_min / (t[1] - t[0]))
    if end_index >= len(t):
        end_index = len(t) - 1

    # Verificar que los índices son válidos
    if start_index < 0 or end_index < 0 or start_index >= len(t) or end_index >= len(t):
        raise IndexError("Los índices de recorte son inválidos.")

    t_recortada = t[start_index:end_index] - t[start_index]
    a_recortada = a[start_index:end_index]

    return t_recortada, a_recortada, start_index, end_index

def enviar_datos_login(app, userTxTBox, passTxTBox):
    username = userTxTBox.value
    password = passTxTBox.value
    if login(iniciar_conexion(), username, password):
        mostrar_pantalla_login(app)
    else:
        mostrar_pantalla_principal(app)

def crear_imagen_texto(texto, width, height, radio, color_fondo, color_texto, ruta_fuente_titulos=None, tamano_fuente_titulos=16):
    imagen = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(imagen)

    draw.rounded_rectangle((0, 0, width, height), radius=radio, fill=color_fondo)

    if ruta_fuente_titulos:
        fuente_titulos = ImageFont.truetype(ruta_fuente_titulos, tamano_fuente_titulos)
    else:
        fuente_titulos = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), texto, font=fuente_titulos)
    w_texto = bbox[2] - bbox[0]
    h_texto = bbox[3] - bbox[1]
    pos_x = (width - w_texto) / 2
    pos_y = (height - h_texto) / 3

    draw.text((pos_x, pos_y), texto, font=fuente_titulos, fill=color_texto)

    return ImageTk.PhotoImage(imagen)

def mostrar_pantalla_realizarSalto(main_content):
    clear_box(main_content)

    canvas = tk.Canvas(main_content.tk, width=650, height=600, highlightthickness=0)
    canvas.place(x=0, y=0, anchor="nw")
    load_image(canvas, fondo_realizar_salto, [650, 600])

    contenido = Box(main_content, layout="grid", align="top", width="fill", height="fill")
    contenido.tk.place(relx=0.5, rely=0, anchor="n")
    contenido.tk.config(bg='', padx=0, pady=0)

    top_box = Box(contenido, grid=[0, 0], width="fill", height=40)
    top_box.tk.config(bg=color_fondo)

    titulo_box = Box(contenido, grid=[0, 1], align="top", width="fill")
    imagen_texto = crear_imagen_texto(get_translation(textos, idioma_actual, "REALIZAR SALTO"), 290, 40, 0, color_fondo, color_titulos, fuente_titulos, 30)
    titulo = tk.Label(titulo_box.tk, image=imagen_texto, bg=color_fondo)
    titulo.grid(row=0, column=0, sticky="nsew")
    titulo_box.tk.grid_columnconfigure(0, weight=1)
    titulo.image = imagen_texto

    top_box = Box(contenido, grid=[0, 2], width="fill", height=40)
    top_box.tk.config(bg=color_fondo)
    top_box = Box(contenido, grid=[0, 3], width="fill", height=60)
    top_box.tk.config(bg=color_fondo)

    centered_container = Box(contenido, grid=[0, 3], align="top")

    form_container = Box(centered_container, align="top", width="fill")
    form_box = Box(form_container, layout="grid", align="top")
    form_container.tk.config(bg=color_fondo)
    form_box.tk.config(bg=color_fondo)

    archivo_imagen = crear_imagen_texto(get_translation(textos, idioma_actual, "Seleccionar datos del salto: "), 205, 30, 0, color_fondo, color_texto, fuente_texto)
    archivoTXT = tk.Label(form_box.tk, image=archivo_imagen, bg=color_fondo)
    archivoTXT.grid(row=0, column=0, sticky="w")
    archivoTXT.image = archivo_imagen

    imagen_boton = crear_imagen_texto(get_translation(textos, idioma_actual, "Seleccionar Archivo"), 180, 35, 0, "white", "black", fuente_subtitulos, 14)
    archivoBTN = PushButton(form_box, text="Seleccionar Archivo", image=imagen_boton, grid=[1, 0], command=lambda: seleccionar_archivo(archivoBTN))
    colores = ["white", "black", "lightgrey"]
    estilizar_boton(archivoBTN, colores)

    box = Box(form_box, grid=[0, 1, 2, 1], height=20)
    box.tk.config(bg=color_fondo)

    masa_imagen = crear_imagen_texto(get_translation(textos, idioma_actual, "Masa del saltador: "), 140, 30, 0, color_fondo, color_texto, fuente_texto)
    masaTXT = tk.Label(form_box.tk, image=masa_imagen, bg=color_fondo)
    masaTXT.grid(row=2, column=0, sticky="w")
    masaTXT.image = masa_imagen

    masaTxTBox = TextBox(form_box, text="", grid=[1, 2], width=30)
    masaTxTBox.tk.config(bg='white')

    box = Box(form_box, grid=[0, 3, 2, 1], height=20)
    box.tk.config(bg=color_fondo)

    nombre_imagen = crear_imagen_texto(get_translation(textos, idioma_actual, "Nombre saltador: "), 131, 30, 0, color_fondo, color_texto, fuente_texto)
    nombreTXT = tk.Label(form_box.tk, image=nombre_imagen, bg=color_fondo)
    nombreTXT.grid(row=4, column=0, sticky="w")
    nombreTXT.image = nombre_imagen

    nombreTxTBox = TextBox(form_box, text="", grid=[1, 4], width=30)
    nombreTxTBox.tk.config(bg='white')

    box = Box(form_box, grid=[0, 5, 2, 1], height=20)
    box.tk.config(bg=color_fondo)

    grupo_imagen = crear_imagen_texto(get_translation(textos, idioma_actual, "Nombre grupo: "), 115, 30, 0, color_fondo, color_texto, fuente_texto)
    grupoTXT = tk.Label(form_box.tk, image=grupo_imagen, bg=color_fondo)
    grupoTXT.grid(row=6, column=0, sticky="w")
    grupoTXT.image = grupo_imagen

    grupoTxTBox = TextBox(form_box, text="", grid=[1, 6], width=30)
    grupoTxTBox.tk.config(bg='white')

    top_box = Box(contenido, grid=[0, 8], width="fill", height=30)
    top_box.tk.config(bg=color_fondo)

    imagen_boton = crear_imagen_texto(get_translation(textos, idioma_actual, "Enviar datos"), 150, 35, 0, "white", "black", fuente_subtitulos, 14)
    enviarBTN = PushButton(contenido, text="Enviar datos", grid=[0, 9], image=imagen_boton, command=lambda: mostrar_pantalla_resultados(main_content))
    estilizar_boton(enviarBTN, colores)


def mostrar_pantalla_resultados(main_content):
    clear_box(main_content)

    # resultado = calcular_datos_salto(archivo_seleccionado)
    # print(resultado)
    canvas = tk.Canvas(main_content.tk, width=650, height=600, highlightthickness=0)  # Quitar el borde del canvas
    canvas.place(x=0, y=0, anchor="nw")
    resultado = 34
    color_diapo = 0
    pikmin_key = ""

    if resultado <= 18:
        load_image(canvas, fondos_resultados[6], [650, 600])
        color_diapo = 0
        pikmin_key = "pikmin_morado"
    elif 18 < resultado <= 22.32:
        load_image(canvas, fondos_resultados[5], [650, 600])
        color_diapo = 1
        pikmin_key = "pikmin_pétreo"
    elif 22.32 < resultado <= 24.29:
        load_image(canvas, fondos_resultados[-1], [650, 600])
        color_diapo = 2
        pikmin_key = "pikmin_gélido"
    elif 24.29 < resultado <= 27.29:
        load_image(canvas, fondos_resultados[7], [650, 600])
        color_diapo = 3
        pikmin_key = "pikmin_blanco"
    elif 27.29 < resultado <= 30.06:
        load_image(canvas, fondos_resultados[3], [650, 600])
        color_diapo = 4
        pikmin_key = "pikmin_azul"
    elif 30.06 < resultado <= 33.63:
        load_image(canvas, fondos_resultados[0], [650, 600])
        color_diapo = 5
        pikmin_key = "pikmin_rojo"
    elif 33.63 < resultado <= 36.98:
        load_image(canvas, fondos_resultados[2], [650, 600])
        color_diapo = 6
        pikmin_key = "pikmin_amarillo"
    elif 36.98 < resultado <= 43.49:
        load_image(canvas, fondos_resultados[1], [650, 600])
        color_diapo = 7
        pikmin_key = "pikmin_luminoso"
    elif resultado > 43.49:
        load_image(canvas, fondos_resultados[4], [650, 600])
        color_diapo = 8
        pikmin_key = "pikmin_alado"

    contenido = Box(main_content, layout="grid", align="top", width="fill", height="fill")
    contenido.tk.place(relx=0.5, rely=0, anchor="n")
    contenido.tk.config(bg='', padx=0, pady=0)

    top_box = Box(contenido, grid=[0, 0], width="fill", height=71)
    top_box.tk.config(bg='#E73734')
    top_box = Box(contenido, grid=[0, 1], width="fill", height=20)
    titulo_box = Box(contenido, grid=[0, 2], align="top", width="fill")
    if len(colores_resultados) == 5:
        top_box.tk.config(bg='white')
        imagen_texto = crear_imagen_texto(get_translation(textos, idioma_actual, "Realizar salto"), 200, 40, 0, "white", color_texto, fuente_titulos, 30)
        titulo = tk.Label(titulo_box.tk, image=imagen_texto, bg='white')
    else:
        top_box.tk.config(bg=colores_resultados[color_diapo])
        imagen_texto = crear_imagen_texto(get_translation(textos, idioma_actual, "Realizar salto"), 200, 40, 0, colores_resultados[color_diapo], color_texto, fuente_titulos, 30)
        titulo = tk.Label(titulo_box.tk, image=imagen_texto, bg=colores_resultados[color_diapo])

    titulo.grid(row=0, column=0, sticky="nsew")
    titulo_box.tk.grid_columnconfigure(0, weight=1)
    titulo.image = imagen_texto

    pikmin_texto = "\n".join(get_translation(textos, idioma_actual, pikmin_key))

    if len(colores_resultados) == 5:
        text_widget = tk.Text(contenido.tk, wrap="word", bg="white", fg=color_texto, height=10, width=55, borderwidth=0, highlightthickness=0)
    else:
        text_widget = tk.Text(contenido.tk, wrap="word", bg=colores_resultados[color_diapo], fg=color_texto, height=10, width=55, borderwidth=0, highlightthickness=0)

    text_widget.insert("1.0", pikmin_texto)
    text_widget.config(state="disabled")
    text_widget.grid(row=3, column=0, sticky="nsew")

    contenido.tk.grid_rowconfigure(3, weight=1)
    contenido.tk.grid_columnconfigure(0, weight=1)


def mostrar_pantalla_inicio(main_content):
    clear_box(main_content)

    canvas = tk.Canvas(main_content.tk, width=650, height=600, highlightthickness=0)
    canvas.place(x=0, y=0, anchor="nw")
    load_image(canvas, fondo_inicio, [650, 600])

    contenido = Box(main_content, align="top", width="fill", height="fill")
    contenido.tk.place(relx=0.5, rely=0, anchor="n")
    contenido.tk.config(bg='', padx=0, pady=0)

    # Crear imágenes para los textos
    titulo_img = crear_imagen_texto(get_translation(textos, idioma_actual, "BIENVENIDO A PEAKLEAP"), 400, 40, 0, color_fondo, color_titulos, fuente_titulos, 24)
    introduccion_img = crear_imagen_texto(get_translation(textos, idioma_actual, "Esta aplicación te permitirá registrar y analizar tus saltos."), 600, 20, 0, color_fondo, color_texto, fuente_texto, 14)
    introduccion2_img = crear_imagen_texto(get_translation(textos, idioma_actual, "Sigue este tutorial para familiarizarte con las funcionalidades."), 600, 20, 0, color_fondo, color_texto, fuente_texto, 14)
    seccion1_titulo_img = crear_imagen_texto(get_translation(textos, idioma_actual, "1. Realizar Salto"), 200, 30, 0, color_fondo, color_texto, fuente_subtitulos, 18)
    seccion1_texto_img = crear_imagen_texto(get_translation(textos, idioma_actual, "En esta sección, puedes registrar los datos de tu salto"), 600, 20, 0, color_fondo, color_texto, fuente_texto, 14)
    seccion1_1_texto_img = crear_imagen_texto(get_translation(textos, idioma_actual, "incluyendo masa y nombre del saltador, y grupo."), 600, 20, 0, color_fondo, color_texto, fuente_texto, 14)
    seccion2_titulo_img = crear_imagen_texto(get_translation(textos, idioma_actual, "2. Ranking"), 200, 30, 0, color_fondo, color_texto, fuente_subtitulos, 18)
    seccion2_texto_img = crear_imagen_texto(get_translation(textos, idioma_actual, "Consulta el ranking de los mejores saltos registrados, ordenados por altura."), 600, 20, 0, color_fondo, color_texto, fuente_texto, 14)
    seccion3_titulo_img = crear_imagen_texto(get_translation(textos, idioma_actual, "3. Configuración"), 200, 30, 0, color_fondo, color_texto, fuente_subtitulos, 18)
    seccion3_texto_img = crear_imagen_texto(get_translation(textos, idioma_actual, "Ajusta las configuraciones de la aplicación, como el tema y el idioma."), 600, 20, 0, color_fondo, color_texto, fuente_texto, 14)
    final_tutorial_img = crear_imagen_texto(get_translation(textos, idioma_actual, "¡Esperamos que disfrutes usando PeakLeap!"), 600, 20, 0, color_fondo, color_texto, fuente_texto, 16)

    # Añadir los textos como etiquetas con imágenes
    titulo = tk.Label(contenido.tk, image=titulo_img, bg=color_fondo)
    titulo.pack(pady=(30, 10))
    titulo.image = titulo_img

    introduccion = tk.Label(contenido.tk, image=introduccion_img, bg=color_fondo)
    introduccion.pack(pady=0)
    introduccion.image = introduccion_img

    introduccion2 = tk.Label(contenido.tk, image=introduccion2_img, bg=color_fondo)
    introduccion2.pack(pady=0)
    introduccion2.image = introduccion2_img

    seccion1_titulo = tk.Label(contenido.tk, image=seccion1_titulo_img, bg=color_fondo)
    seccion1_titulo.pack(pady=10)
    seccion1_titulo.image = seccion1_titulo_img

    seccion1_texto = tk.Label(contenido.tk, image=seccion1_texto_img, bg=color_fondo)
    seccion1_texto.pack(pady=0)
    seccion1_texto.image = seccion1_texto_img

    seccion1_1_texto = tk.Label(contenido.tk, image=seccion1_1_texto_img, bg=color_fondo)
    seccion1_1_texto.pack(pady=0)
    seccion1_1_texto.image = seccion1_1_texto_img

    separador1 = Box(contenido, align="top", width="fill", height=20)
    separador1.tk.config(bg=color_fondo)

    seccion2_titulo = tk.Label(contenido.tk, image=seccion2_titulo_img, bg=color_fondo)
    seccion2_titulo.pack(pady=10)
    seccion2_titulo.image = seccion2_titulo_img

    seccion2_texto = tk.Label(contenido.tk, image=seccion2_texto_img, bg=color_fondo)
    seccion2_texto.pack(pady=5)
    seccion2_texto.image = seccion2_texto_img

    separador2 = Box(contenido, align="top", width="fill", height=20)
    separador2.tk.config(bg=color_fondo)

    seccion3_titulo = tk.Label(contenido.tk, image=seccion3_titulo_img, bg=color_fondo)
    seccion3_titulo.pack(pady=5)
    seccion3_titulo.image = seccion3_titulo_img

    seccion3_texto = tk.Label(contenido.tk, image=seccion3_texto_img, bg=color_fondo)
    seccion3_texto.pack(pady=5)
    seccion3_texto.image = seccion3_texto_img

    separador3 = Box(contenido, align="top", width="fill", height=10)
    separador3.tk.config(bg=color_fondo)

    final_tutorial = tk.Label(contenido.tk, image=final_tutorial_img, bg=color_fondo)
    final_tutorial.pack(pady=10)
    final_tutorial.image = final_tutorial_img


def mostrar_pantalla_configuracion(main_content):
    clear_box(main_content)

    canvas = tk.Canvas(main_content.tk, width=650, height=600, highlightthickness=0)
    canvas.place(x=0, y=0, anchor="nw")
    load_image(canvas, fondo_configuracion, [650, 600])

    contenido = Box(main_content, layout="grid", align="top", width="fill", height="fill")
    contenido.tk.place(relx=0.5, rely=0, anchor="n")
    contenido.tk.config(bg='', padx=0, pady=0)

    top_box = Box(contenido, grid=[0, 0], width="fill", height=40)
    top_box.tk.config(bg=color_fondo)

    titulo_box = Box(contenido, grid=[0, 1], align="top", width="fill")
    imagen_titulo = crear_imagen_texto(get_translation(textos, idioma_actual, "CONFIGURACIÓN"), 270, 40, 0, color_fondo, color_titulos, fuente_titulos, 30)
    titulo = tk.Label(titulo_box.tk, image=imagen_titulo, bg=color_fondo)
    titulo.grid(row=0, column=0, sticky="nsew")
    titulo_box.tk.grid_columnconfigure(0, weight=1)
    titulo.image = imagen_titulo

    top_box = Box(contenido, grid=[0, 2], align="top", width="fill", height=30)
    top_box.tk.config(bg=color_fondo)

    centered_container = Box(contenido, grid=[0, 3], align="top")
    centered_container.tk.config(bg=color_fondo)

    form_container = Box(centered_container, align="top", width="fill")
    form_box = Box(form_container, layout="grid", align="top")
    form_container.tk.config(bg=color_fondo)
    form_box.tk.config(bg=color_fondo)

    tema_imagen = crear_imagen_texto(get_translation(textos, idioma_actual, "Tema:"), 70, 30, 0, color_fondo, color_texto, fuente_texto)
    temaTXT = tk.Label(form_box.tk, image=tema_imagen, bg=color_fondo)
    temaTXT.grid(row=4, column=0, sticky="w")
    temaTXT.image = tema_imagen

    tema_selector = ttk.Combobox(form_box.tk, values=["Claro", "Oscuro"], style='TCombobox')
    tema_selector.grid(row=4, column=1, sticky="e")
    tema_selector.set(tema_actual)
    tema_selector.bind("<<ComboboxSelected>>", lambda event: cambiar_tema(tema_selector.get()))

    top_box = Box(form_box, grid=[0, 5, 2, 1], height=30)
    top_box.tk.config(bg=color_fondo)

    volumen_imagen = crear_imagen_texto(get_translation(textos, idioma_actual, "Volumen:"), 95, 30, 0, color_fondo, color_texto, fuente_texto)
    volumenTXT = tk.Label(form_box.tk, image=volumen_imagen, bg=color_fondo)
    volumenTXT.grid(row=6, column=0, sticky="w")
    volumenTXT.image = volumen_imagen

    volumen_slider = ttk.Scale(form_box.tk, from_=0, to=100, style='TScale', command=cambiar_volumen)
    volumen_slider.grid(row=6, column=1, sticky="e")
    volumen_slider.set(volumen_actual)

    top_box = Box(form_box, grid=[0, 7, 2, 1], height=30)
    top_box.tk.config(bg=color_fondo)

    idioma_imagen = crear_imagen_texto(get_translation(textos, idioma_actual, "Idioma:"), 80, 30, 0, color_fondo, color_texto, fuente_texto)
    idiomaTXT = tk.Label(form_box.tk, image=idioma_imagen, bg=color_fondo)
    idiomaTXT.grid(row=8, column=0, sticky="w")
    idiomaTXT.image = idioma_imagen

    idioma_selector = ttk.Combobox(form_box.tk, values=["Español", "English"], style='TCombobox')
    idioma_selector.grid(row=8, column=1, sticky="e")
    idioma_selector.set(idioma_actual)
    idioma_selector.bind("<<ComboboxSelected>>", lambda event: cambiar_idioma(idioma_selector.get()))


def mostrar_pantalla_ranking(main_content, datos_ranking):
    clear_box(main_content)

    canvas = tk.Canvas(main_content.tk, width=650, height=600, highlightthickness=0)  # Quitar el borde del canvas
    canvas.place(x=0, y=0, anchor="nw")
    load_image(canvas, fondo_ranking, [650, 600])

    contenido = Box(main_content, layout="grid", align="top", width="fill", height="fill")
    contenido.tk.place(relx=0.5, rely=0, anchor="n")
    contenido.tk.config(bg='', padx=0, pady=0)

    top_box = Box(contenido, grid=[0, 0], height=40)
    top_box.tk.config(bg=color_fondo)

    titulo_box = Box(contenido, grid=[0, 1], align="top", width=648, height=30)
    imagen_texto = crear_imagen_texto(get_translation(textos, idioma_actual, "RANKING"), 648, 40, 0, color_fondo, color_titulos, fuente_titulos, 30)  # Ajustar según tu ruta de fuente
    titulo = tk.Label(titulo_box.tk, image=imagen_texto, bg=color_fondo)
    titulo.grid(row=0, column=0, sticky="nsew")
    titulo_box.tk.grid_columnconfigure(0, weight=1)
    titulo.image = imagen_texto

    top_box = Box(contenido, grid=[0, 2], height=30, width="fill")
    top_box.tk.config(bg=color_fondo)

    encabezados_box = Box(contenido, grid=[0, 3], align="top", width="fill")
    encabezados = Box(encabezados_box, align="top")
    encabezados_box.tk.config(bg=color_fondo)
    encabezados.tk.config(bg=color_fondo)

    encabezados_imagenes = [
        crear_imagen_texto(get_translation(textos, idioma_actual, "Nombre"), 100, 30, 0, color_fondo, color_texto, fuente_subtitulos, 17),
        crear_imagen_texto(get_translation(textos, idioma_actual, "Grupo"), 100, 30, 0, color_fondo, color_texto, fuente_subtitulos, 17),
        crear_imagen_texto(get_translation(textos, idioma_actual, "Altura"), 100, 30, 0, color_fondo, color_texto, fuente_subtitulos, 17),
        crear_imagen_texto(get_translation(textos, idioma_actual, "Fecha"), 100, 30, 0, color_fondo, color_texto, fuente_subtitulos, 17)
    ]

    for i, encabezado_imagen in enumerate(encabezados_imagenes):
        label = tk.Label(encabezados.tk, image=encabezado_imagen, bg=color_fondo)
        label.grid(row=0, column=i, sticky="nsew")
        encabezados.tk.grid_columnconfigure(i, weight=1)
        label.image = encabezado_imagen  # Guardar una referencia a la imagen para evitar que se recolecte como basura

    try:
        top_box = Box(contenido, grid=[0, 4], height=20, width="fill")
        top_box.tk.config(bg=color_fondo)
        for i in range(10):
            fila_box = Box(contenido, grid=[0, 5 + i], align="top", width="fill")
            fila = Box(fila_box, align="top")
            fila_box.tk.config(bg=color_fondo)

            # Crear imágenes para los datos del ranking
            datos_imagenes = [
                crear_imagen_texto(datos_ranking[i]['nombre'], 100, 20, 0, color_fondo, color_texto, fuente_texto),
                crear_imagen_texto(datos_ranking[i]['grupo'], 100, 20, 0, color_fondo, color_texto, fuente_texto),
                crear_imagen_texto(datos_ranking[i]['altura'], 100, 20, 0, color_fondo, color_texto, fuente_texto),
                crear_imagen_texto(datos_ranking[i]['fecha'], 100, 20, 0, color_fondo, color_texto, fuente_texto)
            ]

            for j, dato_imagen in enumerate(datos_imagenes):
                label = tk.Label(fila.tk, image=dato_imagen, bg=color_fondo)
                label.grid(row=0, column=j, sticky="nsew")
                fila.tk.grid_columnconfigure(j, weight=1)
                label.image = dato_imagen  # Guardar una referencia a la imagen para evitar que se recolecte como basura

    except IndexError:
        print("No quedan más registros")


def mostrar_pantalla_principal(app):
    clear_box(app)
    center_window(app, 800, 600)

    sidebar = Box(app, align="left", width=150, height="fill")
    sidebar.tk.config(bg=color_sidebar)

    separador = Box(sidebar, width="fill", height=200, align="top")
    separador.tk.config(bg=color_sidebar)

    canvas = tk.Canvas(sidebar.tk, width=150, height=150, highlightthickness=0, bg=color_sidebar)
    canvas.place(x=0, y=30, anchor="nw")
    load_image(canvas, "../../imagenes/icono.png", [150, 150])

    right_container = Box(app, align="left", width="fill", height="fill")
    main_content = Box(right_container, align="top", width="fill", height="fill")
    main_content.tk.config(bg=color_fondo)
    mostrar_pantalla_inicio(main_content)

    imagen_boton = crear_imagen_texto(get_translation(textos, idioma_actual, "Inicio"), 150, 100, 0, color_sidebar, color_texto, fuente_subtitulos, 14)
    instruccionesPB = PushButton(sidebar, image=imagen_boton, text="Inicio", align="top", height=60, command=lambda: mostrar_pantalla_inicio(main_content))
    instruccionesPB.tk.config(bg=color_sidebar)
    imagen_boton = crear_imagen_texto(get_translation(textos, idioma_actual, "Realizar salto"), 150, 100, 0, color_sidebar, color_texto, fuente_subtitulos, 14)
    realizarsaltoPB = PushButton(sidebar, image=imagen_boton, text="Realizar salto", align="top", height=60, command=lambda: mostrar_pantalla_realizarSalto(main_content))
    realizarsaltoPB.tk.config(bg=color_sidebar)
    imagen_boton = crear_imagen_texto(get_translation(textos, idioma_actual, "Ranking"), 150, 100, 0, color_sidebar, color_texto, fuente_subtitulos, 14)
    rankingPB = PushButton(sidebar, text="Ranking", image=imagen_boton, align="top", height=60, command=lambda: mostrar_pantalla_ranking(main_content, datos_ranking))
    rankingPB.tk.config(bg=color_sidebar)
    imagen_boton = crear_imagen_texto(get_translation(textos, idioma_actual, "Configuración"), 150, 100, 0, color_sidebar, color_texto, fuente_subtitulos, 14)
    configPB = PushButton(sidebar, text="Config", image=imagen_boton, align="top", height=60, command=lambda: mostrar_pantalla_configuracion(main_content))
    configPB.tk.config(bg=color_sidebar)

    canvas_boton_volver = tk.Canvas(sidebar.tk, width=75, height=75, highlightthickness=0, bg=color_sidebar)
    canvas_boton_volver.place(x=40, y=510, anchor="nw")
    load_image(canvas_boton_volver, "../../imagenes/boton_volver.png", [75, 75])

    canvas_boton_volver.bind("<Button-1>", lambda event: salir(app))
    canvas_boton_volver.bind("<Enter>", lambda event: canvas_boton_volver.config(cursor="hand2"))
    canvas_boton_volver.bind("<Leave>", lambda event: canvas_boton_volver.config(cursor=""))

    estilizar_boton(instruccionesPB, colores_botones_sidebar)
    estilizar_boton(realizarsaltoPB, colores_botones_sidebar)
    estilizar_boton(rankingPB, colores_botones_sidebar)
    estilizar_boton(configPB, colores_botones_sidebar)

    app.tk.update_idletasks()


def mostrar_pantalla_login(app):
    clear_box(app)

    canvas = tk.Canvas(app.tk, width=800, height=600)
    canvas.place(relx=0.5, rely=0.5, anchor="center")

    load_image(canvas, fondo_login, [802, 602])

    form_box = Box(app, layout="grid", align="top")
    form_box.tk.place(relx=0.5, rely=0.5, anchor="center")
    form_box.tk.config(bg='')

    separador = Box(form_box, grid=[0, 0, 1, 1], height=80)
    separador.tk.config(bg='')

    imagen_usuarioTXT = crear_imagen_texto(get_translation(textos, idioma_actual, "Usuario: "), 90, 35, 0, color_fondo, color_texto, fuente_subtitulos)
    label_usuarioTXT = tk.Label(form_box.tk, image=imagen_usuarioTXT, bg=color_fondo)
    label_usuarioTXT.grid(row=1, column=0, sticky="w")
    label_usuarioTXT.image = imagen_usuarioTXT

    userTxTBox = TextBox(form_box, text="", grid=[1, 1], width=30)
    userTxTBox.tk.config(bg="white")

    imagen_passTXT = crear_imagen_texto(get_translation(textos, idioma_actual, "Contraseña: "), 120, 35, 0, color_fondo, color_texto, fuente_subtitulos)
    label_passTXT = tk.Label(form_box.tk, image=imagen_passTXT, bg=color_fondo)
    label_passTXT.grid(row=2, column=0, sticky="w")
    label_passTXT.image = imagen_passTXT  # Guardar una referencia a la imagen

    passTxTBox = TextBox(form_box, text="", grid=[1, 2], width=30, hide_text=True)
    passTxTBox.tk.config(bg="white")

    separador = Box(form_box, grid=[0, 3, 2, 1], height=30)
    separador.tk.config(bg='')

    button_container = Box(form_box, grid=[0, 4, 2, 1], align="top", width="fill")
    imagen_boton = crear_imagen_texto(get_translation(textos, idioma_actual, "Iniciar sesión"), 150, 50, 0, "white", "black", fuente_titulos)
    sendPB = PushButton(button_container, image=imagen_boton, align="top", command=lambda: enviar_datos_login(app, userTxTBox, passTxTBox))
    estilizar_boton(sendPB, colores_botones_inter)

if __name__ == "__main__":
    app = App(title="PikLeap", width=800, height=600, bg="#fff5a4")
    app.tk.resizable(False, False)
    mostrar_pantalla_login(app)
    #reproducir_musica()
    center_window(app, 800, 600)
    app.display()
