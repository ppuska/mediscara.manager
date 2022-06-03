from django import forms

class LoginForm(forms.Form):
    email_field = forms.EmailField(
        label="Email address"
    )
    password_field = forms.PasswordInput(
        
    )