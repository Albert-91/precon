import smbus2
import math
import time

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c


def read_byte(adr):
    return bus.read_byte_data(address, adr)


def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low
    return val


def read_word_2c(adr):
    val = read_word(adr)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val


def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)

# pitch = 180 * atan (accelerationX/sqrt(accelerationY*accelerationY + accelerationZ*accelerationZ))/M_PI;
# roll = 180 * atan (accelerationY/sqrt(accelerationX*accelerationX + accelerationZ*accelerationZ))/M_PI;
# yaw = 180 * atan (accelerationZ/sqrt(accelerationX*accelerationX + accelerationZ*accelerationZ))/M_PI;


def pitch(a_x, a_y, a_z):
    return 180 * math.atan(a_x / dist(a_y, a_z)) / math.pi


def roll(a_x, a_y, a_z):
    return 180 * math.atan(a_y / dist(a_x, a_z)) / math.pi


def yaw(a_x, a_y, a_z):
    return 180 * math.atan(a_z / dist(a_x, a_z)) / math.pi


def get_z_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


bus = smbus2.SMBus(1)
address = 0x68

bus.write_byte_data(address, power_mgmt_1, 0)
import ctypes

class C:
    MPU6050_RA_GYRO_XOUT_H = 0x43
    MPU6050_ADDRESS_AD0_LOW = 0x68  # address pin low (GND), default
    MPU6050_ADDRESS_AD0_HIGH = 0x69  # address pin high (VCC)
    MPU6050_DEFAULT_ADDRESS = MPU6050_ADDRESS_AD0_LOW

def get_rotation():
    __dev_id = C.MPU6050_DEFAULT_ADDRESS
    raw_data = bus.read_i2c_block_data(__dev_id, C.MPU6050_RA_GYRO_XOUT_H, 6)
    gyro = [0] * 3
    gyro[0] = ctypes.c_int16(raw_data[0] << 8 | raw_data[1]).value
    gyro[1] = ctypes.c_int16(raw_data[2] << 8 | raw_data[3]).value
    gyro[2] = ctypes.c_int16(raw_data[4] << 8 | raw_data[5]).value
    return gyro


while True:
    print("--------------")

    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0

    print("X rotation: ", get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
    print("Y rotation: ", get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
    print(str(get_rotation()))

    time.sleep(1)
