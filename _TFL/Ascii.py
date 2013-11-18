# -*- coding: utf-8 -*-
# Copyright (C) 2004-2013 Mag. Christian Tanzer. All rights reserved
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
#    Ascii
#
# Purpose
#    Functions for unicode/ASCII handling
#
# Revision Dates
#     6-Sep-2004 (CT) Creation
#    13-May-2005 (CT) Call to `strip` added to `sanitized_filename`
#     9-Aug-2006 (CT) Use `unicodedata.normalize` (and simplify `_diacrit_map`)
#     9-Mar-2007 (CT) `_diacrit_map` corrected (`Oe` and `Ue` instead `O`/`U`)
#     9-Mar-2007 (CT) Optional `translate_table` added to `sanitized_unicode`
#                     and `sanitized_filename`
#    23-Dec-2007 (CT) Use `Re_Replacer` and `Dict_Replacer` instead of
#                     home-grown code
#    18-Oct-2010 (CT) `_quote_map` added and used
#    ««revision-date»»···
#--

from   __future__  import print_function, unicode_literals

from   _TFL        import TFL
from   _TFL.Regexp import Regexp, Re_Replacer, Dict_Replacer, re

from   itertools   import chain as ichain
import unicodedata

_diacrit_map    = \
    { "Ä"      : "Ae"
    , "Ö"      : "Oe"
    , "Ü"      : "Ue"
    , "ß"      : "ss"
    , "ä"      : "ae"
    , "ö"      : "oe"
    , "ü"      : "ue"
    }

_diacrit_rep    = Dict_Replacer (_diacrit_map)

_graph_rep      = Re_Replacer \
    ( "(%s)+"
    % "|".join   (re.escape (c) for c in ("^!$%&([{}]) ?`'*+#:;<>|" '"'))
    , "_"
    )

_non_print_rep  = Re_Replacer \
    ( "|".join (re.escape (chr (i)) for i in ichain (range (0, 32), [127]))
    , ""
    )

_quote_map      = \
    { "«"      : "<<"
    , "»"      : ">>"
    , "\u2018" : "'"
    , "\u2019" : "'"
    , "\u201A" : "'"
    , "\u201B" : "'"
    , "\u201C" : '"'
    , "\u201D" : '"'
    , "\u201E" : '"'
    , "\u201F" : '"'
    , "\u2039" : "'"
    , "\u203A" : "'"
    }

_quote_rep      = Dict_Replacer (_quote_map)

def _encoded (s) :
    return unicodedata.normalize ("NFKD", s).encode ("ascii", "ignore")
# end def _encoded

def _sanitized_unicode (s, translate_table = None) :
    if translate_table :
        s = s.translate (translate_table)
    s = _quote_rep (_diacrit_rep (s))
    return s
# end def _sanitized_unicode

def _show (s) :
    from _TFL.pyk import pyk
    result = repr (s)
    if result.startswith ("b'") :
        result = result [1:]
    pyk.fprint (result)
# end def _show

def sanitized_unicode (s, translate_table = None) :
    """Return sanitized version of unicode string `s` reduced to
       pure ASCII 8-bit string. Caveat: passing in an 8-bit string with
       diacriticals doesn't work.

       >>> _show (sanitized_unicode ("üxäyözßuÜXÄYÖZbc¡ha!"))
       'uexaeyoezssuUeXAeYOeZbcha!'
       >>> _show (sanitized_unicode ("«ÄÖÜ»"))
       '<<AeOeUe>>'
       >>> _show \\
       ... (sanitized_unicode ("«ÄÖÜ»", {ord ("«") : "<", ord ("»") : ">"}))
       '<AeOeUe>'
    """
    return _encoded (_sanitized_unicode (s, translate_table))
# end def sanitized_unicode

def sanitized_filename (s, translate_table = None) :
   """Return `sanitized_unicode (s)` with all non-printable and some graphic
      characters removed so that the result is usable as a filename.

       >>> _show (sanitized_filename \\
       ...    ("überflüßig komplexer'; und $gefährlicher*' Filename"))
       'ueberfluessig_komplexer_und_gefaehrlicher_Filename'
       >>> _show (sanitized_filename ("«ÄÖÜß»"))
       '_AeOeUess_'
   """
   s = _sanitized_unicode (s.strip (), translate_table)
   s = _non_print_rep     (s)
   s = _graph_rep         (s)
   return _encoded        (s)
# end def sanitized_filename

__doc__ = """
.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

Module `Ascii`
==========================

"""

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ Ascii
