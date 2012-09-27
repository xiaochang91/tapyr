# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2012 Mag. Christian Tanzer. All rights reserved
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
#    MOM.Link
#
# Purpose
#    Root class for link-types of MOM meta object model
#
# Revision Dates
#    22-Oct-2009 (CT) Creation (factored from TOM.Link)
#     4-Nov-2009 (CT) `Link2` added
#    20-Nov-2009 (CT) `Link3` and `Link2_Ordered` added
#    20-Nov-2009 (CT) Documentation added
#    26-Nov-2009 (CT) `Role_Cacher` added
#    26-Nov-2009 (CT) `_init_epk` and `destroy` redefined to handle
#                     `auto_cache_roles`
#    27-Nov-2009 (CT) `Role_Cacher.setup` changed to store `other_role`
#                     instead of `other_role_name`
#    28-Nov-2009 (CT) `is_partial = True` added to all classes
#     3-Dec-2009 (CT) `Link3` and `Link2_Ordered` derived from `Link` instead
#                     of from `Link2` (and `_Attributes` moved from `Link2`
#                     to `Link`)
#    22-Dec-2009 (CT) `Link2_Ordered` changed to use `A_Int` for `seq_no` and
#                     directly derived from `Link2`
#    18-Jan-2010 (CT) `Role_Cacher_1` factored, `Role_Cacher_n` added
#     8-Feb-2010 (CT) `Link` changed to redefine `_destroy`, not `destroy`
#    18-Feb-2010 (CT) `Link1` added, `_MOM_Link_n_` factored
#    19-Feb-2010 (CT) `Link_Cacher` added, `_Cacher_` factored
#    19-Feb-2010 (CT) `Role_Cacher.setup` changed to create `A_Cached_Role`
#                     for `other_type` (factored in here from
#                     `M_Link_n._m_setup_auto_cache_role`)
#    19-Feb-2010 (CT) Argument `attr_class` added to `_setup_attr`
#    25-Feb-2010 (CT) Redefine `_finish__init__` instead of `_init_epk`
#     4-Mar-2010 (CT) `_Cacher_.cr_attr` added
#    22-Apr-2010 (CT) `_rename` redefined to honor `auto_cache_roles`
#     5-May-2010 (CT) `Link_Cacher._auto_attr_name` changed to call `lower`
#    11-May-2010 (CT) `_Cacher_.grn` added
#     4-Sep-2010 (CT) Use `cache.discard` instead of `cache.remove`
#    29-Mar-2011 (CT) `Link1.left` redefined to mixin `Init_Only_Mixin`
#    22-Sep-2011 (CT) s/Class/P_Type/ for _A_Id_Entity_ attributes
#    23-Mar-2012 (CT) Add `copy`, `copy_args`, and `link_type_name`
#    24-Mar-2012 (CT) Add `__repr__` to `_Cacher_`
#    29-Mar-2012 (CT) Change `_Cacher_._setup_attr` to not redefine `cr_attr`
#    18-Jun-2012 (CT) Add `_Reload_Mixin_` for `Link1`, `Link2`, `Link3`
#    26-Jun-2012 (CT) Add `if cache` to `Role_Cacher_n.__call__`
#     1-Aug-2012 (CT) Add `_Link[123]_Destroyed_Mixin_`
#     4-Aug-2012 (CT) Guard `cache.remove` in `Link_Cacher_n.__call__`
#    13-Sep-2012 (CT) Add `_suffixed`
#    14-Sep-2012 (CT) Add `cr_name` to `Link_Cacher`, `Role_Cacher`
#    27-Sep-2012 (CT) Remove un-implemented `Link_AB` from docstring
#    ��revision-date�����
#--

from   _TFL      import TFL
from   _MOM      import MOM

from   _MOM._Attr.Type import *
from   _MOM._Attr      import Attr
from   _MOM._Pred      import Pred

import  _MOM._Meta.M_Link

import _MOM.Entity

_Ancestor_Essence = MOM.Id_Entity

