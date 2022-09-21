from django.shortcuts import render
from .models import Contrat 
from datetime import datetime, timedelta,date

def status_changeScheduler(request):
    contractList = Contrat.objects.all()
    for contrat in contractList:
    	if contrat.get_NbDays()==date.today():
    		contrat.active='False'
    return render(request, 'home.html')