# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.NAV.E_Type.
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
#    GTW.NAV.E_Type._Mgr_Base_
#
# Purpose
#    Common base class for Admin and Manager of GTW.NAV.E_Type
#
# Revision Dates
#    20-Jan-2010 (CT) Creation
#     5-Mar-2010 (CT) `page_args` added
#    15-Mar-2010 (CT) `kind_filter` and `kind_name` removed
#    17-Mar-2010 (CT) Derived from `GTW.NAV.E_Type.Mixin`
#    19-Mar-2010 (CT) Call to `scope.async_changes` removed from `_get_entries`
#    22-Mar-2010 (CT) Use `_T (name)`, not `_Tn (name)` for `title`
#    12-Apr-2010 (CT) `_get_entries` factored to `Mixin`
#    21-Jun-2010 (MG) Once property `ETM` added
#    10-Jan-2011 (CT) `_Mgr_Base_` changed to use `sanitized_filename` on `name`
#     9-Sep-2011 (CT) Use `.E_Type` instead of `._etype`
#    14-Nov-2011 (CT) Factored `_Query_Mixin_`, add `query_restriction`
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._NAV.Base
import _GTW._NAV._E_Type.Mixin

import _TFL.Ascii
import _TFL.Filter

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.I18N                import _, _T, _Tn

class _Query_Mixin_ (GTW.NAV.E_Type.Mixin) :
    """Mixin for GTW.NAV.E_Type classes using `query`"""

    query_restriction = None

    @property
    def count (self) :
        if self.query_filters :
            result = self.query ().count ()
        else :
            result = self.ETM.count
        return result
    # end def count

    def query (self) :
        result = self.ETM.query \
            (* self.query_filters, sort_key = self.sort_key)
        if self.query_restriction is not None :
            result = self.query_restriction (result)
        return result
    # end def query

# end class _Query_Mixin_

class _Mgr_Base_ (_Query_Mixin_) :
    """Common base class for Admin and Manager of GTW.NAV.E_Type."""

    def __init__ (self, parent, ** kw) :
        ETM = kw ["ETM"]
        if isinstance (ETM, basestring) :
            kw ["_ETM"] = ETM
            E_Type      = self.top.App_Type [ETM]
            del kw ["ETM"]
        else :
            E_Type  = ETM.E_Type
        title       = kw.pop  ("title",       _T (E_Type.__doc__))
        name        = kw.pop  ("name",        E_Type.ui_name)
        short_title = kw.pop  ("short_title", _T (name))
        self.__super.__init__ \
            ( E_Type       = E_Type
            , name         = TFL.Ascii.sanitized_filename (unicode (name))
            , parent       = parent
            , short_title  = short_title
            , title        = title
            , ** kw
            )
    # end def __init__

    @Once_Property
    def ETM (self) :
        return self.scope [self._ETM]
    # end def ETM

# end class _Mgr_Base_

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("_Mgr_Base_", "_Query_Mixin_")
### __END__ GTW.NAV.E_Type._Mgr_Base_
