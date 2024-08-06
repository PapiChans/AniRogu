from django import forms
from backend.models import User
from django.core.exceptions import ValidationError

class SignupForm(forms.ModelForm): 
    password = forms.CharField(widget=forms.PasswordInput)
    cnfm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['profile_name', 'username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        cnfm_password = cleaned_data.get('cnfm_password')

        if password and cnfm_password and password != cnfm_password:
            raise ValidationError("Passwords do not match. Please enter matching passwords.")
        
        if password and len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        return cleaned_data
    
class LoginForm(forms.Form):
    username = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email Address'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your Password', 'minlength': '8', 'maxlength': '20'}))

    def clean(self):
        cleaned_data = super().clean()
        # You can perform additional validation here if needed
        return cleaned_data
    
class ForgotPasswordForm(forms.Form):
    username = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email Address'}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        # Additional validation can be performed here if needed
        return cleaned_data

class SearchAnimeForm(forms.Form):
    animekeyword = forms.CharField(
        label='Anime Keywords',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Anime Keywords'
        }),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        # Additional validation can be performed here if needed
        return cleaned_data
    
class ChangeProfileForm(forms.Form):
    new_profile_name = forms.CharField(
        label='New Profile Name',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Set Profile Name'
        }),
        required=True
    )
    
    def clean(self):
        cleaned_data = super().clean()
        # Additional validation can be performed here if needed
        return cleaned_data

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Old Password', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', required=True)
    cnfm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password', required=True)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data