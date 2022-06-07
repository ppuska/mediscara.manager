from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


class LoginForm(forms.Form):
    """Form class for the user login page"""

    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_show_labels = False
        self.helper.add_input(Submit("submit", "Sign in"))
