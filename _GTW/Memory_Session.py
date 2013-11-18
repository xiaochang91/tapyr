# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.
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
#    GTW.Memory_Session
#
# Purpose
#    Session backend which stores the information only in memory (the session
#    is lost once the process terminates)
#
# Revision Dates
#    20-Feb-2010 (MG) Creation (based on the File_Session)
#     5-Apr-2012 (CT) Sort alphabetically
#    ««revision-date»»···
#--

from   _GTW                     import GTW
import _GTW.Session

_Store_ = dict ()

class Memory_Session (GTW.Session) :
    """Stores the session data in a file on disk.

    >>> session = Memory_Session ()
    >>> session.save ()
    >>> session ["name"] = "user1"
    >>> session ["lang"] = "de_AT"
    >>> session.save ()
    >>> session2 = Memory_Session (session.sid)
    >>> session.sid == session2.sid
    True
    >>> session.name
    'user1'
    >>> session.name == session2 ["name"]
    True
    >>> session.lang == session2 ["lang"]
    True
    >>> session.get ("lang")
    'de_AT'
    >>> del session.lang
    >>> print session.get ("lang")
    None
    >>> session.get ("lang") == session2 ["lang"]
    False
    >>> session.remove ()
    >>> session3 = Memory_Session (session.sid)
    >>> session3.get ("name"), session.name
    (None, 'user1')
    >>> session3.get ("lang"), session.lang
    (None, None)
    """

    def exists (self, sid) :
        return sid in _Store_
    # end def exists

    def remove (self) :
        try :
            del _Store_ [self.sid]
        except KeyError :
            pass
    # end def remove

    def save (self) :
        _Store_ [self.sid] = self._data
    # end def save

    def _load (self) :
        return _Store_.get (self.sid, {}).copy ()
    # end def _load

# end class Memory_Session

if __name__ != "__main__" :
    GTW._Export ("*")
### __END__ GTW.Memory_Session


