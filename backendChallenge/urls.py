from django.urls import path
from .views import get_usd_to_eur_rate
from django.shortcuts import redirect


def redirect_to_currency(request):
    return redirect('usd-to-eur/')

urlpatterns = [
    path('usd-to-eur/', get_usd_to_eur_rate, name='usd_to_eur_rate'),
    path('', redirect_to_currency)
]
