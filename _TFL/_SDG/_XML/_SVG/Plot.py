# -*- coding: utf-8 -*-
# Copyright (C) 2017 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package TFL.SDG.XML.SVG.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    TFL.SDG.XML.SVG.Plot
#
# Purpose
#    Provide classes to build data plots in SVG
#
# Revision Dates
#     2-Mar-2017 (CT) Creation
#     4-Apr-2017 (CT) Use `Parameters`, not `Definition`, in doctest
#    11-Apr-2017 (CT) Add `x_range_s`, `y_range_s` to `add_grid`
#    11-Apr-2017 (CT) Add `Parameters.x_sub_tick_len` and friends
#    11-Apr-2017 (CT) Support multi-line labels in `x_labels`, `y_labels`
#    13-Apr-2017 (CT) Put sub-ticks on both sides
#    26-May-2017 (CT) Add `Parameters.color.background`
#    26-May-2017 (CT) Add support for thin sub-tick grid lines
#    28-May-2017 (CT) Fix support for thin sub-tick grid lines
#                     (use `!=`, not `<`)
#    ««revision-date»»···
#--

from   __future__  import absolute_import
from   __future__  import division
from   __future__  import print_function
from   __future__  import unicode_literals

from   _TFL                       import TFL

from   _TFL.Color                 import RGB_X
from   _TFL.formatted_repr        import formatted_repr
from   _TFL.Parameters            import Definition, P, P_dict
from   _TFL.portable_repr         import portable_repr
from   _TFL.pyk                   import pyk
from   _TFL._D2                   import Transform as T
from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL._SDG._XML._SVG        import SVG

import _TFL._Meta.Object
import _TFL._SDG._XML._SVG.Document
import _TFL.Accessor
import _TFL.Decorator

import operator

class Frame_Axis (TFL.Meta.Object) :
    """Model an axis of a frame of reference.

    .. attribute:: min

      Coordinate of left or top corner of frame

    .. attribute:: max

      Coordinate of right or bottom corner of frame

    .. attribute:: offset

      Offset of frame relative to it's container

    .. attribute:: size

      Width or height of frame

    """

    _max    = None
    _size   = None

    def __init__ (self, min, max = None, size = None, offset = 0) :
        self.min    = min
        self.offset = offset
        if max is None and size is None :
            raise TypeError \
                ("%s needs either `max` or `size`" % self.__class__.__name__)
        if max is not None :
            self._max  = max
        if size is not None :
            self._size = size
    # end def __init__

    @Once_Property
    def max (self) :
        result = self._max
        if result is None :
            result = self.min + self.size
        return result
    # end def max

    @Once_Property
    def size (self) :
        result = self._size
        if result is None :
            result = self.max - self.min
        return result
    # end def size

    def __repr__ (self) :
        args = [("min", self.min), ("size", self.size)]
        if self.offset :
            args.append (("offset", self.offset))
        return "%s (%s)" % \
            ( self.__class__.__name__
            , ", ".join ("%s = %s" % (k, portable_repr (v)) for k, v in args)
            )
    # end def __repr__

# end class Frame_Axis

class Frame (TFL.Meta.Object) :
    """Model a frame of reference for x, y."""

    def __init__ (self, x, y) :
        self.x = x
        self.y = y
    # end def __init__

    def __repr__ (self) :
        return "%s (%r, %r)" % (self.__class__.__name__, self.x, self.y)
    # end def __repr__

# end class Frame

