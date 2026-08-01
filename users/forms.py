from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, School, Player, Parent
from accounting.models import Subscription
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div, HTML, Row
from uniforms.models import Uniform
from accounting.models import UniformPayment


def build_date_picker_attrs(placeholder):
    return {
        "class": "js-date-input",
        "placeholder": placeholder,
        "autocomplete": "off",
        "data-flatpickr-alt-format": "F j, Y",
    }

class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'gender',
            'phone',
            'photo',
            'weight',
            'height',
            'username',
            'email',
            'password1',
            'password2',
        ]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.helper = FormHelper()
        self.helper.render_hidden_fields = True
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Div('first_name',css_class='col-xl-3'),
                Div('last_name',css_class='col-xl-3'),
                Div('gender',css_class='col-xl-3'),
                Div('phone',css_class='col-xl-3'),

                Div('weight',css_class='col-xl-3'),
                Div('height',css_class='col-xl-3'),
                Div('photo',css_class='col-xl-3'),

                Row(
                    HTML("""
                        <h2 class="section-title mt-2">Coach account info</h2>
                        <br><br>
                    """),
                    Div('username',css_class='col-xl-6'),
                    Div('email',css_class='col-xl-6'),
                    Div('password1',css_class='col-xl-6'),
                    Div('password2',css_class='col-xl-6'),
                ),
                css_class='justify-content-center'
            )
        )

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'
        exclude = ['latitude','longitude']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.helper = FormHelper()
        self.helper.render_hidden_fields = True
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Div('name',css_class='col-xl-4'),
                Div('phone',css_class='col-xl-4'),
                Div('logo',css_class='col-xl-4'),
                css_class='justify-content-center'
            )
        )

class PlayerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        if "dob" in self.fields:
            self.fields["dob"].widget = forms.TextInput(
                attrs=build_date_picker_attrs("Select date of birth")
            )

        self.helper.layout = Layout(
            Row(
                Div('primary_name',css_class='col-xl-3'),
                Div('secondary_name',css_class='col-xl-3'),
                Div('first_last_name',css_class='col-xl-3'),
                Div('second_last_name',css_class='col-xl-3'),

                Div('dob',css_class='col-xl-3'),
                Div('gender',css_class='col-xl-3'),
                Div('phone',css_class='col-xl-3'),
                Div('height',css_class='col-xl-3'),
                css_class='justify-content-center'
            )
        )

    class Meta:
        model = Player
        fields = '__all__'
        exclude = ['created_date','school']

class ParentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True

        self.helper.layout = Layout(
            Div('primary_name',css_class='col-xl-3'),
            Div('secondary_name',css_class='col-xl-3'),
            Div('first_last_name',css_class='col-xl-3'),
            Div('second_last_name',css_class='col-xl-3'),
            Div('phone',css_class='col-xl-3'),
        )

    class Meta:
        model = Parent
        fields = '__all__'
        exclude = ('player',)

class UniformForm(forms.ModelForm):
    class Meta:
        model = Uniform
        fierds = '__all__'
        exclude = ['player',]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.helper = FormHelper()
        self.helper.render_hidden_fields = True
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Div(
                Div('name',css_class='col-xl-3'),
                Div('number',css_class='col-xl-3'),
                Div('size',css_class='col-xl-3'),
                css_class='row'
            )
        )

class UniformPaymentForm(forms.ModelForm):
    class Meta:
        model = UniformPayment
        fields = '__all__'
        exclude = ['uniform',]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.helper = FormHelper()
        self.helper.render_hidden_fields = True
        self.helper.form_tag = False
        if "pay_date" in self.fields:
                self.fields["pay_date"].widget = forms.TextInput(
                    attrs=build_date_picker_attrs("Select date of Payment")
                )

        self.helper.layout = Layout(
            Div(
                Div('amount',css_class='col-xl-3'),
                Div('payment_method',css_class='col-xl-3'),
                Div('pay_date',css_class='col-xl-3'),
                # Div('DELETE',css_class='col-xl-3 d-flex align-items-center'),
                css_class='row'
            )
        )