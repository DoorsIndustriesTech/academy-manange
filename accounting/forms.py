from django import forms
from crispy_forms.helper import FormHelper
from accounting.models import Subscription, Outcoming, Savings


def build_date_picker_widget(placeholder):
    return forms.DateInput(
        attrs={
            "class": "js-date-input",
            "placeholder": placeholder,
            "autocomplete": "off",
            "data-flatpickr-alt-format": "F j, Y",
        }
    )

class SubscriptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        if "pay_date" in self.fields:
            self.fields["pay_date"].widget = build_date_picker_widget("Select payment date")

    class Meta:
        model = Subscription
        fields = '__all__'
        exclude = ('player_id', 'expiration_date')

class OutcomingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        if "date" in self.fields:
            self.fields["date"].widget = build_date_picker_widget("Select expense date")

    class Meta:
        model = Outcoming
        fields = '__all__'

class SavingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        if "date" in self.fields:
            self.fields["date"].widget = build_date_picker_widget("Select savings date")
    
    class Meta:
        model = Savings
        fields = '__all__'
