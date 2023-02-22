import os

adc = os.popen('cat /dev/apalis-adc0').read()

print(adc)