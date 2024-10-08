# -*- coding: utf-8 -*-
#
# Copyright (C) 2017-2024 KuraLabs S.R.L
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Transform a Python dictionary into an object.
"""

__author__ = 'KuraLabs S.R.L'
__email__ = 'info@kuralabs.io'
__version__ = '1.1.0'


from copy import deepcopy
from collections.abc import Mapping
try:
    from pprintpp import pformat
except ImportError:
    from pprint import pformat


def update(to_update, update_with):
    """
    Recursively update a dictionary with another.

    :param dict to_update: Dictionary to update.
    :param dict update_with: Dictionary to update with.

    :return: The first dictionary recursively updated by the second.
    :rtype: dict
    """
    for key, value in update_with.items():
        if isinstance(value, Mapping):
            to_update[key] = update(
                to_update.get(key, type(value)()),
                value,
            )
        else:
            to_update[key] = value

    return to_update


class Namespace:
    """
    Transform a Python dictionary into an object.
    """

    def __init__(self, *args, **kwargs):

        spread = list(args) + [kwargs]
        assert all(
            isinstance(element, Mapping)
            for element in spread
        )

        head, *tail = spread

        for element in tail:
            update(head, element)

        data = type(head)(
            (
                key, (
                    Namespace(value)
                    if isinstance(value, Mapping)
                    else value
                )
            )
            for key, value in head.items()
        )

        super().__setattr__('_data', data)

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, attr, value):
        self[attr] = value

    def __iter__(self):
        data = super().__getattribute__('_data')
        for key, value in data.items():
            if isinstance(value, self.__class__):
                yield key, type(data)(value)
                continue
            yield key, value

    def __getitem__(self, key):
        data = super().__getattribute__('_data')
        return data[key]

    def __setitem__(self, key, value):
        if isinstance(value, Mapping):
            value = Namespace(value)

        data = super().__getattribute__('_data')
        data[key] = value

    def __contains__(self, key):
        data = super().__getattribute__('_data')
        return key in data

    def __repr__(self):
        data = super().__getattribute__('_data')
        return pformat(type(data)(self))

    def __str__(self):
        return repr(self)

    def update(self, update_with):
        data = super().__getattribute__('_data')

        if isinstance(update_with, self.__class__):
            update_with = type(data)(update_with)

        to_update = type(data)(self)
        update(to_update, update_with)

        data = type(data)(
            (
                key, (
                    Namespace(value)
                    if isinstance(value, Mapping)
                    else value
                )
            )
            for key, value in to_update.items()
        )
        super().__setattr__('_data', data)

    def copy(self):
        data = super().__getattribute__('_data')
        return Namespace(deepcopy(data))


__all__ = [
    'Namespace',
]
