from PIL import Image

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from p9 import const



from django.db import models
import uuid
from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse
from django.utils.html import mark_safe


RATING = (
    ('0','☆☆☆☆☆'),
    ('1','⭐☆☆☆☆'),
    ('2','⭐⭐☆☆☆'),
    ('3','⭐⭐⭐☆☆'),
    ('4','⭐⭐⭐⭐☆'),
    ('5','⭐⭐⭐⭐⭐'),
)




class Ticket(models.Model):
    type = "ticket"
    title = models.CharField(max_length=128, verbose_name="titre")
    description = models.CharField(max_length=2048, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)

    class Meta:
        ordering = ('-time_created',)

    def resize_image(self):
        if self.image:
            image = Image.open(self.image)
            image.thumbnail(const.IMAGE_MAX_SIZE)
            image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

    def __str__(self):
        return f"{self.title} by {self.user}"


class Review(models.Model):
    type = "review"
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="review")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128, verbose_name="Titre")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Note")
    body = models.TextField(
        max_length=8192, blank=True, verbose_name="Commentaire")
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket} => {self.user}"


class UserFollows(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="follower")
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed")

    class Meta:
        unique_together = ('user', 'followed_user')

    def __str__(self):
        return f"{self.user} is following {self.followed_user}"