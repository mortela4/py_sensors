"""
@file db_utils.py
@brief DataBase utilities
DB functionality includes:
- freezing individual sensor-objects into DB-table entry object
- map JSON into DB-table entry object
- store (sensors-)table in DB
- load (sensors-)table from DB
@note Shim DB-abstraction layer using SQLite file storage as DB per default.
"""

import dataset
import uuid

from sensor_types.sensor_base import ExternalSensorBase, InternalSensorBase


def connect_to_db(conn_string=None):
    print("using DataSet-module version: ", dataset.__version__)
    if conn_string is None:
        print("ERROR: no connection string to DB specified!")
        return None
    try:
        db = dataset.connect('sqlite:///:memory:')  # use 'sqlite:///sensors.db' to persist ...
    except Exception as exc:
        print("ERROR: DB-open failure! Reason: %s" % exc)
        return None
    #
    return db


def insert_class_as_dict(sensor_db=None, cls_instance=None, debug=False):
    def debug_print(msg):
        if debug:
            print(msg)
    if sensor_db is None:
        print("NO database connector given - bailing out!")
    if cls_instance is None:
        print("NO sensor object passed as argument - bailing out!")
    # TODO: check instance-type comparison here!
    if not isinstance(cls_instance, ExternalSensorBase):
        print("Unkown object type - cannot use!")
        return
    # Set up table. TODO: assess - table name as argument?
    sensor_table = sensor_db['sensors']
    # Insert data if any ...
    prop_dict = {}
    for key, val in cls_instance.__dict__.items():
        if val is None:
            debug_print("Key '%s' has no value - skipping ..." % key)
        elif callable(val):
            debug_print("Key '%s' is a callable (func or method reference) - skipping ..." % key)
        elif isinstance(val, uuid.UUID):
            debug_print("Key '%s' is a UUID - need conversion to DB-acknowledged type ..." % key)
            prop_dict[key] = val.bytes_le
        else:
            debug_print("Key '%s' is a property with value = %s - adding to persisted data ..." % (key, val))
            prop_dict[key] = val
    # Store to DB. TODO: add a try-except here!
    sensor_table.insert(prop_dict)
    sensor_db.commit()


def find_sensor_by_type(db=None, sensor_type_name=None, single_hit=False):
    table = db['sensors']
    if single_hit:
        sensors = table.find_one(type_name=sensor_type_name)
    else:
        sensors = table.find(type_name=sensor_type_name)
    #
    return sensors


def find_sensor_by_alias(db=None, sensor_alias=None, single_hit=True):
    table = db['sensors']
    if single_hit:
        sensors = table.find_one(alias=sensor_alias)
    else:
        sensors = table.find(alias=sensor_alias)
    #
    return sensors


def load_sensors_from_db(db=None):
    table = db['sensors']
    return table.find()




