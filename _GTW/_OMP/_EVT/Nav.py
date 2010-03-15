# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.EVT.
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
#    GTW.OMP.EVT.Nav
#
# Purpose
#    Provide configuration for GTW.NAV.E_Type.Admin entries
#
# Revision Dates
#    15-Mar-2010 (CT) Creation
#    ��revision-date�����
#--

from   _TFL                     import TFL
from   _GTW                     import GTW

import _GTW._NAV._E_Type.Admin
import _GTW._Form._MOM.Javascript

from   _GTW._Form._MOM.Inline_Description      import \
    ( Link_Inline_Description      as LID
    , Attribute_Inline_Description as AID
    )
from   _GTW._Form._MOM.Field_Group_Description import \
    ( Field_Group_Description as FGD
    , Field_Prefixer          as FP
    , Wildcard_Field          as WF
    )
from  _GTW._Form.Widget_Spec    import Widget_Spec as WS

from   _TFL.I18N                import _

primary = WF ("primary")

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    Event           =  dict \
        ( ETM       = "GTW.OMP.EVT.Event"
        , Type      = GTW.NAV.E_Type.Admin
        , Form_args =
            ( FGD ("object", "detail")
            , AID
                ( "date"
                , FGD (widget = "html/form.jnj, fg_tr")
                , legend =
                    _("Start (and optionally [for recurring events] finish) date")
                )
            , AID
                ( "time"
                , FGD (widget = "html/form.jnj, fg_tr")
                , legend = _("Start and finish time")
                )
            , AID
                ( "recurrence"
                , FGD ()
                , legend = _("Recurrence rule")
                )
            )
        )

    Event_occurs    = dict \
        ( ETM       = "GTW.OMP.EVT.Event_occurs"
        , Type      = GTW.NAV.E_Type.Admin
        , Form_args =
            ( AID
                ( "event"
                , FGD ("object", "detail", widget = "html/form.jnj, fg_tr")
                )
            , FGD ("date")
            , AID
                ( "time"
                , FGD (widget = "html/form.jnj, fg_tr")
                , legend = _("Start and finish time")
                )
            )
        )

# end class Admin

if __name__ != "__main__" :
    GTW.OMP.EVT._Export_Module ()
### __END__ GTW.OMP.EVT.Nav