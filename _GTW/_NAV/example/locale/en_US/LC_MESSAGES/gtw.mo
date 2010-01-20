��    0      �                �    #     /   =  +   m  -   �  .   �  0   �     '  F   >     �  �   �  -   9	  E   g	  %   �	  "   �	  1   �	     (
  3   =
  7   q
  7   �
  3   �
       $   !     F  "   M     p     w     �     �     �     �        +   "     N  '   l     �  :   �     �       "        ?     M  T   g     �  (   �  !   �  &     �  >  �  �  #   �  /   �  +     -   >  .   l  0   �     �  F   �     *  �   <  -   �  E     %   R  "   x  1   �     �  3   �  7     7   N  3   �     �  $   �     �  "   �               <     W     p     �      �  +   �     �  '        9  :   X     �     �  "   �     �     �  T        a  (   q  !   �  &   �   >>> class Media (Media) :
       ...     url = "/test/"
       ...
       >>> NL = chr (10)

       >>> m = Media (css_links = ("a.css", "/b/c.css"),
       ...       scripts = ("foo.js", "bar.js", "http://baz.js"))
       >>> print NL.join (repr (l) for l in m.css_links)
       all: /test/styles/a.css
       all: /b/c.css
       >>> tuple (str (l) for l in m.scripts)
       ('/test/js/foo.js', '/test/js/bar.js', 'http://baz.js')
       >>> n = Media (("/test/styles/a.css", CSS_Link ("c.css", "screen")))
       >>> print NL.join (repr (l) for l in n.css_links)
       all: /test/styles/a.css
       screen: /test/styles/c.css
       >>> tuple (str (l) for l in n.scripts)
       ()
       >>> q = Media (scripts = ("qux.js", ), children = (m, n))
       >>> print NL.join (repr (l) for l in q.css_links)
       all: /test/styles/a.css
       all: /b/c.css
       screen: /test/styles/c.css
       >>> "; ".join (str (l) for l in q.scripts)
       '/test/js/qux.js; /test/js/foo.js; /test/js/bar.js; http://baz.js' A Inline `form` inside a real form. A Inline_Description `form` inside a real form. A field group description for an MOM object A form which creates or changes a MOM object. A form which is embedded in a `Instance` form. A free field which should be part of a HTML form A group of form field. A javascript code which should be executed once the document is loaded A list of errors. A place holder in the field group description which will expand to
       all attributes of the given kinds which have not been added before the
       wildcard. A plain form with no object in the background A wrapper around the attribute of the MOM object used in field groups Abstract definition of a field group. Add a common prefix to all fields. An acount which uses passwords for authorization. Base class for forms Base class for the real form and the `nested` from. Common base class for essential classes of GTW.OMP.Auth Common base class for essential objects of GTW.OMP.Auth Default account for users which are not logging in. Description Formatter for attributes of Objects. Glueck Handles the login form processing. Martin Meta class for MOM object forms Meta class for plain forms Model a CSS link object. Model a `rel` link object. Model a group of accounts. Model a list of CSS_Link objects Model a list of javascript on-ready objects Model a list of media objects Model a list of media objects with href Model a list of script objects Model a list of unique media objects (filters duplicates). Model a script element Model an user account. Model association Account_in_Group Name of group Password for this account Specification of a widget to be used to render a form, field-group, or
       field. The login form. This account has super-user permissions. This account is currently active. User name associated with this account Project-Id-Version: PROJECT VERSION
Report-Msgid-Bugs-To: EMAIL@ADDRESS
POT-Creation-Date: 2010-01-20 20:56+0100
PO-Revision-Date: 2010-01-20 20:57+0100
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language-Team: en_US <LL@li.org>
Plural-Forms: nplurals=2; plural=(n != 1)
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 0.9.4
 >>> class Media (Media) :
       ...     url = "/test/"
       ...
       >>> NL = chr (10)

       >>> m = Media (css_links = ("a.css", "/b/c.css"),
       ...       scripts = ("foo.js", "bar.js", "http://baz.js"))
       >>> print NL.join (repr (l) for l in m.css_links)
       all: /test/styles/a.css
       all: /b/c.css
       >>> tuple (str (l) for l in m.scripts)
       ('/test/js/foo.js', '/test/js/bar.js', 'http://baz.js')
       >>> n = Media (("/test/styles/a.css", CSS_Link ("c.css", "screen")))
       >>> print NL.join (repr (l) for l in n.css_links)
       all: /test/styles/a.css
       screen: /test/styles/c.css
       >>> tuple (str (l) for l in n.scripts)
       ()
       >>> q = Media (scripts = ("qux.js", ), children = (m, n))
       >>> print NL.join (repr (l) for l in q.css_links)
       all: /test/styles/a.css
       all: /b/c.css
       screen: /test/styles/c.css
       >>> "; ".join (str (l) for l in q.scripts)
       '/test/js/qux.js; /test/js/foo.js; /test/js/bar.js; http://baz.js' A Inline `form` inside a real form. A Inline_Description `form` inside a real form. A field group description for an MOM object A form which creates or changes a MOM object. A form which is embedded in a `Instance` form. A free field which should be part of a HTML form A group of form field. A javascript code which should be executed once the document is loaded A list of errors. A place holder in the field group description which will expand to
       all attributes of the given kinds which have not been added before the
       wildcard. A plain form with no object in the background A wrapper around the attribute of the MOM object used in field groups Abstract definition of a field group. Add a common prefix to all fields. An acount which uses passwords for authorization. Base class for forms Base class for the real form and the `nested` from. Common base class for essential classes of GTW.OMP.Auth Common base class for essential objects of GTW.OMP.Auth Default account for users which are not logging in. Description Formatter for attributes of Objects. Glueck Handles the login form processing. Martin Meta class for MOM object forms Meta class for plain forms Model a CSS link object. Model a `rel` link object. Model a group of accounts. Model a list of CSS_Link objects Model a list of javascript on-ready objects Model a list of media objects Model a list of media objects with href Model a list of script objects Model a list of unique media objects (filters duplicates). Model a script element Model an user account. Model association Account_in_Group Name of group Password for this account Specification of a widget to be used to render a form, field-group, or
       field. The login form. This account has super-user permissions. This account is currently active. User name associated with this account 