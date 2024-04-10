import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import messagebox
2
# Función para detectar monedas en un frame y devolver sus coordenadas y dimensiones
def detectar_monedas(frame):
  # Convertir a escala de grises
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  # Desenfocar la imagen
  blurred = cv2.GaussianBlur(gray, (9, 9), 0)

  # Detectar bordes con Canny
  edges = cv2.Canny(blurred, 50, 150)

  # Detección de contornos
  contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # Lista para almacenar las coordenadas y dimensiones de las monedas
  coordenadas_monedas = []

  for contour in contours:
    area = cv2.contourArea(contour)
    perimetro = cv2.arcLength(contour, True)
    
    # Verificar si el perímetro es mayor que cero antes de calcular la circularidad
    if perimetro > 0:
      circularidad = 4 * np.pi * area / (perimetro * perimetro)

      # Si el contorno es suficientemente circular, consideramos que es una moneda
      if circularidad > 0.5:
        # Encontrar el rectángulo delimitador de la moneda
        x, y, w, h = cv2.boundingRect(contour)
        coordenadas_monedas.append((x, y, w, h))

  return coordenadas_monedas

# Función para clasificar las monedas según su diámetro
def clasificar_monedas(coordenadas_monedas, diametro_max_10, diametro_min_10, diametro_max_1, diametro_min_1):
  clasificaciones = []

  for x, y, w, h in coordenadas_monedas:
    # Calcular el diámetro de la moneda
    diametro = max(w, h)

    # Comparar el diámetro con los rangos establecidos para cada tipo de moneda
    if diametro_min_10 <= diametro <= diametro_max_10:
      clasificacion = "MONEDA_DE_10"
    elif diametro_min_5 <= diametro <= diametro_max_5:
      clasificacion = "MONEDA_DE_5"
    elif diametro_min_2 <= diametro <= diametro_max_2:
      clasificacion = "MONEDA_DE_2"
    elif diametro_min_1 <= diametro <= diametro_max_1:
      clasificacion = "MONEDA_DE_1"
    # elif diametro_min_50 <= diametro <= diametro_max_50:
    #   clasificacion = "MONEDA_DE_0.50"
    elif diametro_min_50pl <= diametro <= diametro_max_50pl:
      clasificacion = "MONEDA_DE_0.50"
    else:
      clasificacion = "NO_IDENTIFICADA"
      
    clasificaciones.append((x, y, w, h, diametro, clasificacion))

  return clasificaciones

def obtener_diametros_min_max(directorio):
  diametros = []

  # Recorrer todas las imágenes en el directorio
  for filename in os.listdir(directorio):
    # Obtener la ruta completa de la imagen
    ruta_imagen = os.path.join(directorio, filename)
    
    # Cargar la imagen
    img = cv2.imread(ruta_imagen)
    
    # Detectar monedas en la imagen
    coordenadas_monedas = detectar_monedas(img)
    
    # Obtener el diámetro de las monedas
    for x, y, w, h in coordenadas_monedas:
      # Calcular el diámetro (el máximo de la anchura y la altura)
      diametro = max(w, h)
      # Agregar el diámetro a la lista
      diametros.append(diametro)
  
  # Calcular el diámetro máximo y mínimo
  diametro_max = max(diametros)
  diametro_min = min(diametros)
  
  return diametro_max, diametro_min

# Inicializacion de variable camera_index
#camera_index = None
#print("Cámara seleccionada:", camera_index)

# Variable global para indicar si se ha tomado la foto
foto_tomada = False

# Función para seleccionar la cámara usando tkinter
#def seleccionar_camara():
    
  #def seleccionar_cam():
    #global camera_index
    #camera_index = var.get()
    #root.destroy()
      
  #root = tk.Tk()
  #root.title("Selección de cámara")

  #label = tk.Label(root, text="Seleccione la cámara:")
  #label.pack()

  #var = tk.IntVar()
  #var.set(0)

  #for i in range(5):  # Probamos hasta 5 cámaras
    #btn = tk.Radiobutton(root, text=f"Cámara {i}", variable=var, value=i)
    #btn.pack()

  #confirm_btn = tk.Button(root, text="Seleccionar", command=seleccionar_cam)
  #confirm_btn.pack()

  #root.mainloop()

current_path = os.getcwd()  # Get the current working directory
direccion = os.path.join(current_path, "img", "Validacion", "Moneda_Mexicana")
name_template = "moneda_Mexicana_"

# Carpeta con las imágenes de validación de monedas de 10 pesos
imagenes_validacion_10_dir = os.path.join(direccion, f"{name_template}10") # Falta cambiar rutas

# Carpeta con las imágenes de validación de monedas de 5 peso
imagenes_validacion_5_dir = os.path.join(direccion, f"{name_template}5")

# Carpeta con las imágenes de validación de monedas de 3 peso
imagenes_validacion_2_dir = os.path.join(direccion, f"{name_template}2")

# Carpeta con las imágenes de validación de monedas de 1 peso
imagenes_validacion_1_dir = os.path.join(direccion, f"{name_template}1")

# Carpeta con las imágenes de validación de monedas de 50 cent
# imagenes_validacion_50_dir = os.path.join(direccion, f"{name_template}50")

# Carpeta con las imágenes de validación de monedas de 50 cent pl
imagenes_validacion_50pl_dir = os.path.join(direccion, f"{name_template}50_pl")

