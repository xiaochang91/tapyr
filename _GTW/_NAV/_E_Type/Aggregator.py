# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
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
#    GTW.NAV.E_Type.Aggregator
#
# Purpose
#    Navigation page aggregating the most recent instances of one or more E_Types
#
# Revision Dates
#    12-Apr-2010 (CT) Creation
#    ��revision-date�����
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._NAV.Base
import _GTW._NAV._E_Type.Mixin

from   _MOM.import_MOM          import Q

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import first

from   posixpath                import join  as pjoin

import datetime

class Aggregator (GTW.NAV.E_Type.Mixin, GTW.NAV.Page) :
    """Navigation page aggregating the most recent instances of one or more
       E_Types.
    """

    query_limit = 25
    template    = "e_type_aggregator"

    class Instance (TFL.Meta.Object) :
        """Model a specific instance in the context of an aggregation page
           for one or more E_Types.
        """

        def __init__ (self, admin, obj) :
            self.admin = admin
            self.obj   = obj
            self.FO    = GTW.FO (obj, admin.top.encoding)
        # end def __init__

        def __getattr__ (self, name) :
            return getattr (self.obj, name)
        # end def __getattr__

    # end class Instance

    Page = Instance

    def __init__ (self, parent, ** kw) :
        ETMS = []
        for ETM in kw ["ETMS"] :
            if isinstance (ETM, basestring) :
                ETM = parent.scope [ETM]
            ETMS.append (ETM)
        kw ["ETMS"] = ETMS
        self.__super.__init__ (parent, ** kw)
        #self.prefix = pjoin (self.parent.prefix, self.name)
    # end def __init__

    def query (self) :
        result = []
        for ETM in self.ETMS :
            r = ETM.query \
                (* self.query_filters, sort_key = self.sort_key)
            if self.query_limit :
                r = r.limit (self.query_limit)
            result.append (r)
        result = TFL.Q_Result_Composite (result)
        result.order_by (self.sort_key)
        if self.query_limit :
            result.limit (self.query_limit)
        return result
    # end def query

    @Once_Property
    def query_filters (self) :
        result = list (self.__super.query_filters)
        result.append (Q.date.alive)
        return tuple  (result)
    # end def query_filters

    def rendered (self, handler, template = None) :
        objects = self._get_entries ()
        handler.context.update \
            ( calendar = getattr (self.top.SC, "Cal", None)
            , objects  = objects
            )
        return self.__super.rendered (handler, template)
    # end def rendered

# end class Aggregator

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Aggregator