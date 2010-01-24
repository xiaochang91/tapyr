# -*- coding: iso-8859-1 -*-
# simple example to test if a redirect works
from   _TFL            import TFL
import _TFL.I18N
from   _GTW            import GTW
import _GTW._NAV.Base

class Redirect (GTW.NAV.Page) :
    """Always redirect"""

    def _view (self, handler) :
        cls = self.top.HTTP.Status.Table [self.code]
        raise cls (self.redirect_to)
    # end def _view

# end class Redirect

class Error (GTW.NAV.Page) :
    """Display error"""

    def _view (self, handler) :
        cls = self.top.HTTP.Status.Table [self.code]
        raise cls
    # end def _view

# end class Error

class E_Type_Form (GTW.NAV.Page) :

    def rendered (self, context) :
        et_man  = self.form.et_man
        context ["objects"] = et_man.query ().limit (10).all ()
        request = context ["request"]
        pid     = request.arguments.get ("obj")
        form    = None
        if pid :
            instance = self.form.et_man.query (pid = pid [0]).one ()
        if request.method == "POST" :
            pass
        else :
            if request.arguments.get ("new") :
                form = self.form (self.abs_href)
        context ["form"] = form
        return self.__super.rendered (context)
    # end def rendered

# end class E_Type_Form

class I18N_Test (GTW.NAV.Page) :

    def rendered (self, context) :
        request = context ["request"]
        lang    = request.arguments.get ("lang", ("en_US", )) [0]
        #import pdb; pdb.set_trace ()
        with TFL.I18N.context (lang) :
            context ["lang"] = lang
            return self.__super.rendered (context)
    # end def rendered

# end class I18N_Test

### __END__ Redirect
