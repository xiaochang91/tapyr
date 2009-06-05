# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    DJO.Apps.Person.Person
#
# Purpose
#    Django model for persons
#
# Revision Dates
#    19-May-2009 (CT) Creation
#    ��revision-date�����
#--

from   _DJO                       import DJO
import _DJO.Form_Set_Description
import _DJO.Models
import _DJO.Model_Field           as     MF

from   django.utils.translation   import gettext_lazy as _

class Person (DJO.Model) :
    """Models a person."""

    class Meta :
        ordering              = ["user"]
        verbose_name          = _("Person")
        verbose_name_plural   = _("Persons")
    # end class Meta

    user                  = MF.One_to_One \
        ( "auth.User"
        , editable        = True
        , verbose_name    = _("User")
        )
    title                 = MF.Char \
        ( _("Title")
        , blank           = True
        , help_text       = _("Academic title")
        , max_length      = 20
        )
    birth_date            = MF.Date \
        ( _("Birth-Date")
        , blank           = True
        , null            = True
        )
    sex                   = MF.Choice \
        ( MF.Char, _("Sex")
        , blank           = True
        , choices         = (("F", _("Female")), ("M", _("Male")))
        , max_length      = 1
        )
    emails                = MF.Many_to_Many \
        ( "Person.Email_Address"
        , blank           = True
        , verbose_name    = _("Email Addresses")
        )
    phones                = MF.Many_to_Many \
        ( "Person.Phone_Number"
        , blank           = False
        , verbose_name    = _("Phone Numbers")
        )
    addresses             = MF.Many_to_Many \
        ( "Person.Address"
        , blank           = True
        , verbose_name    = _("Addresses")
        )

    @property
    def first_name (self) :
        return self.user.first_name
    # end def first_name

    @property
    def last_name (self) :
        return self.user.last_name
    # end def last_name

    def __unicode__ (self) :
        u = self.user
        result = " ".join \
            (x for x in (self.title, u.first_name, u.last_name) if x)
        if not result :
            result = u.username
        return result
    # end def __unicode__

    display = property (__unicode__)

    NAV_admin_args = dict \
        ( list_display = ("birth_date", "sex")
        , form_set_descriptions =
              ( DJO.Form_Set_Description
                  ( DJO.Field_Description ("last_name",  required = True)
                  , DJO.Field_Description ("first_name", required = True)
                  , "title"
                  , legend    = _("Personal info")
                  , template  = "formset_horizontal.html"
                  )
              , DJO.Form_Set_Description
                  ( "sex", "birth_date"
                  , legend    = _("Personal details")
                  , template  = "formset_horizontal.html"
                  )
              , DJO.Form_Set_Description
                  ( "phones", "emails", "addresses")
              )
        )

# end class Person

### __END__ DJO.Apps.Person.Person
