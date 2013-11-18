# -*- coding: utf-8 -*-
# Copyright (C) 1998-2013 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    TFL.Functor
#
# Purpose
#    Encapsulate function with arguments
#
# Revision Dates
#    16-Aug-1998 (CT)  Creation
#     9-Aug-1999 (CT)  `__str__' added
#    10-Dec-1999 (CT)  `_doc' added
#    19-Jul-2000 (CT)  `** kw' added to `__call__'
#    19-Jul-2000 (CT)  `__str__' and `__repr__' taken from `Function'
#     3-Oct-2001 (CT)  Inherit from `_Function_`
#    29-Jun-2004 (CED) Doctest added
#    23-Sep-2004 (CT)  Cleanup
#    14-Feb-2006 (CT)  Moved into package `TFL`
#    21-Feb-2008 (MG) `Functor.__init__`:  simplified by using `kw.pop`
#    ««revision-date»»···
#--

from   __future__  import print_function

from   _TFL             import TFL
import _TFL.Function

class Functor (TFL.Function) :
    """
       >>> def foo (x) :
       ...     print (42 + x)
       ...
       >>> f = Functor (foo, x = 58)
       >>> f ()
       100
       >>> def bar (a, b, c) :
       ...     print ((a, b, c), )
       ...
       >>> f = Functor (bar, 3)
       >>> f (1, 2)
       (1, 2, 3)
       >>> f = Functor (bar, head_args = (1, 2))
       >>> f (3)
       (1, 2, 3)
    """

    Ancestor = __Ancestor = TFL.Function

    def __init__ (self, function, * tail_args, ** kw) :
        self.__Ancestor.__init__ (self, function, kw.pop ("_doc", None))
        self.head_args = kw.pop ("head_args", ())
        self.tail_args = tail_args
        self.kw        = kw
    # end def __init__

    def __call__ (self, * args, ** kw) :
        return self.function \
            ( *  (self.head_args + args + self.tail_args)
            , ** dict (kw, ** self.kw)
            )
    # end def __call__

    def __repr__ (self) :
        tail = ""
        kw   = self.kw
        if kw :
            tail = ", %s" % ", ".join \
                ("%s = %s" % (k, v) for (k, v) in sorted (kw.iteritems ()))
        return "%s (%s + %s + %s%s)" % \
            ( self.__Ancestor.__repr__ (self)
            , self.head_args, "<args>", self.tail_args, tail
            )
    # end def __repr__

    run = __call__

# end class Functor

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Functor
