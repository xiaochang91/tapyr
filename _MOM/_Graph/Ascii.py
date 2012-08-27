# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.Graph.
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
#    MOM.Graph.Ascii
#
# Purpose
#    ASCII renderer for MOM graphs
#
# Revision Dates
#    19-Aug-2012 (CT) Creation
#    26-Aug-2012 (CT) Add `Canvas.line`, `Ascii.render_link`
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM                   import MOM
from   _TFL                   import TFL

import _MOM._Graph._Renderer_
import _MOM._Graph.Entity
import _MOM._Graph.Relation

from   _TFL.predicate         import pairwise
from   _TFL._D2               import D2, Cardinal_Direction as CD
import _TFL._D2.Point
import _TFL._D2.Rect

import _TFL._Meta.Object
import _TFL._Meta.Once_Property

class Canvas (TFL.Meta.Object) :
    """Canvas for ASCII renderer"""

    def __init__ (self, max_x, max_y) :
        self._body = list ([" "] * max_x for i in range (max_y))
    # end def __init__

    def line (self, line, chars = {}) :
        h, t = line
        d    = t - h
        if d.x == 0 :
            return self._line_v (line, chars.get ("y"))
        elif d.y == 0 :
            return self._line_h (line, chars.get ("x"))
        else :
            print ("Slanted line [%s -> %s] not implemented " % (h, t))
    # end def line

    def rectangle (self, rect) :
        self._line_h (rect.top)
        self._line_h (rect.bottom)
        self._line_v (rect.left)
        self._line_v (rect.right)
        for p in rect.corners :
            self [p] = "+"
    # end def rectangle

    def rendered (self) :
        return "\n".join ("".join (l).rstrip () for l in self._body)
    # end def rendered

    def text (self, p, v) :
        self [p] = v
    # end def text

    def _line_h (self, line, char = None) :
        if char is None :
            char = "-"
        head, tail = line
        assert head.y == tail.y
        if head.x > tail.x :
            head, tail = tail, head
        l = int (tail.x - head.x)
        self [head] = char * l
    # end def _line_h

    def _line_v (self, line, char = None) :
        if char is None :
            char = "|"
        head, tail = line
        assert head.x == tail.x
        if head.y > tail.y :
            head, tail = tail, head
        x, y = head
        while y <= tail.y :
            self [x, y] = char
            y += 1
    # end def _line_v

    def __setitem__ (self, key, value) :
        if value :
            x, y = tuple (int (k) for k in key)
            l    = len (value)
            line = self._body [y]
            line [x : x+l] = list (value)
    # end def __setitem__

# end class Canvas

class Renderer (MOM.Graph._Renderer_) :
    """ASCII renderer for MOM.Graph"""

    Canvas             = Canvas
    node_size          = D2.Point (16,  4) ### in characters
    default_grid_scale = D2.Point ( 2,  3)

    conn_chars         = dict \
        ( bottom       = "v"
        , left         = "<"
        , right        = ">"
        , top          = "^"
        )
    link_chars         = dict \
        ( Attr         = dict (x = "_", y = ":")
        , Is_A         = dict (x = ".", y = ".")
        , Role         = dict (x = "-", y = "|")
        )
    rect_chars         = dict \
        ( bottom       = "-"
        , left         = "|"
        , right        = "|"
        , top          = "-"
        )

    def render (self) :
        self.__super.render ()
        return self.canvas.rendered ()
    # end def render

    def render_link (self, link, canvas) :
        chars = self.link_chars [link.relation.kind]
        head  = link.points [ 0]
        tail  = link.points [-1]
        side  = link.relation.source_connector [0].side
        for line in pairwise (link.points) :
            canvas.line (line, chars = chars)
        for p in link.points [1:-1] :
            canvas.text (p, "+")
        canvas.text (head, self.conn_chars [side])
        canvas.text (tail, self.conn_chars [side])
    # end def render_link

# end class Renderer

if __name__ != "__main__" :
    MOM.Graph._Export_Module ()
### __END__ MOM.Graph.Ascii