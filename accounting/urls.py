from django.urls import path
from .views import *

urlpatterns = [
    path('', accounting_dashboard, name="accounting_dashboard"),
    path('ajax/get-outcoming-list/', get_outcoming_list, name='get_outcoming_list'),
    path('add-outcoming/', add_outcoming, name='add_outcoming'),
    path('ajax/get-savings-list/', get_saving_list, name='get_saving_list'),
    path('add-saving/', add_saving, name='add_saving'),
    path('ajax/update-subscription/<id>', update_subscription, name='update_subscription'),
]