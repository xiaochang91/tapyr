# -*- coding: utf-8 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.PAP.
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
#    GTW.OMP.PAP.Subject_has_Property
#
# Purpose
#    Base class for link between Subject and some other object
#
# Revision Dates
#     3-Feb-2010 (CT) Creation
#    19-Feb-2010 (MG) `left.auto_cache` removed
#    28-Feb-2010 (CT) `desc` defined with `Computed_Mixin`
#     9-Feb-2011 (CT) `right.ui_allow_new` set to `True`
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    22-Mar-2012 (CT) Change from `_Person_has_Property_` to
#                     `Subject_has_Property`
#    12-Sep-2012 (CT) Set `right.role_type` to `Property`
#    12-Sep-2012 (CT) Add `auto_cache_np`, `auto_derive_np` to `left`, `right`
#    17-Apr-2013 (CT) Use `Computed_Set_Mixin`, not `Computed_Mixin`
#    15-May-2013 (CT) Rename `auto_cache_np` to `auto_rev_ref_np`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _MOM.import_MOM             import *
from   _GTW                        import GTW
from   _GTW._OMP._PAP              import PAP

import _GTW._OMP._PAP.Entity
import _GTW._OMP._PAP.Property
import _GTW._OMP._PAP.Subject

from   _TFL.I18N                   import _

_Ancestor_Essence = PAP.Link2

class Subject_has_Property (_Ancestor_Essence) :
    """Link a %(left.role_name)s to a %(right.role_name)s"""

    is_partial  = True
    is_relevant = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """%(left.role_type.ui_name)s linked to %(right.role_type.ui_name)s"""

            role_type           = PAP.Subject
            auto_rev_ref_np     = True
            auto_derive_np      = True

        # end class left

        class right (_Ancestor.right) :
            """%(right.role_type.ui_name)s of %(left.role_type.ui_name.lower())s"""

            role_type           = PAP.Property
            auto_rev_ref_np     = True
            auto_derive_np      = True
            ui_allow_new        = True

        # end class right

        class desc (A_String) :
            """Short description of the link"""

            kind                = Attr.Optional
            Kind_Mixins         = (Attr.Computed_Set_Mixin, )
            max_length          = 20
            ui_name             = _("Description")

            completer           = Attr.Completer_Spec  (1)

            def computed (self, obj) :
                return getattr (obj.right, self.name, "")
            # end def computed

        # end class desc

    # end class _Attributes

# end class Subject_has_Property

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Subject_has_Property
