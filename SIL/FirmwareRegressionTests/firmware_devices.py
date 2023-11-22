import slash
from ...Drivers.CANable_driver import CANableDriver

@slash.fixture
def CANAbleSniffer():
    CANDriver = CANableDriver()
    return CANDriver