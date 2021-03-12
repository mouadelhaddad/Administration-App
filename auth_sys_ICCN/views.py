from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import Http404
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from auth_sys_ICCN.models import *
from auth_sys_ICCN.forms import *
from auth_sys_ICCN.Executables.AddDelUsr import *
from auth_sys_ICCN.Executables.SSHconnect import *
from auth_sys_ICCN.Executables.ConnectedUsers import *
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from auth_sys_ICCN.Executables.mem import *
from auth_sys_ICCN.Executables.dd import *

# Create your views here.
global id
id = 0
global usr
usr = ''

global datamem
datamem = []
global datadd
datadd = []
global xvalues_mem
xvalues_mem = []
global xvalues_dd
xvalues_dd = []
global yvalues_mem
yvalues_mem = []
global yvalues_dd
yvalues_dd = []
global listeservers_id
listeservers_id=[]


class LineChartJSONView(BaseLineChartView):
    servers = GestionServeur.objects.all()
    serverIPlist = GestionServeur.objects.all()
    serverlist = []
    dcservers = []
    x = []
    y = []
    global listeservers_id
    global datamem
    for server in serverIPlist:
        try:
            serverlist.append([LastUserConnections(server.ip_address, server.password), server.id])
        except:
            dcservers.append(server.id)
            continue
    serverIPlist.filter(id__in=dcservers).delete()

    for server in serverIPlist:
        datamem.append(tp_reel_mem(server.ip_address, server.password))
        listeservers_id.append(server.id)

    for i in range(0, len(datamem)):
        for j in range(0, 30):
            if j % 2 == 0:
                x.append(datamem[i][j])
            else:
                y.append(float(datamem[i][j]))
    global xvalues_mem
    xvalues_mem = x[:15]

    def get_labels(self):
        return xvalues_mem

    def get_providers(self):
        L = []
        for i in listeservers_id:
            L.append("Serveur " + str(i))
        return L

    global yvalues_mem
    for i in range(0, len(y), 15):
        yvalues_mem.append(y[i:i + 15])

    def get_data(self):
        return yvalues_mem


line_chart_mem = TemplateView.as_view(template_name='auth_sys_ICCN/dashboard.html')
line_chart_json_mem = LineChartJSONView.as_view()


class LineChartJSONView_dd(BaseLineChartView):
    servers = GestionServeur.objects.all()
    serverIPlist = GestionServeur.objects.all()
    serverlist = []
    dcservers = []
    x = []
    y = []
    global datadd
    global listeservers_id
    for server in serverIPlist:
        try:
            serverlist.append([LastUserConnections(server.ip_address, server.password), server.id])
        except:
            dcservers.append(server.id)
            continue
    serverIPlist.filter(id__in=dcservers).delete()
    for server in serverIPlist:
        datadd.append(tp_reel_dd(server.ip_address, server.password))

    for i in range(0, len(datadd)):
        for j in range(0, 30):
            if j % 2 == 0:
                x.append(datadd[i][j])
            else:
                y.append(float(datadd[i][j]))
    global xvalues_dd
    xvalues_dd = x[:15]

    def get_labels(self):

        return xvalues_dd

    def get_providers(self):
        L = []
        for i in listeservers_id:
            L.append("Serveur " + str(i))
        return L

    global yvalues_dd
    for i in range(0, len(y), 15):
        yvalues_dd.append(y[i:i + 15])

    def get_data(self):
        return yvalues_dd


line_chart_dd = TemplateView.as_view(template_name='auth_sys_ICCN/dashboard.html')
line_chart_json_dd = LineChartJSONView_dd.as_view()


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'auth_sys_ICCN/home.html')


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'GET':
            return render(request, 'auth_sys_ICCN/loginuser.html', {'form': AuthenticationForm()})
        else:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, 'auth_sys_ICCN/loginuser.html', {'form': AuthenticationForm(),
                                                                        'error': 'Le nom d\'utilisateur ou le mot de passe est incorrect'})
            else:
                login(request, user)
                return redirect('dashboard')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required(login_url='/login/')
def dashboard(request):
    serverIPlist = GestionServeur.objects.all()
    serverlist = []
    dcservers = []
    for server in serverIPlist:
        try:
            serverlist.append([LastUserConnections(server.ip_address, server.password), server.id])
        except:
            dcservers.append(server.id)
            continue
    serverIPlist.filter(id__in=dcservers).delete()
    return render(request, 'auth_sys_ICCN/dashboard.html', {'serverlist': serverlist, 'servers': serverIPlist})


