import time
import spidev
# import adc_gpio_control_rpi as adcio
import adc_gpio_control_apalis as adcio

AD7616_REG_CONFIG         = 0x02
AD7616_REG_CHANNEL        = 0x03
AD7616_REG_INPUT_RANGE_A1 = 0x04
AD7616_REG_INPUT_RANGE_A2 = 0x05
AD7616_REG_INPUT_RANGE_B1 = 0x06
AD7616_REG_INPUT_RANGE_B2 = 0x07

AD7616_SDEF     = (1 << 7)
AD7616_BURSTEN  = (1 << 6)
AD7616_SEQEN    = (1 << 5)
def AD7616_OS(x):
    return (((x) & 0x7) << 2)
AD7616_STATUSEN = (1 << 1)
AD7616_CRCEN    = (1 << 0)

AD7616_2V5 = 1
AD7616_5V  = 2
AD7616_10V = 3

adc_ch_range = [
    [
        AD7616_10V, AD7616_10V, AD7616_10V, AD7616_10V,
        AD7616_10V, AD7616_10V, AD7616_10V, AD7616_10V
    ],
    [
        AD7616_10V, AD7616_10V, AD7616_10V, AD7616_10V,
        AD7616_10V, AD7616_10V, AD7616_10V, AD7616_10V
    ]
]

def AD7616_INPUT_RANGE(ch, x):
    return (((x) & 0x3) << (((ch) & 0x3) * 2))

class AD7616:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)              # open(bus, device)
        self.spi.mode = 3
        self.spi.max_speed_hz = 1000000  # set transfer speed
        adcio.pin_init()
        self.reset()
        
        adcio.setpin_convst(True)
        time.sleep(0.000001)
        adcio.setpin_convst(False)
        
        self.set_mode()
        self.set_oversampling_ratio(osr = 0)
        
        print("AD7616 initialized!")
        
        
    def deinit(self):
        self.spi.close()
        adcio.pin_deinit()
        
    def reset(self):
        adcio.setpin_reset(False)
        time.sleep(0.000001)
        adcio.setpin_reset(True)
        time.sleep(0.02)
        
    def set_range(self, ch=[0,0], ch_range=AD7616_10V):
        adc_ch_range[ch[0]][ch[1]] = ch_range
        
        if(ch[0] == 0):
            if(ch[1] < 4):
                reg_addr = AD7616_REG_INPUT_RANGE_A1
                mask = AD7616_INPUT_RANGE(ch[1], AD7616_10V);
                data = AD7616_INPUT_RANGE(ch[1], ch_range);
            else:
                reg_addr = AD7616_REG_INPUT_RANGE_A2
                mask = AD7616_INPUT_RANGE(ch[1]-4, AD7616_10V);
                data = AD7616_INPUT_RANGE(ch[1]-4, ch_range);
        else:
            if(ch[1] < 4):
                reg_addr = AD7616_REG_INPUT_RANGE_B1
                mask = AD7616_INPUT_RANGE(ch[1], AD7616_10V);
                data = AD7616_INPUT_RANGE(ch[1], ch_range);
                
            else:
                reg_addr = AD7616_REG_INPUT_RANGE_B2
                mask = AD7616_INPUT_RANGE(ch[1]-4, AD7616_10V);
                data = AD7616_INPUT_RANGE(ch[1]-4, ch_range);
                
        self.write_mask(reg_addr, mask, data)
        
    def set_mode(self):
        for i in range(8):
            self.set_range([0,i], adc_ch_range[0][i])
            self.set_range([1,i], adc_ch_range[1][i])
    
    def set_oversampling_ratio(self, osr = 0):
        self.write_mask(AD7616_REG_CONFIG, AD7616_OS(0x7), AD7616_OS(osr));
        
    def get_adc_value(self):
        adcio.setpin_convst(True)
        time.sleep(0.000001)
        adcio.setpin_convst(False)
        
        buf16_mo = 0x0000
        
        while(adcio.getpin_busy()):
            pass
        buf_mo = [((buf16_mo & 0xFF00) >> 8), (buf16_mo & 0xFF)]
        value_h, value_l = self.spi.xfer2(buf_mo)
        
        return (value_h<<8)+value_l
    
    def get_adc_value_2ch(self):
        adcio.setpin_convst(True)
        time.sleep(0.000001)
        adcio.setpin_convst(False)
        
        buf16_mo = 0x0000
        
        while(adcio.getpin_busy()):
            pass
        buf_mo = [((buf16_mo & 0xFF00) >> 8), (buf16_mo & 0xFF), 0x00, 0x00]
        value_a_h, value_a_l ,value_b_h, value_b_l = self.spi.xfer2(buf_mo)
        
        return [(value_a_h<<8)+value_a_l, (value_b_h<<8)+value_b_l]
        
    def spi_read(self, reg_addr):
        buf16_mo = 0x0000 | ((reg_addr & 0x3F) << 9)
        
        while(adcio.getpin_busy()):
            pass
        buf_mo = [((buf16_mo & 0xFF00) >> 8), (buf16_mo & 0xFF)]
        self.spi.xfer2(buf_mo) #dummy read
        
        buf16_mo = 0x0000 | ((reg_addr & 0x3F) << 9)
        
        while(adcio.getpin_busy()):
            pass
        buf_mo = [((buf16_mo & 0xFF00) >> 8), (buf16_mo & 0xFF)]
        buf16_mi = self.spi.xfer2(buf_mo)
        
        return buf16_mi
        
    def spi_write(self, reg_addr, reg_data):
        buf16_mo = 0x8000 | ((reg_addr & 0x3F) << 9) | (reg_data & 0x1FF)
        
        while(adcio.getpin_busy()):
            pass
        buf_mo = [((buf16_mo & 0xFF00) >> 8), (buf16_mo & 0xFF)]        
        self.spi.xfer2(buf_mo)
        
        #print("buf16_mo :", hex(buf16_mo))
        
        
    def write_mask(self, reg_addr, mask, data):
        reg_data_8 = self.spi_read(reg_addr)
        
        reg_data = (reg_data_8[0] << 8) + reg_data_8[1]
        reg_data &= ~mask
        reg_data |= data
        
        self.spi_write(reg_addr, reg_data);
        
    
    
