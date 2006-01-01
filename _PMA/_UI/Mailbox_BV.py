# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    PMA.UI.Mailbox_BV
#
# Purpose
#    Abstract user interface for box-view of PMA.Mailbox
#
# Revision Dates
#     6-Jun-2005 (CT) Creation
#     6-Jun-2005 (MG) `_MB_TA_`: methods converted to classmethods
#     7-Jun-2005 (MG) Superfluous `@classmethod` removed
#    11-Jun-2005 (MG) `Folder_Cell` added and used
#    17-Jun-2005 (MG) `Folder_Cell` changed: Use new `auto_attributes` feature
#    28-Jul-2005 (MG) `s/Folder_Cell/Box_Cell/s`
#    28-Jul-2005 (MG) `Box_Cell` style handling changed
#    30-Jul-2005 (MG) New styles added and used
#    31-Jul-2005 (CT) Style `Target` changed to match `Copied` of `Mailbox_MV`
#    31-Jul-2005 (CT) `_style` fixed (superfluous `return` removed)
#    ��revision-date�����
#--

from   _TGL                    import TGL
from   _PMA                    import PMA

import _PMA.Mailbox

import _PMA._UI
import _PMA._UI.Mixin
import _PMA._UI.Tree
import _PMA._UI.Tree_Adapter
import _PMA._UI.Mailbox_MV

class Box_Cell (PMA.UI.Message_Cell) :
    """Get the name of the folder from a `mailbox` object"""

    Ancestor = PMA.UI.Message_Cell

    renderer_class      = ("Cell_Renderer_Text")
    auto_attributes     = dict \
        ( Ancestor.auto_attributes
        , name          = ("text",       str, "_get_name")
        , font_weight   = ("weight",     int, "_get_font_weight")
        , font_style    = ("style",      int, "_get_font_style")
        )

    Unseen              = PMA.UI.Style \
        ( "unseen", Ancestor.Normal
        , foreground    = "red"
        )
    Target              = PMA.UI.Style \
        ( "target", Ancestor.Normal
        , background    = "cyan"
        )

    Unseen_Target       = PMA.UI.Style \
        ( "unseen_target", Unseen, Target)

    def _style (self, mailbox, office = None) :
        style = []
        if mailbox.unseen :
            style.append ("Unseen")
        if office.status.target_box is mailbox :
            style.append ("Target")
        if style :
            return getattr (self, "_".join (style))
        return self.Normal
    # end def _style

    def _get_name (self, mailbox, attr, office = None) :
        text = mailbox.name
        if mailbox.unseen :
            return "%s (%s)" % (text, mailbox.unseen)
        return text
    # end def _get_name

    def _get_font_weight (self, mailbox, attr, office = None) :
        style = self._style (mailbox, office)
        return dict (bold = 800).get (style.font_weight, 400)
    # end def _get_font_weight

    def _get_font_style (self, mailbox, attr, office) :
        style = self._style (mailbox, office)
        return dict (italic = 2).get (style.font_style, 0)
    # end def _get_font_style

# end class Box_Cell

class _MB_TA_ (PMA.UI.Tree_Adapter) :
    """Tree adapter for mailbox"""

    rules_hint = False
    schema     = \
        ( TGL.UI.Column ("Name", Box_Cell ())
        ,
        )

    def has_children (self, mailbox) :
        return bool (mailbox._box_dict)
    # end def has_children

    def children (self, mailbox) :
        return mailbox.sub_boxes
    # end def children

# end class _MB_TA_

class Mailbox_BV (PMA.UI.Rooted_Tree) :
    """Box view of mailbox"""

    Adapter = _MB_TA_

# end class Mailbox_BV

if __name__ != "__main__" :
    PMA.UI._Export ("*", "_MB_TA_")
### __END__ PMA.UI.Mailbox_BV
