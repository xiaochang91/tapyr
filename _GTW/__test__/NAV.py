# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.__test__.
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
#    GTW.__test__.NAV
#
# Purpose
#    Test GTW.NAV functionality
#
# Revision Dates
#    27-Jan-2012 (CT) Creation
#     2-Jun-2012 (CT) Rename `suppress_translation_loading` to `load_I18N`
#    26-Jul-2012 (CT) Adapt to use of `GTW.RST.TOP` instead of `GTW.NAV`
#     6-Dec-2012 (CT) Remove `Entity_created_by_Person`
#    11-Dec-2012 (CT) Add error `410`
#    12-Dec-2012 (CT) Add `Person_has_Account`
#    20-Jan-2013 (CT) Change `401`
#    21-Mar-2013 (CT) Add `Company_R` and tests for `Query_Restriction_Spec`
#    ��revision-date�����
#--

from   __future__  import unicode_literals

_test_code = """

    >>> nav_root = app
    >>> TTT      = nav_root.Templateer.Template_Type
    >>> print nav_root.abs_href
    /

    >>> for t in sorted (nav_root.template_iter ()) :
    ...    print t.name
    400
    401
    403
    404
    405
    408
    410
    500
    503
    account_change_email
    account_change_password
    account_make_cert
    account_register
    account_reset_password
    calendar
    calendar_day
    console
    e_type_admin
    e_type_afs
    e_type_afs|afs_div_seq
    e_type_afs|afs_div_seq|afs_fc_horizo
    e_type_aggregator
    e_type_delete
    gallery
    html/static.jnj
    login
    photo
    regatta_calendar
    regatta_page
    regatta_registration
    regatta_result
    regatta_result_teamrace
    site_admin

    >>> for k in sorted (TTT.css_href_map) :
    ...    print k
    400
    401
    403
    404
    405
    408
    410
    500
    503
    account_change_email
    account_change_password
    account_make_cert
    account_register
    account_reset_password
    calendar
    calendar_day
    console
    e_type_admin
    e_type_afs
    e_type_afs|afs_div_seq
    e_type_afs|afs_div_seq|afs_fc_horizo
    gallery
    html/static.jnj
    login
    photo
    site_admin

    >>> for owl in nav_root.own_links_transitive :
    ...   if not owl.hidden:
    ...     print owl.href, owl.template.name
    Admin site_admin
    Admin/Benutzerverwaltung site_admin
    Admin/Personenverwaltung site_admin
    Admin/Personenverwaltung/Address e_type_admin
    Admin/Personenverwaltung/Address_Position e_type_admin
    Admin/Personenverwaltung/Company e_type_admin
    Admin/Personenverwaltung/Company_R e_type_admin
    Admin/Personenverwaltung/Company_has_Address e_type_admin
    Admin/Personenverwaltung/Company_has_Email e_type_admin
    Admin/Personenverwaltung/Company_has_Phone e_type_admin
    Admin/Personenverwaltung/Company_has_Url e_type_admin
    Admin/Personenverwaltung/Email e_type_admin
    Admin/Personenverwaltung/Person e_type_admin
    Admin/Personenverwaltung/Person_has_Account e_type_admin
    Admin/Personenverwaltung/Person_has_Address e_type_admin
    Admin/Personenverwaltung/Person_has_Email e_type_admin
    Admin/Personenverwaltung/Person_has_Phone e_type_admin
    Admin/Personenverwaltung/Person_has_Url e_type_admin
    Admin/Personenverwaltung/Phone e_type_admin
    Admin/Personenverwaltung/Url e_type_admin
    Admin/Regattaverwaltung site_admin
    Admin/Regattaverwaltung/Boat e_type_admin
    Admin/Regattaverwaltung/Boat_Class e_type_admin
    Admin/Regattaverwaltung/Boat_in_Regatta e_type_admin
    Admin/Regattaverwaltung/Club e_type_admin
    Admin/Regattaverwaltung/Regatta_C e_type_admin
    Admin/Regattaverwaltung/Regatta_Event e_type_admin
    Admin/Regattaverwaltung/Regatta_H e_type_admin
    Admin/Regattaverwaltung/Regatta_Page e_type_admin
    Admin/Regattaverwaltung/Sailor e_type_admin
    Admin/Regattaverwaltung/Team e_type_admin
    Admin/Regattaverwaltung/Team_has_Boat_in_Regatta e_type_admin
    Admin/Webseitenverwaltung site_admin
    Admin/Webseitenverwaltung/Calendar e_type_admin
    Admin/Webseitenverwaltung/Clip_X e_type_admin
    Admin/Webseitenverwaltung/Event e_type_admin
    Admin/Webseitenverwaltung/Gallery e_type_admin
    Admin/Webseitenverwaltung/Page e_type_admin
    Admin/Webseitenverwaltung/Picture e_type_admin

    >>> php = nav_root.resource_from_href ("Admin/Personenverwaltung/Person_has_Phone/create")
    >>> print php.href, php.template.name
    Admin/Personenverwaltung/Person_has_Phone/create e_type_afs|afs_div_seq

    >>> css_map = TFL.defaultdict (list)
    >>> for k, v in TTT.css_href_map.iteritems () :
    ...     css_map [v].append (k)
    >>> css_users = sorted (sorted (vs) for vs in css_map.itervalues ())
    >>> print formatted (css_users)
    [
      [ 400
      , 403
      , 404
      , 405
      , 408
      , 410
      , 500
      , 503
      , 'account_change_email'
      , 'account_make_cert'
      , 'account_register'
      , 'account_reset_password'
      , 'calendar'
      , 'calendar_day'
      , 'html/static.jnj'
      ]
    ,
      [ 401
      , 'login'
      ]
    , [ 'account_change_password' ]
    , [ 'console' ]
    , [ 'e_type_admin' ]
    ,
      [ 'e_type_afs'
      , 'e_type_afs|afs_div_seq'
      , 'e_type_afs|afs_div_seq|afs_fc_horizo'
      ]
    , [ 'gallery' ]
    , [ 'photo' ]
    , [ 'site_admin' ]
    ]

    >>> crad = nav_root.ET_Map ["PAP.Company_R"].admin
    >>> crad
    <E_Type Company_R: /Admin/Personenverwaltung/Company_R>

    >>> QR = crad.QR
    >>> QR
    <class '_GTW._RST._TOP._MOM.Query_Restriction.Query_Restriction'>

    >>> crad.E_Type.AQ.affiliate
    <affiliate.AQ [Attr.Type.Querier Id_Entity]>

    >>> crad.E_Type.AQ.affiliate.QR
    Q.affiliate
    >>> tuple (a.QR for a in crad.E_Type.AQ.affiliate.Attrs)
    (Q.affiliate.__raw_name, Q.affiliate.__raw_registered_in, Q.affiliate.lifetime, Q.affiliate.__raw_short_name, Q.affiliate.affiliate, Q.affiliate.owner)

    >>> print (formatted (QR.Filter_Atoms (QR.Filter (crad.E_Type, "affiliate"))))
    ( Record
      ( AQ = <name.AQ [Attr.Type.Querier String]>
      , attr = String `name`
      , edit = None
      , full_name = 'name'
      , id = 'name___AC'
      , name = 'name___AC'
      , op = Record
          ( desc = 'Select entities where the attribute value starts with the specified value'
          , label = 'auto-complete'
          )
      , sig_key = 3
      , ui_name = 'Name'
      , value = None
      )
    , Record
      ( AQ = <registered_in.AQ [Attr.Type.Querier String]>
      , attr = String `registered_in`
      , edit = None
      , full_name = 'registered_in'
      , id = 'registered_in___AC'
      , name = 'registered_in___AC'
      , op = Record
          ( desc = 'Select entities where the attribute value starts with the specified value'
          , label = 'auto-complete'
          )
      , sig_key = 3
      , ui_name = 'Registered in'
      , value = None
      )
    )

    >>> print (formatted (QR.Filter (crad.E_Type, "affiliate")))
    Record
    ( AQ = <affiliate.AQ [Attr.Type.Querier Id_Entity]>
    , Class = 'Entity'
    , attr = Entity `affiliate`
    , attrs =
        [ Record
          ( attr = String `name`
          , full_name = 'affiliate.name'
          , id = 'affiliate__name'
          , name = 'name'
          , sig_key = 3
          , ui_name = 'Affiliate/Name'
          )
        , Record
          ( attr = String `registered_in`
          , full_name = 'affiliate.registered_in'
          , id = 'affiliate__registered_in'
          , name = 'registered_in'
          , sig_key = 3
          , ui_name = 'Affiliate/Registered in'
          )
        , Record
          ( attr = Date_Interval `lifetime`
          , attrs =
              [ Record
                ( attr = Date `start`
                , full_name = 'affiliate.lifetime.start'
                , id = 'affiliate__lifetime__start'
                , name = 'start'
                , sig_key = 0
                , ui_name = 'Affiliate/Lifetime/Start'
                )
              , Record
                ( attr = Date `finish`
                , full_name = 'affiliate.lifetime.finish'
                , id = 'affiliate__lifetime__finish'
                , name = 'finish'
                , sig_key = 0
                , ui_name = 'Affiliate/Lifetime/Finish'
                )
              , Record
                ( attr = Boolean `alive`
                , choices =
                    [ 'no'
                    , 'yes'
                    ]
                , full_name = 'affiliate.lifetime.alive'
                , id = 'affiliate__lifetime__alive'
                , name = 'alive'
                , sig_key = 1
                , ui_name = 'Affiliate/Lifetime/Alive'
                )
              ]
          , full_name = 'affiliate.lifetime'
          , id = 'affiliate__lifetime'
          , name = 'lifetime'
          , ui_name = 'Affiliate/Lifetime'
          )
        , Record
          ( attr = String `short_name`
          , full_name = 'affiliate.short_name'
          , id = 'affiliate__short_name'
          , name = 'short_name'
          , sig_key = 3
          , ui_name = 'Affiliate/Short name'
          )
        , Record
          ( Class = 'Entity'
          , attr = Entity `affiliate`
          , full_name = 'affiliate.affiliate'
          , id = 'affiliate__affiliate'
          , name = 'affiliate'
          , sig_key = 2
          , ui_name = 'Affiliate/Affiliate'
          )
        , Record
          ( Class = 'Entity'
          , attr = Entity `owner`
          , children_np =
              [ { 'type_name' : 'PAP.Company'
                , 'ui_name' : 'Company'
                }
              , { 'type_name' : 'PAP.Person'
                , 'ui_name' : 'Person'
                }
              ]
          , default_child = 'PAP.Person'
          , full_name = 'affiliate.owner'
          , id = 'affiliate__owner'
          , name = 'owner'
          , sig_key = 2
          , ui_name = 'Affiliate/Owner'
          )
        ]
    , edit = None
    , full_name = 'affiliate'
    , id = 'affiliate___AC'
    , name = 'affiliate___AC'
    , op = Record
        ( desc = 'Select entities where the attribute is equal to the specified value'
        , label = 'auto-complete'
        )
    , sig_key = 2
    , ui_name = 'Affiliate'
    , value = None
    )

    >>> print (formatted (QR.Filter (crad.E_Type, "affiliate__name")))
    Record
    ( AQ = <affiliate.name.AQ [Attr.Type.Querier String]>
    , attr = String `name`
    , edit = None
    , full_name = 'affiliate.name'
    , id = 'affiliate__name___AC'
    , name = 'affiliate__name___AC'
    , op = Record
        ( desc = 'Select entities where the attribute value starts with the specified value'
        , label = 'auto-complete'
        )
    , sig_key = 3
    , ui_name = 'Affiliate/Name'
    , value = None
    )

    >>> print (formatted (QR.Filter (crad.E_Type, "affiliate__lifetime")))
    Record
    ( AQ = <affiliate.lifetime.AQ [Attr.Type.Querier Composite]>
    , attr = Date_Interval `lifetime`
    , attrs =
        [ Record
          ( attr = Date `start`
          , full_name = 'affiliate.lifetime.start'
          , id = 'affiliate__lifetime__start'
          , name = 'start'
          , sig_key = 0
          , ui_name = 'Affiliate/Lifetime/Start'
          )
        , Record
          ( attr = Date `finish`
          , full_name = 'affiliate.lifetime.finish'
          , id = 'affiliate__lifetime__finish'
          , name = 'finish'
          , sig_key = 0
          , ui_name = 'Affiliate/Lifetime/Finish'
          )
        , Record
          ( attr = Boolean `alive`
          , choices =
              [ 'no'
              , 'yes'
              ]
          , full_name = 'affiliate.lifetime.alive'
          , id = 'affiliate__lifetime__alive'
          , name = 'alive'
          , sig_key = 1
          , ui_name = 'Affiliate/Lifetime/Alive'
          )
        ]
    , edit = None
    , full_name = 'affiliate.lifetime'
    , id = 'affiliate__lifetime___AC'
    , name = 'affiliate__lifetime___AC'
    , op = Record
        ( desc = 'Select entities where the attribute is equal to the specified value'
        , label = 'auto-complete'
        )
    , ui_name = 'Affiliate/Lifetime'
    , value = None
    )

    >>> print (formatted (QR.Filter (crad.E_Type, "affiliate__lifetime", dict (start = "20130320"))))
    Record
    ( AQ = <affiliate.lifetime.AQ [Attr.Type.Querier Composite]>
    , attr = Date_Interval `lifetime`
    , attrs =
        [ Record
          ( attr = Date `start`
          , full_name = 'affiliate.lifetime.start'
          , id = 'affiliate__lifetime__start'
          , name = 'start'
          , sig_key = 0
          , ui_name = 'Affiliate/Lifetime/Start'
          )
        , Record
          ( attr = Date `finish`
          , full_name = 'affiliate.lifetime.finish'
          , id = 'affiliate__lifetime__finish'
          , name = 'finish'
          , sig_key = 0
          , ui_name = 'Affiliate/Lifetime/Finish'
          )
        , Record
          ( attr = Boolean `alive`
          , choices =
              [ 'no'
              , 'yes'
              ]
          , full_name = 'affiliate.lifetime.alive'
          , id = 'affiliate__lifetime__alive'
          , name = 'alive'
          , sig_key = 1
          , ui_name = 'Affiliate/Lifetime/Alive'
          )
        ]
    , edit =
        { 'start' : '20130320' }
    , full_name = 'affiliate.lifetime'
    , id = 'affiliate__lifetime___AC'
    , name = 'affiliate__lifetime___AC'
    , op = Record
        ( desc = 'Select entities where the attribute is equal to the specified value'
        , label = 'auto-complete'
        )
    , ui_name = 'Affiliate/Lifetime'
    , value = <Recursion on dict...>
    )

    >>> print (formatted (QR.Filter (crad.E_Type, "affiliate__lifetime__start")))
    Record
    ( AQ = <affiliate.lifetime.start.AQ [Attr.Type.Querier Date]>
    , attr = Date `start`
    , edit = None
    , full_name = 'affiliate.lifetime.start'
    , id = 'affiliate__lifetime__start___AC'
    , name = 'affiliate__lifetime__start___AC'
    , op = Record
        ( desc = 'Select entities where the attribute is equal to the specified value'
        , label = 'auto-complete'
        )
    , sig_key = 0
    , ui_name = 'Affiliate/Lifetime/Start'
    , value = None
    )

    >>> qrs = crad.qr_spec
    >>> qrs
    <Attr.Type.Querier.Query_Restriction_Spec for PAP.Company_R>

    >>> print (formatted (qrs.As_Template_Elem))
    [ Record
      ( attr = String `name`
      , full_name = 'name'
      , id = 'name'
      , name = 'name'
      , sig_key = 3
      , ui_name = 'Name'
      )
    , Record
      ( attr = String `registered_in`
      , full_name = 'registered_in'
      , id = 'registered_in'
      , name = 'registered_in'
      , sig_key = 3
      , ui_name = 'Registered in'
      )
    , Record
      ( attr = Date_Interval `lifetime`
      , attrs =
          [ Record
            ( attr = Date `start`
            , full_name = 'lifetime.start'
            , id = 'lifetime__start'
            , name = 'start'
            , sig_key = 0
            , ui_name = 'Lifetime/Start'
            )
          , Record
            ( attr = Date `finish`
            , full_name = 'lifetime.finish'
            , id = 'lifetime__finish'
            , name = 'finish'
            , sig_key = 0
            , ui_name = 'Lifetime/Finish'
            )
          , Record
            ( attr = Boolean `alive`
            , choices =
                [ 'no'
                , 'yes'
                ]
            , full_name = 'lifetime.alive'
            , id = 'lifetime__alive'
            , name = 'alive'
            , sig_key = 1
            , ui_name = 'Lifetime/Alive'
            )
          ]
      , full_name = 'lifetime'
      , id = 'lifetime'
      , name = 'lifetime'
      , ui_name = 'Lifetime'
      )
    , Record
      ( attr = String `short_name`
      , full_name = 'short_name'
      , id = 'short_name'
      , name = 'short_name'
      , sig_key = 3
      , ui_name = 'Short name'
      )
    , Record
      ( Class = 'Entity'
      , attr = Entity `affiliate`
      , attrs =
          [ Record
            ( attr = String `name`
            , full_name = 'affiliate.name'
            , id = 'affiliate__name'
            , name = 'name'
            , sig_key = 3
            , ui_name = 'Affiliate/Name'
            )
          , Record
            ( attr = String `registered_in`
            , full_name = 'affiliate.registered_in'
            , id = 'affiliate__registered_in'
            , name = 'registered_in'
            , sig_key = 3
            , ui_name = 'Affiliate/Registered in'
            )
          , Record
            ( attr = Date_Interval `lifetime`
            , attrs =
                [ Record
                  ( attr = Date `start`
                  , full_name = 'affiliate.lifetime.start'
                  , id = 'affiliate__lifetime__start'
                  , name = 'start'
                  , sig_key = 0
                  , ui_name = 'Affiliate/Lifetime/Start'
                  )
                , Record
                  ( attr = Date `finish`
                  , full_name = 'affiliate.lifetime.finish'
                  , id = 'affiliate__lifetime__finish'
                  , name = 'finish'
                  , sig_key = 0
                  , ui_name = 'Affiliate/Lifetime/Finish'
                  )
                , Record
                  ( attr = Boolean `alive`
                  , choices = <Recursion on list...>
                  , full_name = 'affiliate.lifetime.alive'
                  , id = 'affiliate__lifetime__alive'
                  , name = 'alive'
                  , sig_key = 1
                  , ui_name = 'Affiliate/Lifetime/Alive'
                  )
                ]
            , full_name = 'affiliate.lifetime'
            , id = 'affiliate__lifetime'
            , name = 'lifetime'
            , ui_name = 'Affiliate/Lifetime'
            )
          , Record
            ( attr = String `short_name`
            , full_name = 'affiliate.short_name'
            , id = 'affiliate__short_name'
            , name = 'short_name'
            , sig_key = 3
            , ui_name = 'Affiliate/Short name'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `affiliate`
            , full_name = 'affiliate.affiliate'
            , id = 'affiliate__affiliate'
            , name = 'affiliate'
            , sig_key = 2
            , ui_name = 'Affiliate/Affiliate'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `owner`
            , children_np =
                [ { 'type_name' : 'PAP.Company'
                  , 'ui_name' : 'Company'
                  }
                , { 'type_name' : 'PAP.Person'
                  , 'ui_name' : 'Person'
                  }
                ]
            , default_child = 'PAP.Person'
            , full_name = 'affiliate.owner'
            , id = 'affiliate__owner'
            , name = 'owner'
            , sig_key = 2
            , ui_name = 'Affiliate/Owner'
            )
          ]
      , full_name = 'affiliate'
      , id = 'affiliate'
      , name = 'affiliate'
      , sig_key = 2
      , ui_name = 'Affiliate'
      )
    , Record
      ( Class = 'Entity'
      , attr = Entity `owner`
      , children_np =
          [ { 'type_name' : 'PAP.Company'
            , 'ui_name' : 'Company'
            }
          , { 'type_name' : 'PAP.Person'
            , 'ui_name' : 'Person'
            }
          ]
      , default_child = 'PAP.Person'
      , full_name = 'owner'
      , id = 'owner'
      , name = 'owner'
      , sig_key = 2
      , ui_name = 'Owner'
      )
    ]

"""

