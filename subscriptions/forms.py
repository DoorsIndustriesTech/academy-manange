from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Field
from .models import Subscription
from users.models import Player, Parent

class PlayerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['dob'].widget.attrs.update({'readonly':'readonly', 'class':'dateinput', 'id':'date'})

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Div('primary_name', css_class='col-xl-3'),
                Div('secondary_name', css_class='col-xl-3'),
                Div('first_last_name', css_class='col-xl-3'),
                Div('second_last_name', css_class='col-xl-3'),
                Div(
                    Div(
                        Div(
                            HTML("""<i class="fa-regular fa-calendar"></i>"""),
                            css_class='input-group-text text-muted'
                        ),
                        HTML("""<input type="text" name="player-dob" readonly="readonly" class="flatpickr flatpickr-input dateinput form-control" id="player_dob" placeholder="Select Date of Birth">"""),
                        # Field('dob', css_class='flatpickr flatpickr-input', wrapper_class=''),
                        css_class='input-group'
                    ),
                    css_class='col-xl-3'
                ),
                Div('phone', css_class='col-xl-3'),
                css_class='row'
            )
        )

        placeholders = {
            'primary_name':'Primary Name*',
            'secondary_name':'Second Name',
            'first_last_name':'First Last Name*',
            'second_last_name':'First Last Name',
            'phone':'Phone*',
            'dob':'Select Date of Birth'
        }

        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs.update({'placeholder':placeholder})

    class Meta:
        model = Player
        fields = '__all__'
        exclude = ['created_date']


class ParentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Div('primary_name', css_class='col-xl-3'),
                Div('secondary_name', css_class='col-xl-3'),
                Div('first_last_name', css_class='col-xl-3'),
                Div('second_last_name', css_class='col-xl-3'),
                Div('phone', css_class='col-xl-3'),
                css_class='row'
            )
        )

        placeholders = {
            'primary_name':'First Name*',
            'secondary_name':'Second Name',
            'first_last_name':'First Last Name*',
            'second_last_name':'Second Last Name',
            'phone':'Phone*',
        }

        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs.update({'placeholder':placeholder})
    
    class Meta:
        model = Parent
        fields = '__all__'
        exclude = ['player_id']

class SubscriptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['single_class'].widget = forms.RadioSelect(
            choices = [(True, 'Yes'), (False, 'No')]
        )

        physical_condition = self.fields['physical_condition']
        physical_condition_choices = list(physical_condition.choices)

        if physical_condition_choices and physical_condition_choices[0][0] == "":
            physical_condition_choices[0] = ("", "--Select Physical Condition--")

        physical_condition.choices = physical_condition_choices

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Div('physical_condition', css_class='col-xl-3'),
                Div('condition', css_class='col-xl-3'),
                Div(
                    HTML('<label for="id_single_class">Is Single Class:</label>'),
                    'single_class',
                    css_class='col-xl-3'
                ),
                Div('ammount', css_class='col-xl-3'),
                Div(
                    Div(
                        Div(
                            HTML("""<i class="fa-regular fa-calendar"></i>"""),
                            css_class='input-group-text text-muted'
                        ),
                        HTML("""<input type="text" name="pay-date" readonly="readonly" class="flatpickr flatpickr-input dateinput form-control" id="pay_date" placeholder="Select Payment Date">"""),
                        # Field('dob', css_class='flatpickr flatpickr-input', wrapper_class=''),
                        css_class='input-group'
                    ),
                    css_class='col-xl-3'
                ),
                css_class = 'row'
            )
        )

        placeholders = {
            'condition':'Condition',
            'ammount':'Ammount',
        }

        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs.update({'placeholder':placeholder})
    class Meta:
        model = Subscription
        fields = '__all__'
        exclude = ['player_id', 'expiration_date']