from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from datetime import datetime
from django.utils.dateparse import parse_date
from django.forms import inlineformset_factory
from .forms import OutcomingForm, SavingsForm, OrderForm, OrderPaymentForm
from .models import Outcoming, Subscription, Savings, UniformOrder, OrderPayment
from users.models import Player
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags import humanize
# Create your views here.

OrderPaymentFormSet = inlineformset_factory(
    UniformOrder,
    OrderPayment,
    form=OrderPaymentForm,
    extra=1,
    can_delete=False,
)


def build_accounting_context(order_form=None, order_payment_formset=None, show_order_modal=False):
    if order_form is None:
        order_form = OrderForm(prefix='order')

    if order_payment_formset is None:
        order_payment_formset = OrderPaymentFormSet(prefix='payments')

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

    return {
        'order_form': order_form,
        'order_payment_formset': order_payment_formset,
        'show_order_modal': show_order_modal,
        'total_incomings': total_incomings,
        'total_outcoming': total_outcoming,
        'total_savings': total_savings,
        'balance': balance,
    }

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
    return render(request, template, build_accounting_context())


@login_required
def manage_order(request):
    if request.method != 'POST':
        return redirect('accounting_dashboard')

    order_id = request.POST.get('order_id')
    order_instance = get_object_or_404(UniformOrder, pk=order_id) if order_id else None

    order_form = OrderForm(request.POST, prefix='order', instance=order_instance)
    order_payment_formset = OrderPaymentFormSet(
        request.POST,
        prefix='payments',
        instance=order_instance or UniformOrder(),
    )

    if order_form.is_valid() and order_payment_formset.is_valid():
        order = order_form.save(commit=False)
        if not order.created_by_id:
            order.created_by = request.user
        order.save()

        order_payment_formset.instance = order
        payment_objects = order_payment_formset.save(commit=False)
        for payment in payment_objects:
            payment.order = order
            if not payment.created_by_id:
                payment.created_by = request.user
            payment.save()

        return redirect('accounting_dashboard')

    return render(
        request,
        'accounting/dashboard.html',
        build_accounting_context(
            order_form=order_form,
            order_payment_formset=order_payment_formset,
            show_order_modal=True,
        ),
    )

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

    pay_date = parse_date(request.POST.get('pay_date', ''))
    if not pay_date:
        return redirect('player_detail', id=id)

    player = Player.objects.get(id=id)
    latest_sub = Subscription.objects.filter(player=player).order_by('-pay_date').first()
    subscription_data = {
        'player': player,
        'pay_date': pay_date,
        'created_by': request.user,
    }
    if latest_sub:
        subscription_data.update(
            physical_condition=latest_sub.physical_condition,
            condition=latest_sub.condition,
            single_class=latest_sub.single_class,
            ammount=latest_sub.ammount,
        )
    Subscription.objects.create(**subscription_data)

    return redirect('player_detail', id=id)
