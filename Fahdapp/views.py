from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import TemplateView
from .forms import LoginForm
from django.contrib.auth import authenticate,login
from .forms import SignupForm
from django.contrib.auth.models import User
from .models import Hotel
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime
from .models import Reservation



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
            
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            
            login(request, user)

            
            return redirect('Blog')  
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
           
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user)

           
            return redirect('Blog')  
    else:
        hotel = get_object_or_404(Hotel, id_hotel=hotel_id)
        return render(request=request, template_name="Fahdapp/reservation.html", context={'hotel' : hotel})
    

def reservation_view(request, hotel_id):
    hotel = get_object_or_404(Hotel, id_hotel=hotel_id)
    rooms = hotel.rooms.all()
    rooms_json = json.dumps(list(rooms.values('room_number', 'description', 'price_per_night', 'reservations')))

    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        checkin_date = request.POST.get('checkin_date')
        checkout_date = request.POST.get('checkout_date')

        selected_room = hotel.rooms.filter(room_number=room_number).first()

        if selected_room:
            reservations = selected_room.reservations.all()
            is_available = True
            for reservation in reservations:
                if not (checkout_date <= reservation.check_in or checkin_date >= reservation.check_out):
                    is_available = False
                    break

            if is_available:
                checkin_date_obj = datetime.strptime(checkin_date, '%Y-%m-%d').date()
                checkout_date_obj = datetime.strptime(checkout_date, '%Y-%m-%d').date()
                days = (checkout_date_obj - checkin_date_obj).days
                total_price = selected_room.price_per_night * days
                reservation = Reservation.objects.create(
                    check_in=checkin_date_obj,
                    check_out=checkout_date_obj,
                    reservation_price=total_price,
                    user=request.user  
                )

                
                reservation.rooms.add(selected_room)
                reservation.save()

                return redirect('Confirmation')
            else:
                return render(request, 'Fahdapp/reservation.html', {
                    'hotel': hotel,
                    'rooms_json': rooms_json,
                    'error': 'The selected room is not available for the chosen dates.'
                })

    return render(request, 'Fahdapp/reservation.html', {'hotel': hotel, 'rooms_json': rooms_json})

def confirmation_view(request):
    # Get the last reservation made
    last_reservation = Reservation.objects.last()
    
    return render(request, 'Fahdapp/confirmation.html', {'reservation': last_reservation})