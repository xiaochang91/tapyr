# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.__test__.
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
#    Composite_as_Primary_Optional
#
# Purpose
#    Use composits as primary optional attributes
#
# Revision Dates
#    21-Apr-2010 (MG) Creation
#    ��revision-date�����
#--
"""
    >>> scope = Scope ()
    Creating new scope MOMT__Hash__HPS in memory
    >>> EVT = scope.EVT
    >>> SWP = scope.SWP
    >>> event_page = SWP.Page ("2010-01-01-00:00", text = U"An event")
    >>> event = EVT.Event     (event_page)
    >>> event.date
    MOM.Date_Interval ()
    >>> event.destroy         ()
    >>> event_raw = EVT.Event (event_page.epk_raw, raw = True)
    >>> event_raw.date
    MOM.Date_Interval ()
"""

from _GTW.__test__.model import MOM, GTW, Scope

### __END__ GTW.__test__.Composite_as_Primary_Optional
