import slash
from ...Drivers.CANable_driver import CANableDriver
from ...Drivers.GPIODriver import GPIODriver

@slash.fixture
def CANAbleSniffer():
    driver = CANableDriver()
    return driver

@slash.fixture
def GPIOController():
    driver = GPIODriver()
    return driver