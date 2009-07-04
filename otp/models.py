from django.db import models
from django.contrib.auth.models import User

class UserService(models.Model):
    """
    """
    user = models.ForeignKey(User)
    service_id = models.CharField(max_length=32)
    params = models.TextField()
