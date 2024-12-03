#!/usr/bin/env python
from samplebase import SampleBase
from smbus2 import SMBus, i2c_msg


class GrayscaleBlock(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GrayscaleBlock, self).__init__(*args, **kwargs)

    def run(self):
        max_brightness = self.matrix.brightness # set to 100
        count = 0
        c = 255

        while (True):
            with SMBus(1) as bus:
                # Read 64 bytes from address 80
                msg = i2c_msg.read(0x18, 4)
                bus.i2c_rdwr(msg)
            # Instead of a timer switching brightness, use pressure sensor
            if self.matrix.brightness < 0.5:
                self.matrix.brightness = max_brightness
                # count changes when brightness = 0
                count += 1
            else:
                self.matrix.brightness -= 0.5

            # Instead of count switching the colors, use a push button
            if count % 4 == 0:
                # Maybe don't use matrix.Fill, we should make it scroll or pulse or something based on the other buttons input
                self.matrix.Fill(c, 0, 0)
            elif count % 4 == 1:
                self.matrix.Fill(0, c, 0)
            elif count % 4 == 2:
                self.matrix.Fill(0, 0, c)
            elif count % 4 == 3:
                self.matrix.Fill(c, c, c)

            """
            sub_blocks = 16
            width = self.matrix.width
            height = self.matrix.height
            x_step = max(1, width / sub_blocks)
            y_step = max(1, height / sub_blocks)
            count = 0

            while True:
                for y in range(0, height):
                    for x in range(0, width):
                        c = sub_blocks * int(y / y_step) + int(x / x_step)
                        if count % 4 == 0:
                            self.matrix.SetPixel(x, y, c, c, c)
                        elif count % 4 == 1:
                            self.matrix.SetPixel(x, y, c, 0, 0)
                        elif count % 4 == 2:
                            self.matrix.SetPixel(x, y, 0, c, 0)
                        elif count % 4 == 3:
                            self.matrix.SetPixel(x, y, 0, 0, c)

            count += 1
            """

            self.usleep(20 * 1000)

# Main function
if __name__ == "__main__":
    grayscale_block = GrayscaleBlock()
    if (not grayscale_block.process()):
        grayscale_block.print_help()
