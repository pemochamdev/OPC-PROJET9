from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash

from authy.forms import SignUpForm, ChangePassword
from authy.models import User

def sign_up(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            User.objects.create(
                email=email,
                username=username, 
                password=password,
            )
            return redirect('login')
    else:
        form = SignUpForm()    
    context = {
        'form':form,
    }
    return render(request, 'registration/sign_up.html', context)


def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePassword(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)

            return redirect('password_change_done')
    else:
        form = ChangePassword()
    context = {
        'form':form,
    }
    return render(request, 'registration/change_password.html', context)


def change_password_done(request):
    return render(request, 'registration/change_password_done.html')
            
