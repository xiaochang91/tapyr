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
#    TFL.I18N
#
# Purpose
#    Support for internationalization (I18N)
#
# Revision Dates
#    28-Oct-2009 (CT) Creation
#    ��revision-date�����
#--

from   _TFL         import TFL

def _ (text):
    """Mark `text` for translation."""
    return unicode (text)
# end def _

def _T (text) :
    """Return the localized translation of `text` (as unicode)."""
    return text ### XXX
# end def _T

def _Tn (singular, plural, n) :
    """Return the localized translation of `text` for the plural form
       appropriate for `n` (as unicode).
    """
    return singular ### XXX
# end def _Tn

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.I18N
