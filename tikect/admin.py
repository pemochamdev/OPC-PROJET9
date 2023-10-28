from django.contrib import admin



from tikect.models import Ticket,Review,UserFollows



admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)











# @admin.register(Ticket)
# class TicketAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'time_created', 'time_update', 'view_image', 'reviewed')



# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('headline', 'ticket', 'user',  'time_created', 'time_updated')


# @admin.register(UserFollows)
# class UserFollowsAdmin(admin.ModelAdmin):
#     list_display = ('user', 'followed_user')
    
