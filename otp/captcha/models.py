from django.db import models
from captcha.conf import settings as captcha_settings
import datetime
try:
    import hashlib # sha for Python 2.5+
except ImportError:
    import sha # sha for Python 2.4 (deprecated in Python 2.6)
    hashlib = False

class CaptchaStore(models.Model):
    challenge = models.CharField(blank=False, max_length=32)
    response = models.CharField(blank=False, max_length=32)
    hashkey = models.CharField(blank=False, max_length=40,unique=True)
    expiration = models.DateTimeField(blank=False)
    
    def save(self,*args,**kwargs):
        self.response = self.response.lower()
        if not self.expiration:
            self.expiration = datetime.datetime.now() + datetime.timedelta(minutes= int(captcha_settings.CAPTCHA_TIMEOUT))
        if not self.hashkey:
            if hashlib:
                self.hashkey = hashlib.new('sha', str(self.challenge) + str(self.response)).hexdigest()
            else:
                self.hashkey = sha.new(str(self.challenge) + str(self.response)).hexdigest()
        super(CaptchaStore,self).save(*args,**kwargs)

    def __unicode__(self):
        return self.challenge

    
    def remove_expired(cls):
        cls.objects.filter(expiration__lte=datetime.datetime.now()).delete()
    remove_expired = classmethod(remove_expired)
    