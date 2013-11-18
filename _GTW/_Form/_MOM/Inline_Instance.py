# -*- coding: utf-8 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.MOM.
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
#    Inline_Instance
#
# Purpose
#    Edit or create an MOM instance inside a form for a related MOM instance
#
# Revision Dates
#    19-Jan-2010 (MG) Creation
#     2-Feb-2010 (MG) `Lid_and_State_Field` added
#     3-Feb-2010 (MG) `widget` change to allow multiple field groups in one
#                     table row
#     3-Feb-2010 (MG) Unlinking of inline instances added
#     5-Feb-2010 (MG) `Attribute_Inline_Instance` and `Link_Inline_Instance`
#                     added
#     6-Feb-2010 (MG) `_Inline_Instance_.instances` advance the db_instance
#                     in any case
#     8-Feb-2010 (MG) `Lid_and_State_Field`: guard against entities which
#                     have no `lid` (An_Entity's)
#     9-Feb-2010 (MG) `Lid_and_State_Field.get_raw` fixed
#    10-Feb-2010 (MG) `_Inline_Instance_.instance` fixed to get correct
#                     instance for `An_Entity`
#    11-Feb-2010 (MG) Changed handling of instance to form assignment (to
#                     make sure that each posted form gets assing the correct
#                     instance)
#    22-Feb-2010 (MG) `_create_instance` added to `Attribute_Inline_Instance`
#    27-Feb-2010 (MG) `add_internal_fields` changed
#     6-Mar-2010 (MG) Error handling changed
#    11-Mar-2010 (MG) Use new `Attribute_Inline.instance_as_raw`
#    12-May-2010 (CT) Use `pid`, not `lid`
#    13-May-2010 (MG) `Pid_and_State` splitted into two fields, special css
#                     style applied to the electric fields
#    20-May-2010 (MG) `test_object` fixed
#    26-May-2010 (MG) `instance_or_fake` added to support redering of inline
#                     forms with errors
#    27-May-2010 (MG) Use new `on_error` for `cooked_attrs`
#    28-May-2010 (MG) `instance_or_fake` changed to fake the object only in
#                     case raw data for this for is present
#     1-Jun-2010 (MG) `initial_data` support added
#     9-Jun-2010 (MG) `initial_data.instance` can now be a callable
#     8-Aug-2010 (MG) State handling changed, inline `testing` changed
#    19-Aug-2010 (MG) `Collection_Inline_Instance` missing methods added
#    ««revision-date»»···
#--

from   _TFL                                 import TFL
import _TFL._Meta.Once_Property
from   _TFL.predicate                       import all_true
from   _GTW                                 import GTW
import _GTW._Form.Field
import _GTW._Form.Widget_Spec
import _GTW._Form._MOM
import _GTW._Form._MOM._Instance_

class Pid_Field (GTW.Form.Field) :
    """Stores the pid of edited entity."""

    hidden   = True
    electric = True
    widget   = GTW.Form.Widget_Spec ("html/field.jnj, hidden")

    def get_raw (self, form, defaults = {}) :
        return getattr (form.instance, "pid", "")
    # end def get_raw

# end class Pid_Field

class State_Field (GTW.Form.Field) :
    """Stores the state of the inline form."""

    hidden   = True
    electric = True
    widget   = GTW.Form.Widget_Spec ("html/field.jnj, hidden")

    def get_raw (self, form, defaults = {}) :
        return ""
    # end def get_raw

# end class State_Field

class M_Inline_Instance (GTW.Form.MOM._Instance_.__class__) :
    """Add additional internal fields"""

    def add_internal_fields (cls, et_man) :
        cls.__m_super.add_internal_fields (et_man)
        cls.pid_field   = Pid_Field   \
            ("_pid_",   et_man = et_man, css_class = cls.electric_fields_css)
        cls.state_field = State_Field \
            ("_state_", et_man = et_man, css_class = cls.electric_fields_css)
        cls.hidden_fields.append (cls.pid_field)
        cls.hidden_fields.append (cls.state_field)
    # end def add_internal_fields

# end class M_Inline_Instance

class _Inline_Instance_ (GTW.Form.MOM._Instance_) :
    """Base class for form which are part of a outer form."""

    __metaclass__       = M_Inline_Instance

    electric_fields_css = "mom-object"

    def __init__ ( self, * args, ** kw) :
        self.prototype = kw.pop ("prototype", False)
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    @TFL.Meta.Once_Property
    def pid (self) :
        return self.request_data.get (self.get_id (self.pid_field), "")
    # end def pid

    @TFL.Meta.Once_Property
    def state (self) :
        return self.request_data.get (self.get_id (self.state_field), "")
    # end def state

