from django import forms
from .models import User

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }






