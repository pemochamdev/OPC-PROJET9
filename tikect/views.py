from itertools import chain

from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import (
    Ticket,
    Review,
    UserFollows,
)
from .forms import (
    TicketCreateForm,
    TicketNoImageCreateForm,
    ReviewCreateForm,
    SearchForm,
)
from p9 import const


def home(request):
    """This view is displayed by default,
    even if a user is not connected"""
    return render(request, 'tikect/home.html')


@login_required
def flux(request, page=1):
    followed_users = get_user_model().objects.filter(
        followed__user=request.user)
    reviews = Review.objects.filter(
        Q(user=request.user) | Q(ticket__user=request.user) |
        Q(user__in=followed_users))
    tickets = Ticket.objects.filter(
        Q(user=request.user) | Q(user__in=followed_users))

    posts_created = sorted(
        chain(
            reviews,
            tickets,
            ),
        key=lambda post: post.time_created, reverse=True)
    paginator = Paginator(posts_created, 3)
    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "posts": posts,
    }
    return render(request, "tikect/flux.html", context)


@login_required
def ticket_create(request):
    if request.method == "POST":
        if len(request.FILES) == 0:
            form = TicketNoImageCreateForm(request.POST)
        else:
            form = TicketCreateForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')
    form = TicketCreateForm()
    context = {
        "form": form,
    }
    return render(request, "tikect/ticket_create.html", context)


@login_required
def review_create(request, ticket_id):
    """Creates a review from an existing ticket"""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.reviewed:
        raise Http404()
    if request.method == "POST":
        form = ReviewCreateForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            ticket.reviewed = True
            ticket.save()
            return redirect('flux')

    form = ReviewCreateForm()
    context = {
        "ticket": ticket,
        "form": form,
    }
    return render(request, "tikect/review_create.html", context)


@login_required
def review_publish(request):
    """Creates a spontaneous review without ticket, the ticket is
    genereted beside the review in a row"""
    if request.method == "POST":
        ticket_form = TicketCreateForm(request.POST, request.FILES)
        review_form = ReviewCreateForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            ticket.reviewed = True
            ticket.save()
            return redirect('flux')

    ticket_form = TicketCreateForm()
    review_form = ReviewCreateForm()
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, "tikect/review_publish.html", context)


@login_required
def subscriptions(request):
    """this views allows to follow / unfollow other users"""
    followings = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['entry']
            try:
                user_to_follow = get_user_model().objects.get(username=name)
            except get_user_model().DoesNotExist:
                messages.add_message(
                    request, messages.ERROR, (
                        f"Il n'existe pas d'utilisateur \"{name}\""
                        ),
                    extra_tags=const.ERROR
                )
                return redirect('subscriptions')
            else:
                new_follow = UserFollows(
                    user=request.user, followed_user=user_to_follow)
                new_follow.save()
                messages.add_message(
                    request, messages.SUCCESS, (
                        f"Vous êtes abonné à \"{name}\""
                        ),
                    extra_tags=const.SUCCESS
                )
                return redirect('subscriptions')

    form = SearchForm()
    context = {
        'followings': followings,
        'followers': followers,
        'form': form,
    }
    return render(request, 'tikect/subscriptions.html', context)


@login_required
def unfollow(request, id):
    """This code is called to unfollow a user when the button
    "unsuscribe" is clicked"""
    unfollow = get_object_or_404(get_user_model(), id=id)
    if request.method == "POST":
        unfollowing = get_object_or_404(
            UserFollows, user=request.user, followed_user=unfollow)
        unfollowing.delete()
        messages.add_message(
            request, messages.SUCCESS, (
                f"Vous vous êtes désabonné à \"{unfollow.username}\""
                ),
            extra_tags=const.SUCCESS
        )
        return redirect('subscriptions')

    context = {
        "unfollow": unfollow,
    }
    return render(request, 'tikect/unfollow.html', context)


@login_required
def posts(request, page=1):
    "displays the own posts of a user"
    reviews = request.user.get_reviews()
    tickets = request.user.get_tickets()
    posts_created = sorted(
        chain(
            reviews,
            tickets,
            ),
        key=lambda post: post.time_created, reverse=True)
    paginator = Paginator(posts_created, 3)
    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
    }
    return render(request, "tikect/posts.html", context)


@login_required
def post_delete(request, type, id):
    if type == 'review':
        post = get_object_or_404(Review, id=id)
        request.user.is_user(post)
        ticket = post.ticket
        ticket.reviewed = False
        ticket.save()
    elif type == 'ticket':
        post = get_object_or_404(Ticket, id=id)
    else:
        raise Http404()
    if request.method == "POST":
        post.delete()
        request.user.is_user(post)
        return redirect('posts')
    context = {
        'post': post,
        'type': type,
    }
    request.user.is_user(post)
    return render(request, 'tikect/post_delete.html', context)


@login_required
def post_update(request, type, id):
    if request.method == "POST":
        if type == 'review':
            post = get_object_or_404(Review, id=id)
            request.user.is_user(post)
            form = ReviewCreateForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
        elif type == 'ticket':
            post = get_object_or_404(Ticket, id=id)
            request.user.is_user(post)
            form = TicketCreateForm(
                request.POST, request.FILES, instance=post)
            reviewed = post.reviewed
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.reviewed = reviewed
                ticket.save()
        else:
            raise Http404()
        return redirect('posts')

    if type == 'review':
        post = get_object_or_404(Review, id=id)
        form = ReviewCreateForm(instance=post)

    elif type == 'ticket':
        post = get_object_or_404(Ticket, id=id)
        form = TicketCreateForm(instance=post)
    else:
        raise Http404()

    context = {
        'post': post,
        'form': form,
        'type': type,
    }
    request.user.is_user(post)
    return render(request, 'tikect/post_update.html', context)