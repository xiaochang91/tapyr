# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package TFL.Babel.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# icense along with this module; if not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    TFL.Babel.PO_File
#
# Purpose
#    Create object for handling PO or POT files using functions from Babel
#
# Revision Dates
#    22-Jan-2010 (MG) Creation
#    25-Jan-2010 (MG) `combine_package_translations` fixed
#    24-Feb-2010 (MG) `_make_dir` added and used
#    ��revision-date�����
#--

from   _TFL                    import TFL
import _TFL._Meta.Object
from   _TFL._Meta.Property     import Alias_Property
from    babel.messages.pofile  import write_po, read_po
from    babel.messages.mofile  import write_mo
from    babel.messages.catalog import Catalog
import  os
import  sys
import  json

class PO_File (TFL.Meta.Object) :
    """A object to handle PO/POT files."""

    def __init__ ( self
                 , project            = u"Project"
                 , version            = u"0.9"
                 , bugs_address       = u"bugs@domain.unknown"
                 , copyright_holder   = u"Copyright"
                 , charset            = u"utf-8"
                 , width              = 76
                 , no_location        = False
                 , omit_header        = False
                 , sort               = True
                 , catalog            = None
                 ) :
        if not catalog :
            catalog = Catalog \
                ( project            = project
                , version            = version
                , msgid_bugs_address = bugs_address
                , copyright_holder   = copyright_holder
                , charset            = charset
                )
        self.catalog      = catalog
        self.width        = width
        self.no_location  = no_location
        self.omit_header  = omit_header
        self.sort         = sort
    # end def __init__

    def add (self, * args, ** kw) :
        return self.catalog.add (* args, ** kw)
    # end def add

    @classmethod
    def combined (cls, * file_names, ** kw) :
        result = cls.load (file_names [0], ** kw)
        print "Combine translations from", file_names [0],
        for file in file_names [1:] :
            print file
            result.merge (file)
        print
        return result
    # end def combined

    @classmethod
    def combine_package_translations (cls, packages) :
        files = []
        for pkg in (p.strip () for p in packages) :
            __import__ (pkg)
            base_dir = os.path.dirname (sys.modules [pkg].__file__)
            pot_file = os.path.join (base_dir, "-I18N", "template.pot")
            if os.path.isfile (pot_file) :
                files.append (pot_file)
        if files :
            return cls.combined (* files)
        return dict ()
    # end def combine_package_translations

    @property
    def fuzzy (self) :
        return self.catalog.fuzzy
    # end def fuzzy

    @fuzzy.setter
    def fuzzy (self, value) :
        self.catalog.fuzzy = value
    # end def fuzzy

    def generate_js (self, language, file_name, use_fuzzy = False) :
        file   = open (file_name, "w")
        result = []
        for msg in self.catalog :
            loc = ", ".join ("%s:%s" % (f, l) for (f, l) in msg.locations)
            result.append \
                ( '/* %s */\n      %s : %s'
                % (loc, json.dumps (msg.id), json.dumps (msg.string))
                )

        file.write ("/* Automatically generated translations */\n")
        file.write ("$.I18N.set_catalog\n")
        file.write ( "  ( %r\n  , { %s\n  });\n"
                   % (language, "\n    , ".join (result))
                   )
        file.close ()
    # end def generate_js

    def generate_mo (self, file_name, use_fuzzy = False) :
        self._make_dir (file_name)
        file = open    (file_name, 'wb')
        try:
            write_mo   (file, self.catalog, use_fuzzy = use_fuzzy)
        finally:
            file.close ()
    # end def generate_mo

    @classmethod
    def load (cls, file_name, locale = None, * args, ** kw) :
        return cls \
            ( catalog = read_po (open (file_name, "U"), locale = locale)
            , * args, ** kw
            )
    # end def load

    def _make_dir (self, file_name) :
        dir_name = os.path.dirname (file_name)
        if not os.path.exists (dir_name) :
            os.makedirs (dir_name)
    # end def _make_dir

    def merge (self, filename) :
        other = self.__class__.load (filename)
        for msg in other :
            d = dict ( (k, getattr (msg, k))
                     for k in ( "id", "string", "locations"
                              , "flags", "auto_comments"
                              , "user_comments", "previous_id", "lineno"
                              )
                     )
            self.add (** d)
    # end def merge

    def save (self, file_name, fuzzy = None, ** kw) :
        self._make_dir (file_name)
        if fuzzy is not None :
            self.catalog.fuzzy = fuzzy
        write_po \
            ( open (file_name, "w")
            , catalog      = self.catalog
            , width        = self.width
            , no_location  = self.no_location
            , omit_header  = self.omit_header
            , sort_output  = kw.pop ("sort", self.sort)
            , ** kw
            )
    # end def save

    def update (self, template, no_fuzzy_matching=False) :
        return self.catalog.update (template, no_fuzzy_matching)
    # end def update

    def __contains__ (self, item) :
        return item in self.catalog
    # end def __contains__

    def __iter__ (self) :
        return iter (self.catalog)
    # end def __iter__

    def __len__ (self) :
        return len (self.catalog)
    # end def __len__

    def __repr__ (self) :
        return "<%s %s>" % (self.__class__.__name__, self.catalog.project)
    # end def __repr__

# end class PO_File

if __name__ != "__main__" :
    TFL.Babel._Export ("*")
### __END__ TFL.Babel.PO_File
