from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Row
from accounting.models import Subscription, Outcoming, Savings, OrderPayment, UniformOrder


def build_date_picker_widget(placeholder, custom=False):
    attrs = {
        "autocomplete": "off",
    }

    if custom:
        attrs.update({
            "class": "js-register-date-picker",
            "placeholder": placeholder,
            "inputmode": "none",
            "readonly": "readonly",
            "data-date-picker": "custom",
        })
        return forms.TextInput(attrs=attrs)

    attrs["type"] = "date"
    return forms.DateInput(format="%Y-%m-%d", attrs=attrs)

class SubscriptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        date_picker_mode = kwargs.pop("date_picker_mode", "native")
        super().__init__(*args,**kwargs)

        self.fields['physical_condition'].required = True
        self.fields['ammount'].required = True
        self.fields['pay_date'].required = True

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        if "pay_date" in self.fields:
            self.fields["pay_date"].widget = build_date_picker_widget(
                "Select payment date",
                custom=date_picker_mode == "custom",
            )

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
        exclude = ('player_id', 'expiration_date', 'created_by', 'created_date')

class OutcomingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['description'].required = True
        self.fields['amount'].required = True
        self.fields['date'].required = True

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
        exclude = ['school','created_date','created_by']

class SavingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date'].required = True
        self.fields['ammount'].required = True

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        if "date" in self.fields:
            self.fields["date"].widget = build_date_picker_widget("Select savings date")

        self.helper.layout = Layout(
            Row(
                Div('date',css_class='col-xl-6'),
                Div('ammount',css_class='col-xl-6'),
            )
        )
    
    class Meta:
        model = Savings
        fields = '__all__'
        exclude = ['school','created_by','created_date']


class OrderForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['description'].required = True

        self.helper = FormHelper()
        self.helper.render_hidden_fields = True
        self.helper.form_tag = False
        self.fields['description'].widget = forms.Textarea(attrs={'rows': 3})

        self.helper.layout = Layout(
            Div('description', css_class='col-12'),
        )

    class Meta:
        model = UniformOrder
        fields = ['description']

class OrderPaymentForm(forms.ModelForm):
    class Meta:
        model = OrderPayment
        fields = ['amount', 'pay_date']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['amount'].required = True
        self.fields['pay_date'].required = True

        self.helper = FormHelper()
        self.helper.render_hidden_fields = True
        self.helper.form_tag = False
        self.fields['pay_date'].widget = build_date_picker_widget("Select payment date")

        self.helper.layout = Layout(
            Row(
                Div('amount', css_class='col-md-6'),
                Div('pay_date', css_class='col-md-6'),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        pay_date = cleaned_data.get('pay_date')

        if bool(amount) ^ bool(pay_date):
            raise forms.ValidationError('Amount and pay date must be provided together.')

        return cleaned_data
