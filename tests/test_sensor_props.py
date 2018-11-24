import unittest
#
from sensor_properties import sensor_props    # This is the code being tested


MAX_FLOAT_DIFFERENCE = 0.00001

VALID_I2C_PARAMS = {"uuid": 0xABCDABCDDEADBEEF, "sensor_type": "i2c", "bus_no": 2, "i2c_addr": 78, "clk_speed": 400000, "dev_name": "BM280", "alias": "RHT-sensor1", "pwr_control": "false"}
INVALID_I2C_PARAMS_BASE = {"uuid": 0xABCDABCDDEADBEEF, "sensor_type": "i2c", "i2c_addr": 78, "dev_name": "BM280", "clk_speed": 400000, "alias": "RHT-sensor1", "pwr_control": "false"}
INVALID_I2C_PARAMS_DEV = {"uuid": 0xABCDABCDDEADBEEF, "sensor_type": "i2c", "bus_no": 2, "i2c_addr": 78, "dev_name": "BM280", "alias": "RHT-sensor1", "pwr_control": "false"}


class SensorsTests(unittest.TestCase):
    # Setup & Teardown
    def setUp(self):
        self.base_schema = sensor_props.sensor_base_schema
        self.dev_schemas = sensor_props.json_dev_schemas

    def tearDown(self):
        pass

    # Basic tests (1st level)
    # =======================

    # Step 1: positive tests (valid sensor / valid action)
    # ----------------------------------------------------
    def testBasePropertyFoundInSchema(self):
        schema = self.base_schema
        props = schema["properties"]
        #
        params = VALID_I2C_PARAMS
        print("\nTest for base properties - with valid params for both base and dev ...")
        for prop in props:
            print("Checking for property: %s" % prop)
            self.assertEqual(True, prop in params)
        print("\nTest for dev properties - with valid params for only dev ...")
        params = INVALID_I2C_PARAMS_DEV
        for prop in props:
            print("Checking for property: %s" % prop)
            self.assertEqual(True, prop in params)

    def testDevPropertyFoundInSchema(self):
        schema = self.dev_schemas["i2c"]
        props = schema["properties"]
        #
        params = VALID_I2C_PARAMS
        #
        print("\nTest for base properties - with valid params for both base and dev ...")
        for prop in props:
            print("Checking for property: %s" % prop)
            self.assertEqual(True, prop in params)


if __name__ == '__main__':
    unittest.main()
