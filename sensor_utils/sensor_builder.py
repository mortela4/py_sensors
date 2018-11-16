
# **************** SENSOR-BUILDER ********************
class SensorBuilder(object):
    """
    Generic (almost ...) sensor builder.
    """
    def __init__(self, sensor_instance=None):
        self.sensor_obj = sensor_instance

    def with_field(self, field_name, field_value):
        existing_base_props = self.sensor_obj.base.__dict__
        existing_dev_props = self.sensor_obj.__dict__
        # Start with 'base' object = base class:
        if field_name not in existing_base_props:
            # Then device-specific props:
            self.sensor_obj.__dict__[field_name] = field_value
            if field_name not in existing_dev_props:
                print("Warning: field named '%s' - not in (sub)class! Possibly extending class ..." % field_name)
        else:
            self.sensor_obj.base.__dict__[field_name] = field_value
        #
        return self

    def build(self):
        return self.sensor_obj

