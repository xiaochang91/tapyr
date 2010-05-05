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
#    GTW.__test__.SAS_Sorted_By
#
# Purpose
#    Test the SAS function for sorting by attributes of a composite using the
#    SAS backend.
#
# Revision Dates
#    30-Apr-2010 (MG) Creation
#    ��revision-date�����
#--

_composite = r"""
    >>> scope = Scaffold.scope ("sqlite://")
    Creating new scope MOMT__SAS__SAS in memory
    >>> EVT = scope.EVT
    >>> SWP = scope.SWP
    >>> p1 = SWP.Page ("event-1-text", text = "Text for the 1. event")
    >>> p2 = SWP.Page ("event-2-text", text = "Text for the 2. event")
    >>> e1 = EVT.Event \
    ...     (p1.epk_raw, dict (start = "1.2.2010", raw = True), raw = True)
    >>> e2 = EVT.Event \
    ...     (p2.epk_raw, dict (start = "1.1.2010", raw = True), raw = True)
    >>> for e in EVT.Event.query ().all () : print e
    ((u'event-1-text', ), dict (start = '2010/02/01'), dict ())
    ((u'event-2-text', ), dict (start = '2010/01/01'), dict ())
    >>> q = EVT.Event.query ().order_by (TFL.Sorted_By (Q.date.start))
    >>> for e in q.all () : print e
    ((u'event-2-text', ), dict (start = '2010/01/01'), dict ())
    ((u'event-1-text', ), dict (start = '2010/02/01'), dict ())
"""

_link1_role = r"""
    >>> scope = Scaffold.scope ("sqlite://")
    Creating new scope MOMT__SAS__SAS in memory
    >>> EVT = scope.EVT
    >>> SWP = scope.SWP
    >>> p1 = SWP.Page ("event-1-text", text = "Text for the 1. event")
    >>> p2 = SWP.Page ("event-2-text", text = "Text for the 2. event")
    >>> e1 = EVT.Event \
    ...     (p1.epk_raw, dict (start = "1.2.2010", raw = True), raw = True)
    >>> e2 = EVT.Event \
    ...     (p2.epk_raw, dict (start = "1.1.2010", raw = True), raw = True)
    >>> q = EVT.Event_occurs.query ()
    >>> for e in q.all () : print e ### default sort order
    (((u'event-1-text', ), dict (start = '2010/02/01'), dict ()), '2010/02/01', dict ())
    (((u'event-2-text', ), dict (start = '2010/01/01'), dict ()), '2010/01/01', dict ())
    >>> q = EVT.Event_occurs.query ().order_by (TFL.Sorted_By (Q.event.date.start))
    >>> for e in q.all () : print e ### sorted
    (((u'event-2-text', ), dict (start = '2010/01/01'), dict ()), '2010/01/01', dict ())
    (((u'event-1-text', ), dict (start = '2010/02/01'), dict ()), '2010/02/01', dict ())
"""

_link2_link1 = r"""
    >>> scope = Scaffold.scope ("sqlite://")
    Creating new scope MOMT__SAS__SAS in memory
    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> bc  = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> b   = SRM.Boat.instance_or_new (u'Optimist', "AUT", "1107", raw = True)
    >>> p   = PAP.Person.instance_or_new ("Tanzer", "Christian")
    >>> s   = SRM.Sailor.instance_or_new (p.epk_raw, nation = "AUT", mna_number = "29676", raw = True) ### 1
    >>> rev = SRM.Regatta_Event (dict (start = "20080501", raw = True), u"Himmelfahrt", raw = True)
    >>> reg = SRM.Regatta_C     (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)

    >>> rev = SRM.Regatta_Event (dict (start = "20090521", raw = True), u"Himmelfahrt", raw = True)
    >>> reg = SRM.Regatta_C     (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)

    >>> rev = SRM.Regatta_Event (dict (start = "20100513", raw = True), u"Himmelfahrt", raw = True)
    >>> reg = SRM.Regatta_C     (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)

    >>> q = scope.SRM.Boat_in_Regatta.query ()
    >>> for r in q.order_by (Q.right.left.date.start) : print r
    (((u'Optimist', ), 'AUT', 1107), ((dict (start = '2008/05/01'), u'Himmelfahrt'), (u'Optimist', )))
    (((u'Optimist', ), 'AUT', 1107), ((dict (start = '2009/05/21'), u'Himmelfahrt'), (u'Optimist', )))
    (((u'Optimist', ), 'AUT', 1107), ((dict (start = '2010/05/13'), u'Himmelfahrt'), (u'Optimist', )))
    >>> q = scope.SRM.Boat_in_Regatta.query ()
    >>> for r in q.order_by (TFL.Sorted_By ("-right.left.date.start")) : print r
    (((u'Optimist', ), 'AUT', 1107), ((dict (start = '2010/05/13'), u'Himmelfahrt'), (u'Optimist', )))
    (((u'Optimist', ), 'AUT', 1107), ((dict (start = '2009/05/21'), u'Himmelfahrt'), (u'Optimist', )))
    (((u'Optimist', ), 'AUT', 1107), ((dict (start = '2008/05/01'), u'Himmelfahrt'), (u'Optimist', )))
"""

if 0 :
    __test__ = dict \
        ( composite   = _composite
        , link1_role  = _link1_role
        , link2_link1 = _link2_link1
        )
else :
    #__doc__ = _composite
    __doc__ = _link2_link1
    def test () :pass
    #test .__doc__ = __doc__

from _GTW.__test__.model import *
from _MOM.import_MOM     import Q

if __name__ == "__main__" :
    import doctest, SAS_Sorted_By
    TFL.Environment.exec_python_startup ()
    exec (doctest.testsource (SAS_Sorted_By, "SAS_Sorted_By.test"))
    BIR = scope.SRM.Boat_in_Regatta._etype
    R   = scope.SRM.Regatta._etype
    RE  = scope.SRM.Regatta_Event._etype

    BIRs = BIR._sa_table
    Rs   = R._sa_table
    REs  = RE._sa_table

    E    = scope.ems.session.execute
    q = BIR._SAS.select.select_from (BIRs.join (Rs).join (REs))
    print q
### __END__ GTW.__test__.SAS_Sorted_By
