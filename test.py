import RPi.GPIO as GPIO
from time import sleep

servo_pin = 35
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)
servo_pwm = GPIO.PWM(servo_pin, 50)
servo_pwm.start(0)

# Define los valores de ciclo de trabajo para el servo (correspondientes a los ángulos)
angle_20 = 2.5
angle_90 = 7.5
angle_120 = 12.5

def move_servo_smoothly(target_angle):
    current_angle = angle_90
    # Determina la dirección del movimiento
    if target_angle > current_angle:
        step = 0.1  # Paso más pequeño hacia la derecha
    else:
        step = -0.1  # Paso más pequeño hacia la izquierda

    while abs(current_angle - target_angle) > 0.1:  # Mientras la diferencia sea significativa
        servo_pwm.ChangeDutyCycle(current_angle)
        sleep(0.1)  # Puedes ajustar el tiempo de espera entre pasos según sea necesario
        current_angle += step

    # Ajusta a la posición final
    servo_pwm.ChangeDutyCycle(target_angle)

# Funciones para mover el servo a las posiciones específicas
def move_to_20_degrees():
    move_servo_smoothly(angle_20)

def move_to_90_degrees():
    move_servo_smoothly(angle_90)

def move_to_120_degrees():
    move_servo_smoothly(angle_120)

# Ejemplo de uso:
try:
    while True:
        # Espera la entrada del usuario
        user_input = input("Ingrese 'o' para ir a 120 grados, 'p' para ir a 90 grados, 'q' para ir a 20 grados: ")
        if user_input == 'o':
            move_to_120_degrees()
        elif user_input == 'p':
            move_to_90_degrees()
        elif user_input == 'q':
            move_to_20_degrees()
        else:
            print("Entrada no válida.")
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