@login_required(login_url='/login/')
def Gestion_utilisateur(request):
    if request.method == 'GET':
        return render(request, 'auth_sys_ICCN/Gestion utilisateur.html')
    else:
        global id
        global usr
        ServerID = request.POST['ServerID']
        Username = request.POST['username']
        password = request.POST['password']
        usr = Username
        but1 = request.POST.get('exampleRadios')
        form = GestionUtilisateurForm(request.POST)
        if but1 == 'mod':
            try:
                instance = GestionServeur.objects.get(id=int(ServerID))
                SSHexec(instance.ip_address, Username, password, 'who')
                id = instance.id
                if GestionUtilisateur.objects.filter(username=Username, ip_address=instance.ip_address).exists():
                    print("dkhl lwla")
                    return redirect('modifier_utilisateur')
                else:
                    print("dkhl tanya")
                    instance2 = GestionUtilisateur(username=Username, userpassword=password,
                                                   ip_address=instance.ip_address)
                    instance2.save()
                    return redirect('modifier_utilisateur')
            except:
                return render(request, 'auth_sys_ICCN/Gestion utilisateur.html',
                              {'form': form, 'error': 'Le nom d\'utilisateur ou le mot de passe est incorrect'})
        else:
            try:
                instance = GestionUtilisateur.objects.get(username=Username)
                id = instance.id
                if str(instance.userpassword) == str(password):
                    instance2 = GestionServeur.objects.get(ip_address=instance.ip_address)
                    DelUser(instance.ip_address, instance2.password, instance.username)
                    instance.delete()
                    return redirect('dashboard')
            except:
                return render(request, 'auth_sys_ICCN/Gestion utilisateur.html',
                              {'form': form, 'error': 'Le nom d\'utilisateur ou le mot de passe est incorrect'})


@login_required(login_url='/login/')
def Gestion_serveur(request):
    global id
    if request.method == 'GET':
        return render(request, 'auth_sys_ICCN/Gestion serveur.html')
    else:
        ServerID = request.POST['ServerID']
        password = request.POST['password']
        id = request.POST['ServerID']
        but1 = request.POST.get('exampleRadios')
        form = GestionServeurForm(request.POST)
        if but1 == 'mod':
            try:
                instance = GestionServeur.objects.get(id=ServerID)
                id = int(id)
                if str(instance.password) == str(password):
                    return redirect('modifier_serveur')
                else:
                    return render(request, 'auth_sys_ICCN/Gestion serveur.html',
                                  {'form': form, 'error': 'Le ServerID ou le mot de passe est incorrect'})
            except:
                return render(request, 'auth_sys_ICCN/Gestion serveur.html',
                              {'form': form, 'error': 'Le ServerID ou le mot de passe est incorrect'})
        else:
            try:
                instance = GestionServeur.objects.get(id=ServerID)
                if str(instance.password) == str(password):
                    delcrontab(instance.ip_address,instance.password)
                    instance.delete()
                    return redirect('dashboard')
            except:
                return render(request, 'auth_sys_ICCN/Gestion serveur.html',
                              {'form': form, 'error': 'Le ServerID ou le mot de passe est incorrect'})


@login_required(login_url='/login/')
def modifier_serveur(request):
    global id
    form = GestionServeurForm(request.POST)
    if request.method == 'GET':
        if id == 0:
            return redirect('Gestion_serveur')
        else:
            return render(request, 'auth_sys_ICCN/modofication_serveur.html')
    else:
        try:
            ServerID = request.POST['ServerID']
            IPaddress = request.POST['IPaddress']
            password = request.POST['password']
            instance = GestionServeur.objects.get(id=id)
            if GestionServeur.objects.filter(ip_address=IPaddress).exists():
                if instance.ip_address == IPaddress:
                    instance.delete()
                    instance = GestionServeur(id=ServerID, password=password, ip_address=IPaddress)
                    instance.save()
                    return redirect('dashboard')
                else:
                    return render(request, 'auth_sys_ICCN/modofication_serveur.html',
                                  {'form': form, 'error': 'Cette adresse IP est déjà présente'})
            elif GestionServeur.objects.filter(id=ServerID).exists():
                if instance.id == int(ServerID):
                    instance.delete()
                    instance = GestionServeur(id=ServerID, password=password, ip_address=IPaddress)
                    instance.save()
                    return redirect('dashboard')
                else:
                    return render(request, 'auth_sys_ICCN/modofication_serveur.html',
                                  {'form': form, 'error': 'Cet ID est déjà présent'})
            else:
                instance.delete()
                instance = GestionServeur(id=ServerID, password=password, ip_address=IPaddress)
                instance.save()
                return redirect('dashboard')
        except:
            return redirect('Gestion_serveur')


