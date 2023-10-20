from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages

from itertools import chain
from django.db.models import Q, Value, CharField
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.http import Http404




from authy.models import User
from tikect.models import Ticket, Review, UserFollows
from tikect.forms import TicketForm, ReviewForm, DeleteReviewForm, FollowUsersForm,DeleteTicketReviewForm

########################```````````Welcome to My flux``````````````#######################
########################```````````````````````````````````````````#######################
####################### flux, own_flux                             #######################
#######################~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#######################
#######################~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#######################



@login_required
def flux(request):
    
    
    #Nos followers
    
    user_follows = UserFollows.objects.filter(user=request.user).values('followed_user')


    #Toutes nos reviews et celles de nos followers
    all_reviews = Review.objects.filter( Q(user__in=user_follows) | Q(user = request.user.id))
    

    #Tous nos tickets et ceux de nos follows
    all_tickets= Ticket.objects.filter(Q(author__in = user_follows) | Q(author = request.user))
    

    all_unreviewed_tickets = all_tickets.exclude(review_tikects__in=all_reviews).annotate(
        state=Value("UNREVIEWED", CharField())
    )

    review_and_ticket = sorted(
        chain(
            all_reviews, all_unreviewed_tickets
        ), 
        key=lambda instance:instance.time_created,
        # reverse =True pour indiquer que le tri doit etre effectue dans
        # l'ordre decroissant
        reverse=True
    )
    paginator = Paginator(review_and_ticket, 4)
    page_number = request.GET.get('page')
    user = request.user
    page_flux = paginator.get_page(page_number)

    context = {
        'page_flux': page_flux,
        'user':user,
    }

    return render(request, 'tikect/flux.html', context)


@login_required
def own_flux(request):
    
    
    reviews = Review.objects.filter(user = request.user)
    tickets = Ticket.objects.filter(author = request.user)


    review_ticket = sorted(
        chain(
            reviews, tickets
        ), 
        key= lambda instance: instance.time_created, reverse=True
    )

    paginator = Paginator(review_ticket, 4)
    page_number = request.GET.get('page')
    own_flux_page = paginator.get_page(page_number)
    context = {
        'own_flux_page': own_flux_page,
    }
    return render(request, 'tikect/posts.html', context)


########################```````````Welcome to My ticket````````````#######################
########################```````````````````````````````````````````#######################
####################### create_ticket, edite_tticket, delete_ticket#######################
#######################~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#######################
#######################~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#######################

@login_required
def create_tikect(request):
    if request.method =='POST':
        form = TicketForm(request.POST, request.FILES)
        print('post type')
        if form.is_valid():
            print('valide')
            
            ticket = form.save(commit = False)
            ticket.author = request.user
            
            ticket.save()            
            return redirect ('display_posts')
    else:
        form = TicketForm()
    context = {
        'form':form,
    }
    return render(request, 'tikect/create_ticket_form.html', context)

def edit_ticket(request, ticket_id):

    ticket = get_object_or_404(Ticket, id=ticket_id)
   
    photo_url = ticket.image.url
    edit_form = TicketForm(instance=ticket)
    delete_form = DeleteTicketReviewForm()
    if request.method == "POST":
        print('post ')
    
        edit_form = TicketForm(instance=ticket)
        print('edit_ticket')
        image = request.FILES.get("image")
        ticket.image = image
        edit_form = TicketForm(request.POST, instance=ticket)
        if edit_form.is_valid():
            edit_form.save()
            return redirect("display_posts")
        if "delete_ticket_or_review" in request.POST:
            delete_form = DeleteTicketReviewForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect("display_posts")

    context = {
        "photo_url": photo_url,
        "edit_form": edit_form,
        "delete_form": delete_form,
    }
    return render(request, "tikect/edit_ticket.html", context=context)


@login_required
def delete_ticket(request, ticket_id):
    tikect = get_object_or_404(Ticket , id=ticket_id)
    tikect.delete()
    return redirect('display_posts')



########################```````````Welcome to My review````````````#######################
########################```````````````````````````````````````````#######################
####################### create_review, edite_treview, delete_review#######################
#######################~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#######################
#######################~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#######################


