# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2006 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
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
#    TFL.CDG.Struct
#
# Purpose
#    Root class for class modelling C structs.
#
# Revision Dates
#    11-Jul-2005 (MG)  Creation (Factored from TTA.FTC.TDFT_Data)
#    12-Jul-2005 (MG)  `__new__`: use `super` for upchaining
#    14-Jul-2005 (MG)  `Typedef` added
#    14-Jul-2005 (MG)  `__new__` changed to use `super`
#    14-Jul-2005 (MG)  `add_typedef` added
#     6-Sep-2005 (MPH) Missing `import traceback` added
#    09-Nov-2005 (MG)  `dict` added
#    11-Nov-2005 (MG)  Check for a list in `dict` added
#    11-Nov-2005 (MG)  Handling of the `reference_field` extended
#    01-Dec-2005 (MG)  `typedef_prefix` added
#    02-Dec-2005 (MG)  Use `type_name` instead of `__name__`
#    02-Dec-2005 (MG)  `Struct.as_c_code` changed to handle `Struct` classes
#                      as `struct_fields`
#    06-Dec-2005 (MZO) added optional parameter index to current
#    04-Jan-2006 (MZO) added buffer_name_tail
#    20-Jan-2006 (CED) made `packed` byte-order aware
#    23-Jan-2006 (CED) `format_and_values` sets `self.alignment`
#    10-Feb-2006 (PGO) Error detection added to `format_and_values`
#    13-Feb-2006 (MZO) added `null_termination`
#    19-Feb-2006 (CED) `aligned_and_padded`, `atoms` added
#    23-Feb-2006 (CED) Use `rounded_up` instead of home-grown code
#    ««revision-date»»···
#--

from   _TFL                           import TFL
import _TFL._Meta.Object
import _TFL._Meta.Property
import _TFL._SDG._C
from   _TFL.predicate                 import *
import  struct
import traceback

class Typedef (TFL.Meta.Object) :
    """Generate a new typedef used by the data structures."""

    def __init__ (self, type, name) :
        self.type = type
        self.name = name
    # end def __init__

    def as_typedef (self, C = TFL.SDG.C, c_node = None, ** kw) :
        """Returns a typedef (using `C` as name-space for the C classes. `C`
           should be a subpackage of `TFL.SDG.C`).

           If a `c_node` is passed in, the `result` will be added to it.
        """
        result = C.Typedef (self.type, self.name, ** kw)
        if c_node :
            c_node.add (result)
        return result
    # end def as_typedef

# end class Typedef

