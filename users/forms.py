from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, School, Player, Parent
from accounting.models import Subscription
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div, HTML, Row
from uniforms.models import Uniform
from accounting.models import UniformPayment


def build_date_picker_attrs(placeholder, custom=False):
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
    else:
        attrs["type"] = "date"

    return attrs

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

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['phone'].required = True

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
        exclude = ['latitude','longitude','created_date']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['name'].required = True
        self.fields['phone'].required = True

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
        date_picker_mode = kwargs.pop("date_picker_mode", "native")
        super().__init__(*args, **kwargs)

        self.fields['primary_name'].required = True
        self.fields['first_last_name'].required = True
        self.fields['dob'].required = True
        self.fields['phone'].required = True

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        if "dob" in self.fields:
            if date_picker_mode == "custom":
                self.fields["dob"].widget = forms.TextInput(
                    attrs=build_date_picker_attrs("Select date of birth", custom=True)
                )
            else:
                self.fields["dob"].widget = forms.DateInput(
                    format="%Y-%m-%d",
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
        exclude = ['created_date','created_by','school']

class ParentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['primary_name'].required = True
        self.fields['first_last_name'].required = True
        self.fields['phone'].required = True

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
        exclude = ('player','created_date','created_by')

class UniformForm(forms.ModelForm):
    class Meta:
        model = Uniform
        fierds = '__all__'
        exclude = ['player','created_by','created_date']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['name'].required = True
        self.fields['number'].required = True
        self.fields['size'].required = True

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
        exclude = ['uniform','created_by','created_date']

    def __init__(self,*args,**kwargs):
        date_picker_mode = kwargs.pop("date_picker_mode", "native")
        super().__init__(*args,**kwargs)

        self.fields['amount'].required = True
        self.fields['payment_method'].required = True
        self.fields['pay_date'].required = True

        self.helper = FormHelper()
        self.helper.render_hidden_fields = True
        self.helper.form_tag = False
        if "pay_date" in self.fields:
            if date_picker_mode == "custom":
                self.fields["pay_date"].widget = forms.TextInput(
                    attrs=build_date_picker_attrs("Select date of Payment", custom=True)
                )
            else:
                self.fields["pay_date"].widget = forms.DateInput(
                    format="%Y-%m-%d",
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
