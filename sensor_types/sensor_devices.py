# Helper function(s) and class(es):

MOCKED_DRIVER_TEST = False

if MOCKED_DRIVER_TEST:
    from sensor_drivers.mocked_sensor_driver import *
else:
    from sensor_drivers.generic_drivers import *


class SensorHelper(object):
    def get_info(self):
        # First - get BASE sensor properties (common to ALL sensors):
        self.base.get_info()
        # Then - get DEVICE-SPECIFIC properties, (possibly) unique to the given sensor type(I2C/SPI/UART):
        for sensor_prop, prop_value in self.__dict__.items():
            if sensor_prop != 'base' and sensor_prop != 'type_name':
                print("Sensor property %s = %s" % (sensor_prop, prop_value))


# Bus-specific sensor classes ...


class I2cSensor(SensorHelper):

    def __init__(self, base_type=None):
        print("Creating a I2C sensor ...")
        self.type_name = "i2c"
        self.i2c_addr = None
        if base_type is None:
            print("ERROR: 'base_type' NOT defined!")
        self.base = base_type(type_name="i2c", config=configure_i2c_sensor, read=get_i2c_val)
        # Configure/Initialize sensor if needed:
        if self.base.config is None:
            print("No configuration/initialization of sensor specified initially - skipping.")
        else:
            self.base.config(self.base.bus_no, self.i2c_addr)


class SpiSensor(SensorHelper):

    def __init__(self, base_type=None):
        print("Creating a SPI sensor ...")
        self.type_name = "spi"
        self.cs_no = None
        if base_type is None:
            print("ERROR: 'base_type' NOT defined!")
        self.base = base_type(type_name="spi", config=configure_spi_sensor, read=get_spi_val)
        # Configure/Initialize sensor if needed:
        if self.base.config is None:
            print("No configuration/initialization of sensor specified - skipping.")
        else:
            self.base.config(self.base.bus_no, self.cs_no)


class UartSensor(SensorHelper):

    def __init__(self, base_type=None):
        print("Creating a UART sensor ...")
        self.type_name = "uart"
        self.bus_no = None
        self.baud_rate = None
        if base_type is None:
            print("ERROR: 'base_type' NOT defined!")
        self.base = base_type(type_name="uart", read=get_uart_val)
        # Configure/Initialize sensor if needed:
        if self.base.config is None:
            print("No configuration/initialization of sensor specified - skipping.")
        else:
            self.base.config(self.base.bus_no, self.cs_no)


sensor_type_map = {"i2c": I2cSensor, "spi": SpiSensor, "uart": UartSensor}