class _MOM_Link_ (_Ancestor_Essence) :
    """Root class for link-types of MOM meta object model."""

    __metaclass__         = MOM.Meta.M_Link
    _real_name            = "Link"
    entity_kind           = "link"
    is_partial            = True
    is_synthetic          = False

    class _Attributes (_Ancestor_Essence._Attributes) :

        class left (_A_Link_Role_Left_, A_Link_Role_EB) :
            """Left role of association. Override to define `role_type`, ..."""

        # end class left

    # end class _Attributes

    @property
    def roles (self) :
        return self.epk [:self.number_of_roles]
    # end def roles

    def _finish__init__ (self) :
        self.__super._finish__init__ ()
        for role_cacher in self.auto_cache_roles :
            role_cacher (self, no_value = False)
    # end def

    def _destroy (self) :
        for role_cacher in self.auto_cache_roles :
            role_cacher (self, no_value = True)
        self.__super._destroy ()
    # end def _destroy

    def _rename (self, new_epk, pkas_raw, pkas_ckd) :
        result = self.__super._rename (new_epk, pkas_raw, pkas_ckd)
        for role_cacher in self.auto_cache_roles :
            role_cacher (self, no_value = False)
        return result
    # end def _rename

Link = _MOM_Link_ # end class

_Ancestor_Essence = Link

class Link1 (_Ancestor_Essence) :
    """Common base class for essential unary links of MOM"""

    __metaclass__         = MOM.Meta.M_Link1
    is_partial            = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :

            Kind_Mixins   = (Attr.Init_Only_Mixin, )

        # end class left

    # end class _Attributes

# end class Link1

_Ancestor_Essence = Link

class _MOM_Link_n_ (_Ancestor_Essence) :
    """Root class for link-types of MOM meta object model with more than 1 role."""

    __metaclass__         = MOM.Meta.M_Link_n
    is_partial            = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        class right (_A_Link_Role_Right_, A_Link_Role_EB) :
            """Right role of association. Override to define `role_type`, ..."""

        # end class right

    # end class _Attributes

# end class _MOM_Link_n_

_Ancestor_Essence = _MOM_Link_n_

class Link2 (_Ancestor_Essence) :
    """Common base class for essential binary links of MOM."""

    __metaclass__         = MOM.Meta.M_Link2
    is_partial            = True

# end class Link2

_Ancestor_Essence = Link2

class Link2_Ordered (_Ancestor_Essence) :
    """Common base class for essential binary ordered links of MOM."""

    is_partial            = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        class seq_no (A_Int) :
            """Sequence number of a link in an ordered association."""

            kind       = Attr.Primary

        # end class seq_no

    # end class _Attributes

# end class Link2_Ordered

_Ancestor_Essence = _MOM_Link_n_

class Link3 (_Ancestor_Essence) :
    """Common base class for essential ternary links of MOM."""

    __metaclass__         = MOM.Meta.M_Link3
    is_partial            = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        class middle (_A_Link_Role_Middle_, A_Link_Role_EB) :
            """Middle role of association. Override to define `role_type`, ..."""

        # end class middle

    # end class _Attributes

# end class Link3

@TFL.Add_To_Class ("_Destroyed_Mixin_", Link1)
class _Link1_Destroyed_Mixin_ (MOM._Id_Entity_Destroyed_Mixin_) :
    """Mixin triggering an exception on any attribute access to a
       destroyed Link1.
    """

    __metaclass__ = MOM.Meta.M_E_Type_Link1_Destroyed

# end class _Link1_Destroyed_Mixin_

@TFL.Add_To_Class ("_Destroyed_Mixin_", Link2)
class _Link2_Destroyed_Mixin_ (MOM._Id_Entity_Destroyed_Mixin_) :
    """Mixin triggering an exception on any attribute access to a
       destroyed Link2.
    """

    __metaclass__ = MOM.Meta.M_E_Type_Link2_Destroyed

# end class _Link2_Destroyed_Mixin_

@TFL.Add_To_Class ("_Destroyed_Mixin_", Link3)
class _Link3_Destroyed_Mixin_ (MOM._Id_Entity_Destroyed_Mixin_) :
    """Mixin triggering an exception on any attribute access to a
       destroyed Link3.
    """

    __metaclass__ = MOM.Meta.M_E_Type_Link3_Destroyed

# end class _Link3_Destroyed_Mixin_

@TFL.Add_To_Class ("_Reload_Mixin_", Link1)
class _Link1_Reload_Mixin_ (MOM._Id_Entity_Reload_Mixin_) :
    """Mixin triggering a reload from the database on any attribute access."""

    __metaclass__ = MOM.Meta.M_E_Type_Link1_Reload

# end class _Link1_Reload_Mixin_

