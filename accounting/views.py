from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from datetime import datetime
from .forms import OutcomingForm, SavingsForm
from .models import Outcoming, Subscription, Savings
from users.models import Player
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags import humanize
# Create your views here.

@login_required
def add_outcoming(request, template='accounting/new_outcoming.html'):
    if request.method == 'POST':
        outcoming_form = OutcomingForm(request.POST)

        if outcoming_form.is_valid():
            outcoming = outcoming_form.save(commit=False)
            outcoming.school = request.user.school
            outcoming.save()
            
            return redirect('accounting_dashboard')
    else:
        outcoming_form = OutcomingForm()

    return render(request, template, locals())

def get_outcoming_list(request):
    draw = 1
    length = 100
    start = 0
    outcomings = Outcoming.objects.all().order_by('-date')

    paginator = Paginator(outcomings, length)
    page_number = start // length + 1
    page = paginator.get_page(page_number)

    data = [
        {
            "id" : obj.id,
            "description" : obj.description,
            "amount" : f'$ {humanize.intcomma(obj.amount)}',
            "date" : obj.date
        } for obj in page
    ]

    response = {
        "draw" : draw,
        "length" : length,
        "data" : data
    }

    return JsonResponse(response)

@login_required
def accounting_dashboard(request, template='accounting/dashboard.html'):
    incomings = Subscription.objects.all()
    total_incomings = 0
    for incoming in incomings:
        total_incomings += int(incoming.ammount)
    
    outcomings = Outcoming.objects.all()
    total_outcoming = 0
    for outcoming in outcomings:
        total_outcoming += int(outcoming.amount)
    
    savings = Savings.objects.all()
    total_savings = 0
    for saving in savings:
        total_savings += int(saving.ammount)
    
    balance = (total_incomings - total_outcoming) - total_savings

    return render(request, template, locals())

@login_required
def add_saving(request, template='accounting/new_saving.html'):
    if request.method == 'POST':
        saving_form = SavingsForm(request.POST)

        if saving_form.is_valid():
            saving = saving_form.save(commit=False)
            saving.school = request.user.school
            saving.save()

            return redirect('accounting_dashboard')
    else:
        saving_form = SavingsForm()

    return render(request, template, locals())

def get_saving_list(request):
    draw = 1
    length = 100
    start = 0
    savings = Savings.objects.all().order_by('-date')

    paginator = Paginator(savings, length)
    page_number = start // length + 1
    page = paginator.get_page(page_number)

    data = [
        {
            "id" : obj.id,
            "amount" : f'$ {humanize.intcomma(obj.ammount)}',
            "date" : obj.date
        } for obj in page
    ]

    response = {
        "draw" : draw,
        "length" : length,
        "data" : data
    }

    return JsonResponse(response)

@login_required
def update_subscription(request, id=None):
    if request.method != 'POST':
        return redirect('player_detail', id=id)

    latest_sub = Subscription.objects.filter(player_=id).latest('pay_date')
    current_month = datetime.now().month
    if current_month - latest_sub.expiration_date.month >= 1:
        subscrption = Subscription.objects.create(
            player = Player.objects.get(id=id),
            pay_date = datetime.now().date(),
            physical_condition = latest_sub.physical_condition,
            condition = latest_sub.condition,
            single_class = latest_sub.single_class,
            ammount = latest_sub.ammount
        )
    else:
        subscrption = Subscription.objects.create(
            player = Player.objects.get(id=id),
            pay_date = latest_sub.expiration_date,
            physical_condition = latest_sub.physical_condition,
            condition = latest_sub.condition,
            single_class = latest_sub.single_class,
            ammount = latest_sub.ammount
        )

    return redirect('player_detail', id=id)
