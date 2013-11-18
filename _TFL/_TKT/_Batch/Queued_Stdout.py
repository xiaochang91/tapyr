# -*- coding: utf-8 -*-
# Copyright (C) 2005-2008 Mag. Christian Tanzer. All rights reserved
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
#    TFL.TKT.Batch.Queued_Stdout
#
# Purpose
#    Provide thread-safe redirection of stdout for Batch toolkit
#
# Revision Dates
#     7-Feb-2005 (CT) Creation
#    27-Aug-2008 (CT) Rewritten as function
#    ««revision-date»»···
#--

from   _TFL           import TFL

import _TFL._TKT._Batch

import sys

def Queued_Stdout (out_widget) :
    ### no need for queuing in batch-mode
    return sys.stdout
# end def Queued_Stdout

if __name__ != "__main__" :
    TFL.TKT.Batch._Export ("*")
### __END__ TFL.TKT.Batch.Queued_Stdout
