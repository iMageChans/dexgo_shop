from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    inviter = models.ForeignKey(User, related_name='invitees', on_delete=models.SET_NULL, null=True, blank=True)
    invite_code = models.CharField(max_length=10, unique=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = str(uuid.uuid4())[:10]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
