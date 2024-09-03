from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.models import User
from backend.serializers import UserSerializer
from django.shortcuts import get_object_or_404
import random
import string
from backend.forms import ForgotPasswordForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseBadRequest, JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_recovery_email(user_email, temporary_password):
    subject = 'Account Recovery'

    # HTML content for the email
    html_content = """
<html>
<head>
    <style>
        .paragraph {{
            margin-bottom: 20px;
        }}
        .temporary-password {{
            font-size: 20px;
        }}
        .app-team {{
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col">
                <p class="paragraph">This is an auto-generated email, <strong>DO NOT REPLY.</strong></p>
                <p class="paragraph">Dear User,</p>
                <p class="paragraph">Did you request for account recovery? If yes, here are your recovery details:</p>
                <p class="paragraph"><strong>Temporary Password:</strong> <span class="temporary-password">{temporary_password}</span></p>
                <p class="paragraph">Please log in to your account using this temporary password and change it immediately.</p>
                <p class="paragraph"><strong class="app-team">Best regards,<br>AniRogu Support Team</strong></p>
            </div>
        </div>
    </div>
</body>
</html>
""".format(temporary_password=temporary_password)

    # Create EmailMultiAlternatives object to include both HTML and plain text content
    msg = EmailMultiAlternatives(subject, '', settings.DEFAULT_FROM_EMAIL, [user_email])
    msg.attach_alternative(html_content, "text/html")

    # Send the email
    msg.send(fail_silently=False)  # Set to True if you want to suppress errors

def generate_random_password(length=8):
    """Generate a random password with given length using lowercase letters."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def backendaccountrecovery(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            
            # Check if user with given email exists
            user = User.objects.filter(username=username).first()
            if user is not None:
                # Generate temporary password
                temporary_password = generate_random_password()

                # Set temporary password for the user
                user.set_password(temporary_password)
                user.save()

                # Send email with recovery details
                send_recovery_email(username, temporary_password)

                # Display success message using Notyf.js
                message = "Temporary password sent successfully. Please check your email and change your password immediately."
                return render(request, 'login.html', {
                    'form': form,
                    'notyf': True,
                    'error': False,
                    'message': message
                })
            else:
                # User with given email does not exist
                message = "This email address is not associated with any account."
                return render(request, 'forgot-password.html', {
                    'form': form,
                    'notyf': True,
                    'error': True,
                    'message': message
                })
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'forgot-password.html', {'form': form})