from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ChatBox import forms
from chat import models


def home(request):
    """ Redirects user to main page if logged in or to login in page if not.
    If user has no friends it will redirect to a page to find friends """
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('chat:chat'))
    if request.user.is_authenticated:
        user = models.Profile.objects.get(username=request.user.username)
        friends = user.friends.split(",")
        if len(friends) <= 1:
            return HttpResponseRedirect(reverse('chat:find_friends'))
        return HttpResponseRedirect(reverse('chat:chat'))
    else:
        return HttpResponseRedirect(reverse('login'))


def contact_us(request):
    """  View with form for user to send a message to the staff. Allows even one who is not logged in to sign up. """
    form = forms.ContactStaffForm(request.POST or None)
    if form.is_valid():
        admin = models.Profile.objects.get(username="ChatBox staff")
        if request.user.is_authenticated and request.user.is_staff == False:
            user = models.Profile.objects.get(username=request.user.username)
        else:
            user = models.Profile.objects.get(username="No One")
        message = form.save(commit=False)
        message.from_user = user
        message.to_user = admin
        message.save()
        messages.success(request, "Message was received by our staff. We will contact you soon.")
        if request.user.is_authenticated and request.user.is_staff == False:
            models.FriendMessage.objects.create(
                to_user=user,
                from_user=admin,
                title="We got your " + message.title + " message. We will contact you soon addressing your message."
            )
        return HttpResponseRedirect(reverse('home'))
    return render(request, "contact-us.html", {'form': form, 'message_type': 'contact_us'})


def loginer(request):
    """ logs in user """
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, "Login successful!")
                    return HttpResponseRedirect(reverse('home'))
                else:
                    messages.add_message(request, messages.ERROR, "This account has been disabled sorry!")
                    return HttpResponseRedirect(reverse('home'))
            else:
                messages.add_message(request, messages.ERROR, "Invalid Login!")
    return render(request, 'login.html', {'form': form})


def sign_up(request):
    """ Page the User fills out form to sign up. """
    title = "Sign Up"
    form = forms.ProfileForm()
    if request.method == "POST":
        form = forms.ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name']
            # if User.objects.filter(username=username):
            #    messages.error(request, "Sorry that name or password is already taken")
            #    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            profile = form.save(commit=False)
            profile.picture = form.cleaned_data['picture']
            profile.username = username
            profile.save()

            user = User.objects.create_user(
                username=profile.username,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            new_user = models.Profile.objects.get(username=request.user.username)
            new_user.friends = str(new_user.pk)
            new_user.save()

            messages.success(request, "You are all signed up.")
            return HttpResponseRedirect(reverse('chat:find_friends'))
    return render(request, 'profile_form.html', {"form": form, "title": title})


@login_required()
def update_info(request):
    title = "Update Info"
    if request.user.is_staff:
        messages.error(request, "This page is only for users to change there account info.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    user = models.Profile.objects.get(username=request.user.username)
    form = forms.ProfileUpdateForm(instance=user)
    password_form = forms.UpdatePasswordForm(request.POST or None)
    user_info = request.user
    if request.method == "POST":
        form = forms.ProfileUpdateForm(request.POST, request.FILES, instance=user)
        description = request.POST.get("description")
        if form.is_valid() and password_form.is_valid():
            username = form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name']
            if User.objects.filter(username=username) and user_info.username != username:
                messages.error(request, "Sorry that name or password is already taken")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            else:
                user_info.username = username
                user_info.email = form.cleaned_data['email']
                if password_form.is_valid() and password_form.cleaned_data['password'] != "":
                    print("HERE is the password:   " + password_form.cleaned_data['password'])
                    user_info.set_password(password_form.cleaned_data['password'])
                else:
                    print("Password is empty. The password is not changed")
                user_info.save()

                data = form.save(commit=False)
                if description and description != "None":
                    data.description = description
                data.picture = form.cleaned_data['picture']
                data.username = username
                data.save()
                new_user_info = authenticate(
                    username=data.username,
                    email=data.email
                )
                login(request, new_user_info)
                messages.success(request, "Info Updated")
                return HttpResponseRedirect(reverse('chat:friends'))
    return render(request, 'profile_form.html', {"form": form, 'password_form': password_form,
                                                 'title': title, 'user': user})


def logout_view(request):
    """ logs out user """
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Logout Successfully!")
    return HttpResponseRedirect(reverse('home'))
