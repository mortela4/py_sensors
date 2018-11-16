
from jsonschema import Draft4Validator, exceptions

# ******************* JSON-validation ************************


class JsonValidator:
    def __init__(self, schema=None, formal_check=True, debug=False):
        self.schema = schema
        self.formal_check = formal_check
        self.debug = debug
        if schema is None:
            print("ERROR: cannot construct class correctly without schema argument given!!")
        else:
            self.validator = Draft4Validator(schema)

    def check(self, json_input=None):
        if json_input is None:
            print("ERROR: no input to check!")
            return False
        # Check for required:
        try:
            self.validator.validate(json_input)
        except exceptions.ValidationError:
            for error in self.validator.iter_errors(json_input):
                first_err_line = str(error).splitlines()[0]
                prop_name = first_err_line.split()[0]
                if first_err_line.endswith('required property'):
                    print("JSON-validation ERROR: missing required property %s" % prop_name)
                elif first_err_line.find('not of type') >= 0:
                    print("JSON-validation ERROR: property %s has wrong type." % prop_name)
                else:
                    print("JSON-validation ERROR: %s" % first_err_line)
            return False
        #
        if self.formal_check:
            if self.validator.is_valid(json_input):
                if self.debug:
                    if self.debug:
                        print("JSON has valid format.")
            else:
                print("ERROR: JSON input has invalid format!")
                return False
        if self.debug:
            print("SUCCESS: JSON is valid! :-)")
        return True