@TFL.Add_To_Class ("_Reload_Mixin_", Link2)
class _Link2_Reload_Mixin_ (MOM._Id_Entity_Reload_Mixin_) :
    """Mixin triggering a reload from the database on any attribute access."""

    __metaclass__ = MOM.Meta.M_E_Type_Link2_Reload

# end class _Link2_Reload_Mixin_

@TFL.Add_To_Class ("_Reload_Mixin_", Link3)
class _Link3_Reload_Mixin_ (MOM._Id_Entity_Reload_Mixin_) :
    """Mixin triggering a reload from the database on any attribute access."""

    __metaclass__ = MOM.Meta.M_E_Type_Link3_Reload

# end class _Link3_Reload_Mixin_

class _Cacher_ (TFL.Meta.Object) :

    link_type_name     = None

    def __init__ (self, attr_name = None) :
        self.role_name = None
        self.grn       = None
        self.cr_attr   = None
        self.attr_name = attr_name
    # end def __init__

    def copy (self, Link, role) :
        result = self.__class__ (* self.copy_args)
        result.setup (Link, role)
        return result
    # end def copy

    def setup (self, Link, role) :
        assert self.role_name is None
        self.link_type_name = Link.type_name
        self.role_name      = role_name = role.role_name
        self.grn            = role.generic_role_name
        attr_name           = self.attr_name
        if attr_name is None or attr_name == True :
            self.attr_name = self._suffixed (self._auto_attr_name (Link, role))
        assert isinstance (self.attr_name, basestring)
    # end def setup

    def _repr_tail (self) :
        return ""
    # end def _repr_tail

    def _setup_attr (self, CR, Link, role, role_type, P_Type, desc) :
        attr_name = self.attr_name
        if attr_name in role_type._Attributes._names :
            cr = getattr (role_type._Attributes, attr_name)
            if cr.electric :
                self.cr_attr = cr
            else :
                raise TypeError \
                    ( "Name conflict between attribute '%s' "
                      "and auto-cache %s: %s\n  %s"
                    % (attr_name, CR, Link, self)
                    )
        else :
            kw  = dict \
                ( assoc        = Link.type_name
                , P_Type       = P_Type
                , description  = desc
                , __module__   = role_type.__module__
                )
            self.cr_attr = cr = type (CR) (attr_name, (CR, ), kw)
            role_type.add_attribute (cr, override = True)
    # end def _setup_attr

    def _suffixed (self, name) :
        suffix = self._suffix
        result = name
        if suffix :
            if name.endswith (suffix) :
                result += "e" + suffix
            elif name.endswith ("y") and suffix == "s" :
                result = name [:-1] + "ies"
            else :
                result += suffix
        return result
    # end def _suffixed

    def __repr__ (self) :
        return "<%s (%s) %s --> %s%s>" % \
            ( self.__class__.__name__, self.link_type_name
            , self.role_name, self.attr_name
            , self._repr_tail ()
            )
    # end def __repr__

# end class _Cacher_

@TFL.Add_To_Class ("Cacher", MOM.Meta.M_Link1)
class Link_Cacher (_Cacher_) :

    @property
    def copy_args (self) :
        return (self.attr_name, )
    # end def copy_args

    @property
    def cr_name (self) :
        return self.role_name
    # end def cr_name

    def setup (self, Link, role) :
        self.max_links = max_links = role.max_links
        if max_links == 1 :
            self.__class__ = Link_Cacher_1
            CR             = MOM.Attr.A_Cached_Role
        else :
            self.__class__ = Link_Cacher_n
            CR             = MOM.Attr.A_Cached_Role_Set
        desc = "`%s` link%s" % (Link.type_base_name, self._suffix)
        self.__super.setup (Link, role)
        self._setup_attr   (CR, Link, role, role.role_type, Link, desc)
    # end def setup

    def _auto_attr_name (self, Link, role) :
        return Link.type_base_name.lower ()
    # end def _auto_attr_name

# end class Link_Cacher

class Link_Cacher_1 (Link_Cacher) :

    _suffix = ""

    def __call__ (self, link, no_value = False) :
        assert self.role_name is not None
        o = getattr (link, self.role_name)
        if o is not None :
            if no_value :
                value = None
            else :
                value = link
            setattr (o, self.attr_name, value)
    # end def __call__

# end class Link_Cacher_1

