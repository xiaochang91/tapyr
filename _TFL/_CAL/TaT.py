# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TaT
#
# Purpose
#    Model a recurrence (i.e., something happening Time-after-Time)
#
# Revision Dates
#    23-Oct-2004 (CT) Creation
#    25-Oct-2004 (CT) `TaT_Shifter` and `TaT_Alt_Shifter` added
#    25-Oct-2004 (CT) `TaT_Exception_Handler` renamed to `TaT_Conditioner`
#                     and changed to use `shifters`
#    25-Oct-2004 (CT) Doctests added
#    26-Oct-2004 (CT) `alt_iter` factored
#    ��revision-date�����
#--

from   _TFL                    import TFL
import _TFL._CAL
import _TFL._Meta.Object

from   predicate               import identity, alt_iter

class TaT_Shifter (TFL.Meta.Object) :
    """Model a TaT shifter

       >>> from _TFL._CAL.Date  import *
       >>> from _TFL._CAL.Delta import *
       >>> d = Date (2004, 10, 23)
       >>> ts_1_3  = TaT_Shifter (Date_Delta (days =  1), Date_Delta (days = 3))
       >>> ts__1_2 = TaT_Shifter (Date_Delta (days = -1), Date_Delta (days = 2))
       >>> [str (x) for x in ts_1_3 (d)]
       ['2004-10-24', '2004-10-25', '2004-10-26']
       >>> [str (x) for x in ts__1_2 (d)]
       ['2004-10-22', '2004-10-21']
    """

    def __init__ (self, delta, max_delta) :
        self.delta     = delta
        self.max_delta = max_delta
    # end def __init__

    def __call__ (self, date) :
        delta     = self.delta
        max_delta = abs (self.max_delta)
        next      = date
        while True :
            next  = next + delta
            if abs (next - date) > max_delta :
                raise StopIteration
            yield next
    # end def __call__

# end class TaT_Shifter

class TaT_Alt_Shifter (TFL.Meta.Object) :
    """Model a TaT alternating shifter

       >>> from _TFL._CAL.Date  import *
       >>> from _TFL._CAL.Delta import *
       >>> d = Date (2004, 10, 23)
       >>> ts_1_3  = TaT_Shifter (Date_Delta (days =  1), Date_Delta (days = 3))
       >>> ts__1_1 = TaT_Shifter (Date_Delta (days = -1), Date_Delta (days = 1))
       >>> tas = TaT_Alt_Shifter (ts_1_3, ts__1_1)
       >>> [str (x) for x in tas (d)]
       ['2004-10-24', '2004-10-22', '2004-10-25', '2004-10-26']
    """

    def __init__ (self, * shifters) :
        self.shifters = shifters
    # end def __init__

    def __call__ (self, date) :
        return alt_iter (* [s (date) for s in self.shifters])
    # end def __call__

# end class TaT_Alt_Shifter

class TaT_Conditioner (TFL.Meta.Object) :
    """Model a TaT conditioner

       >>> from _TFL._CAL.Date  import *
       >>> from _TFL._CAL.Delta import *
       >>> upper = Date (2004, 12, 31)
       >>> start = Date (2004, 10, 23)
       >>> ts_1_6  = TaT_Shifter (Date_Delta (days =  1), Date_Delta (days = 6))
       >>> ts__1_6  = TaT_Shifter (Date_Delta (days =  -1), Date_Delta (days = 6))
       >>> ts_1_3  = TaT_Shifter (Date_Delta (days =  1), Date_Delta (days = 3))
       >>> ts__1_3  = TaT_Shifter (Date_Delta (days =  -1), Date_Delta (days = 3))
       >>> for i in range (7) :
       ...   print i, TaT_Conditioner (lambda d : d.weekday == i, ts_1_6) (start)
       ...
       0 2004-10-25
       1 2004-10-26
       2 2004-10-27
       3 2004-10-28
       4 2004-10-29
       5 2004-10-23
       6 2004-10-24
       >>> for i in range (7) :
       ...     print i, TaT_Conditioner (lambda d : d.weekday == i, ts__1_6) (start)
       ...
       0 2004-10-18
       1 2004-10-19
       2 2004-10-20
       3 2004-10-21
       4 2004-10-22
       5 2004-10-23
       6 2004-10-17
       >>> tas = TaT_Alt_Shifter (ts_1_3, ts__1_3)
       >>> md = Month_Delta (1)
       >>> start = Date (2004, 1, 1)
       >>> for i in range (12) :
       ...     print start, TaT_Conditioner (lambda d : d.weekday == 0, tas) (start)
       ...     start = start + md
       ...
       2004-01-01 2003-12-29
       2004-02-01 2004-02-02
       2004-03-01 2004-03-01
       2004-04-01 2004-03-29
       2004-05-01 2004-05-03
       2004-06-01 2004-05-31
       2004-07-01 2004-06-28
       2004-08-01 2004-08-02
       2004-09-01 2004-08-30
       2004-10-01 2004-10-04
       2004-11-01 2004-11-01
       2004-12-01 2004-11-29
    """

    def __init__ (self, condition, * shifters) :
        self.condition = condition
        self.shifters  = shifters
    # end def __init__

    def __call__ (self, date) :
        condition = self.condition
        if condition (date) :
            return date
        else :
            for s in self.shifters :
                for r in s (date) :
                    if condition (r) :
                        return r
    # end def __call__

# end class TaT_Conditioner

class TaT (TFL.Meta.Object) :
    """Model a recurrence (i.e., something happening Time-after-Time)

       >>> from _TFL._CAL.Date  import *
       >>> from _TFL._CAL.Delta import *
       >>> upper = Date (2004, 12, 31)
       >>> start = Date (2004, 10, 23)
       >>> [str (t) for t in TaT (start, Month_Delta (1), upper)]
       ['2004-10-23', '2004-11-23', '2004-12-23']
       >>> [str (t) for t in TaT (start, Month_Delta (2), upper)]
       ['2004-10-23', '2004-12-23']
       >>> ts_1_3  = TaT_Shifter (Date_Delta (days =  1), Date_Delta (days = 3))
       >>> ts__1_3  = TaT_Shifter (Date_Delta (days =  -1), Date_Delta (days = 3))
       >>> tas = TaT_Alt_Shifter (ts_1_3, ts__1_3)
       >>> md = Month_Delta (1)
       >>> start = Date (2004, 1, 1)
       >>> upper = Date (2005, 1, 5)
       >>> is_monday = TaT_Conditioner (lambda d : d.weekday == 0, tas)
       >>> for x in TaT (start, md, upper, is_monday) :
       ...     print x
       ...
       2003-12-29
       2004-02-02
       2004-03-01
       2004-03-29
       2004-05-03
       2004-05-31
       2004-06-28
       2004-08-02
       2004-08-30
       2004-10-04
       2004-11-01
       2004-11-29
       2005-01-03
    """

    def __init__ (self, start, delta, upper, conditioner = identity) :
        self.start         = start
        self.delta         = delta
        self.upper         = upper
        self.conditioner   = conditioner
    # end def __init__

    def __iter__ (self) :
        delta         = self.delta
        upper         = self.upper
        conditioner   = self.conditioner
        next          = self.start
        while True :
            n = conditioner (next)
            if n > upper :
                break
            yield n
            next = next + delta
    # end def __iter__

# end class TaT

if __name__ != "__main__" :
    TFL.CAL._Export ("*")
### __END__ TaT
