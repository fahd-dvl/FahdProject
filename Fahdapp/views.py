from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import TemplateView
from .forms import LoginForm
from django.contrib.auth import authenticate,login
from .forms import SignupForm
from django.contrib.auth.models import User
from .models import Hotel
from django.contrib.auth.decorators import login_required


class HomeView(TemplateView):
    template_name = "Fahdapp/index.html"

def login_view(request):
    login_form = LoginForm()
    if request.method == "POST" :
        login_form = LoginForm(request,data=request.POST)
        if login_form.is_valid():
            user = authenticate(username = login_form.cleaned_data['username'],password= login_form.cleaned_data['password'])
            if user is not None:
                login(request,user)
                return redirect('Blog')
    return render(request,template_name="Fahdapp/login.html",context={"login_form" : login_form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Enregistre l'utilisateur
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Connecte l'utilisateur automatiquement
            login(request, user)

            # Redirige vers la page d'accueil après l'enregistrement
            return redirect('Blog')  # Assurez-vous que 'home' est bien défini dans urls.py
    else:
        form = SignupForm()

    return render(request, 'Fahdapp/signup.html', {'signup_form': form})

@login_required
def blog_view(request): 
    context = {}
    hotels = Hotel.objects.all()
    context['hotels'] = hotels
    return render(request,"Fahdapp/blog.html",context)

@login_required
def reservation_view(request, hotel_id) :
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Enregistre l'utilisateur
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Connecte l'utilisateur automatiquement
            login(request, user)

            # Redirige vers la page d'accueil après l'enregistrement
            return redirect('Blog')  # Assurez-vous que 'home' est bien défini dans urls.py
    else:
        hotel = get_object_or_404(Hotel, id_hotel=hotel_id)
        return render(request=request, template_name="Fahdapp/reservation.html", context={'hotel' : hotel})
    
