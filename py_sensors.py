"""
@file py_sensors.py
@brief Sensor class constructed using a given (sensor-)baseclass as argument,
and using parameter packs created from JSON for adding sensor *properties*,
where only base-class properties are fixed, while device-specific attributes
can be added by extending the subclass.
Sensor *base* classes can be (for example) of type
INTERNAL:
- internal direct --> e.g. MCU/SoC-internal temp-sensor with digital reading
  (need possibly only address of control&data-registers)
- internal indirect --> e.g. internal ADC of SoC/MCU;
  input may need adaptation & data must possibly be scaled
EXTERNAL:
- external generic --> e.g. SPI, I2C, UART, 1-wire, CAN-bus etc. (also MIPI/GreyBus)
- external dedicated --> e.g. USB-device (typically) or FireWire-client
  (access via device class-driver)
In all, this yields a minimum of 2 generic base-classes (w. fields for distinction),
or 4 base-classes that are more specialized.

@note Schema-validation of JSON input is included to avoid faulty input to propagate errors!
"""

import json

from sensor_properties import sensor_props
from sensor_types.sensor_base import ExternalSensorBase, InternalSensorBase
from sensor_types.sensor_devices import I2cSensor, SpiSensor, UartSensor, sensor_type_map
from sensor_utils.json_utils import JsonValidator, check_for_unknown_properties
from sensor_utils.sensor_builder import SensorBuilder


# *********************** SENSORS-CLASS ***********************

