# -*- coding: utf-8 -*-
#
# Copyright (C) 2017-2021 KuraLabs S.R.L
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
Test objns module.
"""

from collections import OrderedDict

from objns import Namespace


def test_objns():
    ns = Namespace(
        {'one': 100},
        {'two': 300},
        {'two': 400, 'three': {'four': 400}},
        one=200,
    )

    assert(ns.two == 400)
    assert(ns.one == 200)
    assert(ns['two'] == 400)

    ns['two'] = 300
    assert(ns['two'] == 300)

    ns.two = 700
    assert(ns['two'] == 700)
    assert(ns.two == 700)

    assert(ns.three.four == 400)
    assert(ns['three'].four == 400)
    assert(ns['three']['four'] == 400)

    nscopy = ns.copy()
    assert(id(ns) != id(nscopy))

    asdict = dict(ns)
    assert(asdict == {'one': 200, 'two': 700, 'three': {'four': 400}})
    assert(type(asdict) == dict)

    ns.update({
        'one': 'override1',
        'three': {'four': 'override2'},
    })
    assert(ns.one == 'override1')
    assert(ns.three.four == 'override2')

    assert(
        str(ns) ==
        "{'one': 'override1', 'three': {'four': 'override2'}, 'two': 700}"
    )

    ns.update(Namespace({
        'one': 'override3',
        'three': {'four': 'override4'},
    }))
    assert(ns.one == 'override3')
    assert(ns.three.four == 'override4')

    ns.three = {'four': 'override5'}
    assert(ns.three.four == 'override5')

    nso = Namespace(OrderedDict([('one', 100), ('two', 200)]))
    assert(
        str(nso) ==
        "OrderedDict([('one', 100), ('two', 200)])"
    )

    oit = iter(nso)
    key, value = next(oit)
    assert(key == 'one' and value == 100)

    key, value = next(oit)
    assert(key == 'two' and value == 200)
