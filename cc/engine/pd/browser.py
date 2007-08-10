from zope.app.pagetemplate import ViewPageTemplateFile
from zope.publisher.browser import BrowserPage

from cc.engine.chooser import BaseBrowserView

class pd_waiting_verification(BrowserPage):

    @property
    def email_result(self):
        """Send the PD verification email."""

        try:
            return self.__email_result
        except AttributeError:
            self.__email_result = self.context.send_pd_confirmation(
                'http://%s/license/publicdomain-3' % self.request['HTTP_HOST'],
                self.request.get('email', False),
                self.request.get('title', False),
                self.request.get('copyright_holder', False),
                )

            return self.__email_result
        

class pd_confirm(BrowserPage):

    @property
    def hash_ok(self):
        """Verify the hash and return True or False."""

        return self.context.generate_hash(
                   self.request.get('email', False),
                   self.request.get('title', False),
                   self.request.get('copyright_holder', False)
               ) == self.request.get('hash', None)

class pd_final(BaseBrowserView):

    _pt = ViewPageTemplateFile('templates/publicdomain-4.pt')
    
    def __call__(self):

        # YYY set the key so Results._issue works right
        self.request.form['publicdomain'] = True
        
        self.email_result = self.context.send_pd_dedication(
            self.request.get('email', False),
            self.request.get('title', False),
            self.request.get('copyright_holder', False),
            )

        # XXX handle partner interface
        return self._pt(self)