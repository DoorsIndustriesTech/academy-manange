from django.shortcuts import render
from .forms import PlayerForm, ParentForm
from django.forms import inlineformset_factory
from users.models import Player
from accounting.models import Subscription
from .forms import *

# Create your views here.
def register_player(request, template='subscriptions/new_form.html'):
    subscriptions_inline = inlineformset_factory(Player, Subscription, form=SubscriptionForm, extra=1)
    if request.method == 'POST':
        player_form = PlayerForm(request.POST)
        parent_form = ParentForm(request.POST)
        subscriptions_form = subscriptions_inline(request.POST)
        if player_form.is_valid() and parent_form.is_valid() and subscriptions_form.is_valid():
            player = player_form.save(commit=False)
            player.save()

            parent = parent_form.save(commit=False)
            parent.player_id = player
            parent.save()

            subscriptions = subscriptions_form.save(commit=False)
            for obj in subscriptions_form.deleted_objects:
                obj.delete()

            for subscription in subscriptions:
                subscription.player_id = player
                subscription.save()
            
            subscriptions_form.save_m2m()
    else:
        player_form = PlayerForm()
        parent_form = ParentForm()
        subscriptions_form = subscriptions_inline()

    return render(request, template, locals())

def players_list(request, template='subscriptions/list.html'):

    players = Player.objects.all()

    return render(request, template, locals())