from django.contrib.auth.models import AbstractUser
from tikect.models import Review, Ticket
from django.core.exceptions import PermissionDenied


class User(AbstractUser):

    def get_reviews(self):
        """Get all the reviews from the user"""
        reviews = Review.objects.filter(user=self)
        return reviews

    def get_tickets(self):
        """Get all the tickets from the user"""
        tickets = Ticket.objects.filter(user=self)
        return tickets

    def is_user(self, post):
        """Verify if the user wrote a post (ticket or review),
        return True or raise PermissionDenied"""
        if post.user == self:
            return True
        else:
            raise PermissionDenied()