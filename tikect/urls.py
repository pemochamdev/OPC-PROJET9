from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('flux/', views.flux, name="flux"),
    path('flux/<int:page>/', views.flux, name="flux"),
    path('ticket_create/', views.ticket_create, name='ticket_create'),
    path(
        'review_create/',
        views.review_create, name='review_create'),
    path('review_publish/', views.review_publish, name='review_publish'),
    path('posts/', views.posts, name='posts'),
    path('posts/<int:page>/', views.posts, name='posts'),
    path(
        'post_delete/<str:type>/<int:id>/',
        views.post_delete, name='post_delete'),
    path(
        'post_update/<str:type>/<int:id>/',
        views.post_update, name='post_update'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('unfollow/<int:id>/', views.unfollow, name='unfollow'),

]