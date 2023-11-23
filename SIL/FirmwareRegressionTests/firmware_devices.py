import slash
from ...Drivers.GPIODriver import GPIODriver
from ...Drivers.CANable_driver import CANableDriver

@slash.fixture
def CANAbleSniffer():
    driver = CANableDriver()
    return driver

@slash.fixture
def GPIOController():
    driver = GPIODriver()
    return driver