# Obtener el diámetro máximo y mínimo de las monedas de 10 pesos
diametro_max_10, diametro_min_10 = obtener_diametros_min_max(imagenes_validacion_10_dir)
#print("Diametro máximo de monedas de 10 pesos:", diametro_max_10)
#print("Diametro mínimo de monedas de 10 pesos:", diametro_min_10)

# Obtener el diámetro máximo y mínimo de las monedas de 5 peso
diametro_max_5, diametro_min_5 = obtener_diametros_min_max(imagenes_validacion_5_dir)
#print("Diametro máximo de monedas de 5 peso:", diametro_max_5)
#print("Diametro mínimo de monedas de 5 peso:", diametro_min_5)

# Obtener el diámetro máximo y mínimo de las monedas de 2 peso
diametro_max_2, diametro_min_2 = obtener_diametros_min_max(imagenes_validacion_2_dir)
#print("Diametro máximo de monedas de 2 peso:", diametro_max_2)
#print("Diametro mínimo de monedas de 2 peso:", diametro_min_2)

# Obtener el diámetro máximo y mínimo de las monedas de 1 peso
diametro_max_1, diametro_min_1 = obtener_diametros_min_max(imagenes_validacion_1_dir)
#print("Diametro máximo de monedas de 1 peso:", diametro_max_1)
#print("Diametro mínimo de monedas de 1 peso:", diametro_min_1)

# Obtener el diámetro máximo y mínimo de las monedas de 50 centavos
# diametro_max_50, diametro_min_50 = obtener_diametros_min_max(imagenes_validacion_50_dir)
#print("Diametro máximo de monedas de 50 cent:", diametro_max_1)
#print("Diametro mínimo de monedas de 50 cent:", diametro_min_1)

# Obtener el diámetro máximo y mínimo de las monedas de 50 centavos plateada
diametro_max_50pl, diametro_min_50pl = obtener_diametros_min_max(imagenes_validacion_50pl_dir)
#print("Diametro máximo de monedas de 50 cent pl", diametro_max_50pl)
#print("Diametro mínimo de monedas de 50 cent pl:", diametro_min_50pl)

def tomar_foto():
  global foto_tomada
  # Capturar un fotograma de la cámara seleccionada
  ret, frame = cap.read()
  if ret:
    # Guardar la imagen capturada
    cv2.imwrite("foto.jpg", frame)
    messagebox.showinfo("Foto tomada", "Se ha guardado la foto como 'foto.jpg'")
        

# Ruta de la foto tomada
imagen_path = "foto.jpg"

def procesar_foto(imagen_path):
  # Cargar la imagen
  frame = cv2.imread(imagen_path)

  # Detectar monedas en la foto
  coordenadas_monedas = detectar_monedas(frame)

  # Clasificar las monedas según su diámetro y los rangos establecidos
  clasificaciones = clasificar_monedas(coordenadas_monedas, diametro_max_10, diametro_min_10, diametro_max_1, diametro_min_1)

  # Variable para almacenar la suma de los valores de todas las monedas
  suma_valores = 0

  # Iterar sobre las clasificaciones y dibujar cuadros y texto en el frame
  for x, y, w, h, diametro, clasificacion in clasificaciones:
    # Calcular el valor de la moneda
    if clasificacion == "MONEDA_DE_10":
      valor = 10
    elif clasificacion == "MONEDA_DE_5":
      valor = 5
    elif clasificacion == "MONEDA_DE_2":
      valor = 2
    elif clasificacion == "MONEDA_DE_1":
      valor = 1
    elif clasificacion == "MONEDA_DE_0.50":
      valor = 0.50
    else:
      valor = 0  # Para monedas no identificadas, el valor es cero
    
    # Sumar el valor de la moneda a la suma total
    suma_valores += valor

    # Dibujar un cuadro alrededor de la moneda
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Mostrar la clasificación (tipo de moneda) y el valor sobre el cuadro
    cv2.putText(frame, f"{clasificacion} - Valor: {valor}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

  # Mostrar la suma de los valores en la parte superior de la pantalla
  cv2.putText(frame, f"Suma de valores: {suma_valores}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
  
  # Mostrar el frame con las monedas detectadas y clasificadas
  cv2.imshow("Monedas", frame)
  cv2.waitKey(0)  # Esperar hasta que se presione una tecla para cerrar la ventana
  cv2.destroyAllWindows()



# Interfaz de usuario para seleccionar la cámara
#seleccionar_camara()
camera_index = 1

print("Camara seleccionada",camera_index)
# Captura de la cámara seleccionada
cap = cv2.VideoCapture(camera_index)

# Mientras se está capturando video
while True:
  ret, frame = cap.read()

  if not ret:
    break

  # Detectar monedas en el fotograma actual
  coordenadas_monedas = detectar_monedas(frame)

  # Clasificar las monedas según su diámetro y los rangos establecidos
  clasificaciones = clasificar_monedas(coordenadas_monedas, diametro_max_10, diametro_min_10, diametro_max_1, diametro_min_1)

  # Iterar sobre las clasificaciones y dibujar cuadros y texto en el frame
  for x, y, w, h, diametro, clasificacion in clasificaciones:
    # Dibujar un cuadro alrededor de la moneda
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Mostrar la clasificación (tipo de moneda) sobre el cuadro
    cv2.putText(frame, f"{clasificacion}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

  # Mostrar el frame con las monedas detectadas y clasificadas
  cv2.imshow("Monedas", frame)

  # Salir del bucle si se presiona la tecla 'q'
  if cv2.waitKey(1) & 0xFF == ord('q'):
    tomar_foto()
    procesar_foto(imagen_path)
    break

# Liberar la captura de video y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()