#!/usr/bin/env python
from samplebase import SampleBase
from smbus2 import SMBus, i2c_msg
import os
import time
# I2C address of the sensor
address = 0x18 

MAXIMUM_PSI = 25
MINIMUM_PSI = 0
OUTPUT_MAX = 0xE66666
OUTPUT_MIN = 0x19999A
bus = SMBus(1) 
c = 32
red = graphics.Color(255, 0, 0)

def grass(self):
    for x in range (0, 32):
        for y in range (0, 4):
            self.matrix.SetPixel(x, y, 55, 148, 4)

def bird(self, y_dist):
    self.matrix.SetPixel(c - 2, c - y_dist + 1, 213, 195, 0) # body
    self.matrix.SetPixel(c - 2, c - y_dist + 2, 213, 195, 0) # body
    self.matrix.SetPixel(c - 3, c - y_dist + 1, 213, 195, 0) # body
    self.matrix.SetPixel(c - 3, c - y_dist + 2, 213, 195, 0) # body
    self.matrix.SetPixel(c - 4, c - y_dist + 1, 255, 77, 68) # beak
    self.matrix.SetPixel(c - 5, c - y_dist + 1, 255, 77, 68) # beak
    self.matrix.SetPixel(c - 3, c - y_dist, 246, 131, 11) # foot
    self.matrix.SetPixel(c - 4, c - y_dist + 2, 227, 253, 218) # eye
    bird_x = [c-2, c-3, c-4, c-5]
    bird_y = [c-y_dist, c-y_dist+1, c-y_dist+2, c-y_dist+3]
    return bird_x, bird_y

def pipe(self, x_pos, length):
    pipe_x = []
    pipe_y = []
    for x in range (x_pos, x_pos + 5):
        pipe_x.append(x)
        for y in range (4, 4 + length):
            # only append to pipe_y once
            if (x == x_pos):
                pipe_y.append(y)
            self.matrix.SetPixel(x, y, 55, 195, 0)
        
    return pipe_x, pipe_y

def check(self, b_x, b_y, p_x, p_y, t_p_x, t_p_y):
    for i in b_x:
        for j in p_x:
            # if any x in bird corresponds with pipe x
            if i == j:
                for j in b_y:
                    for k in p_y:
                        # hit bottom pipe
                        if j == k:
                            return True
        for l in t_p_x:
            if i == l:
                for j in b_y:
                    for p in t_p_y:
                        # hit top pipe
                        if j == p:
                            return True
    return False



def top_pipe(self, x_pos, length):
    top_pipe_x = []
    top_pipe_y = []
    for x in range (x_pos, x_pos + 5):
        top_pipe_x.append(x)
        for y in range (c - length, c):
            if (x == x_pos):
                top_pipe_y.append(y)
            self.matrix.SetPixel(x, y, 55, 195, 0)
    return top_pipe_x, top_pipe_y

class GrayscaleBlock(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GrayscaleBlock, self).__init__(*args, **kwargs)

    def run(self):
        max_brightness = self.matrix.brightness # set to 100
        count = 0
        c = 255
        self.matrix.brightness = 75
        x_pos = 0
        top_x_pos = 16
        while (True):
            time.sleep(0.1)
            write = i2c_msg.write(address, [0xAA,0x00,0x00])
            read = i2c_msg.read(address, 4)
            bus.i2c_rdwr(write, read)
            data = list(read)
            reading = data[1] << 16 | data[2] << 8 | data[3]
            pressure = (reading - OUTPUT_MIN) * (MAXIMUM_PSI - MINIMUM_PSI)
            pressure = (pressure / (OUTPUT_MAX - OUTPUT_MIN)) + MINIMUM_PSI
            #print("Pressure:", pressure)

            percent = ((pressure - 6)/19)
            #print("Percent:", percent * 100)

            y_dist = int(32 * (1-percent))
            #print(y_dist)
            if y_dist < 3:
                y_dist = 3
            if y_dist > 28:
                y_dist = 28

            
            self.matrix.Fill(63, 108 , 113)
            
            x_pos += 2
            top_x_pos += 1

            if x_pos > 31:
                x_pos = -4
            if top_x_pos > 31:
                top_x_pos = -4

            pipe_x, pipe_y = pipe(self, x_pos, 9)
            top_pipe_x, top_pipe_y = top_pipe(self, top_x_pos, 9)
            bird_x, bird_y = bird(self, y_dist)
            grass(self)
            if check(self, bird_x, bird_y, pipe_x, pipe_y, top_pipe_x, top_pipe_y):
                os.system("python /home/pi/Documents/Art_Embedded_Project/RGB/rpi-rgb-led-matrix/bindings/python/samples/runtext.py ")
                time.sleep(5)


# Main function
if __name__ == "__main__":
    grayscale_block = GrayscaleBlock()
    if (not grayscale_block.process()):
        grayscale_block.print_help()
