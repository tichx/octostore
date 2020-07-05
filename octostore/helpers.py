""" Helper files for all functions """

from io import StringIO
import sys
import yaml as YAML
import json as JSON
import uuid
import ast

import base64

import logging


def repr_uuid(dumper, uuid_obj):
    return YAML.ScalarNode("tag:yaml.org,2002:str", str(uuid_obj))


def convert_yaml_to_dict(value):
    """ Converts raw text to yaml using ruamel (put into a helper to ease
        converting to other libraries in the future) """

    if isinstance(value, dict):
        return value
    else:
        return YAML.safe_load(value)


def convert_dict_to_yaml(value):
    """ Converts dict to yaml using ruamel (put into a helper to ease
        converting to other libraries in the future) """
    if isinstance(value, str):
        return value

    # pylint: disable=line-too-long
    string_io_handle = StringIO()
    YAML.SafeDumper.add_representer(uuid.UUID, repr_uuid)
    YAML.safe_dump(value, string_io_handle)
    return string_io_handle.getvalue()


def merge_two_dicts(first_dict, second_dict):
    """ Merges two python dicts by making a copy of first then updating with second.
        Returns a copy. """

    return_dict = first_dict.copy()  # start with x's keys and values
    return_dict.update(
        second_dict
    )  # modifies z with y's keys and values & returns None
    return return_dict


def check_and_return_schema_type_by_string(val):
    """ Looks up string in mlspeclib.mlschemaenums and returns enum of type SchemaTypes """

    return val

    # if isinstance(val, MLSchemaTypes):
    #     return val

    # try:
    #     return MLSchemaTypes[val.upper()]
    # except AttributeError:
    #     raise KeyError("'%s' is not an enum from MLSchemaTypes" % val)
    # except KeyError:
    #     raise KeyError("'%s' is not an enum from MLSchemaTypes" % val)


def recursive_fromkeys(full_dict: dict):
    """ Builds a new dict with no values in it. Works recursively, but only looks for objects \
        with the 'nested' attribute."""
    return_dict = {}
    for key in full_dict.keys():
        if hasattr(full_dict[key], "nested"):
            return_dict[key] = recursive_fromkeys(
                full_dict[key].nested._declared_fields
            )
        else:
            if isinstance(full_dict[key], dict):
                return_dict[key] = {}
            else:
                return_dict[key] = None

    return return_dict


def encode_raw_object_for_db(mlobject):
    # Converts object -> dict -> yaml -> base64
    dict_conversion = mlobject.dict_without_internal_variables()
    yaml_conversion = convert_dict_to_yaml(dict_conversion)
    encode_to_utf8_bytes = yaml_conversion.encode("utf-8")
    base64_encode = base64.urlsafe_b64encode(encode_to_utf8_bytes)
    final_encode_to_utf8 = str(base64_encode, "utf-8")
    return final_encode_to_utf8


def decode_raw_object_from_db(s: str):
    # Converts base64 -> yaml
    base64_decode = base64.urlsafe_b64decode(s)
    return base64_decode


def to_yaml(this_dict: dict):
    return YAML.safe_dump(this_dict)


def to_json(this_dict: dict):
    out_string_io = StringIO()
    JSON.dump(this_dict, out_string_io)
    return out_string_io.getvalue()
