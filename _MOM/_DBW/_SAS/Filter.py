# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    MOM.DBW.SAS.Filter
#
# Purpose
#    Extend FTL.Filter to support the generation of the code required to use
#    the SQL layer of SQLAlchemy
#
# Revision Dates
#    12-Feb-2010 (MG) Creation (based on SA.Filter)
#    ��revision-date�����
#--

from   _TFL              import TFL
import _TFL.Accessor
import _TFL.Decorator
import _TFL.Filter
import _TFL.Q_Exp
from    sqlalchemy.sql   import expression

SAS_Attr_Map = dict \
    ( type_name = TFL.Getter.Type_Name
    )

@TFL.Add_To_Class ("_sa_filter", TFL.Q_Exp.Get)
def _sa_filter (self, SAQ) :
    attr       = self.name.split (".", 1) [0]
    _sa_filter = SAQ._ID_ENTITY_ATTRS.get (attr, None)
    if _sa_filter :
        return _sa_filter (self.name)
    return (), (SAS_Attr_Map.get (self.name, self.getter) (SAQ), )
# end def _sa_filter

@TFL.Add_To_Class ("_sa_filter", TFL.Q_Exp.Bin_Bool, TFL.Q_Exp.Bin_Expr)
def _sa_filter (self, SAQ) :
    args    = []
    joins   = set ()
    for arg in self.lhs, self.rhs :
        if hasattr (arg, "_sa_filter") :
            ajoins, afilter = arg._sa_filter (SAQ)
            joins.update  (ajoins)
            args.extend   (afilter)
        else :
            args.append (arg)
    return joins, (getattr (args [0], self.op.__name__) (args [1]), )
# end def _sa_filter

@TFL.Add_To_Class ("_sa_filter", TFL.Attr_Query.Call)
def _sa_filter (self, SAQ) :
    lhs = self.lhs._sa_filter (SAQ)
    op  = self.op.__name__.lower ()
    return (), (getattr (lhs, op) (* self.args), )
# end def _sa_filter

TFL._Filter_Q_.predicate_precious_p = True
@TFL.Add_To_Class ("_sa_filter", TFL.Filter_And, TFL.Filter_Or, TFL.Filter_Not)
def _sa_filter (self, SAQ) :
    sa_exp = getattr \
        ( expression
        , "%s_" % (self.__class__.__name__.rsplit ("_",1) [-1].lower (), )
        )
    return (), (sa_exp (* (p._sa_filter (SAQ) for p in self.predicates)), )
# end def _sa_filter

### __END__ MOM.DBW.SAS.Filter
