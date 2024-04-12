from gpiozero import AngularServo
from time import sleep

# Crea el servo motor con los pulsos mínimos y máximos ajustados para adaptarse a tu servo
servo = AngularServo(35, min_angle=-90, max_angle=90, min_pulse_width=0.0006, max_pulse_width=0.0023)

def move_to_90_degrees():
    servo.angle = 0

def move_to_120_degrees():
    servo.angle = 30

def move_to_20_degrees():
    servo.angle = -70

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
    servo.detach()  # Libera los recursos del servo al finalizar
