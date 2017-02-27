#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016-2017 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria.
# Web: http://www.c-tanzer.at/en/ Email: tanzer@swing.co.at
# All rights reserved
# ****************************************************************************
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    _ReST.setup
#
# Purpose
#    Setup file for package namespace ReST
#
# Revision Dates
#    12-Oct-2016 (CT) Creation
#    13-Oct-2016 (CT) Use `find_packages`, `_TFL.fs_find`, not home-grown code
#    22-Feb-2017 (CT) Use `TFL_STP`, not home-grown code
#    27-Feb-2017 (CT) Add Python 3.6 to `classifiers`
#    ««revision-date»»···
#--

from   __future__               import print_function

from   setuptools               import setup

import TFL_STP as STP

STP.change_to_dir (__file__)

license = "BSD License"
name    = "ReST-Tapyr"
p_name  = "_ReST"

version              = STP.package_version ()
long_description     = STP.long_description ()
packages, data_files = STP.packages_plus_data_files (p_name)
Test_Command         = STP.Test_Command

if __name__ == "__main__" :
    setup \
    ( name                 = name
    , version              = version
    , description          =
        "Package augmenting docutil's reStructuredText handling."
    , long_description     = long_description
    , license              = license
    , author               = "Christian Tanzer"
    , author_email         = "tanzer@swing.co.at"
    , url                  = "https://github.com/Tapyr/tapyr"
    , packages             = packages
    , package_dir          = { p_name : "." }
    , package_data         = { p_name : data_files }
    , platforms            = "Any"
    , classifiers          = \
        [ "Development Status :: 5 - Production/Stable"
        , "License :: OSI Approved :: " + license
        , "Operating System :: OS Independent"
        , "Programming Language :: Python"
        , "Programming Language :: Python :: 2"
        , "Programming Language :: Python :: 2.7"
        , "Programming Language :: Python :: 3"
        , "Programming Language :: Python :: 3.5"
        , "Programming Language :: Python :: 3.6"
        , "Intended Audience :: Developers"
        , "Topic :: Software Development :: Libraries :: Python Modules"
        ]
    , setup_requires       = ["TFL_STP"]
    , install_requires     = ["TFL", "docutils"]
    , extras_require       = dict ()
    , cmdclass             = dict (test = Test_Command)
    , zip_safe             = False ### no eggs, please
    )

### __END__ _ReST.setup
