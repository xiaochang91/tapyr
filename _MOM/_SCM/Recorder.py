# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.SCM.Recorder
#
# Purpose
#    Recorder of changes in a MOM scope
#
# Revision Dates
#     7-Oct-2009 (CT) Creation (factored from TOM.SCM.Recorder)
#    17-Dec-2009 (CT) Use `tracker.add_change` instead of home-grown code
#    ««revision-date»»···
#--

from   _MOM          import MOM
from   _TFL          import TFL

import _MOM._SCM

import _TFL._Meta.Object

import weakref

class Recorder (TFL.Meta.Object) :
    """Recorder of changes in a MOM scope"""

    weight = 0

    def __init__ (self, tracker) :
        self.tracker = weakref.proxy (tracker)
    # end def __init__

    def __call__ (self, Change, * args, ** kw) :
        pass
    # end def __call__

    def update (self, dependents) :
        pass
    # end def update

# end class Recorder

class Ignorer (Recorder) :
    """Ignores all changes in a MOM scope"""
# end class Ignorer

class Counter (Recorder) :
    """Counter of changes in a MOM scope"""

    weight = 1

    def __call__ (self, Change, * args, ** kw) :
        self.__super.__call__ (Change, * args, ** kw)
        self.tracker.change_count += 1
    # end def __call__

    def update (self, dependents) :
        for d in dependents :
            d.historian.change_count += 1
            d.historian.count_change ()
    # end def update

# end class Counter

class Appender (Counter) :
    """Appends changes in a MOM scope to a history list and counts them"""

    weight = 10

    def __call__ (self, Change, * args, ** kw) :
        self.__super.__call__   (Change, * args, ** kw)
        change = Change         (* args, ** kw)
        self.tracker.add_change (change)
        return change
    # end def __call__

# end class Appender

if __name__ != "__main__" :
    MOM.SCM._Export ("*")
### __END__ MOM.SCM.Recorder
