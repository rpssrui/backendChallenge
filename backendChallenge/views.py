import requests
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from datetime import timedelta
from .models import ExchangeRate
from django.db.models import Avg
import datetime

def fetch_exchange_rate(date):
    url = f'https://api.frankfurter.app/{date}?from=USD&to=EUR'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['rates']['EUR']
    except requests.RequestException as e:
        # Handle different types of exceptions and log the error
        print(f"Error fetching exchange rate: {e}")
        return None

def get_or_create_exchange_rate(date):
    try:
        rate_obj = ExchangeRate.objects.get(date=date)
        return rate_obj.rate
    except ExchangeRate.DoesNotExist:
        rate = fetch_exchange_rate(date)
        if rate is not None:
            rate_obj = ExchangeRate.objects.create(date=date, rate=rate)
            return rate
        else:
            return None

def validate_date(date_str):
    date_obj = parse_date(date_str)
    if date_obj is None:
        return False, None
    return True, date_obj

def get_usd_to_eur_rate(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        is_valid_start, start_date_obj = validate_date(start_date)
        is_valid_end, end_date_obj = validate_date(end_date)

        if not is_valid_start or not is_valid_end:
            return JsonResponse({'error': 'Invalid date format for `start_date` or `end_date`. Expected format: YYYY-MM-DD'}, status=400)
        
        if start_date_obj > end_date_obj:
            return JsonResponse({'error': '`end_date` cannot be before `start_date`.'}, status=400)

        rates = ExchangeRate.objects.filter(date__range=(start_date_obj, end_date_obj))

        existing_dates = rates.values_list('date', flat=True)
        missing_dates = [start_date_obj + timedelta(days=i) for i in range((end_date_obj - start_date_obj).days + 1) if (start_date_obj + timedelta(days=i)) not in existing_dates]

        if missing_dates:
            for date in missing_dates:
                get_or_create_exchange_rate(date)
            rates = ExchangeRate.objects.filter(date__range=(start_date_obj, end_date_obj))
        
        avg_rate = rates.aggregate(Avg('rate'))['rate__avg']
        return JsonResponse({'average_usd_to_eur': avg_rate})
    
    if not start_date and not end_date:
        today = datetime.date.today()
        rate = get_or_create_exchange_rate(today)
        if rate is not None:
            return JsonResponse({'usd_to_eur': rate})
        else:
            return JsonResponse({'error': 'Failed to fetch the exchange rate for today.'}, status=500)

    return JsonResponse({'error': 'Please provide both `start_date` and `end_date`.'}, status=400)
