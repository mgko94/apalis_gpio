import time
import adc_ad7616

adc = adc_ad7616.AD7616()

adc.spi_write(0x03, 0x00)
adc.get_adc_value() # after change the ch, first data is pravious ch's data
#print("adc data : ", adc_value)

adc_value = adc.get_adc_value_2ch()
print("adc data :", adc_value) # 3.3v, float

adc.deinit()