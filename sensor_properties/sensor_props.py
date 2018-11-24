

# TODO: add max/min clk-speed(s) etc!
MAX_BAUD_RATE = 921400
MIN_BAUD_RATE = 2400
MAX_CS_VAL = 7
MAX_I2C_ADDR = 127


# Sensor data types
# ==================
class ComplexValue:
    def __init__(self, triggered=False, channel=-1, ch_val=0.0):
        self.triggered = triggered
        self.channel = channel
        self.ch_val = ch_val


# Sensor JSON schemas
# ====================
# TODO: these should be imported from other (config-)module!
# TODO: should UUID be part of schema at all?? (created internally now)
# ---------------------------------------------------------------------
# Base-level schema:
sensor_base_schema = {
    "type": "object",
    "required": ["sensor_type", "bus_no", "dev_name", "alias"],
    "properties": {
        "uuid": {"type": "integer"},
        "sensor_type": {"type": "string"},
        "bus_no": {"type": "integer"},
        "dev_name": {"type": "string"},
        "alias": {"type": "string"},
        "pwr_control": {"type": "bool"},   # default=False unless specified. TODO: how to set up pwrcntrl-handler?
    },
}

# Device-specific schemas:
sensor_i2c_schema = {
    "type": "object",
    "required": ["i2c_addr"],
    "properties": {
        "i2c_addr": {"type": "integer"},
        "clk_speed": {"type": "integer"},   # default=100000 unless specified  (overridden in sensor-driver?)
    },
}

sensor_spi_schema = {
    "type": "object",
    "required": ["cs_no"],
    "properties": {
        "cs_no": {"type": "integer"},
        "data_bits": {"type": "integer"},  # default unless specified (overridden in sensor-driver?)
        "spi_mode": {"type": "integer"},   # default=(mode)0 unless specified  (overridden in sensor-driver?)
        "clk_speed": {"type": "integer"},   # default=100000 unless specified  (overridden in sensor-driver?)
        "msb_first": {"type": "bool"},      # default=True unless specified  (overridden in sensor-driver?)
        "cs_toggle": {"type": "bool"},      # default=True unless specified  (overridden in sensor-driver?)
        "cycles_before": {"type": "integer"},      # default=0 unless specified  (overridden in sensor-driver?)
        "cycles_after": {"type": "integer"},      # default=0 unless specified  (overridden in sensor-driver?)
    },
}

sensor_uart_schema = {
    "type": "object",
    "required": ["baud_rate"],
    "properties": {
        "baud_rate": {"type": "integer"},
        "data_bits": {"type": "integer"},   # default=8 unless specified
        "parity": {"type": "bool"},         # default=False unless specified
        "stop_bits": {"type": "integer"},    # default=1 unless specified
    },
}



# Mapping to sensor-type:
# -----------------------
json_dev_schemas = {
                    "i2c": sensor_i2c_schema,
                    "spi": sensor_spi_schema,
                    "uart": sensor_uart_schema
                    }
