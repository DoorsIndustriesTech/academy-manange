from django import forms
from crispy_forms.helper import FormHelper
from accounting.models import Subscription

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