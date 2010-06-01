# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.__test__.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.__test__.Person
#
# Purpose
#    Test PAP.Person creation and querying
#
# Revision Dates
#    27-Apr-2010 (CT) Creation
#    ��revision-date�����
#--

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP

    >>> print PAP.Person.count
    0
    >>> PAP.Person.instance_or_new ("Tanzer", "Christian") ### 1
    GTW.OMP.PAP.Person (u'tanzer', u'christian', u'', u'')
    >>> print PAP.Person.count
    1
    >>> PAP.Person.instance ("Tanzer", "Christian")
    GTW.OMP.PAP.Person (u'tanzer', u'christian', u'', u'')
    >>> PAP.Person.query_s ().all ()
    [GTW.OMP.PAP.Person (u'tanzer', u'christian', u'', u'')]

    >>> PAP.Person.instance_or_new ("Tanzer", "Christian") ### 2
    GTW.OMP.PAP.Person (u'tanzer', u'christian', u'', u'')
    >>> print PAP.Person.count
    1

"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ MOM.__test__.Person