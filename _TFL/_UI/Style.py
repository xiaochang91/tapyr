# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    Style
#
# Purpose
#    Provide style objects for abstract UI
#
# Revision Dates
#    25-Jan-2005 (CT)  Creation
#    26-Jan-2005 (CT)  `Style` converted from function to object to allow
#                      `add` and `Style.xxx`
#    26-Jan-2005 (BRU) Added style attributes to `_allowed`, comments
#    27-Jan-2005 (CT)  s/_allowed/_names/g
#    15-Feb-2005 (BRU) Added allowed values to `_values` where appropriate
#    17-Feb-2005 (RSC) Added example doctest for callbacks
#    21-Feb-2005 (CT)  Fixed style crimes committed on 15-Feb-2005
#    21-Feb-2005 (CT)  `arrow` added to `_values.mouse_cursor`
#    ��revision-date�����
#--

"""
>>> Style ("foo", font_style = "normal")
<Style foo>
>>> cb = lambda x : 1
>>> Style ("rightclick", callback = {'click3' : cb })
<Style rightclick>
>>> Style ("fool", font_style = "normalique")
Traceback (most recent call last):
  ...
ValueError: <Style fool> doesn't allow value `normalique` for `font_style`
"""

from   _TFL                    import TFL
import _TFL._Meta.M_Data_Class
import _TFL._Meta.Object
import _TFL._UI

from   predicate               import dict_from_list

class M_Style (TFL.Meta.M_Data_Class) :
    """Meta class used for generating style objects (which are implemented by
       real classes).
    """

    class _names (TFL.Meta.M_Data_Class._names) :
        ### this class must define the names of all valid style attributes

        background     = None # "orange", "#FF2F1F"
        callback       = None
        font_family    = None
        font_size      = None
        font_style     = None
        foreground     = None # "red"   , "#FF2F1F"
        mouse_cursor   = None
        underline      = None

    # end class _names

    class _values (TFL.Meta.M_Data_Class._values) :

        font_family    = dict_from_list (("Monospace", "Sans"))
        font_style     = dict_from_list (("normal", "oblique", "italic"))
        font_size      = dict_from_list \
            ( ( "xx-small", "x-small", "small"
              , "medium"
              , "large", "x-large", "xx-large"
              )
            )

        mouse_cursor   = dict_from_list \
            ( ( "arrow", "crosshair", "default", "fleur", "hand"
              , "hourglass", "text", "watch"
              )
            )

        underline      = dict_from_list (("single", "double", "low", "none"))

    # end class _values

# end class M_Style

class Style (TFL.Meta.Object) :

    def __call__ (self, name, * parents, ** kw) :
        """Returns new style with `name` derived from `parents` with attributes
           given by `kw`.
        """
        return M_Style (name, parents, kw)
    # end def __call__

    def add (self, name, * parents, ** kw) :
        """Add new style with `name` derived from `parents` with attributes
           given by `kw`.
        """
        if hasattr (self, name) :
            raise NameError, "Style %s already defined" % name
        result = self (name, * parents, ** kw)
        setattr (self, name, result)
        return result
    # end def add

# end class Style

Style = Style ()

if __name__ != "__main__" :
    TFL.UI._Export ("*", "Style")
### __END__ Style
