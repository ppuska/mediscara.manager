from crispy_forms.bootstrap import InlineField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Layout, Submit
from django import forms


class CollaborativeForm(forms.Form):
    """Form class for the collaborative bottom navigation bar"""

    inc_type = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Incubator type",
                "class": "mx-1 mb-2 mb-lg-0",
            }
        ),
    )

    part_type = forms.CharField(
        max_length=20, widget=forms.TextInput(attrs={"placeholder": "Part type", "class": "mx-1 mb-2 mb-lg-0"})
    )

    production_count = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Production count",
                "class": "mx-1 mb-2 mb-lg-0",
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            InlineField("inc_type"),
            InlineField("part_type"),
            InlineField("production_count"),
            ButtonHolder(Submit("add", "Add order", css_class="btn-light")),
        )


class IndustrialForm(forms.Form):
    """Form class for the industrial editor bottom navigation bar"""

    type = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Housing type",
                "class": "mx-1 mb-2 mb-lg-0",
            }
        ),
    )

    production_count = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Production count",
                "class": "mx-1 mb-2 mb-lg-0",
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            InlineField("type"),
            InlineField("production_count"),
            ButtonHolder(Submit("add", "Add order", css_class="btn-light")),
        )
