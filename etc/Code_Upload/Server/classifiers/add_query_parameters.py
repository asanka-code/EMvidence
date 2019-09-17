# -*- coding: utf-8 -*-

# Provided by https://stackoverflow.com/users/304644/ivan-gromov

import collections
import yaml

from rest_framework import fields

"""
Convert rest_framework.fields classes to Swagger data types according to http://swagger.io/specification/
Return 'string' by default.
"""
field_to_yaml_type = collections.defaultdict(
    lambda: 'string',
    {
        fields.IntegerField: 'integer',
        fields.FloatField: 'number',
        fields.BooleanField: 'boolean',
        fields.NullBooleanField: 'boolean',
    }
)


def add_query_parameters(serializer_class):
    def decorator(method):
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)

        from rest_framework_swagger.introspectors import IntrospectorHelper, BaseViewIntrospector
        i = BaseViewIntrospector(None, None, None, None)
        parser = i.get_yaml_parser()
        plain_text_doc = IntrospectorHelper.strip_yaml_from_docstring(method.__doc__)
        yaml_object = parser.load_obj_from_docstring(method.__doc__) or {}
        if 'parameters' in yaml_object:
            if not isinstance(yaml_object['parameters'], list):
                raise ValueError('paramters in YAML docstring should be a list instance')
        else:
            yaml_object['parameters'] = list()
        serializer = serializer_class()
        for field_name, field in serializer.fields.items():
            parameter = {
                'name': field_name,
                'description': field.help_text,
                'type': field_to_yaml_type[type(field)],
                'required': field.required,
                'paramType': 'query',
            }
            yaml_object['parameters'].append(parameter)
        wrapper.__doc__ = '\n'.join([plain_text_doc,
                                     '---',
                                     yaml.dump(yaml_object, default_flow_style=False)])
        return wrapper
    return decorator


