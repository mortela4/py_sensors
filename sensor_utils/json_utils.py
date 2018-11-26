import json
from jsonschema import Draft4Validator, exceptions


# ******************* JSON-validation ************************

def property_not_in_schema(schemas=[], json_input=None, debug=False):
    def debug_print(msg):
        if debug:
            print(msg)
    #
    debug_print("Checking over %d schemas ..." % len(schemas))
    debug_print("============================")
    sensor_keys = json.loads(json_input)
    debug_print("INPUT: %s" % sensor_keys)
    #
    for schema_no, schema in enumerate(schemas):
        props = dict(schema["properties"])
        if schema_no == 0:
            debug_print("Checking BASE schema ...")
        else:
            debug_print("Checking DEV schema ...")
        print("Properties: ", str(props))
        #
        for prop in sensor_keys:
            debug_print("Checking for property: %s" % prop)
            if prop in props:
                debug_print("Found property %s in schema." % prop)
                return False
            else:
                if schema_no == 0:
                    debug_print("WARN: property %s NOT found in BASE schema :-/" % prop)
                else:
                    debug_print("ERR: property %s NOT found in DEV schema either!!" % prop)
        #
    return True


class JsonValidator:
    def __init__(self, schema=None, formal_check=True, debug=False):
        self.schema = schema
        self.formal_check = formal_check
        self.debug = debug
        if schema is None:
            print("ERROR: cannot construct class correctly without schema argument given!!")
        else:
            self.validator = Draft4Validator(schema)

    def check(self, json_input=None, ):
        if json_input is None:
            print("ERROR: no input to check!")
            return False
        # Check for required properties:
        try:
            self.validator.validate(json_input)
        except exceptions.ValidationError:
            for error in self.validator.iter_errors(json_input):
                first_err_line = str(error).splitlines()[0]
                # print("JSON validation ERR: ", str(error))
                prop_name = first_err_line.split()[0]
                if first_err_line.endswith('required property'):
                    print("JSON-validation ERROR: missing required property %s" % prop_name)
                elif first_err_line.find('not of type') >= 0:
                    print("JSON-validation ERROR: property %s has wrong type." % prop_name)
                else:
                    print("JSON-validation ERROR: %s" % first_err_line)
            return False
        #
        # Check format (entry-level check):
        if self.formal_check:
            if self.validator.is_valid(json_input):
                if self.debug:
                    if self.debug:
                        print("JSON has valid format.")
            else:
                print("ERROR: JSON input has invalid format!")
                return False
        # Check for parameters NOT found in properties given by schema (only DEV-properties):

        if self.debug:
            print("SUCCESS: JSON is valid! :-)")
        return True

