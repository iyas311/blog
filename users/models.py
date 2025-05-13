from django.db import models
from django.db import transaction
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator
# users/models.py
class CustomUser(AbstractUser):
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    def save(self, *args, **kwargs):
        # Ensure atomic update
        using = kwargs.get('using', 'default')
        with transaction.atomic(using=using):
            super().save(*args, **kwargs)