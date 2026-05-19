from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from datetime import datetime
from .forms import OutcomingForm, SavingsForm
from .models import Outcoming, Subscription, Savings
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def add_outcoming(request, template='accounting/new_outcoming.html'):
    if request.method == 'POST':
        outcoming_form = OutcomingForm(request.POST)

        if outcoming_form.is_valid():
            outcoming_form.save()

            print('Saved')
        
            return redirect('outcoming_list')
    else:
        outcoming_form = OutcomingForm()

    return render(request, template, locals())

def get_outcoming_list(request):
    draw = 1
    length = 100
    start = 0
    outcomings = Outcoming.objects.all().order_by('-date')

    paginator = Paginator(outcomings, length)
    page_number = start // length - 1
    page = paginator.get_page(page_number)

    data = [
        {
            "id" : obj.id,
            "description" : obj.description,
            "amount" : obj.amount,
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

    return render(request, template, locals())

@login_required
def add_saving(request, template='accounting/new_saving.html'):
    if request.method == 'POST':
        saving_form = SavingsForm(request.POST)

        if saving_form.is_valid():
            saving_form.save()

            print('Saved')
        
            return redirect('saving_list')
    else:
        saving_form = SavingsForm()

    return render(request, template, locals())

def get_saving_list(request):
    draw = 1
    length = 100
    start = 0
    savings = Savings.objects.all().order_by('-date')

    paginator = Paginator(savings, length)
    page_number = start // length - 1
    page = paginator.get_page(page_number)

    data = [
        {
            "id" : obj.id,
            "amount" : obj.ammount,
            "date" : obj.date
        } for obj in page
    ]

    response = {
        "draw" : draw,
        "length" : length,
        "data" : data
    }

    return JsonResponse(response)