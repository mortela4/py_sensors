

# TODO: add max/min clk-speed(s) etc!
MAX_BAUD_RATE = 921400
MIN_BAUD_RATE = 2400
MAX_CS_VAL = 7
MAX_I2C_ADDR = 127


# Sensor data types
# TODO: put in separate module!
# ==============================
class ComplexValue:
    def __init__(self, triggered=False, channel=-1, ch_val=0.0):
        self.triggered = triggered
        self.channel = channel
        self.ch_val = ch_val


# JSON schemas
# =============
# TODO: these should be imported from other (config-)module!
# ----------------------------------------------------------
# Base-level schema:
sensor_base_schema = {
    "type": "object",
    "required": ["sensor_type", "bus_no", "dev_name"],
    "properties": {
        "sensor_type": {"type": "string"},
        "bus_no": {"type": "integer"},
        "dev_name": {"type": "string"},
    },
}

# Device-specific schemas:
sensor_i2c_schema = {
    "type": "object",
    "required": ["i2c_addr"],
    "properties": {
        "i2c_addr": {"type": "integer"},
    },
}
sensor_spi_schema = {
    "type": "object",
    "required": ["cs_no"],
    "properties": {
        "cs_no": {"type": "integer"},
    },
}
sensor_uart_schema = {
    "type": "object",
    "required": ["baud_rate"],
    "properties": {
        "baud_rate": {"type": "integer"},
    },
}

# Mapping to sensor-type:
json_dev_schemas = {"i2c": sensor_i2c_schema,
                    "spi": sensor_spi_schema,
                    "uart": sensor_uart_schema}