class Sensors:
    """
    Class which is a PLACEHOLDER for multiple sensors of different type.
    """
    def __init__(self, sensors=[]):
        self.sensors = sensors

    def i2c_validate(self, sensor):
        i2c_sensors = self.get_i2c_sensors()
        for i2c_sensor in i2c_sensors:
            if sensor.i2c_addr == i2c_sensor.i2c_addr:
                print("ERROR validating I2C-sensor: address=%d already in use on bus#=%d!" %
                      (sensor.i2c_addr, sensor.base.bus_no))
                return False
        return True

    def spi_validate(self, sensor):
        spi_sensors = self.get_spi_sensors()
        for spi_sensor in spi_sensors:
            if sensor.base.bus_no == spi_sensor.base.bus_no and sensor.cs_no == spi_sensor.cs_no:
                print("ERROR: validating SPI-sensor: CS=%d already in use on bus#=%d!" %
                      (sensor.cs_no, sensor.base.bus_no))
                return False
        return True

    def uart_validate(self, sensor):
        uart_sensors = self.get_uart_sensors()
        for uart_sensor in uart_sensors:
            if sensor.base.bus_no == uart_sensor.base.bus_no:
                print("ERROR: validating UART-sensor: serialport=%d already in use!" % sensor.base.bus_no)
                return False
        return True

    @staticmethod
    def build_sensor(sensor_clsname=None, base_clsname=None, props=None):
        if sensor_clsname is None or base_clsname is None or props is None:
            # TODO: possibly emit ERROR msg here - and/or throw??
            print("ERROR: build_sensor() requires all of 'sensor_clsname', "
                  "'base_clsname' and 'ppack' parameters to be provided!")
            return None
        #
        raw_obj = sensor_clsname(base_type=base_clsname)
        sensor_builder = SensorBuilder(sensor_instance=raw_obj)
        #
        # Set up list of props:
        # Build sensor:
        first_pass = True
        for sensor_prop_name, prop_value in props.items():
            if sensor_prop_name != "sensor_type":
                if first_pass:
                    tmp = sensor_builder.with_field(sensor_prop_name, prop_value)
                    first_pass = False
                else:
                    tmp = tmp.with_field(sensor_prop_name, prop_value)
        # Get final object:
        sensor = tmp.build()
        #
        return sensor

    def add_sensor(self, json_spec):
        validators = {"i2c": self.i2c_validate, "spi": self.spi_validate, "uart": self.uart_validate}
        #
        json_base_validator = JsonValidator(sensor_props.sensor_base_schema)
        #
        # Turn JSON-input into dictionary:
        sensor_spec = json.loads(json_spec)
        # Validate JSON:
        if json_base_validator.check(sensor_spec):
            # May log something for DEBUG-purposes here ...
            pass
        else:
            print("ERROR: invalid sensor JSON input!")
            return False
        #
        sensor_type = sensor_spec['sensor_type']
        #
        sensor_class_type = sensor_type_map[sensor_type]
        # Can validate device-specific JSON:
        json_dev_spec_schema = sensor_props.json_dev_schemas[sensor_type]
        json_dev_spec_validator = JsonValidator(json_dev_spec_schema)
        # Validate ...
        if json_dev_spec_validator.check(sensor_spec):
            # May log something for DEBUG-purposes here ...
            pass
        else:
            print("ERROR: invalid device-specific JSON input!")
            return False
        # Create sensor ...
        try:
            if check_for_unknown_properties([sensor_props.sensor_base_schema, json_dev_spec_schema], json_spec):
                print("Found unknown property!")
                raise Exception
            #
            sensor = self.build_sensor(sensor_clsname=sensor_class_type,
                                       base_clsname=ExternalSensorBase,
                                       props=sensor_spec)
            # Validating sensor instance BEFORE appending to list:
            validator = validators[sensor.base.type_name]
            if validator(sensor):
                self.sensors.append(sensor)
            else:
                # TODO: qualify use of 'raise' here!
                raise Exception("Parameter ERROR: cannot add sensor to sensor-list!")
        except Exception as exc:
            print("ERROR creating sensor!!")
            print(exc.args)
            return False
        #
        return True

    def list_sensors(self):
        if len(self.sensors) == 0:
            print("No sensors registered!")
            return
        print("")
        print("Registered sensors:")
        print("===================")
        for sensor in self.sensors:
            # TODO: check if 'sensor' has attribute(=method) 'get_info()' before attempting invocation!
            sensor.get_info()

    def read_sensors(self):
        sensor_data = []
        print("Registered sensors:")
        print("===================")
        for idx, sensor in enumerate(self.sensors):
            val = sensor.base.read()
            sensor_data.append(val)
            if type(val) is not float:
                # Check if list or complex value:
                if type(val) is list:
                    print("Value list:")
                    print("------------")
                    for val_no, item_val in enumerate(val):
                        print("Value no.%d = %d" % (val_no, item_val))
                    print("")
                else:
                    if isinstance(val, sensor_props.ComplexValue):
                        print("Complex value:")
                        print("--------------")
                        print("Triggered: ", val.triggered)
                        print("Channel no: ", val.channel)
                        print("Value: ", val.ch_val)
                        print("")
                    else:
                        print("ERROR: cannot parse sensor readout result!")
            else:
                print("Sensor no.%d: %s (type=%s) value = %s" % (idx, sensor.base.alias, sensor.base.dev_name, val))
        #
        return sensor_data

    def get_sensor_data(self):
        """ Generator version of 'read_sensors()' which may be more usable. """
        for sensor in self.sensors:
            sensor_val = sensor.base.read()
            sensor_name = sensor.base.alias
            yield (sensor_name, sensor_val)  # use 'sdata_gen = sensors.get_sensor_data()' to obtain generator.

    def get_i2c_sensors(self):
        i2c_sensors = []
        for sensor in self.sensors:
            if sensor.base.type_name == "i2c":
                i2c_sensors.append(sensor)
        return i2c_sensors

    def get_spi_sensors(self):
        spi_sensors = []
        for sensor in self.sensors:
            if sensor.base.type_name == "spi":
                spi_sensors.append(sensor)
        return spi_sensors

    def get_uart_sensors(self):
        uart_sensors = []
        for sensor in self.sensors:
            if sensor.base.type_name == "uart":
                uart_sensors.append(sensor)
        return uart_sensors

    def get_sensor_by_alias(self, s_alias=None):
        """
        Find sensor by alias - which SHOULD be unique.
        This is NOT the case with attribute 'dev_name'.
        TODO: infer checks for alias uniqueness! (on input also ...)
        """
        sensor_found = None
        if s_alias is None:
            # TODO: rather throw ArgumentException error ... (no?)
            print("ERROR: no sensor name specified!")
        else:
            for sensor in self.sensors:
                if s_alias == sensor.base.alias:
                    sensor_found = sensor
                    break
        return sensor_found

    def get_sensor_by_uuid(self, s_uuid=None):
        """
        Find sensor by UUID - which SHOULD be unique.
        This is NOT the case with attribute 'dev_name'.
        TODO: infer checks for UUID uniqueness! (on input also(?))
        TODO: make more pythonic search ...
        """
        sensor_found = None
        if s_uuid is None:
            # TODO: rather throw ArgumentException error ... (no?)
            print("ERROR: no sensor name specified!")
        else:
            for sensor in self.sensors:
                if s_uuid == sensor.base.uuid:
                    sensor_found = sensor
                    break
        return sensor_found


