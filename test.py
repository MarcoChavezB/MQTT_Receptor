import RPi.GPIO as GPIO
from time import sleep

# Configura el número del pin GPIO que estás utilizando para controlar el motor
motor_pin = 18

# Configura el modo de los pines GPIO
GPIO.setmode(GPIO.BOARD)
# Configura el pin GPIO como salida
GPIO.setup(motor_pin, GPIO.OUT)

try:
    # Gira el motor en una dirección
    print("Girando el motor en una dirección")
    GPIO.output(motor_pin, GPIO.HIGH)  # Enciende el motor
    sleep(2)  # Espera 2 segundos
    # Detiene el motor
    print("Deteniendo el motor")
    GPIO.output(motor_pin, GPIO.LOW)  # Apaga el motor

finally:
    # Limpia los pines GPIO y restablece cualquier configuración previa
    GPIO.cleanup()
