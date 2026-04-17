from django import forms
from users.models import Player, User, Parent
from crispy_forms.helper import FormHelper
from accounting.models import Subscription

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

class SubscriptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True

    class Meta:
        model = Subscription
        fields = '__all__'
        exclude = ('player_id', 'expiration_date')