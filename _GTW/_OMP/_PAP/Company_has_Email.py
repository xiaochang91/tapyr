# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2012 Mag. Christian Tanzer All rights reserved
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
#    GTW.OMP.PAP.Company_has_Email
#
# Purpose
#    Model the link between a company and an email address
#
# Revision Dates
#    22-Mar-2012 (CT) Creation
#    ��revision-date�����
#--

from   __future__            import unicode_literals

from   _MOM.import_MOM        import *
from   _GTW                   import GTW
from   _GTW._OMP._PAP         import PAP

import _GTW._OMP._PAP.Entity
from   _GTW._OMP._PAP.Company                import Company
from   _GTW._OMP._PAP.Subject_has_Email      import Subject_has_Email

_Ancestor_Essence = Subject_has_Email

class Company_has_Email (_Ancestor_Essence) :
    """Model the link between a company and an email address"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :

            role_type      = Company
            auto_cache     = "companies"

        # end class left

    # end class _Attributes

# end class Company_has_Email

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Company_has_Email