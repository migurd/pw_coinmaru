import cv2
import os
import numpy as np

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

  # Iterar sobre los contornos encontrados
  for contour in contours:
    area = cv2.contourArea(contour)
    perimetro = cv2.arcLength(contour, True)
    circularidad = 4 * np.pi * area / (perimetro * perimetro)

    # Si el contorno es suficientemente circular, consideramos que es una moneda
    if circularidad > 0.5:
      # Encontrar el rectángulo delimitador de la moneda
      x, y, w, h = cv2.boundingRect(contour)
      coordenadas_monedas.append((x, y, w, h))

  return coordenadas_monedas

# Función para capturar imágenes de monedas y guardarlas en la carpeta de validación
def capturar_imagenes():
  # Carpeta donde se almacenarán las imágenes de validación de monedas mexicanas de 10 pesos
  nombre = "moneda_Mexicana_50_pl"
  current_path = os.getcwd()  # Get the current working directory
  direccion = os.path.join(current_path, "img", "Validacion", "Moneda_Mexicana")
  carpeta = os.path.join(direccion, nombre)

  if not os.path.exists(carpeta):
    print("Carpeta creada:", carpeta)
    os.makedirs(carpeta)

  # Captura de la cámara
  camera_index = 1
  cap = cv2.VideoCapture(camera_index)

  # Configurar el tamaño del fotograma capturado
  #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 754)  # Ancho de 754 píxeles
  #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 644)  # Alto de 644 píxeles

  # Contador para las imágenes de monedas
  cont = 0

  # Mientras se está capturando video
  while True:
    ret, frame = cap.read()
    if not ret:
      break

    # Detectar monedas en el fotograma actual
    coordenadas_monedas = detectar_monedas(frame)

    # Si se encontraron monedas
    if coordenadas_monedas:
      for x, y, w, h in coordenadas_monedas:
        # Calcular el diámetro de la moneda
        diametro = max(w, h)

        # Mostrar el diámetro en el centro del rectángulo delimitador
        #cv2.putText(frame, f"Diametro: {diametro}", (x + w // 2 - 50, y + h // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Guardar la imagen de la moneda en la carpeta de validación
        cv2.imwrite(os.path.join(carpeta, f"moneda_{cont}.jpg"), frame)
        cont += 1

        # Mostrar el frame con un cuadro para indicar que se está capturando
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Mostrar el frame con las monedas detectadas
    cv2.imshow("Capturando", frame)

    # Salir del bucle si se presiona la tecla 'q' o se alcanza un cierto número de imágenes capturadas
    if cv2.waitKey(1) & 0xFF == ord('q') or cont >= 300:
      break

  # Liberar la captura de video y cerrar todas las ventanas
  cap.release()
  cv2.destroyAllWindows()

# Capturar imágenes de las monedas
capturar_imagenes()