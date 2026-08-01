from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Row
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

        self.helper.layout = Layout(
            Row(
                Div('physical_condition', css_class='col-xl-2 js-subscription-physical-condition'),
                Div('condition', css_class='col-xl-3 js-subscription-condition'),
                Div('ammount',css_class='col-xl-3'),
                Div('pay_date',css_class='col-xl-3'),
                Div('single_class',css_class='col-1 d-flex align-items-center'),
                # Div('DELETE',css_class='col-1 d-flex align-items-center'),
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        physical_condition = cleaned_data.get('physical_condition')

        if physical_condition != 1:
            cleaned_data['condition'] = ''

        return cleaned_data

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
        self.fields['description'].widget = forms.Textarea(attrs={'rows':2})

        self.helper.layout = Layout(
            Div('description',css_class='col-xl-12'),
            Row(
                Div('amount',css_class='col-xl-6'),
                Div('date',css_class='col-xl-6'),
            )
        )

    class Meta:
        model = Outcoming
        fields = '__all__'
        exclude = ['school',]

class SavingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        if "date" in self.fields:
            self.fields["date"].widget = build_date_picker_widget("Select savings date")

        self.helper.layout = Layout(
            Row(

            )
        )
    
    class Meta:
        model = Savings
        fields = '__all__'
        exclude = ['school',]
