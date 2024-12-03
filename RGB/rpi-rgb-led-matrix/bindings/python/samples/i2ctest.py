import smbus2
import time
# I2C address of the sensor
address = 0x18 

# Create an I2C bus object
bus = smbus2.SMBus(1) 
time.sleep(0.1)
# Read pressure data
try:
    regaddr = [0xAA, 0x00, 0x00]
    #bus.write_i2c_block_data(address, 0x00, )
    # Read 3 bytes of pressure data
    time.sleep(0.05)
    #data = bus.read_i2c_block_data(address, 0x00, 4) 

    # Convert raw data to pressure value (refer to the sensor datasheet for calculations)
    #pressure = data  # Your conversion logic here

    #print("Pressure:", pressure)

    wr = smbus2.i2c_msg.write (address, [regaddr])
	rd = smbus2.i2c_msg.read (address, n)
	bus.i2c_rdwr (wr, rd)

except OSError as e:
    print("Error:", e)