class Link_Cacher_n (Link_Cacher) :

    _suffix = "s"

    def __call__ (self, link, no_value = False) :
        assert self.role_name is not None
        o = getattr (link, self.role_name)
        if o is not None :
            cache = getattr (o, self.attr_name)
            value = link
            if no_value :
                try :
                    cache.remove (value)
                except LookupError :
                    pass
            else :
                cache.add (value)
    # end def __call__

# end class Link_Cacher_n

@TFL.Add_To_Class ("Cacher", MOM.Meta.M_Link_n)
class Role_Cacher (_Cacher_) :

    def __init__ (self, attr_name = None, other_role_name = None) :
        self.__super.__init__ (attr_name)
        self.other_role_name = self._orn = other_role_name
        self.other_role      = None
    # end def __init__

    @property
    def copy_args (self) :
        return (self.attr_name, self._orn)
    # end def copy_args

    @property
    def cr_name (self) :
        try :
            return self.other_role.name
        except AttributeError :
            return self.other_role_name
    # end def cr_name

    def setup (self, Link, role) :
        other_role_name = \
            self.other_role_name or Link.other_role_name (role.name)
        self.other_role = other_role = getattr \
            (Link._Attributes, other_role_name)
        del self.other_role_name
        self.max_links = max_links = other_role.max_links
        if max_links == 1 :
            self.__class__ = Role_Cacher_1
            CR = ( MOM.Attr.A_Cached_Role
                 , MOM.Attr.A_Cached_Role_DFC
                 ) [bool (other_role.dfc_synthesizer)]
        else :
            self.__class__ = Role_Cacher_n
            if other_role.dfc_synthesizer :
                raise NotImplementedError \
                    ( "Autocache for DFC and max_links > 1: %s.%s"
                    % (Link, self.role_name)
                    )
            CR = MOM.Attr.A_Cached_Role_Set
        self.__super.setup (Link, role)
        other_type = other_role.role_type
        if other_type is None :
            raise TypeError \
                ( "XXX Can't create attribute for auto_cache of role: %s.%s"
                % (Link, self.role_name)
                )
        desc = "`%s` linked to `%s`" % \
            ( self._suffixed (self.role_name.capitalize ())
            , other_role.role_name
            )
        self._setup_attr (CR, Link, role, other_type, role.role_type, desc)
    # end def setup

    def _auto_attr_name (self, Link, role) :
        return role.role_name
    # end def _auto_attr_name

    def _repr_tail (self) :
        return " [%s]" % (self.other_role.role_type.type_name, )
    # end def _repr_tail

# end class Role_Cacher

class Role_Cacher_1 (Role_Cacher) :

    _suffix = ""

    def __call__ (self, link, no_value = False) :
        assert self.role_name is not None
        o = getattr (link, self.other_role.name)
        if o is not None :
            if no_value :
                value = None
            else :
                value = getattr (link, self.role_name)
            setattr (o, self.attr_name, value)
    # end def __call__

# end class Role_Cacher_1

class Role_Cacher_n (Role_Cacher) :

    _suffix = "s"

    def __call__ (self, link, no_value = False) :
        assert self.role_name is not None
        o = getattr (link, self.other_role.name)
        if o is not None :
            cache = getattr (o, self.attr_name)
            if cache is not None :
                value = getattr (link, self.role_name)
                if no_value :
                    cache.discard (value)
                else :
                    cache.add     (value)
    # end def __call__

# end class Role_Cacher_n

