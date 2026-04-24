from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, School, Player, Parent
from accounting.models import Subscription
from crispy_forms.helper import FormHelper

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
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'

class PlayerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True

    class Meta:
        model = Player
        fields = '__all__'
        exclude = ['coach','created_date']

class ParentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True

    class Meta:
        model = Parent
        fields = '__all__'
        exclude = ('player_id',)