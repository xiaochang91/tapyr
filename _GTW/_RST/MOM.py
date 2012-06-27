# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.
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
#    GTW.RST.MOM
#
# Purpose
#    RESTful resource for essential types and objects of MOM meta object model
#
# Revision Dates
#    22-Jun-2012 (CT) Creation
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.Resource
import _GTW._RST.HTTP_Method

from   _MOM.import_MOM          import *

from   _TFL._Meta.Once_Property import Once_Property

class RST_Mixin (TFL.Meta.Object) :
    """Mixin for MOM-specific RST classes."""

    _change_info               = None
    _sort_key_cid_reverse      = TFL.Sorted_By ("-cid")

    @property
    def change_info (self) :
        result = self._change_info
        if result is None :
            result = self._change_info = self._get_change_info ()
        return result
    # end def change_info

    def query_changes (self) :
        scope = self.top.scope
        cqf   = self.change_query_filter
        return scope.query_changes (cqf).order_by (self._sort_key_cid_reverse)
    # end def query_changes

    def _get_change_info (self) :
        result = None
        lc     = self.query_changes ().first ()
        if lc is not None :
            result = TFL.Record \
                ( cid           = lc.cid
                , etag          = "ET-%s-%s" % (lc.time, lc.cid)
                , last_modified = lc.time.replace (microsecond = 0)
                )
        return result
    # end def _get_change_info

    @TFL.Contextmanager
    def _handle_method_context (self, method, request) :
        with self.LET (_change_info = self._get_change_info ()) :
            yield
    # end def _prepare_handle_method

# end class RST_Mixin

class RST_E_Type_Mixin (RST_Mixin) :
    """Mixin for classes of E_Type classes."""

    query_restriction          = None
    sort_key                   = None

    _last_change               = None
    _objects                   = []
    _old_cid                   = -1

    objects                    = property (lambda s : s._get_objects ())

    def __init__ (self, ** kw) :
        self.pop_to_self (kw, "ETM", prefix = "_")
        if "name" not in kw :
            kw ["name"] = self.E_Type.type_name
        self.__super.__init__ (** kw)
    # end def __init__

    @property
    def count (self) :
        if self.query_filters :
            result = self.query ().count_transitive ()
        else :
            result = self.ETM.count_transitive
        return result
    # end def count

    @Once_Property
    def E_Type (self) :
        ETM = self._ETM
        if isinstance (ETM, basestring) :
            result = self.top.App_Type [ETM]
        else :
            result = ETM.E_Type
        return result
    # end def E_Type

    @Once_Property
    def ETM (self) :
        result = self._ETM
        if isinstance (result, basestring) :
            result = self.top.scope [result]
        return result
    # end def ETM

    @Once_Property
    def change_query_filter (self) :
        E_Type = self.E_Type
        if E_Type.is_partial :
            result = Q.OR (* ((Q.type_name == ctn) for ctn in E_Type.children))
        else :
            result = Q.type_name == E_Type.type_name
        return result
    # end def change_query_filter

    @Once_Property
    def query_filters (self) :
        return tuple ()
    # end def query_filters

    def query (self, sort_key = None) :
        result = self.ETM.query \
            (* self.query_filters, sort_key = sort_key or self.sort_key)
        if self.query_restriction is not None :
            result = self.query_restriction (result)
        return result
    # end def query

    def _get_objects (self) :
        change_info = self.change_info
        cid = change_info and change_info.cid
        if  self._old_cid != cid :
            self._old_cid  = cid
            self._objects = self.query ().all ()
        return self._objects
    # end def _get_objects

    @TFL.Contextmanager
    def _handle_method_context (self, method, request) :
        with self.__super._handle_method_context (method, request) :
            ### XXX setup query_restriction if request.req_data specifies any
            yield
    # end def _prepare_handle_method

# end class RST_E_Type_Mixin

_Ancestor = GTW.RST.Leaf

class RST_Entity (RST_Mixin, _Ancestor) :
    """RESTful node for a specific instance of an essential type."""

    class RST_Entity_GET (_Ancestor.GET) :

        _real_name             = "GET"

        def _response_body (self, resource, request, response) :
            obj = resource.obj
            return dict \
                ( attributes = dict
                    (   (a.name, a.get_raw (obj))
                    for a in obj.edit_attr
                    if  a.to_save (obj)
                    )
                , cid        = obj.last_cid
                , pid        = obj.pid
                , type_name  = obj.type_name
                )
        # end def _response

    GET = RST_Entity_GET # end class

    def __init__ (self, ** kw) :
        assert "name" not in kw
        obj = kw.pop ("obj")
        if isinstance (obj, int) :
            obj   = self.ETM.pid_query (obj)
        self.obj  = obj
        self.name = str (obj.pid)
        self.__super.__init__ (** kw)
    # end def __init__

    @property
    def change_query_filter (self) :
        return Q.pid == self.obj.pid
    # end def change_query_filter

Entity = RST_Entity # end class

_Ancestor = GTW.RST.Node_V

class RST_E_Type (RST_E_Type_Mixin, _Ancestor) :
    """RESTful node for a specific essential type."""

    _real_name                 = "E_Type"

    _ETM                       = None

    class RST_E_Type_GET (_Ancestor.GET) :

        _real_name             = "GET"

        ### XXX redefine _response_dict_top and _response_entry to regard
        ###     query parameters (full vs. bare bone answer...)

        def _response_entry (self, resource, request, entry) :
            return entry.pid
        # end def _response_entry

        def _resource_entries (self, resource, request) :
            result = resource.objects
            return sorted (result, key = Q.pid)
        # end def _resource_entries

    GET = RST_E_Type_GET # end class

    def _get_child (self, child, * grandchildren) :
        try :
            obj = self.ETM.pid_query (child)
        except (LookupError, TypeError) :
            pass
        else :
            result = self._new_entry (obj)
            if not grandchildren :
                return result
            else :
                return result._get_child (* grandchildren)
    # end def _get_child

    def _new_entry (self, instance) :
        return Entity (obj = instance, parent = self)
    # end def _new_entry

E_Type = RST_E_Type # end class

_Ancestor = GTW.RST.Node

class RST_Scope (_Ancestor) :
    """RESTful node for a scope."""

    _real_name                 = "Scope"

    def __init__ (self, ** kw) :
        if "entries" not in kw :
            kw ["entries"] = tuple \
                (   E_Type (ETM = et.type_name)
                for et in self.top.scope._T_Extension
                if  issubclass (et, MOM.Id_Entity)
                )
        self.__super.__init__ (** kw)
    # end def __init__

Scope = RST_Scope # end class

if __name__ != "__main__" :
    GTW.RST._Export_Module ()
### __END__ GTW.RST.MOM