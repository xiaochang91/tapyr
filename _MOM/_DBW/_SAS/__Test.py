# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package MOM.DWB.SAS.
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
#    MOM.DWB.SAS__Test
#
# Purpose
#    Base test during development
#
# Revision Dates
#    11-Feb-2010 (MG) Creation
#    24-Feb-2010 (CT) s/Lifetime/Date_Interval/
#    ��revision-date�����
#--

from _MOM.__doc__ import *

from _MOM._EMS.SAS          import Manager as EMS
from _MOM._DBW._SAS.Manager import Manager as DBW

from _MOM._EMS.Hash         import Manager as HEMS
from _MOM._DBW._HPS.Manager import Manager as HDBW

apt  = MOM.App_Type (u"BMT",  BMT).Derived (EMS,   DBW)
#hapt = MOM.App_Type (u"HBMT", BMT).Derived (HEMS, HDBW)

scope = MOM.Scope.new (apt, "sqlite:///:memory:")
Ris   = scope.BMT.Rodent_is_sick
#scope = MOM.Scope.new (apt, "sqlite:///test.sqlite")
if 0 :
    m     = scope.BMT.Mouse   ("mouse")
    r     = scope.BMT.Rat     ("rat")
    t1   = scope.BMT.Trap     ("X", 1)
    t2   = scope.BMT.Trap     ("X", 2)

sr = scope.BMT.Mouse ("Sick_Rodent")
osm = Ris (sr, scope.MOM.Date_Interval (start = "20100218", raw = True))
osm.fever = 42

old_epk = osm.epk
print Ris.instance (* old_epk)
osm.sick_leave.set_raw (start = "2010/03/01")
print Ris.instance (* old_epk)

### __END__ MOM.DWB.SAS__Test
