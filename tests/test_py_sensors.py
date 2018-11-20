# @file test_py_sensors.py


import unittest
#
from py_sensors import Sensors    # This is the code being tested
from sensor_types.sensor_devices import I2cSensor, SpiSensor, UartSensor, ComplexValue
from sensor_types.sensor_base import ExternalSensorBase, InternalSensorBase


MAX_FLOAT_DIFFERENCE = 0.00001


class SensorsTests(unittest.TestCase):
    sensors = None
    # Setup & Teardown

    def setUp(self):
        self.sensors = Sensors()

    def tearDown(self):
        pass

    # Basic tests (1st level)
    # =======================

    # Step 1: positive tests (valid sensor / valid action)
    # ----------------------------------------------------
    def testAddValidSensor(self):
        orig_no_of_sensors = len(self.sensors.sensors)
        params = """{"sensor_type": "i2c", "bus_no": 2, "i2c_addr": 78, "dev_name": "BM280", "alias": "RHT-sensor1"}"""
        status = self.sensors.add_sensor(params)
        self.assertEqual(True, status)
        new_no_of_sensors = len(self.sensors.sensors)
        self.assertEqual(1, new_no_of_sensors - orig_no_of_sensors)

    def testAddMultipleValidSensors(self):
        orig_no_of_sensors = len(self.sensors.sensors)
        #
        params = """{"sensor_type": "spi", "bus_no": 1, "cs_no": 3, "dev_name": "SHT721", "alias": "RHT-sensor2A"}"""
        self.sensors.add_sensor(params)
        #
        params = """{"sensor_type": "spi", "bus_no": 1, "cs_no": 7, "dev_name": "SHT721", "alias": "RHT-sensor2B"}"""
        self.sensors.add_sensor(params)
        #
        params = """{"sensor_type": "uart", "bus_no": 4, "baud_rate": 115200, "dev_name": "CustomHygrometerSubmodule", "alias": "RHT-sensor3"}"""
        self.sensors.add_sensor(params)
        #
        new_no_of_sensors = len(self.sensors.sensors)
        self.assertEqual(3, new_no_of_sensors - orig_no_of_sensors)

    def testGetSensorByAlias(self):
        params = """{"sensor_type": "i2c", "bus_no": 2, "i2c_addr": 77, "dev_name": "BM280", "alias": "RHT-sensor4"}"""
        status = self.sensors.add_sensor(params)
        self.assertEqual(True, status)
        #
        test_sensor = self.sensors.get_sensor_by_alias("RHT-sensor4")
        self.assertEqual(True, isinstance(test_sensor, I2cSensor))
        self.assertEqual("BM280", test_sensor.base.dev_name)
        self.assertEqual(77, test_sensor.i2c_addr)

    def testGetSensorData(self):
        data = self.sensors.read_sensors()
        no_of_data = len(data)
        no_of_sensors = len(self.sensors.sensors)
        self.assertEqual(no_of_data, no_of_sensors)
        #
        for sdata in data:
            self.assertEqual(True, isinstance(sdata, int) or
                             isinstance(sdata, float) or
                             isinstance(sdata, list) or
                             isinstance(sdata, ComplexValue))

    # Step 2: negative tests (invalid sensor / invalid actions)
    # ---------------------------------------------------------
    def testAddNonValidSensorConfig(self):
        self.assertNotEqual(0, len(self.sensors.sensors))
        # Search for non-existing sensor by alias:
        test_sensor = self.sensors.get_sensor_by_alias("non-existent-sensor")
        self.assertIsNone(test_sensor)

    def testAddNonValidSensorConfig(self):
        # Adding a valid sensor:
        params = """{"sensor_type": "i2c", "bus_no": 2, "i2c_addr": 80, "dev_name": "BM280", "alias": "valid-sensor"}"""
        status = self.sensors.add_sensor(params)
        orig_no_of_sensors = len(self.sensors.sensors)
        self.assertEqual(True, status)
        # Trying to add a non-valid sensor:
        params = """{"sensor_type": "i2c", "bus_no": 2, "i2c_addr": 80, "dev_name": "BM280", "alias": "nonvalid-sensor"}"""
        status = self.sensors.add_sensor(params)
        self.assertEqual(False, status)
        new_no_of_sensors = len(self.sensors.sensors)
        self.assertEqual(0, new_no_of_sensors - orig_no_of_sensors)

    def testAddNonValidSensorJSONmissingBaseProperty(self):
        orig_no_of_sensors = len(self.sensors.sensors)
        # Trying to add sensor with invalid JSON-spec:
        params = """{"sensor_type": "i2c", "bus_no": 2, "i2c_addr": 81, "alias": "json-error-sensor"}"""
        status = self.sensors.add_sensor(params)
        self.assertEqual(False, status)
        new_no_of_sensors = len(self.sensors.sensors)
        self.assertEqual(0, new_no_of_sensors - orig_no_of_sensors)

    def testAddNonValidSensorJSONmissingDevProperty(self):
        orig_no_of_sensors = len(self.sensors.sensors)
        # Trying to add sensor with invalid JSON-spec:
        params = """{"sensor_type": "i2c", "bus_no": 2, "clk_speed": 100000, "dev_name": "BM281", "alias": "sensor2F"}"""
        status = self.sensors.add_sensor(params)
        self.assertEqual(False, status)
        new_no_of_sensors = len(self.sensors.sensors)
        self.assertEqual(0, new_no_of_sensors - orig_no_of_sensors)


if __name__ == '__main__':
    unittest.main()