class _Coordinate_Op_ (TFL.Meta.Object) :
    """Arithmetic operation on coordinates."""

    _op_map         = dict \
        ( add       = "+"
        , div       = "/"
        , floordiv  = "/"
        , mod       = "%"
        , mul       = "*"
        , sub       = "-"
        , truediv   = "/"
        )

    def __new__ (cls, lhs, rhs, op) :
        if lhs.__class__ == rhs.__class__ :
            return lhs.__class__ (op (lhs.value, rhs.value))
        result = cls.__c_super.__new__ (cls)
        result._init_ (lhs, rhs, op)
        return result
    # end def __new__

    def _init_ (self, lhs, rhs, op) :
        self.lhs = lhs
        self.rhs = rhs
        self.op  = op
    # end def _init_

    @property
    def op_symbol (self) :
        name = self.op.__name__.strip ("_")
        return self._op_map.get (name, repr (name))
    # end def op_symbol

    @property
    def _CC (self) :
        def find_CT (lhs, rhs) :
            for s in (lhs, rhs) :
                if isinstance (s, _World_Coordinate_) :
                    return WC
            for s in (lhs, rhs) :
                if isinstance (s, _Coordinate_Op_) :
                    result = find_CT (s.lhs, s.rhs)
                    if result is WC :
                        return result
            return DC
        CT = find_CT (self.lhs, self.rhs)
        return getattr (CT, self.lhs.name.upper ())
    # end def _CC

    def as_length (self, vp) :
        return self.op (self.lhs.as_length (vp), self.rhs.as_length (vp))
    # end def as_length

    def as_pos (self, vp) :
        return self.op (self.lhs.as_pos (vp), self.rhs.as_pos (vp))
    # end def as_pos

    def __add__ (self, rhs) :
        return _Coordinate_Op_ (self, self._CC (rhs), operator.__add__)
    __radd__ = __add__ # end def

    def __mul__ (self, rhs) :
        return _Coordinate_Op_ (self, DC.x (rhs), operator.__mul__)
    __rmul__ = __mul__ # end def

    def __rsub__ (self, lhs) :
        return _Coordinate_Op_ (self._CC (lhs), self, operator.__sub__)
    # end def __rsub__

    def __sub__ (self, rhs) :
        return _Coordinate_Op_ (self, self._CC (rhs), operator.__sub__)
    # end def __sub__

    def __repr__ (self) :
        return "%r %s %r" % (self.lhs, self.op_symbol, self.rhs)
    # end def __repr__

# end class _Coordinate_Op_

