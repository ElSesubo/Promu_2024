import tempfile
from io import BytesIO
from unittest.mock import patch, MagicMock, call, ANY, Mock, mock_open
import pytest
from main import *

# Prueba para la función aplicar_tema ---------------------- CHECK (No puede acceder a las variables globales)
def test_aplicar_tema():
    global color_fondo
    color_fondo = ""

    with open('../config_data/temas.json', 'r') as archivo_temas:
        temas = json.load(archivo_temas)

    # Llamar a la función aplicar_tema
    aplicar_tema(temas["Oscuro"])

    # Verificar que todas las variables globales se establecieron correctamente
    assert color_fondo == temas["Oscuro"]["color_fondo"]

# Prueba para la funcion center_window ---------------------- CHECK
def test_center_window():
    # Crear un mock para app.tk
    mock_tk = MagicMock()
    mock_tk.winfo_screenwidth.return_value = 1920
    mock_tk.winfo_screenheight.return_value = 1080

    # Crear un mock para app
    mock_app = MagicMock()
    mock_app.tk = mock_tk

    # Parámetros de ejemplo
    width = 800
    height = 600

    # Llamar a la función a probar
    center_window(mock_app, width, height)

    # Calcular los valores esperados
    expected_x = (1920 // 2) - (width // 2)
    expected_y = (1080 // 2) - (height // 2)
    expected_geometry = f'{width}x{height}+{expected_x}+{expected_y}'

    # Verificar que winfo_screenwidth y winfo_screenheight se llamaron correctamente
    mock_tk.winfo_screenwidth.assert_called_once()
    mock_tk.winfo_screenheight.assert_called_once()

    # Verificar que geometry se llamó correctamente
    mock_tk.geometry.assert_called_once_with(expected_geometry)

# Prueba para la funcion load_image ---------------------- CHECK
@patch('main.ImageTk.PhotoImage')
@patch('main.Image.open')
def test_load_image(mock_open, mock_photo_image):
    # Configurar los mocks
    mock_image_instance = MagicMock()
    mock_open.return_value = mock_image_instance
    mock_resized_image = MagicMock()
    mock_image_instance.resize.return_value = mock_resized_image
    mock_photo_image_instance = MagicMock()
    mock_photo_image.return_value = mock_photo_image_instance

    # Mock del canvas
    mock_canvas = MagicMock()

    # Parámetros de ejemplo
    path = "dummy_path.png"
    dimensiones = (100, 100)

    # Llamar a la función a probar
    load_image(mock_canvas, path, dimensiones)

    # Verificar que Image.open se llamó correctamente
    mock_open.assert_called_once_with(path)

    # Verificar que resize se llamó correctamente
    mock_image_instance.resize.assert_called_once_with((dimensiones[0], dimensiones[1]), Image.LANCZOS)

    # Verificar que PhotoImage se creó correctamente
    mock_photo_image.assert_called_once_with(mock_resized_image)

    # Verificar que create_image se llamó correctamente en el canvas
    mock_canvas.create_image.assert_called_once_with(0, 0, anchor=tk.NW, image=mock_photo_image_instance)

    # Verificar que la imagen se asignó correctamente al atributo del canvas
    assert mock_canvas.image == mock_photo_image_instance

# Prueba para la función insertar_salto_linea_en_punto ---------------------- CHECK
def test_insertar_salto_linea_en_punto():
    assert insertar_salto_linea_en_punto("Hola. Mundo") == "Hola.\n\n Mundo"
    assert insertar_salto_linea_en_punto("Hola Mundo") == "Hola Mundo"
    assert insertar_salto_linea_en_punto("Hola.Mundo") == "Hola.\n\nMundo"
    assert insertar_salto_linea_en_punto("Hola.  Mundo") == "Hola.\n\n  Mundo"

# Prueba para la función load_translations ---------------------- CHECK
def test_load_translations(tmp_path):
    file_content = '{"es": {"key1": "valor1", "key2": "valor2"}}'
    file_path = tmp_path / "translations.json"
    file_path.write_text(file_content)
    translations = load_translations(file_path)
    assert translations == {"es": {"key1": "valor1", "key2": "valor2"}}

# Prueba para la función get_translations ---------------------- CHECK
def test_get_translation():
    translations = {
        "en": {
            "greeting": "Hello",
            "farewell": "Goodbye"
        },
        "es": {
            "greeting": "Hola",
            "farewell": "Adiós"
        },
        "fr": {
            "greeting": "Bonjour",
            "farewell": "Au revoir"
        }
    }

    # Pruebas para el idioma inglés
    assert get_translation(translations, "en", "greeting") == "Hello"
    assert get_translation(translations, "en", "farewell") == "Goodbye"
    assert get_translation(translations, "en", "unknown_key") == "unknown_key"

    # Pruebas para el idioma español
    assert get_translation(translations, "es", "greeting") == "Hola"
    assert get_translation(translations, "es", "farewell") == "Adiós"
    assert get_translation(translations, "es", "unknown_key") == "unknown_key"

    # Pruebas para el idioma francés
    assert get_translation(translations, "fr", "greeting") == "Bonjour"
    assert get_translation(translations, "fr", "farewell") == "Au revoir"
    assert get_translation(translations, "fr", "unknown_key") == "unknown_key"

    # Pruebas para un idioma que no está en las traducciones
    with pytest.raises(KeyError):
        get_translation(translations, "de", "greeting")

# Prueba para la función importar_datos ---------------------- CHECK
def test_importar_datos():
    # Datos de prueba
    datos = {
        't': ['0.0', '0.1', '0.2'],
        'a': ['0.1', '0.2', '0.3'],
        'ax': ['0.1', '0.2', '0.3'],
        'ay': ['0.1', '0.2', '0.3'],
        'az': ['0.1', '0.2', '0.3']
    }
    df = pd.DataFrame(datos)
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False, engine='openpyxl')
    excel_file.seek(0)

    # Mock de pandas.read_excel
    with patch('pandas.read_excel', return_value=pd.read_excel(excel_file, engine='openpyxl')) as mock_read_excel:
        t, a, ax, ay, az = importar_datos("dummy_file.xlsx")

        # Verificar que read_excel fue llamado con el archivo correcto
        mock_read_excel.assert_called_once_with("dummy_file.xlsx", engine='openpyxl')

        # Verificar los datos importados
        assert t.tolist() == [0.0, 0.1, 0.2]
        assert a.tolist() == [0.1, 0.2, 0.3]
        assert ax.tolist() == [0.1, 0.2, 0.3]
        assert ay.tolist() == [0.1, 0.2, 0.3]
        assert az.tolist() == [0.1, 0.2, 0.3]

# Prueba para la función corregir_aceleracion ---------------------- CHECK
def test_corregir_aceleracion():
    # Datos de aceleración y aceleración en el eje y
    a = np.array([1, 2, 3, 4, 5])
    ay = np.array([-1, -2, -3, -4, -5])

    # Aplicar corrección
    a_corregida = corregir_aceleracion(a, ay)

    # Verificar si todos los valores de la aceleración corregida tienen el mismo signo que los valores originales
    assert np.all(np.sign(a_corregida) == np.sign(ay))

# Prueba para la función recortar_combinar_datos ---------------------- CHECK
def test_recortar_combinar_datos():
    t = np.linspace(0, 10, 100)
    a = np.sin(t)
    t_combinada, a_combinada = recortar_combinar_datos(t, a)

    # Asegurarse de que las longitudes sean iguales
    assert len(t_combinada) == len(a_combinada)

    # Verificar el primer segmento
    reposo_indice = np.searchsorted(t, 0.5, side='left')
    t_reposo_esperado = t[:reposo_indice] - t[0]
    a_reposo_esperado = a[:reposo_indice]

    assert np.allclose(t_combinada[:reposo_indice], t_reposo_esperado)
    assert np.array_equal(a_combinada[:reposo_indice], a_reposo_esperado)

    # Verificar el segundo segmento
    start_index = np.searchsorted(t, 0.5, side='left')
    end_index = np.searchsorted(t, 3, side='left')
    t_recortada_esperada = t[start_index:end_index] - t[start_index] + t_reposo_esperado[-1] + (t[1] - t[0])
    a_recortada_esperada = a[start_index:end_index]

    assert np.allclose(t_combinada[reposo_indice:], t_recortada_esperada)
    assert np.array_equal(a_combinada[reposo_indice:], a_recortada_esperada)

# Prueba para la función aplicar_filtro_savgol ---------------------- CHECK
def test_aplicar_filtro_savgol():
    # Datos de prueba
    a_combinada = np.array([1, 3, 2, 4, 6, 8, 7, 5, 3, 2, 1, 0, 1, 2, 3])

    # Resultado esperado usando la misma función de filtro
    expected_result = savgol_filter(a_combinada, window_length=11, polyorder=3)

    # Llamada a la función
    result = aplicar_filtro_savgol(a_combinada)

    # Verificación de los resultados
    assert np.allclose(result, expected_result), f"Result: {result}, Expected: {expected_result}"

# Prueba para la función obtener_instantes_clave ---------------------- CHECK
def test_obtener_instantes_clave():
    t_combinada = np.linspace(0, 10, 100)
    a_filtrada = np.sin(t_combinada)

    t1, t2, t3, t1_index, t2_index, t3_index = obtener_instantes_clave(t_combinada, a_filtrada)

    # Calcular los valores esperados manualmente
    diff_a_filtrada = np.diff(a_filtrada)
    expected_t1_index = np.argmax(diff_a_filtrada > 0.1) + 1
    expected_t1 = t_combinada[expected_t1_index]

    min_abs_a = np.argmin(np.abs(a_filtrada))
    if min_abs_a == 0:
        expected_t2_index = 0
    else:
        expected_t2_index = np.argmax(a_filtrada[:min_abs_a])
    expected_t2 = t_combinada[expected_t2_index]

    expected_t3_index = min_abs_a + np.argmax(np.abs(np.gradient(a_filtrada[min_abs_a:])) > 0.1)
    expected_t3 = t_combinada[expected_t3_index]

    assert t1 == expected_t1
    assert t2 == expected_t2
    assert t3 == expected_t3
    assert t1_index == expected_t1_index
    assert t2_index == expected_t2_index
    assert t3_index == expected_t3_index

# Prueba para la función calcular_fuerza_salto ---------------------- CHECK
def test_calcular_fuerza_salto():
    # Datos de prueba
    a_filtrada = np.array([10.0, 9.5, 10.5, 11.0, 9.0])
    g_medida = 9.8
    m = 70  # masa en kg

    # Resultado esperado
    a_salt = a_filtrada - g_medida
    F_esperada = m * (a_salt + 9.81)

    # Llamada a la función
    F = calcular_fuerza_salto(a_filtrada, g_medida, m)

    # Verificación de los resultados
    assert np.allclose(F, F_esperada)

# Prueba para la función calcular_velocidad_salto ---------------------- CHECK
def test_calcular_velocidad_salto():
    t_combinada = np.linspace(0, 10, 100)
    a_filtrada = np.sin(t_combinada)
    v_recortada, t_v_recortada, _ = calcular_velocidad_salto(t_combinada, a_filtrada, 9.81, 0, 99)
    assert len(v_recortada) == len(t_v_recortada)
    assert np.allclose(v_recortada[0], 0)

# Prueba para la función calcular_potencia_salto ---------------------- CHECK
def test_calcular_potencia_salto():
    # Datos de prueba
    F = np.array([100, 150, 200, 250, 300, 350])
    v_recortada = np.array([2, 2.5, 3, 3.5, 4])
    t1_index = 1
    t3_index = 5
    t_combinada = np.linspace(0, 10, 6)

    # Resultados esperados
    F_recortada = F[t1_index:t3_index + 1]
    P_esperada = F_recortada * v_recortada
    t_recortado_esperado = t_combinada[t1_index:t3_index + 1]

    # Llamada a la función
    P, t_recortado = calcular_potencia_salto(F, v_recortada, t1_index, t3_index, t_combinada)

    # Verificación de los resultados
    assert np.allclose(P, P_esperada)
    assert np.allclose(t_recortado, t_recortado_esperado)

# Prueba para la función calcular_altura_salto ---------------------- CHECK
def test_calcular_altura_salto():
    # Datos de prueba
    v_max = 5.0  # velocidad máxima en m/s
    g_medida = 9.81  # aceleración debida a la gravedad en m/s^2
    t_vuelo = 1.0  # tiempo de vuelo en segundos

    # Resultados esperados
    H_a_esperada = (v_max ** 2) / (2 * g_medida)
    H_b_esperada = (g_medida * (t_vuelo / 2) ** 2) / 2

    # Llamada a la función
    H_a, H_b = calcular_altura_salto(v_max, g_medida, t_vuelo)

    # Verificación de los resultados
    assert H_a == H_a_esperada
    assert H_b == H_b_esperada

# Prueba para la función calcular_datos_salto ---------------------- CHECK
@patch('main.importar_datos')
@patch('main.corregir_aceleracion')
@patch('main.recortar_combinar_datos')
@patch('main.aplicar_filtro_savgol')
@patch('main.obtener_instantes_clave')
@patch('main.calcular_fuerza_salto')
@patch('main.calcular_velocidad_salto')
@patch('main.calcular_potencia_salto')
@patch('main.calcular_altura_salto')
def test_calcular_datos_salto(mock_calcular_altura_salto, mock_calcular_potencia_salto, mock_calcular_velocidad_salto, 
                              mock_calcular_fuerza_salto, mock_obtener_instantes_clave, mock_aplicar_filtro_savgol, 
                              mock_recortar_combinar_datos, mock_corregir_aceleracion, mock_importar_datos):
    
    # Configura los mocks
    mock_importar_datos.return_value = (np.array([0, 1, 2, 3]), np.array([1, 2, 3, 4]), 
                                        np.array([0.1, 0.2, 0.3, 0.4]), np.array([0.1, 0.2, 0.3, 0.4]), 
                                        np.array([0.1, 0.2, 0.3, 0.4]))
    mock_corregir_aceleracion.return_value = np.array([1, 2, 3, 4])
    mock_recortar_combinar_datos.return_value = (np.array([0, 1, 2]), np.array([1, 2, 3]))
    mock_aplicar_filtro_savgol.return_value = np.array([1, 1.5, 2])
    mock_obtener_instantes_clave.return_value = (0.5, 1.5, 2.5, 0, 1, 2)
    mock_calcular_fuerza_salto.return_value = np.array([10, 20, 30])
    mock_calcular_velocidad_salto.return_value = (np.array([0, 1, 2]), np.array([0, 1, 2]), 1)
    mock_calcular_potencia_salto.return_value = (np.array([5, 10, 15]), np.array([0, 1, 2]))
    mock_calcular_altura_salto.return_value = (0.5, 0.6)

    # Datos de prueba
    fichero = 'path/to/file'
    masa = 70

    # Llama a la función
    H_b, datos = calcular_datos_salto(fichero, masa)

    # Verifica los resultados
    assert H_b == 0.6
    assert datos['t'].tolist() == [0, 1, 2, 3]
    assert datos['ax'].tolist() == [0.1, 0.2, 0.3, 0.4]
    assert datos['ay'].tolist() == [0.1, 0.2, 0.3, 0.4]
    assert datos['az'].tolist() == [0.1, 0.2, 0.3, 0.4]
    assert datos['a'].tolist() == [1, 2, 3, 4]
    assert datos['a_fixed'].tolist() == [1, 2, 3, 4]
    assert datos['t_combinada'].tolist() == [0, 1, 2]
    assert datos['a_combinada'].tolist() == [1, 2, 3]
    assert datos['a_filtrada'].tolist() == [1, 1.5, 2]
    assert datos['t1'] == 0.5
    assert datos['t2'] == 1.5
    assert datos['t3'] == 2.5
    assert datos['t1_index'] == 0
    assert datos['t2_index'] == 1
    assert datos['t3_index'] == 2
    assert datos['v_recortada'].tolist() == [0, 1, 2]
    assert datos['t_v_recortada'].tolist() == [0, 1, 2]
    assert datos['t_v_max'] == 2  # Verifica que el tiempo de la velocidad máxima sea correcto
    assert datos['v_max'] == 2
    assert datos['t_v_min'] == 0  # Verifica que el tiempo de la velocidad mínima sea correcto
    assert datos['v_min'] == 0
    assert datos['P'].tolist() == [5, 10, 15]
    assert datos['t_recortado'].tolist() == [0, 1, 2]
    assert datos['t_p_max'] == 2
    assert datos['p_max'] == 15
    assert datos['start_index'] == 0
    assert datos['end_index'] == 2


# Prueba para la función representar_todos_los_datos ---------------------- CHECK
@pytest.mark.mpl_image_compare
def test_representar_todos_los_datos():
    # Datos de prueba
    datos = {
        't': np.array([0, 1, 2, 3]),
        'ax': np.array([0.1, 0.2, 0.3, 0.4]),
        'ay': np.array([0.1, 0.2, 0.3, 0.4]),
        'az': np.array([0.1, 0.2, 0.3, 0.4]),
        'a': np.array([1, 2, 3, 4]),
        'a_fixed': np.array([1, 2, 3, 4]),
        't_combinada': np.array([0, 1, 2]),
        'a_combinada': np.array([1, 2, 3]),
        'a_filtrada': np.array([1, 1.5, 2]),
        't1': 0.5,
        't2': 1.5,
        't3': 2.5,
        't1_index': 0,
        't2_index': 1,
        't3_index': 2,
        'v_recortada': np.array([0, 1, 2]),
        't_v_recortada': np.array([0, 1, 2]),
        't_v_max': 1,
        'v_max': 2,
        't_v_min': 2,
        'v_min': 0,
        'P': np.array([5, 10, 15]),
        't_recortado': np.array([0, 1, 2]),
        't_p_max': 1,
        'p_max': 10
    }

    fig, axs = plt.subplots(3, 2, figsize=(14, 18))

    # Gráfico de aceleraciones originales
    axs[0, 0].plot(datos['t'], datos['ax'], label='ax')
    axs[0, 0].plot(datos['t'], datos['ay'], label='ay')
    axs[0, 0].plot(datos['t'], datos['az'], label='az')
    axs[0, 0].plot(datos['t'], datos['a'], label='a')
    axs[0, 0].set_title('Aceleraciones originales')
    axs[0, 0].set_xlabel('Tiempo [s]')
    axs[0, 0].set_ylabel('Aceleración [m/s²]')
    axs[0, 0].grid(True)
    axs[0, 0].legend()

    # Gráfico de aceleración corregida
    axs[0, 1].plot(datos['t'], datos['a_fixed'], label='a corregida')
    axs[0, 1].set_title('Aceleración corregida')
    axs[0, 1].set_xlabel('Tiempo [s]')
    axs[0, 1].set_ylabel('Aceleración [m/s²]')
    axs[0, 1].grid(True)
    axs[0, 1].legend()

    # Gráfico de señales filtradas
    axs[1, 0].plot(datos['t_combinada'], datos['a_combinada'], label='a combinada')
    axs[1, 0].plot(datos['t_combinada'], datos['a_filtrada'], label='a filtrada')
    axs[1, 0].set_title('Señales combinadas y filtradas')
    axs[1, 0].set_xlabel('Tiempo [s]')
    axs[1, 0].set_ylabel('Aceleración [m/s²]')
    axs[1, 0].grid(True)
    axs[1, 0].legend()

    # Gráfico de instantes clave
    axs[1, 1].plot(datos['t_combinada'], datos['a_filtrada'], label='a filtrada')
    axs[1, 1].plot(datos['t1'], datos['a_filtrada'][datos['t1_index']], 'ro')  # t1
    axs[1, 1].plot(datos['t2'], datos['a_filtrada'][datos['t2_index']], 'go')  # t2
    axs[1, 1].plot(datos['t3'], datos['a_filtrada'][datos['t3_index']], 'bo')  # t3
    axs[1, 1].set_title('Instantes clave')
    axs[1, 1].set_xlabel('Tiempo [s]')
    axs[1, 1].set_ylabel('Aceleración [m/s²]')
    axs[1, 1].grid(True)
    axs[1, 1].legend()

    # Gráfico de velocidad
    axs[2, 0].plot(datos['t_v_recortada'], datos['v_recortada'], label='Velocidad')
    axs[2, 0].plot(datos['t_v_max'], datos['v_max'], 'ro')  # Velocidad máxima
    axs[2, 0].plot(datos['t_v_min'], datos['v_min'], 'bo')  # Velocidad mínima
    axs[2, 0].set_title('Velocidad en función del tiempo')
    axs[2, 0].set_xlabel('Tiempo [s]')
    axs[2, 0].set_ylabel('Velocidad [m/s]')
    axs[2, 0].grid(True)
    axs[2, 0].legend()

    # Gráfico de potencia
    axs[2, 1].plot(datos['t_recortado'], datos['P'], label='Potencia')
    axs[2, 1].plot(datos['t_p_max'], datos['p_max'], 'ro')  # Potencia máxima
    axs[2, 1].set_title('Potencia en función del tiempo')
    axs[2, 1].set_xlabel('Tiempo [s]')
    axs[2, 1].set_ylabel('Potencia [W]')
    axs[2, 1].grid(True)
    axs[2, 1].legend()

    fig.subplots_adjust(hspace=0.4, wspace=0.3)

    return fig

# Prueba para la función salir ---------------------- CHECK
def test_salir():
    app_mock = MagicMock()

    # Parchea las funciones y la variable global
    with patch('main.messagebox.askyesno') as mock_askyesno, \
         patch('main.quit_session') as mock_quit_session, \
         patch('main.mostrar_pantalla_login') as mock_mostrar_pantalla_login, \
         patch('main.get_translation', side_effect=lambda texts, lang, key: key), \
         patch('main.server', new_callable=MagicMock) as mock_server:

        # Simula que el usuario responde "Sí" al mensaje de confirmación
        mock_askyesno.return_value = True

        # Llama a la función salir
        salir(app_mock)

        # Verifica que messagebox.askyesno fue llamado correctamente
        mock_askyesno.assert_called_once_with("confirmacion", "continuar")
        # Verifica que quit_session fue llamado con el servidor correcto
        mock_quit_session.assert_called_once_with(mock_server)
        # Verifica que mostrar_pantalla_login fue llamado con la aplicación correcta
        mock_mostrar_pantalla_login.assert_called_once_with(app_mock)
        # Verifica que el servidor global se estableció a None
        assert server is None

# Prueba para la función ajustar_texto ---------------------- CHECK
def test_ajustar_texto():
    texto = "Este es un texto muy largo que necesita ser ajustado"
    max_length = 15
    resultado = ajustar_texto(texto, max_length)
    assert resultado == "Este es un t..."

# Prueba para la función estilizar_boton ---------------------- CHECK
def test_estilizar_boton():
    # Crear un mock para el botón y las funciones
    boton_mock = MagicMock()
    boton_mock.tk = MagicMock()
    colores = ["#ffffff", "#000000", "#cccccc"]

    with patch('main.on_hover') as mock_on_hover, \
         patch('main.on_leave') as mock_on_leave, \
         patch('main.ignore_event') as mock_ignore_event, \
         patch('main.on_button_release') as mock_on_button_release:

        # Llama a la función estilizar_boton
        estilizar_boton(boton_mock, colores)

        # Verifica que los métodos de configuración del botón se llamaron correctamente
        boton_mock.tk.config.assert_called_once_with(
            bg=colores[0],
            fg=colores[1],
            font=("Helvetica", 10),
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=5,
        )

        # Verifica que los métodos de enlace del botón se llamaron correctamente
        assert boton_mock.tk.bind.call_count == 4
        calls = [
            call("<Enter>", ANY),
            call("<Leave>", ANY),
            call("<ButtonPress-1>", ANY, add="+"),
            call("<ButtonRelease-1>", ANY)
        ]
        boton_mock.tk.bind.assert_has_calls(calls, any_order=True)

# Prueba para la función on_hover ---------------------- CHECK
def test_on_hover():
    # Crear un mock para el botón
    boton_mock = MagicMock()
    boton_mock.tk = MagicMock()

    # Llama a la función on_hover
    on_hover(boton_mock)

    # Verifica que los métodos de configuración del botón se llamaron correctamente
    boton_mock.tk.config.assert_any_call(cursor="hand2")
    boton_mock.tk.config.assert_any_call(bg='white')

# Prueba para la función on_leave ---------------------- CHECK
def test_on_leave():
    # Crear un mock para el botón
    boton_mock = MagicMock()
    boton_mock.tk = MagicMock()

    # Llama a la función on_leave
    on_leave(boton_mock, 'white')

    # Verifica que los métodos de configuración del botón se llamaron correctamente
    boton_mock.tk.config.assert_any_call(cursor="")
    boton_mock.tk.config.assert_any_call(bg='white')

# Prueba para la función ignore_events ---------------------- CHECK
def test_ignore_events():
    event = MagicMock()
    assert ignore_event(event) == "break"

# Prueba para la función on_button_release ---------------------- CHECK
def test_on_button_release():
    widget_mock = MagicMock()

    # Crear un mock para el evento
    event_mock = MagicMock()
    event_mock.widget = widget_mock

    # Llama a la función on_button_release con el evento de prueba
    on_button_release(event_mock)

    # Verifica que los métodos de configuración del widget se llamaron correctamente
    widget_mock.config.assert_called_once_with(bg=None)
    widget_mock.invoke.assert_called_once()

@pytest.fixture
def archivo_btn_mock():
    return MagicMock()

# Prueba para la función seleccionar_archivo ---------------------- CHECK
def test_seleccionar_archivo(archivo_btn_mock):
    # Valor de prueba para el archivo seleccionado
    archivo = "/ruta/al/archivo/seleccionado.xlsx"

    # Crear un mock para app
    mock_app = MagicMock()
    mock_app.select_file.return_value = archivo

    # Parchea las funciones y la variable global
    with patch.dict('main.__dict__', {'app': mock_app, 'archivo_seleccionado': None}), \
         patch('main.ajustar_texto', side_effect=lambda text, length: text[:length-3] + '...' if len(text) > length else text) as mock_ajustar_texto, \
         patch('main.info') as mock_info:

        # Llama a la función seleccionar_archivo
        resultado = seleccionar_archivo(archivo_btn_mock)

        # Verifica que select_file fue llamado correctamente
        mock_app.select_file.assert_called_once_with(filetypes=[["Excel files", "*.xls"], ["Excel files", "*.xlsx"]])

        # Verifica que ajustar_texto fue llamada correctamente
        mock_ajustar_texto.assert_called_once_with('seleccionado.xlsx', 15)

        # Verifica que el botón de archivo fue actualizado correctamente
        assert archivo_btn_mock.text == f"Archivo: {mock_ajustar_texto('seleccionado.xlsx', 15)}"

        # Verifica que la función info fue llamada correctamente
        mock_info.assert_called_once_with("Archivo seleccionado", f"Has seleccionado: {archivo}")

        # Verifica que la variable global archivo_seleccionado se actualizó correctamente
        from main import archivo_seleccionado
        assert archivo_seleccionado == archivo

        # Verifica que el resultado de la función es el archivo seleccionado
        assert resultado == archivo

# Prueba para la función cambiar_tema ---------------------- CHECK
@patch('main.guardar_ajustes')
@patch('main.mostrar_pantalla_principal')
@patch('main.aplicar_tema')
@patch('main.get_translation')
def test_cambiar_tema_oscuro(mock_get_translation, mock_aplicar_tema, mock_mostrar_pantalla, mock_guardar_ajustes):
    # Configurar los mocks
    mock_get_translation.side_effect = lambda textos, idioma, key: "Oscuro" if key == "oscuro" else key
    global tema_actual, textos, idioma_actual, temas, app
    tema_actual = "Oscuro"
    textos = {"es": {"oscuro": "Oscuro"}}
    idioma_actual = "es"
    temas = {"Oscuro": {"color_fondo": "#000000"}, "Claro": {"color_fondo": "#FFFFFF"}}
    app = MagicMock()

    with patch.dict('main.__dict__', {'temas': temas, 'app': app, 'tema_actual': tema_actual, 'textos': textos, 'idioma_actual': idioma_actual}):
        # Llamar a la función a probar
        cambiar_tema("Oscuro")

        # Verificar que tema_actual se actualizó correctamente
        assert tema_actual == "Oscuro"
        # Verificar que las funciones se llamaron correctamente
        mock_aplicar_tema.assert_called_once_with(temas["Oscuro"])
        mock_mostrar_pantalla.assert_called_once_with(app)
        mock_guardar_ajustes.assert_called_once_with("Tema", "Oscuro")


# Pruebas para la función guardar_ajustes ---------------------- CHECK
@pytest.fixture
def mock_open_file():
    with patch('builtins.open', mock_open()) as mock_file:
        yield mock_file

@pytest.fixture
def mock_os_path_exists():
    with patch('os.path.exists') as mock:
        yield mock

def test_guardar_ajustes_tema(mock_open_file, mock_os_path_exists):
    # Configurando el mock para que os.path.exists devuelva False
    mock_os_path_exists.return_value = False

    # Llamando a la función a testear
    guardar_ajustes("Tema", "Oscuro")

    # Verificando que se escribió correctamente en el archivo
    mock_open_file.assert_called_once_with("ajustes_guardados.txt", 'w')
    handle = mock_open_file()
    handle.writelines.assert_called_once_with(["Tema:Oscuro\n", "Idioma:"])

def test_guardar_ajustes_idioma(mock_open_file, mock_os_path_exists):
    # Configurando el mock para que os.path.exists devuelva False
    mock_os_path_exists.return_value = False

    # Llamando a la función a testear
    guardar_ajustes("Idioma", "Español")

    # Verificando que se escribió correctamente en el archivo
    mock_open_file.assert_called_once_with("ajustes_guardados.txt", 'w')
    handle = mock_open_file()
    handle.writelines.assert_called_once_with(["Tema:\n", "Idioma:Español"])


# Pruebas para la función cargar_ajustes ---------------------- CHECK
mock_file_content = """
Tema:Claro
Idioma:es
"""

def test_cargar_ajustes():
    temas = {
         "Claro": {
            "color_fondo": "#BDEAFA",
            "color_texto": "black",
            "color_titulos": "#31c816",
            "color_sidebar": "#fcef89",
            "musica_login": "audio/023 - The Forest of Hope.mp3",
            "musica_principal": "audio/009 - Impact Site.mp3",
            "colores_botones_sidebar": ["#fcef89", "#000000", "#fff5a4"],
            "colores_resultados": "white",
            "colores_fondos_resultados": ["#954C8D", "#646666", "#98F4F8", "#E9EBE7", "#3D88F5", "#E73734", "#F4D71C", "#80DF37", "#F681AF"],
            "fondo_login": "../imagenes/fondo_login.png",
            "fondo_inicio": "../imagenes/fondo_inicio.png",
            "fondo_ranking": "../imagenes/fondo_ranking.png",
            "fondo_realizar_salto": "../imagenes/fondo_realizar_salto.png",
            "fondo_configuracion": "../imagenes/fondo_configuracion.png",
            "fondos_resultados": ["../imagenes/fondos_resultados/4.png","../imagenes/fondos_resultados/5.png","../imagenes/fondos_resultados/6.png",
                                  "../imagenes/fondos_resultados/7.png","../imagenes/fondos_resultados/8.png","../imagenes/fondos_resultados/9.png",
                                  "../imagenes/fondos_resultados/10.png","../imagenes/fondos_resultados/11.png","../imagenes/fondos_resultados/12.png"]
        },
        "Oscuro": {
            "color_fondo": "#361057",
            "color_texto": "white",
            "color_titulos": "#31c816",
            "color_sidebar": "#1E1E1E",
            "colores_botones_sidebar": ["#1E1E1E", "#FFFFFF", "#555555"],
            "musica_login": "audio/025 - The Forest of Hope (Dawn).mp3",
            "musica_principal": "audio/020 - Impact Site (Dawn).mp3",
            "colores_resultados": ["#270F26", "#0F2327", "#0F2327", "#262829", "#100F27", "#27110F", "#27240F", "#14270F", "#270F21"],
            "colores_fondos_resultados": ["#5D254D", "#646666", "#6FCCD5", "#B9BFB2", "#1E56D6", "#C62321", "#D1B70E", "#61B222", "#DF6192"],
            "fondo_login": "../imagenes/fondo_login_osc.png",
            "fondo_inicio": "../imagenes/fondo_inicio_osc.png",
            "fondo_ranking": "../imagenes/fondo_ranking_osc.png",
            "fondo_realizar_salto": "../imagenes/fondo_realizar_salto_osc.png",
            "fondo_configuracion": "../imagenes/fondo_configuracion_osc.png",
            "fondos_resultados": ["../imagenes/fondos_resultados/17.png","../imagenes/fondos_resultados/18.png","../imagenes/fondos_resultados/19.png",
                                  "../imagenes/fondos_resultados/20.png","../imagenes/fondos_resultados/21.png","../imagenes/fondos_resultados/22.png",
                                  "../imagenes/fondos_resultados/23.png","../imagenes/fondos_resultados/24.png","../imagenes/fondos_resultados/25.png"]
        }
    }

    with patch("builtins.open", mock_open(read_data=mock_file_content)), \
         patch("os.path.exists", return_value=True):
        cargar_ajustes(temas)
        assert tema_actual == "Claro"
        assert idioma_actual == "es"

# Prueba para la función cambiar_volumen ---------------------- CHECK
def test_cambiar_volumen():
    # Valor de prueba para el volumen
    volumen = "75"

    # Parchea las funciones y la variable global
    with patch.dict('main.__dict__', {'volumen_actual': None}), \
         patch('main.pygame.mixer.music.set_volume') as mock_set_volume:

        # Llama a la función cambiar_volumen
        cambiar_volumen(volumen)

        # Verifica que la variable global volumen_actual se actualizó correctamente
        from main import volumen_actual
        assert volumen_actual == int(float(volumen))

        # Verifica que pygame.mixer.music.set_volume fue llamada correctamente
        mock_set_volume.assert_called_once_with(int(float(volumen)) / 100.0)

# Prueba para la función reproducir_musica ---------------------- CHECK
@patch('pygame.mixer.music.load')
@patch('pygame.mixer.music.play')
def test_reproducir_musica(mock_play, mock_load):
    # Parámetros de ejemplo para la prueba
    bucle = -1
    ruta = "test_audio.mp3"
    fadein_duration = 5000

    # Llamar a la función a probar
    reproducir_musica(bucle, ruta, fadein_duration)

    # Verificar que pygame.mixer.music.load se llamó correctamente
    mock_load.assert_called_once_with(ruta)

    # Verificar que pygame.mixer.music.play se llamó correctamente
    mock_play.assert_called_once_with(bucle, fade_ms=fadein_duration)

# Prueba para la función reproducir_sonido_boton ---------------------- CHECK
@patch('main.pygame.mixer.Sound')
@patch('main.CANAL_BOTONES')
def test_reproducir_sonido_boton(mock_CANAL_BOTONES, mock_Sound):
    # Configurar los mocks
    mock_sound_instance = MagicMock()
    mock_Sound.return_value = mock_sound_instance

    # Parámetros de ejemplo
    ruta = "test_sonido.mp3"

    # Asegurar el valor global para volumen_actual
    global volumen_actual
    volumen_actual = 20  # Valor de ejemplo para volumen_actual

    # Llamar a la función a probar
    reproducir_sonido_boton(ruta)

    # Verificar que pygame.mixer.Sound se llamó correctamente
    mock_Sound.assert_called_once_with(ruta)

    # Verificar que set_volume se llamó correctamente
    expected_volume = volumen_actual / 200
    mock_sound_instance.set_volume.assert_called_once_with(expected_volume)

    # Verificar que CANAL_BOTONES.play se llamó correctamente
    mock_CANAL_BOTONES.play.assert_called_once_with(mock_sound_instance)

# Prueba para la función cambiar_pista_despues_de_tiempo ---------------------- CHECK
@patch('main.threading.Timer')
@patch('main.reproducir_musica')
def test_cambiar_pista_despues_de_tiempo(mock_reproducir_musica, mock_Timer):
    # Configurar el mock de Timer
    mock_timer_instance = MagicMock()
    mock_Timer.return_value = mock_timer_instance

    # Parámetros de ejemplo para la prueba
    tiempo = 5
    siguiente_pista = "siguiente_pista.mp3"
    fadein_duration = 5000

    # Llamar a la función a probar
    cambiar_pista_despues_de_tiempo(tiempo, siguiente_pista, fadein_duration)

    # Verificar que threading.Timer se creó con los parámetros correctos
    mock_Timer.assert_called_once_with(tiempo, mock_reproducir_musica, args=(-1, siguiente_pista, fadein_duration))

    # Verificar que el temporizador se inició
    mock_timer_instance.start.assert_called_once()

# Prueba para la función detener_musica ---------------------- CHECK
@patch('main.pygame.mixer.music.fadeout')
def test_detener_musica(mock_fadeout):
    # Parámetro de ejemplo para la prueba
    fadeout_duration = 1500

    # Llamar a la función a probar
    detener_musica(fadeout_duration)

    # Verificar que pygame.mixer.music.fadeout se llamó correctamente
    mock_fadeout.assert_called_once_with(fadeout_duration)

# Prueba para la función cambiar_idioma ---------------------- CHECK
def test_cambiar_idioma():
    # Define el nuevo idioma
    nuevo_idioma = "es"

    # Crear un mock para app
    mock_app = MagicMock()

    # Parchea las funciones y la variable global
    with patch.dict('main.__dict__', {'idioma_actual': None, 'app': mock_app}), \
         patch('main.mostrar_pantalla_principal') as mock_mostrar_pantalla_principal:

        # Llama a la función cambiar_idioma
        cambiar_idioma(nuevo_idioma)

        # Verifica que la variable global idioma_actual se actualizó correctamente
        from main import idioma_actual
        assert idioma_actual == nuevo_idioma

        # Verifica que mostrar_pantalla_principal fue llamada correctamente
        mock_mostrar_pantalla_principal.assert_called_once_with(mock_app)

# Prueba para la función crear_imagen_texto ---------------------- CHECK
def test_crear_imagen_texto():
    # Valores de prueba
    texto = "Prueba"
    width = 200
    height = 100
    radio = 10
    color_fondo = "blue"
    color_texto = "white"
    ruta_fuente_titulos = None
    tamano_fuente_titulos = 16

    # Parchea los métodos de PIL
    with patch('main.Image.new') as mock_new, \
         patch('main.ImageDraw.Draw') as mock_draw, \
         patch('main.ImageFont.truetype') as mock_truetype, \
         patch('main.ImageFont.load_default') as mock_load_default, \
         patch('main.ImageTk.PhotoImage') as mock_photoimage:

        # Mocks de retorno
        mock_image = MagicMock()
        mock_draw_instance = MagicMock()
        mock_font = MagicMock()
        mock_bbox = (0, 0, 50, 20)

        mock_new.return_value = mock_image
        mock_draw.return_value = mock_draw_instance
        mock_load_default.return_value = mock_font
        mock_draw_instance.textbbox.return_value = mock_bbox
        mock_photoimage.return_value = MagicMock()

        # Llama a la función
        resultado = crear_imagen_texto(texto, width, height, radio, color_fondo, color_texto, ruta_fuente_titulos, tamano_fuente_titulos)

        # Verifica que se crean la imagen y el objeto draw
        mock_new.assert_called_once_with("RGBA", (width, height), (255, 255, 255, 0))
        mock_draw.assert_called_once_with(mock_image)

        # Verifica que se dibuja el rectángulo redondeado
        mock_draw_instance.rounded_rectangle.assert_called_once_with((0, 0, width, height), radius=radio, fill=color_fondo)

        # Verifica que se carga la fuente por defecto
        mock_load_default.assert_called_once()

        # Verifica que se calcula correctamente la posición del texto
        mock_draw_instance.text.assert_called_once_with((75.0, 26.666666666666668), texto, font=mock_font, fill=color_texto)

        # Verifica que se crea la imagen final
        mock_photoimage.assert_called_once_with(mock_image)

        # Verifica que el resultado es el esperado
        assert resultado == mock_photoimage.return_value

# Pruebas para la función guardar_datos ---------------------- CHECK
@patch('main.reproducir_sonido_boton')
@patch('main.send_data')
@patch('main.guardar_datos_locales')
@patch('main.messagebox.showinfo')
@patch('main.messagebox.showerror')
@patch('main.get_translation')
@patch('main.mostrar_pantalla_realizarSalto')
def test_guardar_datos_online_success(mock_mostrar, mock_get_translation, mock_showerror, mock_showinfo, mock_guardar_datos_locales, mock_send_data, mock_reproducir_sonido):
    # Configurar los mocks
    mock_send_data.return_value = True
    mock_get_translation.side_effect = lambda textos, idioma, key: key  # Devolver la clave como traducción
    datos = {"key": "value"}
    main_content = MagicMock()
    global modo, server, textos, idioma_actual
    modo = "Online"
    server = "mock_server"
    textos = {}
    idioma_actual = "es"

    # Llamar a la función a probar
    guardar_datos(datos, main_content)

    # Verificar que las funciones se llamaron correctamente
    mock_reproducir_sonido.assert_called_once_with("audio/buttons.mp3")
    mock_send_data.assert_called_once_with(server, datos)
    mock_showinfo.assert_called_once_with("Confimacion", "resultados_salto_si")
    mock_mostrar.assert_called_once_with(main_content)

# Pruebas para la función guardar_datos_locales ---------------------- CHECK
def test_guardar_datos_locales():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, "top_prueba.txt")

        # Crear el archivo con cabeceras previamente
        with open(file_path, 'w') as archivo:
            archivo.write("nombre,grupo_ProMu,altura,fecha\n")

        # Llamada a la función
        resultado = guardar_datos_locales(["pepe", "asd", "30", "02072025"], file_path)

        # Verificar el contenido del archivo
        with open(file_path, 'r') as archivo:
            lineas = archivo.readlines()
            assert lineas[0].strip() == "nombre,grupo_ProMu,altura,fecha"
            assert lineas[1].strip() == "pepe,asd,30,02072025"

