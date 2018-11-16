# ***************************** Sensor BASE-classes ********************************


class ExternalSensorBase:
    """
    Base sensor class no.1 (external sensors, connected to a bus)
    """
    bus_property1 = {"i2c": "bus-address", "spi": "ChipSelect-number", "uart": "baud_rate"}

    def __init__(self, type_name=None, bus_no=None, dev_name=None, alias=None, config=None, read=None):
        #
        self.config = config
        self.read = read
        self.type_name = type_name
        self.bus_no = bus_no
        if dev_name:
            self.dev_name = dev_name
        else:
            self.dev_name = "none"
        #
        if alias:
            self.alias = alias
        else:
            self.alias = "none"
        #
        self.bus_prop1 = self.bus_property1[self.type_name]

    def get_info(self):
        if self.type_name is None:
            print("Unknown sensor type - cannot show info!")
            return
        # INFO:
        bus_type_name = self.type_name.upper()
        print("%s-sensor properties:" % bus_type_name)
        print("---------------------")
        print("%s-interface no: %d" % (bus_type_name, self.bus_no))
        print("%s connected device: %s" % (bus_type_name, self.dev_name))
        print("%s sensor alias: %s" % (bus_type_name, self.alias))
        print("Bus-specific properties:")


class InternalSensorBase:
    """
    Base sensor class no.2 (MCU/SoC-internal sensors)
    """
    def __init__(self, type_name=None, dev_no=None, dev_addr=None, dev_name=None, use_irq=False, alias=None, read=None):
        self.read = read
        # TODO: throw error if =None or negative (and possibly above some limit)!
        self.type_name = type_name
        self.dev_no = dev_no
        self.dev_addr = dev_addr   # Start of register-block for peripheral, e.g. ADC0, ADC1 etc.
        if dev_name:
            self.dev_name = dev_name
        else:
            self.dev_name = "none"
        #
        if alias:
            self.alias = alias
        else:
            self.alias = "none"
        #
        self.use_irq = use_irq

    def get_info(self):
        if self.type_name is None:
            print("Unknown sensor type - cannot show info!")
            return
        # INFO:
        print("Internal sensor properties:")
        print("---------------------------")
        print("%Device no: %d" % self.dev_no)
        print("Sensor alias: %s" % self.alias)
        print("Device-specific properties:")
        print("Device address: %x" % self.dev_addr)
        print("Using IRQ: %s" % self.use_irq)

