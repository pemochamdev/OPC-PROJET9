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
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, null=True,
        related_name='ticket_user'
    )
    title = models.CharField(max_length=200,
        verbose_name='Ticket'
    )
    description = models.TextField(max_length=5000)
    image = models.ImageField(upload_to='tikect',
        null=False
    )
    reviewed = models.BooleanField(default=False)
    time_created = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)



    def view_image(self):
        if self.image:
            return mark_safe('<img src="{}" width = "50" height="50"/>'.format(self.image.url))
        
        return ''        
    
    
    def __str__(self):
        return self.title
    
    
    
    def get_absolute_url(self):
        return reverse("tikect", args=[self.pk])





class Review(models.Model):
    headline = models.CharField(max_length=128)
    
    ticket = models.ForeignKey(Ticket,
        on_delete=models.CASCADE,
        related_name='review_tikects'
    )
    rating = models.CharField(default=None, max_length=10, choices=RATING)

    description = models.CharField(max_length=8192, blank=True)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_review')
    
    time_created = models.DateTimeField(auto_now_add=True)
    
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.headline


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
     
        verbose_name = 'User Follows'
        verbose_name_plural = 'User Follows'