# Pruebas para la función cargar_datos_locales ---------------------- CHECK
def test_cargar_datos_locales():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, "top_prueba.txt")

        with open(file_path, 'w') as archivo:
            archivo.write("nombre,grupo_ProMu,altura,fecha\n")
            archivo.write("asd,3asd,29,01062024\n")
            archivo.write("pepe,asd,30,02072025\n")
            archivo.write("maria,grupo1,28,03082026\n")

        datos_ordenados = cargar_datos_locales(file_path)

        assert len(datos_ordenados) == 3
        assert datos_ordenados[0]["nombre"] == "pepe"
        assert datos_ordenados[0]["altura"] == 30
        assert datos_ordenados[1]["nombre"] == "asd"
        assert datos_ordenados[1]["altura"] == 29
        assert datos_ordenados[2]["nombre"] == "maria"
        assert datos_ordenados[2]["altura"] == 28

@pytest.fixture
def setup_fields():
    app = MagicMock()
    userTxTBox = MagicMock()
    passTxTBox = MagicMock()
    return app, userTxTBox, passTxTBox

# Pruebas para la función enviar_datos_login ---------------------- CHECK
def test_enviar_datos_login_campos_vacios(setup_fields):
    app, userTxTBox, passTxTBox = setup_fields
    userTxTBox.value = ""
    passTxTBox.value = ""

    with patch('main.messagebox.showerror') as mock_showerror, \
         patch('main.get_translation', return_value="Obligatorio") as mock_get_translation:

        enviar_datos_login(app, userTxTBox, passTxTBox)

        mock_showerror.assert_called_once_with("Error", "Obligatorio")

def test_enviar_datos_login_servidor_no_conectado(setup_fields):
    app, userTxTBox, passTxTBox = setup_fields
    userTxTBox.value = "user"
    passTxTBox.value = "pass"

    with patch('main.messagebox.showerror') as mock_showerror, \
         patch('main.get_translation', return_value="LoginIncorrecto") as mock_get_translation, \
         patch('main.server', None), \
         patch('main.iniciar_conexion', return_value=None):

        enviar_datos_login(app, userTxTBox, passTxTBox)

        mock_showerror.assert_called_once_with("Error", "LoginIncorrecto")

def test_enviar_datos_login_exitoso(setup_fields):
    app, userTxTBox, passTxTBox = setup_fields
    userTxTBox.value = "user"
    passTxTBox.value = "pass"

    mock_server = MagicMock()

    with patch('main.messagebox.showerror') as mock_showerror, \
         patch('main.server', mock_server), \
         patch('main.login', return_value=True), \
         patch('main.mostrar_pantalla_principal') as mock_mostrar_pantalla_principal:

        enviar_datos_login(app, userTxTBox, passTxTBox)

        mock_showerror.assert_not_called()
        mock_mostrar_pantalla_principal.assert_called_once_with(app)