__doc__ = """
Class `MOM.Link`
================

.. class:: Link

    `MOM.Link` provides the framework for defining essential
    associations. It is based on :class:`~_MOM.Entity.Id_Entity`.

    An association models the relationship between two or
    more objects of essential classes. An association manages the set
    of links between the objects of the associated classes.
    Conceptually, each link is an independent entity.

    The class `Link` simultaneously models two concepts:

    - The class `Link` itself models the association, i.e., the
      collection of all links.

      The behavior of the association is provided by the methods and
      properties of the link manager
      :class:`MOM.E_Type_Manager<_MOM.E_Type_Manager.E_Type_Manager>`.

    - Each instance of `Link` models one specific link of the association.

    Each essential association is characterized by:

    - `arity`_

    - `roles`_

    - `multiplicity`_

Arity
-----

Arity defines how many objects one link comprises. A binary
association relates pairs of objects to each other, a ternary
association relates triples of objects to each other, and so on.

For each arity, a separate subclass exists, e.g.,
:class:`Link2`, :class:`Link3`, etc. Each arity-specific subclass has
its own arity-specific metaclass, e.g., :class:`M_Link3` defines the
behavior of :class:`Link3`.

An essential association is modelled by a class that inherits from the
proper arity-specific descendent of :class:`Link_EB`.

.. autoclass:: Link1()

.. autoclass:: Link2()

.. autoclass:: Link2_Ordered()

.. autoclass:: Link3()

Roles
-----

Each object participating in a link of an association plays a specific
`role`. A role is characterized by:

* Role type: the type of essential object expected.

* Role name (default `role_type.type_base_name.lower ()`).

  - If an association links objects of the same types in different
    roles to each other, at least one, preferably all of these roles
    need a unique role name that's different from the default role
    name.

* Generic role name (e.g., `left` or `right`).

* Role abbreviation (e.g., `l` or `r`).

* Multiplicity constraint, if any.

* Non-essential properties:

  - `auto_cache` (see `auto-caching`_)

Each role of a specific association is defined by a link-role attribute named
by the generic role name. For a specific association, the link-role attribute

  * Must define :attr:`role_type` (unless that's already inherited).

  * May define :attr:`role_name`, multiplicity constraints
    (:attr:`max_links`) or any non-essential property of the role.

For instance::

    class Person_works_for_Company (Link2) :

        class _Attributes (Link2._Attributes) :

            class left (Link2._Attributes.left) :
                role_type   = Person
                role_name   = "employee"
                auto_cache  = True
                max_links   = 1 ### Danger, Will Robinson
            # end class left

            class right (Link2._Attributes.right) :
                role_type   = Company
                role_name   = "employer"
            # end class right

        # end class _Attributes

Multiplicity
------------

Multiplicity restricts how many links can exist for a single object
in a specific role. Constraints on multiplicity frequently change over
the lifetime of a software application.

Common multiplicities (of binary associations) are:

- 1 <--> 1

- 1 <--> n

- n <--> m

Associations with at least one role with multiplicity 1 could be
implemented by an attribute of the respective object instead of an
association. Any change of requirements might invalidate that
implementation, though.

Simple multiplicity constraints are implemented by defining
`max_links` for the appropriate role. In this case, the `Link` class
will enforce the constraint.

Auto-Caching
------------

By specifying `auto_cache` for one of the `roles` of an entity-based
association, an attribute caching the objects linked via this
association is automagically added to another role of the association.

`auto_cache` can be set to one of the values:

- `True`. This only works for binary associations without any
  non-default properties for auto-caching. As it is the simplest case,
  it should be preferred over the other possibilities, if possible.

- A string specifying the name of the attribute used for caching.

- A tuple of strings specifying the name of the attribute used for
  caching and the name of the other role holding the cache.

- XXX An instance of :class:`_MOM.Link_Role.Role_Cacher<MOM.Link_Role.Role_Cacher>`.

In all cases, an instance of `Role_Cacher` will manage the automatic
cache for the role in question.

"""

future_features = """

DFC-Synthesis
-------------

Some object models allow recursive structures of the form:

- A container-like class `C` inherits from class `X`. `C` thus is
  substitutable for `X` and can participate in all associations
  defined for `X`.

- An association `X_in_C` that defines a container-like association
  with the multiplicity constraint that each instance of `X` is
  restricted to a single link to `C`.

In many such models, the instances of `X` linked to a specific
container `c` should reflect the links `c` itself participates in. To
avoid numerous redundant links, the module :mod:`~_MOM.DFC_Link`
provides classes that allow the automatic synthesis of links derived
from a container association.

DFC-synthesis is specified for the association that needs synthetic
`DFC_Links` by defining the property `dfc_synthesizer` (which must be
an instance of a subclass of :class:`~_MOM.DFC_Link.DFC_Synthesizer`)
for the role related to `X`.

For instance, given `C`, `X`, and `X_in_C` as described above,
DFC-synthesis for an association `X_has_P` would be defined like::

    class X_has_P (Link2) :

        class _Attributes (Link2._Attributes) :

            class left (Link2._Attributes.left) :
                role_type       = X
                dfc_synthesizer = MOM.DFC_Synthesizer_LL (X_in_C)
            # end class left

            class right (Link2._Attributes.right) :
                role_type       = P
            # end class right

        # end class _Attributes



"""

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.Link
