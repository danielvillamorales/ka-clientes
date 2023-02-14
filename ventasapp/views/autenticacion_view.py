from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect
from django.urls import reverse

def Login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("ventasapp:index"))
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user )
                return HttpResponseRedirect(reverse("ventasapp:index"))
            else:
                return render(request, "login/login.html", {
                    "mensaje": "Dato incorrectos"
                    })
        else:
            return render(request, "login/login.html")

def logOut(request):
    logout(request)
    return HttpResponseRedirect(reverse("ventasapp:login"))
    #return render(request, "login/logout.html")