# *********** TEST ******************
if __name__ == "__main__":
    sensors = Sensors()
    sensors.list_sensors()
    #
    # Example JSON-data:
    params = """{"sensor_type": "i2c", "bus_no": 2, "i2c_addr": 78, "dev_name": "BM280", "alias": "RHT-sensor1"}"""
    sensors.add_sensor(params)
    #
    params = """{"sensor_type": "spi", "bus_no": 1, "cs_no": 3, "dev_name": "SHT721", "alias": "RHT-sensor2A"}"""
    sensors.add_sensor(params)
    #
    params = """{"sensor_type": "spi", "bus_no": 1, "cs_no": 8, "dev_name": "SHT721", "alias": "RHT-sensor2B"}"""
    sensors.add_sensor(params)
    #
    params = {"sensor_type": "uart", "bus_no": 4, "baud_rate": 115200,
              "dev_name": "CustomHygrometerSubmodule", "alias": "RHT-sensor3"}
    sensors.add_sensor(json.dumps(params))
    #
    sensors.list_sensors()
    #
    # Alt1:
    sensors.read_sensors()
    #
    # Alt2 (no special handling of list-data or ComplexValue-data here):
    print("Sensor data from dataset:")
    print("=========================")
    sdata = sensors.get_sensor_data()
    for num in range(len(sensors.sensors)):
        name, value = next(sdata)
        print("Sensor %d named '%s' value: %s" % (num, name, value))
    # Alt3 (using generator just as Alt2 - but simpler):
    print("Sensor data from generator:")
    print("===========================")
    sdata = sensors.get_sensor_data()
    for sd_item in sdata:
        name, value = sd_item   # indirectly calling 'next(sdata)'
        print("Sensor named '%s' value: %s" % (name, value))
    #
    print("")
    print("Adding some more sensors ...")
    sensors.add_sensor(json.dumps({"sensor_type": "uart", "bus_no": 4, "baud_rate": 38400, "dev_name": "CustomHygrometerSubmodule", "alias": "RHT-sensor4"}))
    sensors.add_sensor(json.dumps({"sensor_type": "spi", "bus_no": 1, "cs_no": 3, "clk_speed": 5000000, "dev_name": "MPU6050", "alias": "IMU-A1"}))
    sensors.add_sensor(json.dumps({"sensor_type": "spi", "bus_no": 1, "cs_no": 4, "clk_speed": 5000000, "dev_name": "MPU6050", "alias": "IMU-A2"}))
    sensors.add_sensor(json.dumps({"sensor_type": "i2c", "bus_no": 2, "i2c_addr": 78, "clk_speed": 100000, "dev_name": "BM281", "alias": "sensor2C"}))
    sensors.add_sensor(json.dumps({"sensor_type": "i2c", "bus_no": 2, "i2c_addr": 77, "clk_speed": 100000, "dev_name": "BM281", "alias": "sensor2D"}))
    #
    sensors.list_sensors()
    #
    my_sensor = sensors.get_sensor_by_alias("sensor2D")
    if my_sensor is None:
        print("No sensor by alias 'sensor2D' found!")
    else:
        print("Sensor by alias 'sensor2D' found! Characteristics: %s" % repr(my_sensor))
        my_sensor.get_info()
        print("Full list:")
        print(my_sensor.base.__dict__)
        print(my_sensor.__dict__)
    #
    # Fails base-schema test:
    sensors.add_sensor("""{"sensor_type": "i2c", "i2c_addr": 77, "clk_speed": 100000, "dev_name": "BM281","alias": "sensor2E"}""")
    # Fails devspec-schema test:
    sensors.add_sensor("""{"sensor_type": "i2c", "bus_no": 2, "clk_speed": 100000, "dev_name": "BM281", "alias": "sensor2F"}""")
    # Fails check for 'unkown property':
    sensors.add_sensor("""{"sensor_type": "i2c", "bus_no": 2, "i2c_addr": 79, "clock_speed": 100000, "dev_name": "BM281", "alias": "sensor2F"}""")






