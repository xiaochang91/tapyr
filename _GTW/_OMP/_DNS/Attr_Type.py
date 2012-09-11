# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Dr. Ralf Schlatterbeck All rights reserved
# Reichergasse 131, A-3411 Weidling, Austria. rsc@runtux.com
# #*** <License> ************************************************************#
# This module is part of the package FFM.
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
#    FFM.Attr_Type
#
# Purpose
#    Define attribute types for package FFM
#
# Revision Dates
#    27-Aug-2012 (RS) Creation
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _MOM.import_MOM          import *
from   _MOM.import_MOM          import _A_Composite_, _A_Named_Value_
from   _MOM.import_MOM          import _A_Unit_, _A_Int_
from   _GTW._OMP._DNS           import DNS
from   _TFL.I18N                import _
from   _TFL.Regexp              import Regexp

class A_DNS_Time (_A_Unit_, _A_Int_) :
    """ Allow specification of DNS times in other units than seconds """

    typ             = _ ("DNS Time")
    needs_raw_value = True
    min_value       = 0
    max_value       = 2147483647
    _unit_dict      = dict \
        ( seconds   = 1
        , minutes   = 60
        , hours     = 60 * 60
        , days      = 60 * 60 * 24
        , weeks     = 60 * 60 * 24 * 7
        )

# end class A_DNS_Time

class A_DNS_Name (Syntax_Re_Mixin, A_String) :
    """ DNS name consisting of labels separated by '.'
        See rfc1034 for details.
    """

    max_length      = 253
    ignore_case     = True
    syntax          = _ \
        ( u"DNS name must consist of up to 127 labels. A label starts"
           " with a letter and is optionally followed by letters,"
           " digits or dashes. A label may be up to 63 characters long."
        )
    _label          = r"[a-z][-a-z0-9]{0,62}"
    _syntax_re      = Regexp \
        (r"%s([.]%s){0,126}" % (_label, _label))

# end class A_DNS_Name

if __name__ != "__main__" :
    GTW.OMP.DNS._Export ("*")
### __END__ GTW.OMP.DNS.Attr_Type