class Struct (TFL.Meta.Object) :
    """Root class for classes modelling C structs of the table-driven FT-Com
       Layer.

       Each descendent class must define a list `struct_fields' containing
       `Struct_Field' instances.
    """

    ### Set the __metaclass__ attribute a new M_Struct class, e.g.:
    ### __metaclass__      = TFL.CDG.M_Struct.New ("TDFT")

    buffer_name_format     = "%(cls_name)s_buffer"
    buffer_name_tail       = ""

    __autowrap             = dict \
      ( add_typedef        = TFL.Meta.Class_Method
      , as_c_code          = TFL.Meta.Class_Method
      , as_forward_typedef = TFL.Meta.Class_Method
      , as_typedef         = TFL.Meta.Class_Method
      , buffer_name        = TFL.Meta.Class_Method
      , current            = TFL.Meta.Class_Method
      , _struct_fields     = staticmethod
      )

    reference_field    = None
    struct_fields      = ()

    uses_global_buffer = False
    is_solitaire       = False
    const              = True

    def __new__ (cls, * args, ** kw) :
        result        = super (Struct, cls).__new__ (cls, * args,  ** kw)
        for sf in result.struct_fields :
            setattr (result, sf.name, sf.init)
        return result
    # end def __new__

    def as_forward_typedef (cls, C = TFL.SDG.C, c_node = None, ** kw) :
        """Returns a typedef for a struct-object (using `C` as name-space for
           the C classes. `C` should be a subclass of `TFL.SDG.C`).

           If a `c_node` is passed in, the `result` will be added to it.
        """
        name   = cls.type_name
        result = C.Typedef ("struct _%s" % name, name, ** kw)
        if c_node :
            c_node.add (result)
        return result
    # end def as_forward_typedef

    def as_c_code (cls, C = TFL.SDG.C, ** kw) :
        """Returns c-code for the definition of C.Struct for `self`"""
        fields   = []
        for f in cls.struct_fields :
            if not isinstance (f, TFL.CDG.Struct_Field) :
                print "Add struct to struct"
                c_field = "%s %s" % (f.type_name, f.__name__.lower ())
            else :
                c_field = f.as_c_code (C)
            fields.append (c_field)
        return C.Struct \
            ( cls.type_name
            , fields
            , description = cls.__doc__
            , ** kw
            )
    # end def as_c_code

    def as_typedef (cls, C = TFL.SDG.C, c_node = None, ** kw) :
        """Returns a typedef for a struct-object (using `C` as name-space for
           the C classes. `C` should be a subclass of `TFL.SDG.C`).

           If a `c_node` is passed in, the `result` will be added to it.
        """
        result = C.Typedef (cls.as_c_code (C), ** kw)
        if c_node :
            c_node.add (result)
        return result
    # end def as_typedef

    def add_typedef (cls, type, name) :
        cls.needs_typedef.append (Typedef (type, name))
    # end def add_typedef

    def buffer_name (cls) :
        name = getattr (cls, "buffer_field_name", None)
        if name is None :
            d = dict (cls_name = cls.type_name)
            name = cls.buffer_name_format % d
            name = name.lower ()
        buffer_name = "%s%s" % (name.lower (), cls.buffer_name_tail)
        return buffer_name
    # end def buffer_name

    def current (cls, index = None) :
        if index is None :
            index = cls.count
        if cls.reference_field.index :
            result = index
        else :
            result = "& (%s [%3d])" % (cls.buffer_name (), index)
        return result
    # end def current

    def packed (self, byte_order = "native") :
        """Returns a string containing a binary representation of the actual
           value of the struct's attributes.
        """
        format, values = self.format_and_values ()
        bo_map         = self.struct_fields [0].bo_map
        try :
            result = struct.pack \
                ( "%s%s"
                % (bo_map [byte_order], format)
                , * values
                )
        except :
            traceback.print_exc ()
            print self.__class__.__name__, format, values
            raise
        return result
    # end def packed

    def format_and_values (self) :
        values  = []
        formats = []
        for f in self.struct_fields :
            value  = getattr (self, f.name)
            format = f.format_code ()
            if format :
                ### `value` is a primitive data type
                formats.append (format)
                if isinstance (value, (list, tuple)) :
                    values.extend (value)
                else :
                    values.append (value)
            else :
                ### `value` is a `Struct` or sequence of `Struct`
                if isinstance (value, Struct) :
                    value = (value, )
                elif not isinstance (value, (tuple, list)) :
                    raise TypeError \
                        ( "No valid format found for %s.%s"
                        % (self.type_name, f.name)
                        )
                for v in value :
                    format, value = v.format_and_values ()
                    formats.append  (format)
                    values.extend   (value)
        format         = "".join (formats)
        ### Since we use a byte_order marker in `packed`,
        ### `struct` does not align (see python doc).
        ### So we must manually add pad bytes
        format         = self.aligned_and_padded (format)
        self.alignment = struct.calcsize (self.atoms (format).next ())
        return format, values
    # end def format_and_values

    def aligned_and_padded (self, format) :
        result = []
        offset = 0
        for atom in self.atoms (format) :
            size = struct.calcsize (atom)
            gap  = rounded_up (offset, size) - offset
            if gap :
                result.append ("%dx" % gap)
            result.append (atom)
            offset += (gap + size)
        return "".join (result)
    # def aligned_and_padded

    def atoms (self, format) :
        current = []
        for c in format :
            current.append (c)
            if not c.isdigit () :
                yield "".join (current)
                current = []
    # def atoms

    def dict (self) :
        result = {}
        for f in self.struct_fields :
            value  = getattr       (self, f.name)
            if f.bounds is not None :
                raise TypeError, "C-Code generation does not support Arrays"
            if f.user_code or f.fmt_code.get (f.type, None) :
                ### `value` is a primitive data type
                result [f.name] = value
            else :
                ### `value` is another struct or an array of structs
                if isinstance (value, Struct) :
                    result [f.name] = value.dict ()
                elif isinstance (value, list) :
                    result [f.name] = [v.dict () for v in value]
                else  :
                    result [f.name] = value
        return result
    # end def dict

    @classmethod
    def null_termination (cls) :
        result = {}
        for f in cls.struct_fields :
            result [f.name] = "0"
        return result
    # end def null_termination

# end class Struct

if __name__ != "__main__" :
    import _TFL._CDG
    TFL.CDG._Export ("*")
### __END__ TFL.CDG.Struct