@login_required(login_url='/login/')
def ajouter_serveur(request):
    if request.method == 'GET':
        return render(request, 'auth_sys_ICCN/ajoute_serveur.html')
    else:
        ServerID = request.POST['ServerID']
        IPaddress = request.POST['IPaddress']
        password = request.POST['password']
        form = GestionServeurForm(request.POST)
        try:
            if GestionServeur.objects.filter(ip_address=IPaddress).exists():
                return render(request, 'auth_sys_ICCN/ajoute_serveur.html',
                              {'form': form, 'error': 'Cette adresse IP est déjà présente'})
            elif GestionServeur.objects.filter(id=ServerID).exists() or int(ServerID) == 0:
                return render(request, 'auth_sys_ICCN/ajoute_serveur.html', {'form': form,
                                                                             'error': 'Cet ID est déjà présent où vous avez utilisé un ID interdit  (id=0)'})
            else:
                instance = GestionServeur(id=ServerID, password=password, ip_address=IPaddress)
                instance.save()
                crontab(IPaddress, password)
                return redirect('dashboard')
        except:
            return render(request, 'auth_sys_ICCN/ajoute_serveur.html',
                          {'form': form, 'error': 'Une erreur est survenue veuillez remplir tous les champs'})


@login_required(login_url='/login/')
def modifier_utilisateur(request):
    global id
    global usr
    form = GestionUtilisateur(request.POST)
    if request.method == 'GET':
        if id == 0:
            return redirect('Gestion_utilisateur')
        else:
            return render(request, 'auth_sys_ICCN/modofication_utilisateur.html')
    else:
        password = request.POST['password']
        newpassword = request.POST['newpassword']
        if password != newpassword or len(password) == 0:
            return render(request, 'auth_sys_ICCN/modofication_utilisateur.html',
                          {'form': form, 'error': 'les mots de passe ne sont pas identiques retapez un mot de passe'})
        else:
            instance2 = GestionServeur.objects.get(id=id)
            instance = GestionUtilisateur.objects.get(username=usr, ip_address=instance2.ip_address)
            try:
                ModUserPwd(instance2.ip_address, instance2.password, instance.username, password)
                instance.delete()
                instance = GestionUtilisateur(username=instance.username, userpassword=password,
                                              ip_address=instance2.ip_address)
                instance.save()
                return redirect('dashboard')
            except:
                return render(request, 'auth_sys_ICCN/modofication_utilisateur.html', {'form': form,
                                                                                       'error': 'Une erreur est survenue veuillez retaper le nouveau mot de passe'})


@login_required(login_url='/login/')
def ajouter_utilisateur(request):
    if request.method == 'GET':
        return render(request, 'auth_sys_ICCN/ajoute_utilisateur.html')
    else:
        username = request.POST['username']
        IPaddress = request.POST['IPaddress']
        password = request.POST['password']
        form = GestionUtilisateur(request.POST)
        if GestionServeur.objects.filter(ip_address=IPaddress).exists():
            instance2 = GestionServeur.objects.get(ip_address=IPaddress)
            if utilexist(IPaddress, instance2.password, username):
                return render(request, 'auth_sys_ICCN/ajoute_utilisateur.html',
                              {'form': form, 'error': 'Ce nom d\'utilisateur est déjà présent'})
            else:
                instance = GestionUtilisateur(username=username, userpassword=password, ip_address=IPaddress)
                instance.save()
                AddUser(IPaddress, instance2.password, username, password)
                return redirect('dashboard')
        else:
            return render(request, 'auth_sys_ICCN/ajoute_utilisateur.html',
                          {'form': form, 'error': 'Aucun serveur avec cette adresse ip penser à ajouter un serveur'})


@login_required(login_url='/login/')
def server(request, server_id):
    try:
        server = GestionServeur.objects.get(id=server_id)

    except GestionServeur.DoesNotExist:
        raise Http404("Server does not exist.")
    ConnectedUsers = ConnectedUsrNow(server.ip_address, server.password)
    UserConnectionHistory = ConnectedUsrLast(server.ip_address, server.password)
    context = {
        "server": server,
        "ConnectedUsers": ConnectedUsers,
        "UserConnectionHistory": UserConnectionHistory
    }
    return render(request, "auth_sys_ICCN/server.html", context)


@login_required(login_url='/login/')
def ramdisk(request, server_id):
    try:
        server = GestionServeur.objects.get(id=server_id)
    except GestionServeur.DoesNotExist:
        raise Http404("Server does not exist.")
    Listdiskramusage = getinfo(server.ip_address, server.password)
    context = {
        "Listdiskramusage": Listdiskramusage,
        "server": server,
    }
    return render(request, "auth_sys_ICCN/ramdisk.html", context)