import RPi.GPIO as GPIO
from time import sleep

## agregar el número de pin BOARD del servo ##
servo_pin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)

pwm=GPIO.PWM(servo_pin, 50)
pwm.start(0)

## editar estos valores de ciclo de trabajo % ##
adelante = 2.5
neutro = 7.5
atras = 12
#### Fin de la edición ####

print("Comenzando la prueba")

print("Ciclo de trabajo", adelante,"% en la izquierda -90 grados")
pwm.ChangeDutyCycle(adelante)
sleep(1)

print("Ciclo de trabajo", neutro,"% en 0 grados")
pwm.ChangeDutyCycle(neutro)
sleep(1)

print("Ciclo de trabajo", atras, "% a la derecha +90 grados")
pwm.ChangeDutyCycle(atras)
sleep(1)

print("Fin de la prueba")

pwm.stop()
GPIO.cleanup()
