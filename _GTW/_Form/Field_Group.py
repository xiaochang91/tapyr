# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.
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
#    GTW.Form.Field_Group
#
# Purpose
#    A field group which is bsaically a Field_Group_Description but with
#    field's which are `bound` to an object.
#
# Revision Dates
#    18-Jan-2010 (MG) Creation
#    29-Jan-2010 (MG) Reference to `field_group_description` added and
#                     `__getattr__` added to take undefined attrs from the
#                     `field_group_description`
#    ��revision-date�����
#--

from   _TFL                                 import TFL
import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL.NO_List

from   _GTW                                 import GTW
import _GTW._Form._MOM

class Field_Group (TFL.Meta.Object) :
    """A group of form field."""

    def __init__ (self, fields, field_group_description) :
        self.fields                  = TFL.NO_List         (fields)
        self.field_group_description = field_group_description
    # end def __init__

    @TFL.Meta.Once_Property
    def hidden_fields (self) :
        return [f for f in self.fields if     f.hidden]
    # end def hidden_fields

    @TFL.Meta.Once_Property
    def visible_fields (self) :
        return [f for f in self.fields if not f.hidden]
    # end def visible_fields

    def __getattr__ (self, name) :
        result = getattr (self.field_group_description, name)
        setattr (self, name, result)
        return result
    # end def __getattr__

# end class Field_Group

if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form.Field_Group
