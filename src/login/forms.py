from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'login'))
        self.helper.add_input(Button('use keyrock', "Button"))
