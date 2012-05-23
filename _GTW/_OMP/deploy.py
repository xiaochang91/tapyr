# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this module; if not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.OMP.deploy
#
# Purpose
#    Provide an extendable Command for the deployment of applications based
#    on GTW.OMP
#
# Revision Dates
#    23-May-2012 (CT) Creation
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function#, unicode_literals

from   _GTW                   import GTW
from   _MOM                   import MOM
from   _TFL                   import TFL

import _GTW.deploy

class _GTW_OMP_Sub_Command_ (TFL.Sub_Command) :

    _rn_prefix = "_GTW_OMP"

_Sub_Command_ = _GTW_OMP_Sub_Command_ # end class

class GTW_OMP_Command (GTW.deploy.Command) :
    """Manage deployment applications based on GTW.OMP."""

    _rn_prefix              = "GTW_OMP_"

    class _GTW_OMP_Babel_ (_Sub_Command_, GTW.deploy.Command._Babel_) :

        _package_dirs           = \
            [ "_MOM"
            , "_GTW"
            , "_GTW/_OMP/_Auth"
            , "_GTW/_OMP/_PAP"
            , "_GTW/_OMP/_SWP"
            , "_GTW/_OMP/_SRM"
            , "_GTW/_OMP/_EVT"
            ]

    _Babel_ = _GTW_OMP_Babel_ # end class

    class _GTW_OMP_Migrate_ (_Sub_Command_) :
        """Migrate database from `active` or file to file or `passive`."""

        _opts                   = \
            ( "-Active:B?Migrate database from `active_name`"
            , "-Passive:B?Migrate database to `passive_name`"
            , "-db_name:Q=migration?Name of migration database"
            )

    _Migrate_ = _GTW_OMP_Migrate_ # end class

    def _handle_migrate (self, cmd) :
        P      = self._P (cmd)
        cwd    = self.pbl.cwd
        pyc    = self.pbc.python
        db_url = "hps://" + cmd.db_name
        args   = ("-overwrite", "-verbose")
        if cmd.app_config :
            args += ("-config", ":".join (cmd.app_config))
        def _do (path, migration_cmd) :
            with cwd (P.root / path / cmd.app_dir) :
                if cmd.verbose or cmd.dry_run :
                    print ("cd", self.pbl.path ())
                    print (migration_cmd, " ".join (args))
                if not cmd.dry_run :
                    migration_cmd (* args)
        if cmd.Active :
            cmd_a = pyc \
                [cmd.app_module, "@mig1", "-target_db_url", db_url, "-readonly"]
            _do ( P.active
                , pyc
                    [ cmd.app_module, "@mig1", "-target_db_url", db_url
                    , "-readonly"
                    ]
                )
        if cmd.Passive :
            _do ( P.passive, pyc [cmd.app_module, "@mig2", "-db_url", db_url])
    # end def _handle_migrate

Command = GTW_OMP_Command # end class

if __name__ != "__main__" :
    GTW.OMP._Export_Module ()
### __END__ GTW.OMP.deploy
