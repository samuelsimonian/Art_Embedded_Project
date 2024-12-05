#!/usr/bin/env python
from samplebase import SampleBase
from smbus2 import SMBus, i2c_msg
import time
from rgbmatrix import graphics
import random

# I2C address of the sensor
address = 0x18 

MAXIMUM_PSI = 25
MINIMUM_PSI = 0
OUTPUT_MAX = 0xE66666
OUTPUT_MIN = 0x19999A
bus = SMBus(1) 
c = 0

def grass(self):
    for x in range (0, 32):
        for y in range (28, 32):
            self.matrix.SetPixel(x, y, 55, 148, 4)

def bird(self, y_dist):
    self.matrix.SetPixel(1, y_dist + 1, 213, 195, 0) # body
    self.matrix.SetPixel(1, y_dist , 213, 195, 0) # body
    self.matrix.SetPixel(2, y_dist + 1, 213, 195, 0) # body
    self.matrix.SetPixel(2, y_dist , 213, 195, 0) # body
    self.matrix.SetPixel(3, y_dist + 1, 255, 77, 68) # beak
    self.matrix.SetPixel(4, y_dist + 1, 255, 77, 68) # beak
    self.matrix.SetPixel(2, y_dist + 2, 246, 131, 11) # foot
    self.matrix.SetPixel(3, y_dist , 227, 253, 218) # eye
    bird_x = [1, 2, 3, 4]
    bird_y = [y_dist, y_dist+1, y_dist+2]
    return bird_x, bird_y

def pipe(self, x_pos, length):
    pipe_x = []
    pipe_y = []
    for x in range (x_pos, x_pos + 5):
        pipe_x.append(x)
        for y in range (28 - length,28):
            # only append to pipe_y once
            if (x == x_pos):
                pipe_y.append(y)
            self.matrix.SetPixel(x, y, 55, 195, 0)
        
    return pipe_x, pipe_y


def top_pipe(self, x_pos, length):
    top_pipe_x = []
    top_pipe_y = []
    for x in range (x_pos, x_pos + 5):
        top_pipe_x.append(x)
        for y in range (0, length):
            if (x == x_pos):
                top_pipe_y.append(y)
            self.matrix.SetPixel(x, y, 55, 195, 0)
    return top_pipe_x, top_pipe_y

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

def gg(self):
    offscreen_canvas = self.matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("../../../fonts/7x13.bdf")
    textColor = graphics.Color(255, 0, 0)
    pos = offscreen_canvas.width
    my_text = self.args.text
    x = 1
    while (x > 0):
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
        pos -= 1
        time.sleep(0.05)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
        x = pos + len

class GrayscaleBlock(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GrayscaleBlock, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Game over!")


    def run(self):
        max_brightness = self.matrix.brightness # set to 100
        count = 0
        c = 255
        self.matrix.brightness = 60

        # variables
        x_pos = 35
        top_x_pos = 16
        bottom_speed = 2
        top_speed = 1
        bottom_length = 9
        top_length = 9
        counter = 0

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
            if y_dist < 0:
                y_dist = 0
            if y_dist > 25:
                y_dist = 25

            
            self.matrix.Fill(63, 108 , 113)
            
            x_pos -= bottom_speed
            top_x_pos -= top_speed

            if x_pos < -4:
                #bottom_speed = random.randint(2,4)
                plus = int(random.uniform(0.1,1.1))
                if plus == 1:
                    print('added to bottom')
                bottom_speed += plus
                bottom_length = random.randint(7,13)
                x_pos = 35
                counter += 1
                print(counter)
            if top_x_pos < -4:
                #top_speed = random.randint(2,4)
                plus = int(random.uniform(0.1,1.1))
                if plus == 1:
                    print('added to top')
                top_speed += plus
                top_length = random.randint(7,13)
                top_x_pos = 35
                counter += 1
                print(counter)
                
            pipe_x, pipe_y = pipe(self, x_pos, bottom_length)
            
            top_pipe_x, top_pipe_y = top_pipe(self, top_x_pos, top_length)
            bird_x, bird_y = bird(self, y_dist)
            grass(self)
            if check(self, bird_x, bird_y, pipe_x, pipe_y, top_pipe_x, top_pipe_y):
                x_pos = 35
                top_x_pos = 35
                self.matrix.Fill(0,0,0)
                time.sleep(0.05)
                gg(self)
                x_pos = 35
                top_x_pos = 16
                bottom_speed = 2
                top_speed = 1
                bottom_length = 9
                top_length = 9
                counter = 0 


# Main function
if __name__ == "__main__":
    grayscale_block = GrayscaleBlock()
    if (not grayscale_block.process()):
        grayscale_block.print_help()
