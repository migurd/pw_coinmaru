import cv2
import numpy as np

# Índice de la cámara que deseas utilizar (cambiar según sea necesario)
camera_index = 1

# Inicializar la cámara
cap = cv2.VideoCapture(camera_index)

while True:
  # Capturar fotograma por fotograma
  ret, frame = cap.read()
  if not ret:
    break
  
  image = frame.copy()
  copia = image

  # Convertir a escala de grises
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Desenfocar la imagen
  image = cv2.GaussianBlur(image, (9, 9), 0)

  # Detectar bordes
  image = cv2.Canny(image, 50, 150)

  # Detección de contornos
  (contornos, jerarquia) = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # Dibujar contornos
  copia = cv2.drawContours(copia, contornos, -1, (255, 0, 0), 2)

  # Dibujar contornos circulares
  for contorno in contornos:
    area = cv2.contourArea(contorno)
    perimetro = cv2.arcLength(contorno, True)
    circularidad = 4 * np.pi * area / (perimetro * perimetro)

    if circularidad > 0.5:  # Umbral para considerar el contorno como circular
      (x, y), radius = cv2.minEnclosingCircle(contorno)
      center = (int(x), int(y))
      radius = int(radius)
      diameter = 2 * radius

      # Dibujar círculo y centroide
      cv2.circle(copia, center, radius, (0, 255, 0), 2)
      cv2.circle(copia, center, 3, (0, 0, 255), -1)

      # Mostrar diámetro junto al centroide
      cv2.putText(copia, f'{diameter} px', (center[0] + 10, center[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

      # Dibujar cuadro alrededor del círculo
      cv2.rectangle(copia, (int(x - radius), int(y - radius)), (int(x + radius), int(y + radius)), (0, 255, 0), 2)

      # Mostrar diámetro encima del cuadro
      cv2.putText(copia, f'{diameter} px', (int(x - radius), int(y - radius) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

  # Mostrar el resultado en tiempo real
  cv2.imshow("resultado", copia)

  # Salir del bucle si se presiona la tecla 'q'
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# Liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()