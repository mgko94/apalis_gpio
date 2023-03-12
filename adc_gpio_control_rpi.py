import RPi.GPIO as GPIO

pin_busy = 33
pin_convst = 35
pin_reset = 37

def pin_init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin_convst, GPIO.OUT)
    GPIO.setup(pin_busy, GPIO.IN)
    GPIO.setup(pin_reset, GPIO.OUT)
    
def pin_deinit():
    GPIO.cleanup()

def setpin_reset(state):
    if(state):
        GPIO.output(pin_reset, GPIO.HIGH)
    else:
        GPIO.output(pin_reset, GPIO.LOW)

def setpin_convst(state):
    if(state):
        GPIO.output(pin_convst, GPIO.HIGH)
    else:
        GPIO.output(pin_convst, GPIO.LOW)
    
def getpin_busy():
    return GPIO.input(pin_busy)

