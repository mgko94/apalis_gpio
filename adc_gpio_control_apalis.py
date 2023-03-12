import gpiod
import sys

CHIP0='gpiochip0'
CHIP4='gpiochip4'
BUSY_LINE_OFFSET = 8
CONVST_LINE_OFFSET = 12
RESET_LINE_OFFSET = 1


chip0 = gpiod.chip(CHIP0)
pin_busy_pin = chip0.get_line(BUSY_LINE_OFFSET)
pin_convst_pin = chip0.get_line(CONVST_LINE_OFFSET)

chip4 = gpiod.chip(CHIP4)
pin_reset_pin = chip4.get_line(RESET_LINE_OFFSET)


def pin_init():
    config = gpiod.line_request()
    config.consumer = "adc7616_busy"
    config.request_type = gpiod.line_request.DIRECTION_INPUT
    pin_busy_pin.request(config)

    config.consumer = "adc7616_convst"
    config.request_type = gpiod.line_request.DIRECTION_OUTPUT    
    pin_convst_pin.request(config)

    config.consumer = "adc7616_reset"
    config.request_type = gpiod.line_request.DIRECTION_OUTPUT     
    pin_reset_pin.request(config)

    
def pin_deinit():
    pass

def setpin_reset(state):
    if(state):
        pin_reset_pin.set_value(1)
    else:
        pin_reset_pin.set_value(0)

def setpin_convst(state):
    if(state):
        pin_convst_pin.set_value(1)
    else:
        pin_convst_pin.set_value(0)
    
def getpin_busy():
    return pin_busy_pin.get_value()

