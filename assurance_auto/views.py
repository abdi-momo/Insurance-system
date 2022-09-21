from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .forms import ProprietaireAddForm, VehiculeAddForm, ModelAddForm,\
    MarqueAddForm,ContratAddFrom, ReglementAddForm, TypeContratAddForm,DepenseAddForm
from .models import ProprietaireVehicule, Vehicule, Contrat, \
    Model_Vehicule,Marque_Vehicule,Reglement, TypeContrat, Depenses
from django.shortcuts import get_object_or_404, redirect
# Importing the render_to_pdf function from the render.py file.
from .render import render_to_pdf
from django.contrib.auth.models import User
from datetime import datetime, timedelta,date
import datetime
from decimal import *
from itertools import chain
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count

from celery import Celery
from celery.schedules import crontab
from django.contrib.admin.views.decorators import staff_member_required

from twilio.rest import Client
from django.conf import settings


from rest_framework import viewsets
from .serializers import ContratSerializer, ReglementSerializer
# def status_changeScheduler(request):
#     contractList = Contrat.objects.all()

#     return render(request, 'home.html')


@login_required(login_url='/account/login')
def home_page(request):

    return render(request,'home.html', {})

@login_required(login_url='/account/login')
def Dashboard(request):
    template = 'auto/dashboard.html'
    from_date = request.GET.get('datedebut')
    to_date = request.GET.get('datefin')

    year_from = request.GET.get('year')

    month_from = request.GET.get('month')

    ListReglement=Reglement.objects.all().order_by('date_reglement')

    # Daily income
    list_benefice=[]
    list_periode = []
    benefice_periodique = Reglement.objects.filter(date_reglement__range=(from_date, to_date))\
    .values('date_reglement').annotate(Total_benefice=Sum('montant_a_regler')).order_by('date_reglement')
    for dict_item in benefice_periodique:
        paymentPeriode=dict_item['date_reglement'].strftime("%d-%m-%Y")
        list_benefice.append(float(dict_item['Total_benefice']))
        list_periode.append(paymentPeriode)
    
    # Daily expenses
    daily_list_expense=[]
    daily_periode_expense = []
    daily_expense = Depenses.objects.filter(date_depense__range=(from_date, to_date))\
    .values('date_depense').annotate(Total_expense=Sum('montant')).order_by('date_depense')
    for dict_item in daily_expense:
        expensePeriode=dict_item['date_depense'].strftime("%d-%m-%Y")
        daily_list_expense.append(float(dict_item['Total_expense']))
        daily_periode_expense.append(expensePeriode)

    
    # Yearly income
    YearList=[]
    YearlyIncome=[]

    yearly_income = Reglement.objects\
    .values('date_reglement__year').annotate(Total_benefice=Sum('montant_a_regler'))\
    .order_by('-date_reglement__year')[:5]
    for dict_item in yearly_income:
        YearList.append(dict_item['date_reglement__year'])
        YearlyIncome.append(float(dict_item['Total_benefice']))
    # print(YearList, YearlyIncome)

    # Yearly expense
    listEpenseAnnuelle=[]
    depensePeriode=[]
    yearly_expense = Depenses.objects\
    .values('date_depense__year').annotate(Total_depense=Sum('montant'))\
    .order_by('-date_depense__year')[:5]
    for dict_item in yearly_expense:
        depensePeriode.append(dict_item['date_depense__year'])
        listEpenseAnnuelle.append(float(dict_item['Total_depense']))


    # Monthly reports

    # Monthly incomes
    monthly_income_list=[]
    MonthList=[]
    monthly_income = Reglement.objects\
    .values('date_reglement__month').annotate(Total_benefice=Sum('montant_a_regler'))\
    .order_by('-date_reglement__month')[:12]
    for dict_item in monthly_income:
        MonthList.append(dict_item['date_reglement__month'])
        monthly_income_list.append(float(dict_item['Total_benefice']))
    # print(YearList, YearlyIncome)

    # monthly expenses
    monthlyExpenseList=[]
    monthlyExpense=[]
    monthly_expense = Depenses.objects\
    .values('date_depense__month').annotate(Total_depense=Sum('montant'))\
    .order_by('-date_depense__month')[:12]
    for dict_item in monthly_expense:
        monthlyExpenseList.append(dict_item['date_depense__month'])
        monthlyExpense.append(float(dict_item['Total_depense']))
    expenseListe= Depenses.objects.all()
    context={
        'ListReglement':ListReglement,
        # Daily reports
            # Incomes
        'benefice':list_benefice,
        'list_periode':list_periode,
            # Expenses
        'list_daily_expense':daily_list_expense,
        'list_periode_expense':daily_periode_expense,
        
        # Monthly reports
            # Incomes
        'monthly_income_list':monthly_income_list,
        'MonthIncomeList':MonthList,
            # Expenses
        'monthlyExpenseList':monthlyExpenseList,
        'monthlyExpense':monthlyExpense,

        # Yearly reports
        'YearList':YearList,
        'YearlyIncome':YearlyIncome,
        'listEpenseAnnuelle':listEpenseAnnuelle,
        'depensePeriode':depensePeriode, 
        'expenseListe':expenseListe
    }
    return render(request, template, context)

