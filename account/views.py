from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from rolepermissions.roles import assign_role
from django.template.loader import render_to_string
from django.views.generic import ListView

@staff_member_required(login_url='/account/login')
def add_user_view(request):
    if request.user.has_perm('create_stuff'):
        if request.method == 'POST':
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                role = request.POST.get('user_role')
                if role == 'admin':
                    user = user_form.save()
                    assign_role(user, 'admin')
                    return redirect('account:all_accounts')
                elif role == 'stuff':
                    user = user_form.save()
                    assign_role(user, 'stuff')
                    return redirect('account:all_accounts')
            else:
                return render(request, 'account/add_user.html')
        else:
            user_form = UserRegistrationForm()
        context = {
            'user_form': user_form,
        }
        return render(request, 'account/add_user.html', context)
    else:
        return render(request, 'account/permission_required.html')


@staff_member_required(login_url='/account/login')
def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser = User(username=username)
        newUser.set_password(password)

        newUser.save()
        login(request, newUser)
        messages.info(request, "Vous vous êtes inscrit avec succès ...")

        return redirect("hr:accueil")
    context = {
        "form": form
    }
    return render(request, "account/register.html", context)

@staff_member_required(login_url='/account/login')
def userList(request):
    list_user = User.objects.all()
    return render(request,'account/userListe.html',{'list_user':list_user})

def loginUser(request):
    form = LoginForm(request.POST or None)

    context = {
        "form": form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.warning(request, "Identifiant ou mot de passe incorrect")
            return render(request, "account/login.html", context)

        messages.success(request, "Connexion réussie")
        login(request, user)
        return redirect("/")
        # return redirect("assurance_auto:home_page")
    return render(request, "account/login.html", context)


def logoutUser(request):
    logout(request)
    messages.success(request, "Déconnexion réussie")
    return redirect("account:login")

class AccountListView(ListView):
    model = User
    template_name = 'account/accounts_list.html'
    context_object_name = 'accounts'