@login_required
def review_create(request):
   
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST, request.FILES)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.author = request.user
            ticket.reviewed = True
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('display_posts')
     
    else:
        review_form = ReviewForm()
        ticket_form  = TicketForm()
    context = {
        "ticket_form": ticket_form,
        "review_form": review_form,
    }
    return render(request, "tikect/review_create.html", context)

@login_required
def edit_review(request, review_id):

    review = get_object_or_404(Review, id=review_id)
    
    edit_form = ReviewForm(instance=review)
    delete_form = DeleteTicketReviewForm()
    if request.method == "POST":
        print('post')
        delete_form = DeleteTicketReviewForm(request.POST)
        rating = request.POST.get("rating")
        review.rating = rating
        edit_form = ReviewForm(request.POST, instance=review)
        if edit_form.is_valid():
            print()
            edit_form.save()
            return redirect("display_posts")
        if "delete_ticket_or_review" in request.POST:
            delete_form = DeleteTicketReviewForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect("display_posts")

    context = {
        "review": review,
        "edit_form": edit_form,
        "delete_form": delete_form,
        "range": range(6),
    }
    return render(request, "tikect/edit_review.html", context=context)



@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    ticket = get_object_or_404(Ticket, id = review.ticket.id)
    ticket.reviewed = False
    ticket.save()
    review.delete()
    return redirect('display_posts')



@login_required
def review_with_ticket(request):

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST, request.FILES)

        if ticket_form.is_valid():
            print('valide ticket')
            if review_form.is_valid():
                print('valide review')
                new_ticket_form = ticket_form.save(commit=False)
                new_ticket_form.author = request.user
                new_ticket_form.save()

                new_review_form = review_form.save(commit=False)
                new_review_form.ticket = new_ticket_form
                new_review_form.user = request.user

                new_review_form.save()
                new_ticket_form.reviewed = True
                new_ticket_form.save()

                return redirect('flux')
        
    else:
        review_form = ReviewForm()
        ticket_form = TicketForm()
    
    context = {
        'review_form':review_form,
        'ticket_form':ticket_form,
    }

    return render(request, 'tikect/review_with_ticket.html', context)

@login_required
def delete_subscript_user(request, pk_subs):
    user = get_object_or_404(User, id = request.user.id)
    subscript_user = get_object_or_404(UserFollows, pk = pk_subs)
    user.follows.remove(subscript_user.followed_user)
    subscript_user.delete()

    return redirect('follow_users')

@login_required
def follow_users(request):

    user_follows = UserFollows.objects.filter(user=request.user)
    user_followed = UserFollows.objects.filter(followed_user=request.user)
    if request.method == "POST":
        user = request.POST.get("username")
        try:
            user_to_follow = User.objects.get(email=user)
            if user_to_follow == request.user:
                messages.error(request, "Vous ne pouvez pas vous ajouter vous-même !")
                return redirect("follow_users")
            elif UserFollows.objects.filter(followed_user=user_to_follow):
                messages.error(request, "Vous suivez déjà cet utilisateur")
                return redirect("follow_users")
        except User.DoesNotExist:
            messages.error(request, "nom incorrect ou utilisateur inexistant")
            return redirect("follow_users")
        else:
            subscription = UserFollows(
                user=request.user, followed_user=user_to_follow
            )
            subscription.save()

    user = request.user

    context = {
        "user_follows": user_follows,
        "user_followed": user_followed,
        "user": user,
    }
    return render(request, "tikect/follow_users_form.html", context=context)



def display_posts(request):

    tickets = Ticket.objects.filter(author=request.user)
    reviews =Review.objects.filter(user=request.user)
    delete_form = DeleteTicketReviewForm()

    for ticket in tickets:
        if "delete_ticket_or_review" in request.POST:
            delete_form = DeleteTicketReviewForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect("display_posts")

    for review in reviews:
        if "delete_ticket_or_review" in request.POST:
            delete_form = DeleteTicketReviewForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect("display_posts")

    tickets_sorted = sorted(
        tickets, key=lambda instance: instance.time_created, reverse=True
    )
    reviews_sorted = sorted(
        reviews, key=lambda instance: instance.time_created, reverse=True
    )

    context = {
        "tickets": tickets_sorted,
        "reviews": reviews_sorted,
        "delete_form": delete_form,
    }
    return render(request, "tikect/posts.html", context=context)
