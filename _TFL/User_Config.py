# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package TFL.
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
#    TFL.User_Config
#
# Purpose
#    Provide thread-local user configuration
#
# Revision Dates
#    19-Jul-2011 (CT) Creation
#    20-Jul-2011 (CT) `get_tz` and `set_defaults` added
#    30-Apr-2012 (CT) Convert `tz` to lazy `Once_Property`, allow
#                     `ImportError` by `dateutil`
#    21-Jun-2012 (CT) Handle `time_zone` properly in `set_default`
#    21-Jun-2012 (CT) Autoconvert `time_zone` values passed as string
#    21-Jun-2012 (CT) Fix typo
#    ««revision-date»»···
#--

from   __future__  import unicode_literals, absolute_import

from   _MOM        import MOM
from   _TFL        import TFL

from   _TFL._Meta.Once_Property import Once_Property

import _TFL._Meta.Property
import _TFL.Context

import locale
import threading
import sys

class User_Config (threading.local) :
    """Provide thread-local user configuration."""

    _initialized         = False

    file_system_encoding = sys.getfilesystemencoding ()
    input_encoding       = locale.getpreferredencoding ()
    language             = "en"
    output_encoding      = input_encoding
    user                 = None

    _time_zone           = None

    def __init__ (self, ** kw) :
        if self._initialized :
            raise SystemError \
                ( "TFL.User_Config must not be called more than "
                  "once per thread"
                )
        self._initialized = True
        self.__dict__.update (kw)
    # end def __init__

    @property
    def time_zone (self) :
        if self.tz is not None :
            if self._time_zone is None :
                self._time_zone = self.tz.tzutc ()
            elif isinstance (self._time_zone, basestring) :
                self._time_zone = self.get_tz (self._time_zone)
        return self._time_zone
    # end def time_zone

    @time_zone.setter
    def time_zone (self, value) :
        if isinstance (value, basestring) :
            value = self.get_tz (value)
        self._time_zone = value
    # end def time_zone

    @Once_Property
    def tz (self) :
        try :
            from dateutil import tz
            return tz
        except ImportError :
            pass
    # end def tz

    def get_tz (self, name = None) :
        """Return tz-info for `name` (default taken from environment).

           For instance::

               tz.gettz ("Europe/Vienna") -->
                   tzfile ('/usr/share/zoneinfo/Europe/Vienna')

        """
        if self.tz is not None :
            return self.tz.gettz (name)
    # end def get_tz

    LET = TFL.Meta.Class_and_Instance_Method (TFL.Context.attr_let)

    def set_default (self, name, value) :
        """Set default of attribute `name` to `value`."""
        if name == "_initialized" :
            raise AttributeError ("Cannot set default for _initialized")
        if name == "time_zone" :
            name = "_time_zone"
            if isinstance (value, basestring) :
                value = self.get_tz (value)
        setattr (self.__class__, name, value)
        return value
    # end def set_default

    def set_defaults (self, ** kw) :
        for k, v in kw.iteritems () :
            self.set_default (k, v)
    # end def set_defaults

# end class User_Config

user_config = User_Config ()

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.User_Config
