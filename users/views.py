import calendar
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Player, Parent
from uniforms.models import Uniform
from .serializers import PlayerSerializer
from rest_framework import viewsets
from rest_framework_api_key.permissions import HasAPIKey
from .forms import AdminRegistrationForm, SchoolForm, PlayerForm, ParentForm, UniformForm, UniformPaymentForm
from accounting.forms import SubscriptionForm
from accounting.models import Subscription,UniformPayment
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

def get_players_list(request):
    draw = 1
    length = 100
    start = 0
    players = Player.objects.all().order_by('created_date')
    current_month = datetime.now().month

    paginator = Paginator(players, length)
    page_number = start // length + 1
    page = paginator.get_page(page_number)

    data = [
        {
            'id' : player.id,
            'full_name' : player.full_name(),
            'dob' : player.dob,
            'gender' : player.gender,
            'phone' : player.phone if player.phone else '---',
            'status' : 'Remember' if current_month - (Subscription.objects.filter(player=player).latest('pay_date').expiration_date.month if Subscription.objects.filter(player=player) else 0) >= 1 else 'Updated',
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

def get_uniform_list(request):
    draw = 1
    length = 100
    start = 0
    uniforms = Uniform.objects.distinct('player').order_by('player','created_date')

    paginator = Paginator(uniforms, length)
    page_number = start // length + 1
    page = paginator.get_page(page_number)

    data = [
        {
            'id' : uniform.id,
            'player_name' : uniform.player.full_name(),
            'name' : uniform.name,
            'number' : uniform.number,
            'size' : uniform.size,
            'payments' : list(
                UniformPayment.objects.filter(uniform=uniform).values_list('amount', flat=True)
            ),
            'view' : f'<a class="table-action" href="{reverse("player_detail", args=[uniform.player.id])}">Open profile</a>'
        }
        for uniform in page
    ]

    response = {
        "draw" : draw,
        "length" : length,
        "total_uniforms" : uniforms.count(),
        "data"  : data
    }

    return JsonResponse(response)

@login_required
def register_player(request, template='players/new_form.html'):
    subscriptions_inline = inlineformset_factory(Player, Subscription, form=SubscriptionForm, extra=1)
    uniform_pay_inline = inlineformset_factory(Uniform, UniformPayment, form=UniformPaymentForm, extra=1)
    if request.method == 'POST':
        player_form = PlayerForm(request.POST, date_picker_mode='custom')
        uniform_form = UniformForm(request.POST)
        uniform_payment_form = uniform_pay_inline(
            request.POST,
            prefix='up',
            form_kwargs={'date_picker_mode': 'custom'},
        )
        parent_form = ParentForm(request.POST,prefix='parent')
        subscriptions_form = subscriptions_inline(
            request.POST,
            prefix='sp',
            form_kwargs={'date_picker_mode': 'custom'},
        )
        if player_form.is_valid() and parent_form.is_valid() and subscriptions_form.is_valid() and uniform_form.is_valid() and uniform_payment_form.is_valid():
            player = player_form.save(commit=False)
            player.school = request.user.school
            player.created_by = request.user
            player.save()

            uniform = uniform_form.save(commit=False)
            uniform.player = player
            uniform.created_by = request.user
            uniform.save()

            un_payments = uniform_payment_form.save(commit=False)
            for up in un_payments:
                up.uniform = uniform
                up.created_by = request.user
                up.save()

            for up in uniform_payment_form.deleted_objects:
                up.delete()

            uniform_payment_form.save_m2m()
            
            parent = parent_form.save(commit=False)
            parent.player = player
            parent.created_by = request.user
            parent.save()

            subscriptions = subscriptions_form.save(commit=False)
            for obj in subscriptions_form.deleted_objects:
                obj.delete()

            for subscription in subscriptions:
                subscription.player = player
                subscription.created_by = request.user
                subscription.save()
            
            subscriptions_form.save_m2m()

            return redirect('player_detail', id=player.id)
        else:
            print("ERRORS:", subscriptions_form.errors)
    else:
        player_form = PlayerForm(date_picker_mode='custom')
        parent_form = ParentForm(prefix='parent')
        uniform_form = UniformForm()
        uniform_payment_form = uniform_pay_inline(
            prefix='up',
            form_kwargs={'date_picker_mode': 'custom'},
        )
        subscriptions_form = subscriptions_inline(
            prefix='sp',
            form_kwargs={'date_picker_mode': 'custom'},
        )

    return render(request, template, locals())

@login_required
def players_list(request, template='players/list.html'):

    players = Player.objects.all()

    return render(request, template, locals())

@login_required
def uniforms_list(request, template='players/uniforms_list.html'):

    uniforms = Uniform.objects.all()
    uniform_payments = UniformPayment.objects.filter(uniform__in=uniforms)
    total_uniforms = uniforms.distinct('player').count()

    return render(request, template, locals())

@login_required
def player_detail(request, template='players/detail.html', id=None):
    current_date = datetime.now().date()
    player = Player.objects.get(id=id)
    parent = Parent.objects.filter(player=player)
    uniforms = Uniform.objects.filter(player=player).prefetch_related('uniformpayment_set').order_by('-created_date')
    uniform_pay_inline = inlineformset_factory(Uniform, UniformPayment, form=UniformPaymentForm, extra=1)
    uniform_payments_prefix = 'uniformpayment_set'

    pay_months = Subscription.objects.filter(player=player).values_list(
        'pay_date__month', flat=True
    ).distinct().order_by('pay_date__month')
    subscriptions = [calendar.month_name[month] for month in pay_months]
    latest_subscription = Subscription.objects.filter(player=player).order_by('-expiration_date').first()
    if latest_subscription and latest_subscription.expiration_date:
        due_date = latest_subscription.expiration_date
        if current_date >= due_date:
            subscription_status = 'Remember'
        else:
            subscription_status = 'Updated'
    else:
        subscription_status = 'Updated'
    
    if request.method == 'POST':
        uniform_form = UniformForm(request.POST)
        up_form = uniform_pay_inline(
            request.POST,
            prefix=uniform_payments_prefix,
            form_kwargs={'date_picker_mode': 'custom'},
        )
        uniform_valid = uniform_form.is_valid()
        payments_valid = up_form.is_valid()
        if uniform_valid and payments_valid:
            uniform = uniform_form.save(commit=False)
            uniform.player = player
            uniform.created_by = request.user
            uniform.save()

            upays = up_form.save(commit=False)
            for up in upays:
                up.uniform = uniform
                up.created_by = request.user
                up.save()

            up_form.save_m2m()

            return redirect('player_detail', id=player.id)
    else:
        uniform_form = UniformForm()
        up_form = uniform_pay_inline(
            prefix=uniform_payments_prefix,
            form_kwargs={'date_picker_mode': 'custom'},
        )

    show_uniform_modal = request.method == 'POST' and (not uniform_form.is_valid() or not up_form.is_valid())

    return render(request, template, locals())

@login_required
def edit_player(request, id=None,template='players/edit_form.html'):
    object = Player.objects.get(id=id)
    parent = Parent.objects.filter(player_id=object).first()
    uniform = Uniform.objects.filter(player=object).first()
    uniform_pay = UniformPayment.objects.filter(uniform=uniform).first()
    uniform_pay_inline = inlineformset_factory(Uniform, UniformPayment, form=UniformPaymentForm, extra=1)
    uniform_payments_prefix = 'uniformpayment_set'
    if request.method == 'POST':
        player_form = PlayerForm(request.POST,instance=object)
        parent_form = ParentForm(request.POST,instance=parent,prefix='parent')
        uniform_form = UniformForm(request.POST,instance=uniform)
        uniform_payment_form = uniform_pay_inline(request.POST,instance=uniform_pay,prefix=uniform_payments_prefix)
        if player_form.is_valid() and parent_form.is_valid() and uniform_form.is_valid() and uniform_payment_form.is_valid():
            player = player_form.save(commit=False)
            player.save()

            uniform = uniform_form.save(commit=False)
            uniform.player = player
            uniform.save()

            uniform_payment = uniform_payment_form.save(commit=False)
            uniform_payment.uniform = uniform
            uniform_payment.save()

            parent = parent_form.save(commit=False)
            parent.player = player
            parent.save()

            return redirect('player_detail', id=id)
    else:
        player_form = PlayerForm(instance=object)
        parent_form = ParentForm(instance=parent,prefix='parent')
        uniform_form = UniformForm(instance=object)
        uniform_payment_form = uniform_pay_inline(instance=uniform,prefix=uniform_payments_prefix)
    
    return render(request, template, locals())
