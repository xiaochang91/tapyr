# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.DBW.SAW.PG.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.DBW.SAW.PG.Sequence
#
# Purpose
#    Wrap a PostgreSQL sequence
#
# Revision Dates
#    24-Jun-2013 (CT) Creation
#    26-Jul-2013 (CT) Redefine `_reserve`, not `reserve`
#    28-Jul-2013 (CT) Quote `seq_name` in `SELECT setval`; fix typo
#    ��revision-date�����
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _MOM       import MOM
from   _TFL       import TFL

from   _TFL.pyk   import pyk

import _MOM._DBW
import _MOM._DBW._SAW._PG.DBS
import _MOM._DBW._SAW.Sequence

class _SAW_PG_Sequence_ (MOM.DBW.SAW._SAW_Sequence_S_) :
    """Wrap a PostgreSQL sequence"""

    _real_name          = "Sequence"

    def _reserve (self, conn, value) :
        result = self.__super._reserve (conn, value)
        stmt   = "SELECT setval('%s', %d)" % (self.seq_name, value)
        conn.execute (stmt)
        return result
    # end def _reserve

Sequence = _SAW_PG_Sequence_ # end class

if __name__ != "__main__" :
    MOM.DBW.SAW.PG._Export ("*")
### __END__ MOM.DBW.SAW.PG.Sequence
