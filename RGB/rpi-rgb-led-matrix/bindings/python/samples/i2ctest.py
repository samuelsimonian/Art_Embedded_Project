import smbus2

# I2C address of the sensor
address = 0x18 

# Create an I2C bus object
bus = smbus2.SMBus(1) 

# Read pressure data
try:
    # Read 3 bytes of pressure data
    data = bus.read_i2c_block_data(address, 0x00, 4) 

    # Convert raw data to pressure value (refer to the sensor datasheet for calculations)
    pressure = data  # Your conversion logic here

    print("Pressure:", pressure)

except OSError as e:
    print("Error:", e)