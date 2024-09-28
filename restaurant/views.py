# from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from .models import Menu
from django.core import serializers
from .models import Booking
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)
def bookings(request):
    if request.method == "POST":
        # Create a variable called data and assign it the value of json.load() with the request object passed as an argument.
        data = json.load(request)

        # Create a variable called exist and assign the following value to it:
        exist = Booking.objects.filter(reservation_date=data['reservation_date'])\
                               .filter(reservation_slot=data['reservation_slot']).exists()

        # If the value of the exist variable is False:
        if not exist:
            # Create a variable called booking and assign the value of the Booking() class object with the following code passed inside it:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot']
            )

            # Call the save() function over the booking variable using the dot operator.
            booking.save()
        else:
            # Else return HttpResponse() with the following arguments passed inside it:
            return HttpResponse(
                "{'error':1}",
                content_type='application/json'
            )

    # Create a variable called date and assign it the value:
    date = request.GET.get('date', datetime.today().date())

    # Create a variable called bookings and assign it the value:
    bookings = Booking.objects.all().filter(reservation_date=date)

    # Create a variable called booking_json and assign it the value:
    booking_json = serializers.serialize('json', bookings)

    # Return HttpResponse() with the following arguments passed inside it:
    return HttpResponse(
        booking_json,
        content_type='application/json'
    )
# Add your code here to create new views
def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 

@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()
        if exist==False:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    date = request.GET.get('date',datetime.today().date())

    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')