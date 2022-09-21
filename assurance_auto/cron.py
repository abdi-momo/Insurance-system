from django.shortcuts import render
from .models import Contrat 

from datetime import datetime, timedelta,date
from importlib import reload
from petshop import parrot as parrot

def change_active_status():
    contractList = Contrat.objects.all()
    for contrat in contractList:
        end_date=contrat.get_NbDays()
        if contrat.get_NbDays()<=date.today():
            contractList.update(active='False')
    # one_minute_ago = timezone.now() - timezone.timedelta(minutes=1)
    # expired_discounts = Discount.objects.filter(
    #     created_at__lte=one_minute_ago
    # )
        print(end_date)
    
