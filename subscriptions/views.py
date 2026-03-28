from django.shortcuts import redirect, render
from users.models import Player, Parent
from .forms import PlayerForm, ParentForm, SubscriptionForm
from .models import Subscription, Player, Parent
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth
import calendar
from datetime import datetime

def new_subscription(request, template = 'subscriptions/new_subscription.html'):
    if request.method == 'POST':
        player_form = PlayerForm(request.POST, prefix = 'player')
        parent_form = ParentForm(request.POST, prefix = 'parent')
        subscription_form = SubscriptionForm(request.POST)

        if player_form.is_valid() and parent_form.is_valid() and subscription_form.is_valid():
            player = player_form.save()

            parent = parent_form.save(commit = False)
            parent.player_id = player
            parent.save()

            subscription = subscription_form.save(commit = False)
            subscription.player_id = player
            subscription.save()

            return redirect('/')
    else:
        player_form = PlayerForm(prefix = 'player')
        parent_form = ParentForm(prefix = 'parent')
        subscription_form = SubscriptionForm()
    
    return render(request, template, locals())

def list_subscriptions(request, template = 'subscriptions/list.html'):
    return render(request, template, locals())

def get_subscriptions(request):
    subscriptions_list = Subscription.objects.all().order_by('-pay_date')

    data = [
        {
            "player_name":subscription.player_id.full_name(),
            "condition":subscription.physical_condition,
            "condition_type":subscription.condition if subscription.condition else 'Healthy',
            "single_class":subscription.single_class,
            "ammount":subscription.ammount,
            "pay_date":subscription.pay_date,
            "expiration_date":subscription.expiration_date
        }
        for subscription in subscriptions_list
    ]

    response = {
        "data" : data
    }

    return JsonResponse(response)

def get_months_subscribed(playerId):
    current_year = datetime.now().year
    paid_months = Subscription.objects.filter(player_id = playerId).annotate(month=ExtractMonth('pay_date')).values_list('month', flat = True)
    return [calendar.month_abbr[m] for m in paid_months]

def get_players(request):
    players_list = Player.objects.all().order_by('-created_date')

    data = [
        {
            "player_name":player.full_name(),
            "dob":player.dob,
            "phone":player.phone,
            "paid_months":get_months_subscribed(player.id)
        }
        for player in players_list
    ]

    response = {
        "data" : data
    }

    return JsonResponse(response)