from signal import signal, SIGTERM, SIGHUP, pause
from gpiozero import MCP3002, Motor

adc = (MCP3002(0), MCP3002(1))
fan = Motor(16, 20)

def safe_exit(signum, frame):
    exit(1)

def run_fan():
    while True:
        yield adc[0].value*2-1

try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    fan.source = run_fan()
    pause()
except KeyboardInterrupt:
    pass

finally:
    fan.source = None
    fan.close()
    adc[0].close()
    adc[1].close()