@pyk.adapt__bool__
@pyk.adapt__div__
class _Coordinate_ (TFL.Meta.Object) :
    """Base class for classes that model a single coordinate (x or y)."""

    name = None

    def __new__ (cls, value = 0.0) :
        if isinstance (value, (_Coordinate_, _Coordinate_Op_)) :
            return value
        result = cls.__c_super.__new__ (cls)
        result._init_ (value)
        return result
    # end def __new__

    def _init_ (self, value = 0.0) :
        self.value = value
    # end def _init_

    def as_length (self, vp) :
        return self.value * abs (self.scaling_factor (vp))
    # end def as_length

    def as_pos (self, vp) :
        sf = self.scaling_factor (vp)
        wo = self.window_offset  (vp)
        result = (self.value - wo) * sf
        return result
    # end def as_pos

    def __add__ (self, rhs) :
        return _Coordinate_Op_ (self, self.__class__ (rhs), operator.__add__)
    __radd__ = __add__ # end def

    def __bool__ (self) :
        return bool (self.value)
    # end def __bool__

    def __floordiv__ (self, rhs) :
        return self.__class__ (self.value // rhs)
    # end def __floordiv__

    def __mul__ (self, rhs) :
        return self.__class__ (self.value * rhs)
    __rmul__ = __mul__ # end def

    def __neg__ (self) :
        return self.__class__ (- self.value)
    # end def __neg__

    def __repr__ (self) :
        return "%s (%s)" % (self.__class__.__name__, self.value)
    # end def __repr__

    def __rsub__ (self, lhs) :
        return _Coordinate_Op_ (self.__class__ (lhs), self, operator.__sub__)
    # end def __rsub__

    def __sub__ (self, rhs) :
        return _Coordinate_Op_ (self, self.__class__ (rhs), operator.__sub__)
    # end def __sub__

    def __truediv__ (self, rhs) :
        return self.__class__ (self.value / rhs)
    # end def __truediv__

    def __rtruediv__ (self, lhs) :
        DCT = getattr (DC, self.name.upper ())
        return _Coordinate_Op_ (DCT (lhs), self, operator.__truediv__)
    # end def __rtruediv__

# end class _Coordinate_

class _Coordinate_Pair_ (TFL.Meta.Object) :
    """Base class for classes that model a x, y pair of coordinates."""

    def __new__ (cls, pair) :
        if isinstance (pair, _Coordinate_Pair_) :
            return pair
        result = cls.__c_super.__new__ (cls)
        result._init_ (pair)
        return result
    # end def __new__

    def _init_ (self, pair) :
        self.pair = pair
    # end def _init_

    @Once_Property
    def x (self) :
        result = self.pair [0]
        if not isinstance (result, _Coordinate_) :
            result = self.X (result)
        return result
    # end def x

    @Once_Property
    def y (self) :
        result = self.pair [0]
        if not isinstance (result, _Coordinate_) :
            result = self.Y (result)
        return result
    # end def y

    def as_pos (self, vp) :
        return (self.x.as_pos (vp), self.y.as_pos (vp))
    # end def as_pos

    def __repr__ (self) :
        return "%s (%s)" % (self.__class__.__name__, self.pair)
    # end def __repr__

# end class _Coordinate_Pair_

class _Device_Coordinate_ (_Coordinate_) :
    """Base class for single x or y device coordinates."""

    def scaling_factor (self, vp) :
        return 1.0
    # end def scaling_factor

    def window_offset (self, vp) :
        return 0.0
    # end def window_offset

# end class _Normalized_Coordinate_

class _Normalized_Coordinate_ (_Device_Coordinate_) :
    """Base class for single x or y normalized ([0, 1]) coordinates."""

    def scaling_factor (self, vp) :
        fa = getattr (vp.frame, self.name)
        return fa.size
    # end def scaling_factor

# end class _Normalized_Coordinate_

class _World_Coordinate_ (_Coordinate_) :
    """Base class for single x or y world coordinates."""

    def scaling_factor (self, vp) :
        fa = getattr (vp.frame,  self.name)
        w  = getattr (vp.window, self.name)
        return fa.size / w.size
    # end def scaling_factor

    def window_offset (self, vp) :
        w = getattr (vp.window, self.name)
        return w.min
    # end def window_offset

# end class _World_Coordinate_

class DC_x (_Device_Coordinate_) :
    """Device coordinate for x."""

    name = "x"

# end class DC_x

class DC_y (_Device_Coordinate_) :
    """Device coordinate for y."""

    name = "y"

# end class DC_y

class DC (_Coordinate_Pair_) :
    """Pair of x, y device coordinates."""

    X    = DC_x
    Y    = DC_y

# end class DC

class NC_x (_Normalized_Coordinate_) :
    """Normalized viewport coordinate for x."""

    name = "x"

# end class NC_x

class NC_y (_Normalized_Coordinate_) :
    """Normalized viewport coordinate for y."""

    name = "y"

# end class NC_y

class NC (_Coordinate_Pair_) :
    """Pair of x, y normalized viewport coordinates."""

    X    = NC_x
    Y    = NC_y

# end class NC

class WC_x (_World_Coordinate_) :
    """World coordinate for x."""

    name = "x"

# end class WC_x

class WC_y (_World_Coordinate_) :
    """World coordinate for y."""

    name = "y"

# end class WC_y

class WC (_Coordinate_Pair_) :
    """Pair of x, y world coordinates."""

    X    = WC_x
    Y    = WC_y

# end class WC

class _Plot_Element_ (TFL.Meta.Object) :
    """Base classes for plot elements mapping to SVG."""

    def add (self, svg_element, * els) :
        self.svg.add (svg_element, * els)
        return svg_element
    # end def add

    def _create_svg (self, frame, ** kwds) :
        if frame.x.offset :
            kwds ["x"] = frame.x.offset
        if frame.y.offset :
            kwds ["y"] = frame.y.offset
        view_box = "%d %d %d %d" % \
            (frame.x.min, frame.y.min, frame.x.size, frame.y.size)
        result   = self.SVG_T (view_box = view_box, ** kwds)
        return result
    # end def _create_svg

# end class _Plot_Element_

class Plot (_Plot_Element_) :
    """Define a data plot using SVG.

    >>> plot = Plot (100, 80, P = Parameters ())
    >>> plot.frame
    Frame (Frame_Axis (min = 0, size = 100), Frame_Axis (min = 0, size = 80))

    >>> vp   = plot.add_viewport (60, 40, wc_x_min = 1, wc_x_max = 13, wc_y_min = 0, wc_y_max = 1)

    >>> vp.frame
    Frame (Frame_Axis (min = 0, size = 60, offset = 20), Frame_Axis (min = 0, size = 40, offset = 20))
    >>> vp.window
    Frame (Frame_Axis (min = 1, size = 12), Frame_Axis (min = 1, size = -1))

    >>> DC.X (0.25).as_length (vp)
    0.25

    >>> NC.X (0.0).as_pos (vp), NC.X (1.0).as_pos (vp), NC.X (1.0).as_length (vp)
    (0.0, 60.0, 60.0)
    >>> NC.Y (0.0).as_pos (vp), NC.Y (1.0).as_pos (vp), NC.Y (1.0).as_length (vp)
    (0.0, 40.0, 40.0)

    >>> for x in range (2, 13) :
    ...     print (portable_repr ((x, WC.X (x).as_pos (vp))))
    (2, 5)
    (3, 10)
    (4, 15)
    (5, 20)
    (6, 25)
    (7, 30)
    (8, 35)
    (9, 40)
    (10, 45)
    (11, 50)
    (12, 55)

    >>> for v in range (2, 10, 2) :
    ...     y = v / 10.
    ...     print (portable_repr ((y, WC.Y (y).as_pos (vp))))
    (0.2, 32)
    (0.4, 24)
    (0.6, 16)
    (0.8,  8)

    >>> for op in (WC.X (6) + 5, WC.X (6) + DC.X (5), WC.X (6) + NC.X (0.1)) :
    ...     print (op, "-->", op.as_pos (vp))
    WC_x (11) --> 50.0
    WC_x (6) + DC_x (5) --> 30.0
    WC_x (6) + NC_x (0.1) --> 31.0

    >>> for m in (2, 3, 4) :
    ...     for op in (WC.X (2) * m, DC.X (2) * m) :
    ...         print (op, "-->", op.as_pos (vp))
    WC_x (4) --> 15.0
    DC_x (4) --> 4.0
    WC_x (6) --> 25.0
    DC_x (6) --> 6.0
    WC_x (8) --> 35.0
    DC_x (8) --> 8.0

    >>> for op in (WC.X (3) + 2 + 2 + DC_x (5), WC.X (3) + DC_x (5), WC.X (3) + DC_x (5) + 4) :
    ...     print (op, "-->", op.as_pos (vp))
    WC_x (7) + DC_x (5) --> 35.0
    WC_x (3) + DC_x (5) --> 15.0
    WC_x (3) + DC_x (5) + WC_x (4) --> 30.0

    """

    SVG_T = SVG.SVG

    def __init__ (self, width, height, P, ** kwds) :
        self.frame = frame = Frame \
            (x = Frame_Axis (0, width), y = Frame_Axis (0, height))
        self.P   = P
        self.svg = self._create_svg (frame, ** kwds)
    # end def __init__

    def add_viewport \
            ( self
            , width    = None, height   = None
            , margin_l = None, margin_t = None
            , margin_r = None, margin_b = None
            , ** kwds
            ) :
        frame    = self.frame
        vp_frame = Frame \
            ( self._viewport_frame_axis (frame.x, width,  margin_l, margin_r)
            , self._viewport_frame_axis (frame.y, height, margin_t, margin_b)
            )
        result   = Viewport (self, vp_frame, ** kwds)
        self.add (result.svg)
        return result
    # end def add_viewport

    def _viewport_frame_axis (self, fa, size, margin_1, margin_2) :
        if size is None :
            if margin_1 is None :
                if not margin_2 :
                    margin_1 = margin_2 = self.P.line_height * 4.0
                else :
                    margin_1 = 0
            size = fa.size - margin_1 - margin_2
        elif margin_1 is None :
            margin_1 = 0 if margin_2 else (fa.size - size) / 2.0
        return Frame_Axis (min = 0, size = size, offset = margin_1)
    # end def _viewport_frame_axis

# end class Plot

class Root_Plot (Plot) :
    """Define a data plot using the SVG root element"""

    SVG_T = SVG.Root

    def _create_svg \
            ( self, frame
            , preserve_aspect_ratio = "xMinYMin"
            , want_document         = True
            , ** kwds
            ) :
        result = self.__super._create_svg \
             (frame, preserve_aspect_ratio = preserve_aspect_ratio, ** kwds)
        if want_document :
            result = SVG.Document \
                ( result
                , encoding    = "utf-8"
                , standalone  = False
                )
        return result
    # end def _create_svg

# end class Root_Plot

class Viewport (_Plot_Element_) :
    """Viewport of a SVG plot."""

    SVG_T                = SVG.SVG

    _length_attr_map     = dict \
        ( dx             = WC.X
        , dy             = WC.Y
        , font_size      = DC.Y
        , height         = WC.Y
        , marker_width   = DC.X
        , marker_height  = DC.Y
        , path_length    = DC.X
        , r              = WC.X
        , ref_x          = WC.X
        , ref_y          = WC.Y
        , rx             = WC.X
        , ry             = WC.Y
        , start_offset   = WC.Y
        , stroke_width   = DC.X
        , width          = WC.X
        )

    _pos_attr_map        = dict \
        ( cx             = WC.X
        , cy             = WC.Y
        , fx             = WC.X
        , fy             = WC.Y
        , x              = WC.X
        , x1             = WC.X
        , x2             = WC.X
        , y              = WC.Y
        , y1             = WC.Y
        , y2             = WC.Y
        )

    def __init__ \
            ( self, plot, frame
            , wc_x_min = 0.0, wc_x_max = 1.0
            , wc_y_min = 0.0, wc_y_max = 1.0
            , ** kwds
            ) :
        self.plot    = plot
        self.frame   = frame
        self.P       = P = plot.P
        font_family  = kwds.pop ("font_family",  P.font_family)
        font_size    = kwds.pop ("font_size",    P.font_size)
        stroke_width = kwds.pop ("stroke_width", P.stroke_width)
        self.window  = Frame \
            ( x = Frame_Axis (wc_x_min, wc_x_max)
            , y = Frame_Axis (wc_y_max, wc_y_min)
                ### plot y-coordinate grows from bottom to top
                ### svg  y-coordinate grows from top to bottom
                ### --> interchange wc_y_min and wc_y_max
            )
        self.svg           = self.group \
            ( fill         = "none"
            , font_family  = font_family
            , font_size    = font_size
            , stroke_width = stroke_width
            , transform    = T.Translate (frame.x.offset, frame.y.offset)
            , ** kwds
            )
        self.inner_svg     = SVG.SVG \
            ( height       = frame.y.size
            , width        = frame.x.size
            , x            = 0
            , y            = 0
            )
        self.svg.add (self.inner_svg)
    # end def __init__

    def add (self, svg_element, * els) :
        self.inner_svg.add (svg_element, * els)
        return svg_element
    # end def add

    def add_grid \
            ( self, x_range, y_range
            , font_size    = None
            , label_x      = True
            , label_y      = True
            , P            = None
            , x_len        = None
            , y_len        = None
            , x_range_s    = None
            , y_range_s    = None
            ) :
        """Add a grid of x- and y-lines at points in `x_range` and `y_range`."""
        P      = self.P if P is None else P
        x1     = NC.X (0.0)
        x2     = NC.X (1.0)
        y1     = NC.Y (0.0)
        y2     = NC.Y (1.0)
        sw     = P.stroke_width
        if font_size is None :
            font_size = P.font_size
        if x_len is None :
            x_len   = x2
            x_len_s = P.x_sub_tick_len
        else :
            x_len_s = x_len / (P.x_tick_len / P.x_sub_tick_len)
        if y_len is None :
            y_len   = y2
            y_len_s = P.y_sub_tick_len
        else :
            y_len_s = y_len / (P.y_tick_len / P.y_sub_tick_len)
        frame  = self.frame
        result = self.group \
            ( font_size    = font_size * 1.5
            , klass        = "axes"
            , stroke       = P.color.axis
            )
        self.svg.add (result)
        result.add \
            (self.rect (x1, y1, x2, y2, stroke_width = sw * 1.5))
        if x_range_s :
            for xi in x_range_s :
                if y_len_s != y2 :
                    result.add (self.line (xi, y1, xi, y_len_s))
                    result.add (self.line (xi, y2, xi, y2 - y_len_s))
                else :
                    result.add \
                        (self.line (xi, y1, xi, y_len_s, stroke_width = sw / 2.))
        for xi in x_range :
            result.add (self.line (xi, y1, xi, y_len))
        if y_range_s :
            for yi in y_range_s :
                if x_len_s != x2 :
                    result.add (self.line (x1, yi, x_len_s, yi))
                    result.add (self.line (x2, yi, x2 - x_len_s, yi))
                else :
                    result.add \
                        (self.line (x1, yi, x_len_s, yi, stroke_width = sw / 2.))
        for yi in y_range :
            result.add (self.line (x1, yi, x_len, yi))
        if label_x :
            result.add \
                ( self.x_labels
                    (x_range, (formatted_repr (xi) for xi in x_range))
                )
        if label_y :
            result.add \
                ( self.y_labels
                    (y_range, (formatted_repr (yi) for yi in y_range))
                )
        return result
    # end def add_grid

    def circle (self, cx, cy, r, ** kwds) :
        """Add a circle with center (x, y) and radius `r` to the plot."""
        self._convert_kwds (kwds)
        result = SVG.Circle \
            ( cx     = WC.X (cx).as_pos   (self)
            , cy     = WC.Y (cy).as_pos   (self)
            , r      = WC.X (r).as_length (self)
            , ** kwds
            )
        return result
    # end def circle

    def ellipse (self, cx, cy, rx, ry, ** kwds) :
        """Add an ellipse with center (x, y) and axes (rx, ry) to the plot."""
        self._convert_kwds (kwds)
        result = SVG.Circle \
            ( cx     = WC.X (cx).as_pos    (self)
            , cy     = WC.Y (cy).as_pos    (self)
            , rx     = WC.X (rx).as_length (self)
            , ry     = WC.X (ry).as_length (self)
            , ** kwds
            )
        return result
    # end def ellipse

    def group (self, * args, ** kwds) :
        """Add a SVG group to the plot."""
        return self._svg_element (SVG.Group, args, kwds)
    # end def group

    def image (self, * args, ** kwds) :
        """Add a SVG image element to the plot."""
        return self._svg_element (SVG.Image, args, kwds)
    # end def image

    def line (self, x1, y1, x2, y2, ** kwds) :
        """Add a line from (x1, y1) to (x2, y2) to the plot."""
        self._convert_kwds (kwds)
        result = SVG.Line \
            ( x1 = WC.X (x1).as_pos (self)
            , y1 = WC.Y (y1).as_pos (self)
            , x2 = WC.X (x2).as_pos (self)
            , y2 = WC.Y (y2).as_pos (self)
            , ** kwds
            )
        return result
    # end def line

    def marker (self, * args, ** kwds) :
        """Add a SVG marker element to the plot."""
        return self._svg_element (SVG.Marker, args, kwds)
    # end def Marker

    def path (self, points, ** kwds) :
        """Add a SVG path element through `points` to the plot."""
        self._convert_kwds (kwds)
        result = SVG.Path  (d = self._converted_points (points), ** kwds)
        return result
    # end def polygon

    def polygon (self, points, ** kwds) :
        """Add a polygon through `points` to the plot."""
        self._convert_kwds (kwds)
        result = SVG.Polygon (points = self._converted_points (points), ** kwds)
        return result
    # end def polygon

    def polyline (self, points, ** kwds) :
        """Add a polyline through `points` to the plot."""
        self._convert_kwds (kwds)
        result = SVG.Polyline \
            (points = self._converted_points (points), ** kwds)
        return result
    # end def polyline

    def rect (self, x, y, width, height, ** kwds) :
        """Add a rect at (x, y) with `width` and `height` to the plot."""
        self._convert_kwds (kwds)
        is_wc  = isinstance (y, (int, float))
        height = WC.Y (height).as_length (self)
        width  = WC.X (width).as_length  (self)
        x      = WC.X (x).as_pos  (self)
        y      = WC.Y (y).as_pos  (self)
        if is_wc and self.window.y.size < 0 :
            y = max (y - height, 0.0)
        result = SVG.Rect \
            (x = x, y = y, width = width, height = height, ** kwds)
        return result
    # end def rect

    def svg_elem (self, x, y, width, height, ** kwds) :
        """Add a nested svg element at (x, y) with `width` and `height` to the plot."""
        self._convert_kwds (kwds)
        result = SVG.SVG \
            ( x      = WC.X (x).as_pos         (self)
            , y      = WC.Y (y).as_pos         (self)
            , width  = WC.X (width).as_length  (self)
            , height = WC.Y (height).as_length (self)
            , ** kwds
            )
        return result
    # end def svg_elem

    def text (self, * args, ** kwds) :
        """Add a SVG text element to the plot."""
        return self._svg_element (SVG.Text, args, kwds)
    # end def text

    def text_path (self, * args, ** kwds) :
        """Add a SVG text-path element to the plot."""
        return self._svg_element (SVG.Text_Path, args, kwds)
    # end def text_path

    def tspan (self, * args, ** kwds) :
        """Add a SVG tspan element to the plot."""
        return self._svg_element (SVG.Tspan, args, kwds)
    # end def tspan

    def use (self, * args, ** kwds) :
        """Add a SVG use element to the plot."""
        return self._svg_element (SVG.Use, args, kwds)
    # end def use

    def x_labels \
            ( self, x_range, x_labels
            , dx           = 0
            , dy           = None
            , fill         = None
            , klass        = "x labels"
            , stroke_width = 0
            , text_anchor  = "begin"
            , y            = NC.Y (1.0)
            , ** kwds
            ) :
        P = self.P
        result = self.group \
            ( fill         = P.color.axis_text if fill is None else fill
            , klass        = klass
            , stroke_width = stroke_width
            , text_anchor  = text_anchor
            , ** kwds
            )
        if dy is None :
            dy = DC.Y (P.line_height)
        dyd = DC.Y (P.line_height) * 1.25
        for xi, x_label in zip (x_range, x_labels) :
            xls = x_label.split ("\n")
            dyi = dy
            for xl in xls :
                result.add (self.text (xl, dx = dx, dy = dyi, x = xi, y = y))
                dyi += dyd
        return result
    # end def x_labels

    def y_labels \
            ( self, y_range, y_labels
            , dx           = None
            , dy           = None
            , fill         = None
            , klass        = "y labels"
            , stroke_width = 0
            , text_anchor  = "end"
            , x            = NC.X (0.0)
            , ** kwds
            ) :
        P = self.P
        result = self.group \
            ( fill         = P.color.axis_text if fill is None else fill
            , klass        = klass
            , stroke_width = stroke_width
            , text_anchor  = text_anchor
            , ** kwds
            )
        if dx is None :
            dx = - DC.X (P.font_char_width)
        if dy is None :
            dy = DC.Y (P.font_size * 0.25)
        dyd = DC.Y (P.line_height) * 1.25
        for yi, y_label in zip (y_range, y_labels) :
            yls = y_label.split ("\n")
            dyi = dy
            for yl in yls :
                result.add (self.text (yl, dx = dx, dy = dyi, x = x, y = yi))
                dyi -= dyd
        return result
    # end def y_labels

    def _converted_points (self, points) :
        return tuple \
            (   (WC.X (x).as_pos (self), WC.Y (y).as_pos (self))
            for (x, y) in points
            )
    # end def _converted_points

    def _converted_view_box (self, view_box) :
        result = view_box
        if isinstance (result, (list, tuple)) :
            x, y, w, h = result
            result = tuple \
                ( WC.X (x).as_pos    (self)
                , WC.Y (y).as_pos    (self)
                , WC.X (w).as_length (self)
                , WC.Y (h).as_length (self)
                )
        return result
    # end def _converted_view_box

    def _convert_kwds (self, kwds) :
        l_map = self._length_attr_map
        p_map = self._pos_attr_map
        for k, v in list (pyk.iteritems (kwds)) :
            if k == "view_box" :
                kwds [k] = self._converted_view_box (v)
            elif k in l_map :
                kwds [k] = l_map [k] (v).as_length (self)
            elif k in p_map :
                kwds [k] = p_map [k] (v).as_pos    (self)
    # end def _convert_kwds

    def _svg_element (self, SVG_T, args, kwds) :
        self._convert_kwds (kwds)
        result = SVG_T     (* args, ** kwds)
        return result
    # end def _svg_element

# end class Viewport

@TFL.eval_function_body
class Parameters (Definition) :
    """Default parameters for SVG renderer."""

    class color (Definition) :

        axis                = RGB_X     ("#AAAAAA")
        axis_text           = RGB_X     ("#0088DD")
        background          = RGB_X     ("#FFFFFF")
        color_map_text      = RGB_X     ("#888888")
        symbol              = RGB_X     ("#0088DD")
        text                = RGB_X     ("#000033")

    # end class color

    font_family             = "sans-serif"
    font_size               = 5
    font_char_width         = P.font_size   / 2.0
    line_height             = P.font_size   * 1.5
    stroke_width            = 0.25
    symbol_size             = 2.5
    x_sub_tick_len          = P.x_tick_len / 2.0
    y_sub_tick_len          = P.y_tick_len / 2.0
    x_tick_len              = DC.Y (4.0)
    y_tick_len              = DC.X (4.0)

# end class Parameters

if __name__ != "__main__" :
    TFL.SDG.XML.SVG._Export_Module ()
### __END__ TFL.SDG.XML.SVG.Plot
