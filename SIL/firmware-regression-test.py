import can
import os
import slash

os.system('sudo ifconfig can0 down')
os.system('sudo ip link set can0 type can bitrate 500000')
os.system('sudo ifconfig can0 up')

bus = can.interface.Bus(channel="can0", bustype='socketcan')

def test_MC_clear_faults():
    pass

def read():
    message = bus.recv(10.0)
    print(message)

try:
    while True:
        read()
except:
    pass

finally:
    os.system('sudo ifconfig can0 down')
