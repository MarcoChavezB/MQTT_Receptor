import RPi.GPIO as GPIO
from time import sleep

camera_pin = 35
GPIO.setmode(GPIO.BOARD)
GPIO.setup(camera_pin, GPIO.OUT)
camera_pwm = GPIO.PWM(camera_pin, 50)
camera_pwm.start(0)

# Define los valores de ciclo de trabajo para la cámara (más bajos para un movimiento más lento)
camera_neutral = 7.5
camera_max_right = 12
camera_max_left = 2.5

def move_camera_smoothly(target_position):
    current_position = camera_neutral
    while abs(current_position - target_position) > 0.05:  # Mientras la diferencia sea significativa
        camera_pwm.ChangeDutyCycle(current_position)
        sleep(0.05)  # Puedes ajustar el tiempo de espera entre pasos según sea necesario


    camera_pwm.ChangeDutyCycle(target_position)


try:
    # Mueve la cámara hacia la derecha
    move_camera_smoothly(camera_max_right)
    sleep(2)  # Espera 2 segundos
    # Mueve la cámara hacia la izquierda
    move_camera_smoothly(camera_max_left)
    sleep(2)  # Espera 2 segundos
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
