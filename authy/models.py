from django.db import models
from django.contrib.auth.models import AbstractUser

#study gyaan

from tikect.models import Review, Ticket


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=100)
    username = models.CharField(max_length=100)
    follows = models.ManyToManyField(
        'self',
        symmetrical=False,
        verbose_name='suit',
    )


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
   