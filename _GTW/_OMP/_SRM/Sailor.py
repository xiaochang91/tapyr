# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.SRM.
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
#    GTW.OMP.SRM.Sailor
#
# Purpose
#    Model a sailor
#
# Revision Dates
#    15-Apr-2010 (CT) Creation
#     7-May-2010 (CT) `club` added
#     9-Feb-2011 (CT) `Sailor.left.ui_allow_new` set to `True`
#     7-Sep-2011 (CT) `completer` added to `nation`, `mna_number`, and `club`
#     7-Sep-2011 (CT) `club` changed from `Optional` to `Primary_Optional`
#     9-Sep-2011 (CT) `completer` re-added to `mna_number`,
#                     `completer` removed from `nation`
#    23-Sep-2011 (CT) `club` changed from `A_String` to `A_Id_Entity`
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    20-Jan-2012 (CT) Change `mna_number` from `A_String` to `A_Int`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _GTW                     import GTW
from   _MOM.import_MOM          import *

from   _GTW._OMP._SRM.Attr_Type import *

import _GTW._OMP._PAP.Person

import _GTW._OMP._SRM.Club
import _GTW._OMP._SRM.Entity

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SRM.Link1

class Sailor (_Ancestor_Essence) :
    """A person that is member of a sailing club."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :

            role_type          = GTW.OMP.PAP.Person
            ui_allow_new       = True

            completer          = Attr.E_Completer_Spec (Attr.Selector.primary)

        # end class left

        class nation (A_Nation) :
            """Nation for which the sailor sails."""

            kind               = Attr.Primary_Optional

        # end class nation

        class mna_number (A_Int) :
            """Membership number in Member National Authorities (MNA)."""

            kind               = Attr.Primary_Optional
            completer          = Attr.Completer_Spec  (1, Attr.Selector.primary)
            min_value          = 0
            max_value          = 999999
            needs_raw_value    = True
            css_align          = "right"

        # end class mna_number

        class club (A_Id_Entity) :
            """Club the sailor is starting for."""

            P_Type             = GTW.OMP.SRM.Club
            kind               = Attr.Primary_Optional

        # end class club

    # end class _Attributes

# end class Sailor

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Sailor