# end class _Inline_Instance_

class Attribute_Inline_Instance (_Inline_Instance_) :
    """Base class for attribute inline instances"""

# end class Attribute_Inline_Instance

class An_Attribute_Inline_Instance (Attribute_Inline_Instance) :
    """A form which handles an attribute of an An_Entity as a seperate form."""

    instance = None

    def get_object_raw (self, defaults = {}) :
        return dict (getattr (self.instance, "raw_attr_dict", ()), raw = True)
    # end def get_object_raw

# end class An_Attribute_Inline_Instance

class Id_Attribute_Inline_Instance (Attribute_Inline_Instance) :
    """A form which handles an attribute of an Id_Entity as a seperate form."""

    def __init__ (self, instance, * args, ** kw) :
        initial_data = kw.get ("initial_data", {})
        if instance is None and initial_data :
            instance = initial_data.get ("instance")
            if callable (instance) :
                instance = instance (self)
        self.__super.__init__ (instance, * args, ** kw)
    # end def __init__

    def create_object (self, form) :
        if self.pid and not self.instance and not self.test :
            self.instance = self.et_man.pid_query (self.pid)
        return self.__super.create_object (form)
    # end def create_object

    def _create_instance (self, on_error) :
        if self.raw_attr_dict and not self.test :
            ### if raw data is provided for this form -> let's check if we
            ### find an instance with this raw data before we try to create
            ### a new one
            errors       = []
            cooked_attrs = self.et_man._etype.cooked_attrs \
                (self.raw_attr_dict, errors.append)
            if not errors :
                instance = self.et_man.query (** cooked_attrs).first ()
                if instance :
                    return instance
        return self.__super._create_instance (on_error)
    # end def _create_instance

# end class Id_Attribute_Inline_Instance

class Link_Inline_Instance (_Inline_Instance_) :
    """A form which handles an inline link"""

    electric_fields_css = "mom-link"

    def __init__ (self, * args, ** kw) :
        self.form_number = kw.pop ("form_number", -1)
        self.inline      = kw.pop ("inline",      None)
        self.__super.__init__ (* args, ** kw)
        if self.instance is None and self.initial_data :
            import pdb; pdb.set_trace ()
    # end def __init__

    def create_object (self, * args, ** kw) :
        state = self.state
        pid   = self.pid
        if state == "U" :
            if self.instance :
                ### this form handles an link which should be removed
                ### we need to destroy the instance in the database
                self.instance.destroy ()
                ### and mark that this form does not have a valid instance
                ### (needed for the min/max count check's)
                self.instance = None
                ### XXX handle deleting of links object's
            return
        if not self.instance and pid and not self.test :
            self.instance = self.et_man.pid_query (pid)
        if self.raw_attr_dict and not self.instance :
            ### this is not a rename -> set othe owner role
            ### (a rename on a link does not work if all roles are specified)
            self.raw_attr_dict [self.owner_role_name] = \
                self.parent.get_object_raw ()
        self.__super.create_object (* args, ** kw)
    # end def create_object

    @property
    def fake_or_instance (self) :
        if not self.instance :
            form          = self.parent.__class__.Test_Inline (self.parent.action)
            self.instance = form.test_inline \
                ( self.request_data, self.inline.prefix, self.form_number
                ) [1].instance
        return self.instance
    # end def fake_or_instance

    def _update_test_inline_fields (self, if_dict) :
        ### force create of parent object
        self.parent.get_object_raw ()
        if_dict [self.owner_role_name] = self.parent.instance
        self.raw_attr_dict.pop (self.owner_role_name, None)
    # end def _update_test_inline_fields

# end class Link_Inline_Instance

class Collection_Inline_Instance (An_Attribute_Inline_Instance) :
    """Collection of inline An_Entities"""

    @property
    def fake_or_instance (self) :
        if not self.instance :
            form          = self.parent.__class__.Test_Inline (self.parent.action)
            self.instance = form.test_inline \
                ( self.request_data, self.inline.prefix, self.form_number
                ) [1].instance
        return self.instance
    # end def fake_or_instance

    def _update_test_inline_fields (self, if_dict) :
        ### force create of parent object
        self.parent.get_object_raw ()
        if_dict [self.owner_role_name] = self.parent.instance
        self.raw_attr_dict.pop (self.owner_role_name, None)
    # end def _update_test_inline_fields

    def create_object (self, * args, ** kw) :
        state = self.state
        if state == "U" :
            if self.instance :
                self.instance = None
            return
        self.__super.create_object (* args, ** kw)
    # end def create_object

# end class Collection_Inline_Instance

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Inline_Instance
