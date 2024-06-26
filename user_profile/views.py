import magic
import json
import os
from django.shortcuts import render, get_object_or_404, HttpResponse, HttpResponseRedirect, reverse, Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.utils.encoding import force_bytes
from django.core.mail import get_connection


# Importing token
from .tokens import account_activation_token




from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Import for sending mail
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from .models import UserProfile

from .forms import AvatarUploadForm

User = get_user_model()


def user_profile_view(request, username):

    visited_user_qs = User.objects.filter(username=username)
    if not visited_user_qs:
        message = f"User with username {username} not found!"
        return render(request, '404.html', {"message": message})

    visitor = request.user
    visited_user = visited_user_qs[0]
    # if visitor.is_authenticated:
    visited_profile = UserProfile.objects.get(user=visited_user)
    avatar_upload_form = AvatarUploadForm()



    custom_games_played = visited_profile.total_custom_games_count

    STATS = {
        "games_played": int(custom_games_played),

    }

    context = {
        "visited_user": visited_user,
        "visited_profile": visited_profile,
        "avatar_upload_form": avatar_upload_form,
    }
    context.update(STATS)

    return render(request, 'user_profile/profile_new.html', context=context)


@login_required
def verify_email(request, username):
    """
        This function sends a verification link to your email.
    """
    requested_user_qs = User.objects.filter(username=username)
    if not requested_user_qs:
        message = f"User with username {username} not found!"
        return render(request, '404.html', {"message": message})

    requested_user = requested_user_qs[0]

    user = request.user
    if user == requested_user:
        email = requested_user.email
        host = request.get_host()
        subject = 'Activate your Articulate account.'

        email_context = {
            'user': user,
            'host': host,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
        html_message = render_to_string('user_profile/mail_template_email_verification.html', context=email_context)
        plain_message = strip_tags(html_message)

        from_email = "nehalc2107@gmail.com"
        to = str(email)
        connection = get_connection()
        connection.open()
        try:
            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        except mail.BadHeaderError:
            messages.info(request, f"Invalid Header found, mail not sent!")
        finally:
            connection.close()

        return HttpResponse('Verification link has been sent to your email. '
                            'Please confirm your email address to complete the registration.')
    message = f"You are not authorised to visit this page."
    return render(request, '404.html', {"message": message})


def activate(request, uidb64, token):
    """
        A function that verifies email through activation link.
        It decodes the encoded pk (primary key).
    """
    try:
        uid = (urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.user == user:
            if user.is_authenticated:
                profile = UserProfile.objects.get(user=user)

                profile.is_email_verified = True
                profile.save()

                messages.success(request, f"Your email has been verified.")
                return HttpResponseRedirect(reverse('home'))
            messages.success(request, f"Login to verify email.")
            return HttpResponseRedirect(reverse('home'))
    return HttpResponse('Activation link is invalid!')


def clean_file(request, form):
    file = form.cleaned_data['avatar']
    if file.size > 5242880:
        return False
    return True


def check_in_memory_mime(request):
    mime = magic.from_buffer(request.FILES.get('avatar').read(), mime=True)
    return mime


def delete_existing_avatar(username):
    """
    Function to delete existing avatar (if exists) of user before uploading new avatar.
    :param username: username of user whose avatar is to be deleted.
    :return:
    """
    try:
        media_url = str(settings.MEDIA_URL)[1:]
        path = f"{media_url}img/profile_avatars/{username}"
        files = os.listdir(path=path)
        for file_ in files:
            os.remove(f"{path}/{file_}")
        print(f"Existing avatar deleted.")
        return
    except OSError:
        return


@login_required
def avatar_upload(request, username):
    """
        This function uploads/re-uploads profile picture of a user.
    """
    if request.method == 'POST':
        avatar_form = AvatarUploadForm(request.POST, request.FILES)
        print(request.FILES)
        if request.FILES:
            if avatar_form.is_valid():
                user = User.objects.get(username=username)
                user_prof = UserProfile.objects.get(user=user)
                if clean_file(request, avatar_form):
                    mime = check_in_memory_mime(request)
                    if mime == 'image/jpg' or mime == 'image/jpeg' or mime == 'image/png':
                        img = avatar_form.cleaned_data['avatar']

                        # Deleting existing avatar of user.
                        delete_existing_avatar(username=username)

                        user_prof.avatar = img
                        user_prof.save()
                        message = f"Avatar uploaded successfully!"
                        messages.success(request, message=message)
                        return HttpResponseRedirect(reverse("user_profile", kwargs={'username': username}))
                    else:
                        messages.success(request, f"Please upload an Image File only of jpeg/jpg/png format only...")
                        return HttpResponseRedirect(reverse("user_profile", kwargs={'username': username}))
                else:
                    messages.success(request, f"File too Large to be uploaded...")
                    return HttpResponseRedirect(reverse("user_profile", kwargs={'username': username}))
            else:
                if avatar_form.errors:
                    for field in avatar_form:
                        for error in field.errors:
                            print(error)
                            messages.success(request, error)
                return HttpResponseRedirect(reverse("user_profile", kwargs={'username': username}))
        else:
            message = f"Please choose a file before uploading."
            messages.error(request, message)
            return HttpResponseRedirect(reverse("user_profile", kwargs={'username': username}))
    else:
        message = None
        return render(request, '404.html', {"message": message})



@login_required
def edit_profile(request, username):
    """
    Method to updated edited personal details.
    :param request:
    :param username:
    :return:
    """
    user = request.user
    if user.username != username:
        message = f"{user.username}, why are you trying to edit {username}'s profile?"
        return render(request, '404.html', {"message": message})

    if request.method == "POST":

        user_profile = UserProfile.objects.get(user=user)
        all_users_qs = User.objects.all()

        # Fetching the edited values
        edited_first_name = request.POST["first_name"]
        edited_last_name = request.POST["last_name"]
        edited_email = request.POST["email"]

        # Updating the values
        user.first_name = edited_first_name
        user.last_name = edited_last_name

        # If user has edited the email, set is_email_verified to false
        print(user.email, edited_email)
        if user.email != edited_email:
            for user_ in all_users_qs:
                if user_.email == edited_email:
                    message = f"This email is already taken. Try again!"
                    messages.info(request, message)
                    response = {
                        "status": "error",
                        "message": "Request Failed!",
                    }
                    return JsonResponse(response)
            user.email = edited_email
            user_profile.is_email_verified = False
            user_profile.save()

        user.save()

        response = {
            "status": "success",
            "message": "Request Received Successfully!",
        }
        messages.success(request, f"Details have been updated successfully.")
        return JsonResponse(response)