# @login_required(login_url='/account/login')
# def ListeDepense(request):
#     expenseListe= Depenses.objects.all()
#     return render(request, 'auto/dashboard.html', 
#                     {'expenseListe':expenseListe})



@login_required(login_url='/account/login')
def Clients(request):
    clients = ProprietaireVehicule.objects.all()
    form =ProprietaireAddForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        form=ProprietaireAddForm()
    else:
        ProprietaireAddForm()
    return render(request,'auto/clients.html',
                  {'form':form,
                   'client_list':clients})

@login_required(login_url='/account/login')
def AddClient(request):
    clients = ProprietaireVehicule.objects.all()
    if request.method=='POST':
        form = ProprietaireAddForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('assurance_auto:ListeClient')
            # form = ProprietaireAddForm()
    else:
        form = ProprietaireAddForm()
    return render(request,
                    'auto/AddClients.html',
                    {'form': form})


@login_required(login_url='/account/login')
def ClientList(request):
    clients = ProprietaireVehicule.objects.all()
    return render(request,
                    'auto/ListeClients.html',
                    {
                      'listClient': clients})

@login_required(login_url='/account/login')
def ClientUpdate(request, id=None):
    context={}
    detail = get_object_or_404(ProprietaireVehicule, id=id)
    form = ProprietaireAddForm(request.POST or None, request.FILES, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        id = form.instance.id
        return redirect('assurance_auto:ListeClient')
    else:
        form = ProprietaireAddForm(instance=detail)
    context["form"] = form
    return render(request, 'auto/UpdateClient.html', context)



@login_required(login_url='/account/login')
def CreateMarque(request):
    MarqueList = Marque_Vehicule.objects.all()
    form = MarqueAddForm(request.POST or None,)
    if form.is_valid():
        form.save()
        form = MarqueAddForm()
    else:
        MarqueAddForm()
    return render(request, 'auto/AddMarque.html',
                  {'form': form,
                   'client_list': MarqueList})

@login_required(login_url='/account/login')
def MarqueList(request):
    form = MarqueAddForm(request.POST or None, )
    if form.is_valid():
        form.save()
        form = MarqueAddForm()
    else:
        MarqueAddForm()
    MarqueList = Marque_Vehicule.objects.all()
    return render(request,
                  'auto/MarqueListe.html',
                  {
                      'form': form,
                      'MarqueList':MarqueList})

@login_required(login_url='/account/login')
def UpdateMarque(request, id=None):
    detail = get_object_or_404(Marque_Vehicule, id=id)
    form = MarqueAddForm(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # id = form.instance.id
        # return redirect('hr:personnel_details', id=id)
        return redirect('hr:paymentList')
    else:
        form=MarqueAddForm(instance=detail)
    context = {
        "form": form,
        "title": "Update payment"
    }
    return render(request, 'auto/AddMarque.html', context)

@login_required(login_url='/account/login')
def CreateModel(request):
    ModelList = Model_Vehicule.objects.all()
    form = ModelAddForm(request.POST or None,)
    if form.is_valid():
        form.save()
        form = ModelAddForm()
    else:
        ModelAddForm()
    return render(request, 'auto/AddModel.html',
                  {'form': form,
                   'client_list': ModelList})

@login_required(login_url='/account/login')
def ModelListe(request):
    form = ModelAddForm(request.POST or None, )
    if form.is_valid():
        form.save()
        form = ModelAddForm()
    else:
        ModelAddForm()
    ModelList = Model_Vehicule.objects.all()
    return render(request,
                  'auto/ListeModels.html',
                  {
                      'form': form,
                      'ModelList':ModelList})

@login_required(login_url='/account/login')
def CreateVehicule(request):
    VehiculeList = Vehicule.objects.all().order_by('-created')
    if request.method=='POST':
        form = VehiculeAddForm(request.POST or None,)
        if form.is_valid():
            form.save()
            return redirect('assurance_auto:Vehicule_Liste')
            # form = VehiculeAddForm()
    else:
        form=VehiculeAddForm()
    return render(request, 'auto/vehicule.html',
                  {'form': form,
                   'VehiculeList': VehiculeList})


@login_required(login_url='/account/login')
def VehiculeListe(request):
    form = VehiculeAddForm(request.POST or None, )
    if form.is_valid():
        form.save()
        form = VehiculeAddForm()
    else:
        VehiculeAddForm()
    VehiculeList = Vehicule.objects.all().order_by('-created')
    return render(request,
                  'auto/VehiculeListe.html',
                  {
                      'form': form,
                      'VehiculeList':VehiculeList})

@login_required(login_url='/account/login')
def VehiculeUpdate(request, id=None):
    context = {}
    detail = get_object_or_404(Vehicule, id=id)
    form = VehiculeAddForm(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        id = form.instance.id
        return redirect('assurance_auto:Vehicule_Liste')
    else:
        form = VehiculeAddForm(instance=detail)
    context["form"] = form
    return render(request, 'auto/UpdateVehicule.html', context)

@login_required(login_url='/account/login')
def vehicule_detail(request, id):
    detail=get_object_or_404(Vehicule,id=id)
    context={'vehicule_detail':detail}
    return render(request,'auto/vehiculeDetails.html', context)


@staff_member_required
def CreateContratType(request):
    list_TypeContrat=TypeContrat.objects.all()
    form = TypeContratAddForm(request.POST or None, )
    if form.is_valid():
        typecontrat=form.save(commit=False)
        typecontrat.utilisateur=request.user
        typecontrat.save()
        TypeContratAddForm()
    else:
        TypeContratAddForm()
    return render(request, 'auto/CategoryAssurance.html',
                  {'form': form,
                  'list_TypeContrat':list_TypeContrat
                  })

@staff_member_required
def ContratTypeUpdate(request, id):
    context = {}
    detail = get_object_or_404(TypeContrat, id=id)
    form = TypeContratAddForm(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        id = form.instance.id
        return redirect('assurance_auto:TypeContrat_Assurance')
    else:
        form = TypeContratAddForm(instance=detail)
    context["form"] = form
    return render(request, 'auto/UpdateTypeContrat.html', context)


@login_required(login_url='/account/login')
def CreateContrat(request):
    form = ContratAddFrom(request.POST or None, )
    if form.is_valid():
        contrat=form.save(commit=False)
        contrat.numero_de_contrat='K{0:07d}'.format(contrat.pk+1)+\
        '{-}'.format(date.today().strftime("%m"))+'{A}'.format(date.today()).strftime("%Y")
        print(contrat.numero_de_contrat)
        form = ContratAddFrom()
    else:
        ContratAddFrom()
    ContratList = Contrat.objects.all().order_by('-numero_de_contrat')
    return render(request,
                  'auto/Contrat.html',
                  {
                      'form': form,
                      'ContratList': ContratList})

@login_required(login_url='/account/login')
def ContratListe(request):
    duration=0
    ContratList = Contrat.objects.all().order_by('-numero_de_contrat')
    page = request.GET.get('page', 1)
    paginator = Paginator(ContratList, 10)

    form = ContratAddFrom(request.POST or None)
    last_contrat_id=Contrat.objects.latest('id')
    # print(last_contrat_id)
    try:
        if request.method == 'POST':
            if form.is_valid():
                obj, created = Contrat.objects.update_or_create(type_contrat=form.cleaned_data['type_contrat'],\
                    statut_assurance=form.cleaned_data['statut_assurance'],\
                    vehicule=form.cleaned_data['vehicule'],utilisateur=request.user,
                    numero_de_contrat='C{0:03d}'.format(last_contrat_id.pk+1)+\
            '-'+ date.today().strftime("%m") +'A'+ date.today().strftime("%y"),
                    sous_couvert=form.cleaned_data['sous_couvert'],
                    categorie=form.cleaned_data['categorie'],
                    active=form.cleaned_data['active'],
                    remainingdays=form.cleaned_data['type_contrat'].duration,
                    blocked_date=date.today()
                            )
                return redirect('assurance_auto:Contrat_Liste') 
            
        else:
            ContratAddFrom()
        contrats = paginator.page(page)
    except PageNotAnInteger:
        contrats = paginator.page(1)
    except EmptyPage:
        contrats=paginator.page(paginator.num_pages)
    return render(request,
                  'auto/ContratList.html',
                  {
                      'form': form,
                      'ContratList': contrats,
                  })

@login_required(login_url='/account/login')
def ContratUpdate(request, id=None):
    context = {}
    detail = get_object_or_404(Contrat, id=id)
    vehicule_num = request.POST.get('vehicule')
    form = ContratAddFrom(request.POST or None, instance=detail)
    nb_Days=0
    if form.is_valid():
        instance = form.save(commit=False)
        id = form.instance.id
        contrats=Contrat.objects.filter(vehicule=vehicule_num)
        for contrat in contrats:
            nb_Days=contrat.remainingdays
            if form.cleaned_data['statut_assurance']=='Suspendu':
                nb_Days = contrat.remainingdays-(date.today().day-contrat.blocked_date.day)
                blockedDate=date.today()
                # Mettre à jour les nombre des jours restants, la date du reactivation, et le statut de l'assurance
                contrats.update(remainingdays=nb_Days,blocked_date=blockedDate,statut_assurance=form.cleaned_data['statut_assurance'])
            elif form.cleaned_data['statut_assurance']=='Encours':
                nb_Days = contrat.remainingdays
                unblockedDate=contrat.unblocked_date
                blockedDate=date.today()
                # print('Last',nb_Days)
                contrats.update(remainingdays=nb_Days,unblocked_date=contrat.blocked_date, statut_assurance=form.cleaned_data['statut_assurance'],blocked_date=blockedDate)
            else:
                instance.save()
        return redirect('assurance_auto:Contrat_Liste')
    else:
        form = ContratAddFrom(instance=detail)
    context["form"] = form
    return render(request, 'auto/UpdateContrat.html', context)





@login_required(login_url='/account/login')
def StatusContrat(request):
    template='auto/ContratList.html'
    ContratList = Contrat.objects.all()
    compteur=0
    return render(request,template, {})

@login_required(login_url='/account/login')
def ContractDetail(request, id):
    contrats = get_object_or_404(Contrat, id=id)
    return render(request,
                  'auto/ContratDetails.html',
                  {'contrats': contrats})


@login_required(login_url='/account/login')
def ModifContrat(request, id=None):
    context = {}
    detail = get_object_or_404(Contrat, id=id)
    form = ContratAddFrom(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        id = form.instance.id
        return redirect('assurance_auto:Contrat_Liste')
    else:
        form = ContratAddFrom(instance=detail)
    context["form"] = form
    return render(request, 'auto/ModifContrat.html', context)


# @login_required(login_url='/account/login')
# def AddReglement(request):
#     contrats = Contrat.objects.all()
#     total_amount=0
#     form = ReglementAddForm(request.POST or None, )
#     if request.method == 'POST': 
#         if form.is_valid():
#             keyword = form.cleaned_data['contrat']
            # reglement = form.save(commit=False)
            # reglement.utilisateur = request.user
#             for contrat in contrats:
#                 reglement = Reglement.objects.filter(contrat=keyword)
#                 if keyword == contrat.numero_de_contrat:
#                     total_amount=total_amount+reglement.montant_a_regler 
#                     print(total_amount)
#                     if form.cleaned_data['montant_a_regler'] > contrat.montant_du_contrat:
#                         messages.error(request, " Vous avez payé plus que vous dever payer. ")
#                         form=ReglementAddForm()
#                     else:
#                         finalAmount=contrat.montant_du_contrat - form.cleaned_data['montant_a_regler']
#                         contrat.update(remainAmount=finalAmount)
#                         messages.success(request,"Paiement enregistré avec succés")
#                         reglement.save()
#                         return redirect('assurance_auto:addReglement')
#                         form = ReglementAddForm()
#                         print(contrat.remainAmount)
#     else:
#         form = ReglementAddForm()
#     ReglementList = Reglement.objects.all()
#     return render(request,
#                   'auto/AddReglement.html',
#                   {'form':form,
#                  'ReglementList':ReglementList})


@login_required(login_url='/account/login')
def AddReglement(request):
    amount_to_pay=0
    total_amount=0
    amount_paid=0
    num_contract = request.GET.get('num_contrat')
    List_contrat= Contrat.objects.all()

    form = ReglementAddForm(request.POST or None, )
    # ListReglement=Reglement.objects.all().order_by('date_reglement')
    ListReglement=Reglement.objects.all().order_by('-created')
    contrats = Contrat.objects.all()
    lastReglement = Reglement.objects.latest('id')

    page = request.GET.get('page', 1)
    paginator = Paginator(ListReglement, 5)
    
    # Test
    for number in ListReglement:
        # for contract_num in contrats:
        if number.contrat.numero_de_contrat == num_contract:
            amount_to_pay=number.contrat.type_contrat.montant_du_contrat
            amount_paid = amount_paid+float(number.montant_a_regler)
    try:
        if request.method == 'POST':
            if form.is_valid():
                keyword = form.cleaned_data['contrat']
                newPayement = form.cleaned_data['montant_a_regler']
                ReglementList = Reglement.objects.filter(contrat=keyword)
                for item in ReglementList:
                    total_amount=total_amount+item.montant_a_regler 
                
                # Comparaison du montant total payé avec le montant du contrat
                for contratID in Contrat.objects.filter(numero_de_contrat=keyword):
                    if contratID.type_contrat.montant_du_contrat<total_amount+newPayement:
                        messages.warning(request, " L\'opération ne peut pas être enregistrée\
                            car vous voulez payer plus que ce que nous vous devons. ")
                        form=ReglementAddForm()
                        break
                    elif contratID.type_contrat.montant_du_contrat==total_amount+newPayement:
                        messages.info(request, "Vous avez tout soldé. Merci beaucoup. ")
                        # reglement.save()
                        obj, created = Reglement.objects.update_or_create(
                            code_reglement='K{0:03d}'.format(lastReglement.pk+1)+\
            '-'+ date.today().strftime("%m") +'A'+ date.today().strftime("%y"),
                            contrat=form.cleaned_data['contrat'],
                            utilisateur=request.user,
                            montant_a_regler=form.cleaned_data['montant_a_regler'],
                            mode_de_paiment=form.cleaned_data['mode_de_paiment'],
                            regle=form.cleaned_data['regle']
                            )
                        return redirect('assurance_auto:addReglement')
                        # form=ReglementAddForm()
                    else:
                        # ListReglement.create(code_reglement=reglement.code_reglement)
                        obj, created = Reglement.objects.update_or_create(
                            code_reglement='K{0:03d}'.format(lastReglement.pk+1)+\
            '-'+ date.today().strftime("%m") +'A'+ date.today().strftime("%y"),
                            contrat=form.cleaned_data['contrat'],
                            utilisateur=request.user,
                            montant_a_regler=form.cleaned_data['montant_a_regler'],
                            mode_de_paiment=form.cleaned_data['mode_de_paiment'],
                            regle=form.cleaned_data['regle']
                            )
                        return redirect('assurance_auto:addReglement')
        else:
            form = ReglementAddForm()
        reglements = paginator.page(page)
    except PageNotAnInteger: 
        reglements = paginator.page(1) 
    except EmptyPage:
         reglements = paginator.page(paginator.num_pages)   
    return render(request,
                    'auto/AddReglement.html',
                    {'form':form,
                    'num_contract':num_contract,
                    'ListReglement':reglements,
                    'total_paid':total_amount, 
                    'num_contract':num_contract,
                    'amount_to_pay':amount_to_pay,
                    'amount_paid':amount_paid
                    }
                )
# @login_required(login_url='/account/login')
# def CreateReglement(request):
#     ListReglement=Reglement.objects.all().order_by('date_reglement')
#     form = ReglementAddForm(request.POST or None, )
#     if form.is_valid():
#         reglement=form.save(commit=False)
#         reglement.utilisateur=request.user
#         reglement.save()
#         ReglementAddForm()
#     else:
#         ReglementAddForm()
#     return render(request, 'auto/AddReglement.html',
#                     {'form':form,
#                     'ListReglement':ListReglement,
#                     # 'total_paid':total_amount, 
#                     }
#                 )



@login_required(login_url='/account/login')
def CreateDepenses(request):
    list_Depenses=Depenses.objects.all()
    form = DepenseAddForm(request.POST or None, )
    if form.is_valid():
        depense=form.save(commit=False)
        depense.utilisateur=request.user
        depense.save()
        DepenseAddForm()
    else:
        DepenseAddForm()
    return render(request, 'auto/addDepenses.html',
                  {'form': form,
                  'list_Depenses':list_Depenses
                  })

@login_required(login_url='/account/login')
def DepenseDetail(request, id):
    depense = get_object_or_404(Depenses, id=id)
    return render(request,
                  'auto/DepenseDetails.html',
                  {'depense': depense})


@login_required(login_url='/account/login')
def ModifDepense(request, id=None):
    context = {}
    detail = get_object_or_404(Depenses, id=id)
    form = DepenseAddForm(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.utilisateur=request.user
        instance.save()
        id = form.instance.id
        return redirect('assurance_auto:nouvelleDepense')
    else:
        form = DepenseAddForm(instance=detail)
    context["form"] = form
    return render(request, 'auto/ModifDepense.html', context)




@login_required(login_url='/account/signin')
def order_pdf(request, id):
    reglement = get_object_or_404(Reglement, id=id)
    utilisateur=request.user
    pdf = render_to_pdf('auto/pdf.html', {'reglement': reglement, 'user':utilisateur})
    if pdf:
        response= HttpResponse(pdf,content_type='application/pdf')
        response['Content-Disposition'] = 'filename=\
                "order_{}.pdf"'.format(reglement.code_reglement)
        return response
    else:
        return HttpResponse("Fichier n'existe pas")

@login_required(login_url='/account/signin')
def Carton_assurance(request, id):
    contrat = get_object_or_404(Contrat, id=id)
    utilisateur=request.user
    pdf = render_to_pdf('auto/CartonAssurance.html', 
            {'contrat': contrat, 
            'user':utilisateur}
        )
    if pdf:
        response= HttpResponse(pdf,content_type='application/pdf')
        response['Content-Disposition'] = 'filename=\
                "order_{}.pdf"'.format(contrat.numero_de_contrat)
        return response
    else:
        return HttpResponse("Fichier n'existe pas")



@login_required(login_url='/account/login')
def UpdateReglement(request, id=None):
    context = {}
    detail = get_object_or_404(Reglement, id=id)
    form = ReglementAddForm(request.POST or None, instance=detail)
    keyword = request.GET.get("contrat")
    amount_to_pay=request.GET.get('montant_a_regler')
    contrats = Contrat.objects.all()
    if form.is_valid():
        reglement=form.save(commit=False)
        reglement.utilisateur=request.user
        id = form.instance.id
        for contrat in contrats:
            if keyword == contrat.numero_de_contrat: 
                if form.cleaned_data['montant_a_regler'] > contrat.remainAmount:
                    messages.error(request, " Vous avez payé plus que vous dever payer. ")
                    ReglementAddForm()
                else:
                    finalAmount=contrat.montant_du_contrat - amount_to_pay
                    contrat.update(remainAmount=finalAmount)
                    messages.success(request,"Modification éffectuée avec succés")
                    reglement.save()
                    return redirect('assurance_auto:addReglement')
        # return redirect('assurance_auto:addReglement')
    else:
        form = ReglementAddForm(instance=detail)
    context["form"] = form
    return render(request,
                  'auto/UpdateReglement.html',
                  {'form':form})

@login_required(login_url='/account/login')
def ModifyReglement(request, id=None):
    context = {}
    detail = get_object_or_404(Reglement, id=id)
    form = ReglementAddForm(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.utilisateur=request.user
        instance.save()
        id = form.instance.id
        return redirect('assurance_auto:addReglement')
    else:
        form = ReglementAddForm(instance=detail)
    context["form"] = form
    return render(request, 'auto/ModifyReglement.html', context)



@login_required(login_url='/account/login')
def detailReglement(request,id):
    detail=get_object_or_404(Reglement,id=id)
    context={'reglement':detail}
    return render(request,'auto/ReglementDetails.html', context)

@login_required(login_url='/account/login')
def ListReglement(request):
    keyword = request.GET.get("keyword")
    if keyword:
        ReglementList=Reglement.objects.filter(Q(contrat__vehicule__immatriculation__contains=keyword)|Q(contrat__numero_de_contrat=keyword))
        return render(request,'auto/UpdateReglement.html',{'ReglementList':ReglementList})
    ReglementList = Reglement.objects.all()
    return render(request, 'auto/UpdateReglement.html', {'ReglementList': ReglementList})

@login_required(login_url='/account/login')
def new_invoice(request):
    from django.db import connection, transaction
    form = ReglementAddForm(request.POST or None)
    contrats = Contrat.objects.all()
    remainAmount=0
    NumContrat = request.POST.get('contrat')
    # montant que le client est prêt à regler. il peut être inférieur ou égale au montant du contrat.
    amount_to_pay = request.POST.get('montant_a_regler')
    total_paid=0
    montantContrat=0
    reglements = Reglement.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            reglt = form.save(commit=False)
            reglt.utilisateur = request.user
            cursor = connection.cursor()
            # reglmts=Reglement.objects.raw("SELECT SUM(montant_a_regler) FROM assurance_auto_reglement WHERE contrat_id=39")
            # print(reglmts)
            cursor.execute("SELECT sum(montant_a_regler) FROM assurance_auto_reglement WHERE contrat_id=%s"%(NumContrat))
            result=cursor.fetchone()
            print('Montant payé: ', result[0])
            total_paid=result[0]

            for contrat in contrats:
                if result[0] is None:
                    result[0]==0
                    form.save()
                elif result[0]+Decimal(amount_to_pay)<=contrat.montant_du_contrat:
                    # messages.info(request,"Montant du contrat: " + str(contrat.montant_du_contrat)+' and montant du contrat: ' + str(contrat.montant_du_contrat))
                    # print('Montant du contrat: ' + str(contrat.montant_du_contrat))
                    # print('Montant déjà payé: ' +str(result))
                    # print(result[])
                    messages.info(request,"Done")
                    form.save()
                # elif result[0]+Decimal(amount_to_pay)==contrat.montant_du_contrat:
                #     print("Félicitations, vous avez tout payé votre contrat d'assurance.")
                #     messages.success(request, "Félicitations, vous avez tout payé votre contrat d'assurance. ")
                #     # print(result[])
                #     form.save()
                else:
                    # if result[0]+Decimal(amount_to_pay)>contrat.montant_du_contrat:
                    print(result[0]+Decimal(amount_to_pay))
                    print(Decimal(amount_to_pay))
                    # form.save()
                    messages.info(request,"Vous avez déjà soldé le montant de votre contrat. ")
                    break
            form = ReglementAddForm()
    else:
        form = ReglementAddForm()
    context = {
        'title': 'Nouveau réglement',
        'contrat_list': contrats,
        'reglements':reglements,
        'form':form,
        'paidAmount':total_paid,
        'remainAmount':remainAmount,
        'montantContrat':montantContrat,
    }
    return render(request, 'auto/reglement.html', context)

def notification(request):
    # template = 'auto/ContratList.html'
    template = 'auto/alerte.html'
    contrats=Contrat.objects.all()
    info = request.GET.get("greatings")
    if info:
        for contrat in contrats:
            today=datetime.datetime.now().date()
            number_of_days=abs(int(today.strftime('%Y%m%d')))-int(contrat.get_NbDays().strftime('%Y%m%d'))
            if contrat.get_NbDays().strftime("%B")==\
            datetime.datetime.now().strftime("%B") and abs(number_of_days)<=3:
                client =  Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                response = client.messages.create(body=info + ' Mr/Mme ' + contrat.vehicule.proprietaire.prenom+ ' '+ contrat.vehicule.proprietaire.nom +\
                    '. Kamil Assurance vous informe que votre contrat d\'assurance expire dans '\
                    + str(abs(number_of_days))+ ' jours. Veuillez penser venir  pour le renouvellement. Merci.', 
                    to=contrat.vehicule.proprietaire.telephone, from_=settings.TWILIO_PHONE_NUMBER)
                # print('Remaining days',abs(number_of_days))
                # print(echeance.pret.compte.numero_compte, echeance.date_theorique.strftime("%B"), echeance.pret.compte.client.telephone)
        return redirect('assurance_auto:alerte_expiration')    
    return render(request, template, {'contrats':contrats})




# Set Up Routers and Create API URLs
class ContratViewSet(viewsets.ModelViewSet):
    queryset = Contrat.objects.all()
    serializer_class = ContratSerializer


class ReglementViewSet(viewsets.ModelViewSet):
   queryset = Reglement.objects.all()
   serializer_class = ReglementSerializer