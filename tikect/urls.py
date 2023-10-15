from django.urls import path
from tikect import views 


urlpatterns = [

    path('tikect/create/',views.create_tikect,
         name = 'create_tikect'
    ),

    path('ticket/<review_id>/delete/', views.delete_ticket,
        name="delete_ticket"
    ),
        
    path(
        'review/create/',
        views.review_create, name='review_create'
    ),

    path("ticket/<int:ticket_id>/edit", views.edit_ticket, name="edit_ticket"),
    path('review/<review_id>/edite/', views.edit_review,
        name="edit_review"
    ),
    path('review/<review_id>/delete/', views.delete_review,
        name="delete_review"
    ),
    path('flux/', views.flux, name="flux"),
    
    path('flux/own/', views.own_flux, name="own_flux"),
    
    path('follow-users/', views.follow_users, name='follow_users'),
    
    path('follow-users/<int:pk_subs>/delete',views.delete_subscript_user, name='delete_subs_user'),
    
    path('review_with_ticket/', views.review_with_ticket,
        name='review_with_ticket'
    ),
    
    path("posts", views.display_posts, name="display_posts"),
]
