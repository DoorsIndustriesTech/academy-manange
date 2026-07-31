import calendar
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Player, Parent
from .serializers import PlayerSerializer
from rest_framework import viewsets
from rest_framework_api_key.permissions import HasAPIKey
from .forms import AdminRegistrationForm, SchoolForm, LoginForm, PlayerForm, ParentForm
from accounting.forms import SubscriptionForm
from accounting.models import Subscription
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.urls import reverse

class PlayerViewset(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey]
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

def adminRegistration(request, template='registration/register.html'):
    if request.method == 'POST':
        registration_form = AdminRegistrationForm(request.POST)
        school_form = SchoolForm(request.POST)
        if registration_form.is_valid() and school_form.is_valid():
            school = school_form.save()

            user = registration_form.save(commit=False)
            user.school = school
            user.job_position = 'Coach'
            user.save()

            return redirect('/')
    else:
        registration_form = AdminRegistrationForm()
        school_form = SchoolForm()

    return render(request, template, locals())

def loginUser(request, template='registration/login.html'):

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('register_player')
            else:
                login_form.add_error(None, "Invalid Credentials")
    else:
        login_form = LoginForm()

    return render(request, template, locals())

def get_players_list(request):
    draw = 1
    length = 100
    start = 0
    players = Player.objects.all().order_by('created_date')

    paginator = Paginator(players, length)
    page_number = start // length + 1
    page = paginator.get_page(page_number)

    data = [
        {
            'id' : player.id,
            'full_name' : player.full_name(),
            'dob' : player.dob,
            'gender' : player.gender,
            'phone' : player.phone,
            'view' : f'<a class="table-action" href="{reverse("player_detail", args=[player.id])}">Open profile</a>'
        }
        for player in page
    ]

    response = {
        "draw" : draw,
        "length" : length,
        "total_players" : players.count(),
        "data"  : data
    }

    return JsonResponse(response)

@login_required
def register_player(request, template='players/new_form.html'):
    subscriptions_inline = inlineformset_factory(Player, Subscription, form=SubscriptionForm, extra=1)
    if request.method == 'POST':
        player_form = PlayerForm(request.POST)
        parent_form = ParentForm(request.POST)
        subscriptions_form = subscriptions_inline(request.POST)
        if player_form.is_valid() and parent_form.is_valid() and subscriptions_form.is_valid():
            player = player_form.save(commit=False)
            player.school = request.user.school
            player.save()

            parent = parent_form.save(commit=False)
            parent.player = player
            parent.save()

            subscriptions = subscriptions_form.save(commit=False)
            for obj in subscriptions_form.deleted_objects:
                obj.delete()

            for subscription in subscriptions:
                subscription.player = player
                subscription.save()
            
            subscriptions_form.save_m2m()

            return redirect('player_detail', id=player.id)
    else:
        player_form = PlayerForm()
        parent_form = ParentForm()
        subscriptions_form = subscriptions_inline()

    return render(request, template, locals())

@login_required
def players_list(request, template='players/list.html'):

    players = Player.objects.all()

    return render(request, template, locals())

@login_required
def player_detail(request, template='players/detail.html', id=None):
    current_date = datetime.now().date()
    player = Player.objects.get(id=id)
    parent = Parent.objects.filter(player_id=player)
    pay_months = Subscription.objects.filter(player_id=player).values_list(
        'pay_date__month', flat=True
    ).distinct().order_by('pay_date__month')
    subscriptions = [calendar.month_name[month] for month in pay_months]
    due_date = Subscription.objects.filter(player_id=player).latest('expiration_date').expiration_date
    if current_date >= due_date:
        subscription_status = 'Remember'
    else:
        subscription_status = 'Updated'
    
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)

        subscription = subscription_form.save(commit=False)
        subscription.player_id = player
        subscription.save()
    else:
        subscription_form = SubscriptionForm()
    return render(request, template, locals())

@login_required
def edit_player(request, id=None,template='players/edit_form.html'):
    object = Player.objects.get(id=id)
    parent = Parent.objects.filter(player_id=object).first()
    if request.method == 'POST':
        player_form = PlayerForm(request.POST,instance=object)
        parent_form = ParentForm(request.POST,instance=parent)
        if player_form.is_valid() and parent_form.is_valid():
            player = player_form.save(commit=False)
            player.save()

            parent = parent_form.save(commit=False)
            parent.player = player
            parent.save()

            return redirect('player_detail', id=id)
    else:
        player_form = PlayerForm(instance=object)
        parent_form = ParentForm(instance=parent)
    
    return render(request, template, locals())