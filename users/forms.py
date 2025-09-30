from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

from django.contrib.auth.forms import SetPasswordForm
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone','avatar','city','about']


class PasswordResetRequestForm(forms.Form):
    identifier = forms.CharField(
        label="Email yoki telefon (username ham bo‘lishi mumkin)",
        widget=forms.TextInput(attrs={'placeholder': 'email@example.com yoki telefon yoki username'})
    )

class CodeConfirmForm(forms.Form):
    code = forms.CharField(label="Tasdiqlovchi kod", max_length=10)

class PasswordSetForm(SetPasswordForm):
    pass
