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

while True:
    print("Gyroscope data")
    print("--------------")

    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    print("{}\t{}\t{}\t{}".format("X out: ", gyro_xout, "scaled: ", (gyro_xout / 131)))
    print("{}\t{}\t{}\t{}".format("Y out: ", gyro_yout, " scaled: ", (gyro_yout / 131)))
    print("{}\t{}\t{}\t{}".format("Z out: ", gyro_zout, " scaled: ", (gyro_zout / 131)))

    print("Accelerometer data")
    print("------------------")

    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0

    print("X rotation: ", get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
    print("Y rotation: ", get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))

    print("NEW X rotation:", pitch(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
    print("NEW Y rotation:", roll(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
    print("NEW Z rotation:", yaw(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))

    time.sleep(1)
