import smbus2
import time
# I2C address of the sensor
address = 0x18 

MAXIMUM_PSI = 25
MINIMUM_PSI = 0
OUTPUT_MAX = 0xE66666
OUTPUT_MIN = 0x19999A
c = 255

# Create an I2C bus object
bus = smbus2.SMBus(1) 
time.sleep(0.1)
# Read pressure data
try:
    while True:
        write = smbus2.i2c_msg.write(address, [0xAA,0x00,0x00])
    
        # Read 3 bytes of pressure data
        time.sleep(0.05)
        read = smbus2.i2c_msg.read(address, 4)
        bus.i2c_rdwr(write, read)
        #print(list(read))
        data = list(read)
        reading = data[1] << 16 | data[2] << 8 | data[3]
        #print(reading)
        # Convert raw data to pressure value (refer to the sensor datasheet for calculations)
        #pressure = data  # Your conversion logic here
        pressure = (reading - OUTPUT_MIN) * (MAXIMUM_PSI - MINIMUM_PSI)
        pressure = (pressure / (OUTPUT_MAX - OUTPUT_MIN)) + MINIMUM_PSI
        print("Pressure:", pressure)


        


        time.sleep(0.25)

    

except OSError as e:
    print("Error:", e)

