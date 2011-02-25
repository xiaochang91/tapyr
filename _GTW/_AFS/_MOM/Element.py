# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.AFS.MOM.
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
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.AFS.MOM.Element
#
# Purpose
#    Model MOM-specific elements of AJAX-enhanced forms
#
# Revision Dates
#    23-Feb-2011 (CT) Creation
#    24-Feb-2011 (CT) Creation continued..
#    25-Feb-2011 (CT) Creation continued...
#    ��revision-date�����
#--

from   _GTW._AFS.Element import *
import _GTW._AFS._MOM

class _MOM_Entity_ (Entity) :
    """Model a MOM-specific sub-form for a single entity."""

    _real_name = "Entity"

    def __call__ (self, ETM, entity, ** kw) :
        if entity is not None :
            assert isinstance (entity, ETM._etype), \
                "%s <-> %r" % (ETM, entity)
            assert ETM.type_name == self.type_name, \
                 "%s <-> %s" % (ETM.type_name, self.type_name)
        result = dict \
            ( cid = getattr (entity, "cid", None)
            , pid = getattr (entity, "pid", None)
            )
        for c in self.children :
            result [c.id] = c (ETM, entity, ** kw)
        return result
    # end def __call__

Entity = _MOM_Entity_ # end class

class _MOM_Entity_Link_ (Entity_Link, Entity) :
    """Model a MOM-specific sub-form for a link to entity in containing
       sub-form.
    """

    _real_name = "Entity_Link"

    def __call__ (self, ETM, entity, ** kw) :
        assoc = ETM.home_scope [self.type_name]
        link  = None
        if entity is not None :
            try :
                link = assoc.query (** { self.role_name : entity }).one ()
            except IndexError :
                pass
        return self.__super.__call__ (assoc, link, ** kw)
    # end def __call__

    def instance_call (self, assoc, link, ** kw) :
        return self.__super.__call__ (assoc, link, ** kw)
    # end def instance_call

Entity_Link = _MOM_Entity_Link_ # end class

class _MOM_Entity_List_  (Entity_List) :
    """Model a MOM-specific sub-form for a list of entities."""

    _real_name = "Entity_List"

    def __call__ (self, ETM, entity, ** kw) :
        cs     = []
        proto  = self.proto
        this   = self.clone ()
        result = {}
        if entity is not None :
            assoc  = ETM.home_scope [proto.type_name]
            for link in assoc.query_s (** { proto.role_name : entity }) :
                cs.append ((link, this.add_child ()))
            for link, c in cs :
                result [c.id] = c.instance_call (assoc, link, ** kw)
        return result
    # end def __call__

Entity_List = _MOM_Entity_List_ # end class

class _MOM_Field_ (Field) :
    """Model a MOM-specific field of an AJAX-enhanced form."""

    _real_name = "Field"

    def __call__ (self, ETM, entity, ** kw) :
        attr = ETM.attributes [self.name]
        if self.name in kw :
            init = kw [self.name].get ("init")
        else :
            init = attr.get_raw (entity)
        result = dict (init = init)
        return result
    # end def __call__

Field = _MOM_Field_ # end class

class _MOM_Field_Composite_ (Field_Composite) :
    """Model a MOM-specific composite field of a AJAX-enhanced form."""

    _real_name = "Field_Composite"

    def __call__ (self, ETM, entity, ** kw) :
        attr     = ETM._etype.attributes [self.name]
        c_type   = attr.C_Type
        c_entity = getattr (entity, self.name, None)
        result   = {}
        for c in self.children :
            result [c.id] = c (c_type, c_entity, ** kw.get (self.name, {}))
        return result
    # end def __call__

Field_Composite = _MOM_Field_Composite_ # end class

class _MOM_Field_Entity_ (Entity, Field_Entity) :
    """Model a MOM-specific entity-holding field of an AJAX-enhanced form."""

    _real_name = "Field_Entity"

    def __call__ (self, ETM, entity, ** kw) :
        attr     = ETM._etype.attributes [self.name]
        a_type   = attr.etype_manager (ETM)
        a_entity = getattr (entity, self.name, None)
        a_kw     = kw.get (self.name, {})
        kw       = dict \
            ( a_kw
            , allow_new = attr.ui_allow_new and a_kw.get ("allow_new", True)
            # XXX completer
            )
        result   = self.__super.__call__ (a_type, a_entity, ** kw)
        return result
    # end def __call__

Field_Entity = _MOM_Field_Entity_ # end class

class _MOM_Form_ (Form) :
    """Model a MOM-specific AJAX-enhanced form."""

    _real_name = "Form"

    def __call__ (self, * args, ** kw) :
        data   = {}
        result = GTW.AFS.Instance.Form (self, data)
        if len (self.children) == 1 and len (args) <= 2 :
            c = self.children [0]
            data [c.id] = c (* args, ** kw)
        else :
            assert len (args) == len (self.children), repr (self)
            assert not kw, repr (self)
            for a, c in zip (args, self.children) :
                data [c.id] = c (e.ETM, a.entity, ** a.kw)
        return result
    # end def __call__

Form = _MOM_Form_ # end class

if __name__ != "__main__" :
    GTW.AFS.MOM._Export_Module ()
### __END__ GTW.AFS.MOM.Element