import os
os.environ.update \
    ( dict
        ( GTW_FULL_OBJECT_MODEL = "True"
        )
    )

from   _GTW.__test__.model      import *

from   _TFL.Formatter           import Formatter

_Ancestor_Essence = GTW.OMP.PAP.Company

class Company_R (_Ancestor_Essence) :
    """Company subcluss to test recursive E_Type attribute"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class affiliate  (A_Id_Entity) :
            """Affiliate of the company"""

            kind               = Attr.Optional
            P_Type             = "GTW.OMP.PAP.Company_R"

        # end class affiliate

        class owner (A_Id_Entity) :
            """Owner of the company"""

            kind               = Attr.Optional
            P_Type             = "GTW.OMP.PAP.Subject"

        # end class affiliate

    # end class _Attributes

# end class Company_R

GTW.OMP.PAP.Nav.Admin.Company_R = dict (ETM = "GTW.OMP.PAP.Company_R")

formatted = Formatter (width = 240)

__test__ = dict \
    ( NAV_test = _test_code
    )

app = Scaffold \
    ( [ "wsgi"
      , "-db_url",    "hps://"
      , "-db_name",   "test"
      , "-debug",     "yes"
      , "-load_I18N", "no"
      ]
    )

### __END__ GTW.__test__.NAV
