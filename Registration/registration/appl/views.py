from django.shortcuts import render, HttpResponse, redirect    
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from datetime import time, timedelta
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.core.cache import cache
from PIL import Image
import io
import easyocr
import re
from django.db.models import Q

# Create your views here.

def homepage(request):
    user = request.user
    return render(request, 'home.html', {'username':user})


def aboutpage(request):
    return render(request, 'about.html')


def contactpage(request):
    return render(request, 'contact.html')
def chat_bot(request):
    return render(request, 'chat.html')



@login_required(login_url=('login'))
def bookpage(request):
    
    return render(request, 'booking.html')

@login_required(login_url=('login'))
def bookinghistory(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)
    return render(request, 'booking_history.html', {'bookings': bookings})

def signuppage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        my_user = User.objects.create_user(username, email, password)
        my_user.save()
        return redirect('login')
    return render(request, 'signup.html')

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
    return render(request, 'login.html')

def logoutpage(request):
    logout(request)
    return redirect('home')
@login_required(login_url=('login'))
def bookingsuccess(request):
    return render(request, 'booking_success.html')

@login_required(login_url=('login'))
def extendsuccess(request):
    return render(request, 'extend_success.html')

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        booking.delete()
        return redirect('bookinghistory')
    
@login_required
def extend_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        extend_time = request.POST.get('extend_time')
        if extend_time:
            extend_time = int(extend_time) 
            booking = get_object_or_404(Booking, id=booking_id)
            new_endtime = booking.end_time + timedelta(minutes=extend_time)
            new_totalendtime = booking.total_endtime + timedelta(minutes=extend_time)
            filter_for_unique_slot = Booking.objects.filter(
                selected_slot = booking.selected_slot,
                start_time__lt = new_totalendtime,
                total_endtime__gt=booking.start_time
            ).exclude(id = booking_id)
            if filter_for_unique_slot.exists():
                messages.error(request, "Time extension overlaps with another booking.")
                return redirect('bookextend')
            booking.end_time = new_endtime
            booking.total_endtime = new_totalendtime
            booking.save()
            return redirect('extendsuccess')
        return redirect('book')
    
@login_required
def bookfixed(request):##################################current work
    print(f"Current user: {request.user}")
    if request.method == 'POST':
        fullname = request.POST.get('name')
        phone = request.POST.get('phone')
        # licenseplate = request.POST.get('licensePlate')
        location = request.POST.get('location')
        selected_slot = request.POST.get('selected_slot')
        start_time_str = request.POST.get('startTime')
        hour_num= request.POST.get('numHours')
        print(fullname, phone, location, selected_slot, start_time_str, type(start_time_str), hour_num)
        try:
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
        except ValueError:
            start_time = None
        current_date = datetime.today().date()
        start_datetime = datetime.combine(current_date, start_time)
        start_datetime_str = str(start_datetime)
        end_datetime = start_datetime + timedelta(hours=int(hour_num))
        end_datetime_str = str(end_datetime)
        buffer_time = timedelta(minutes=15)
        total_endtime_str = str(end_datetime + buffer_time)
        # a= start_time# starttime in just hour and minute but in string 
        # end_time_hr_min = str(int(a[0:2])+ int(hour_num)) + str(a[2:5])# maile start time ma hr jodeko ani yeslai str mai convert gare ko
        # b = current_date# current date in datetime
        # start_time = str(b)+ " " +a# make start time as desired format paila string concatination 
        # end_time = end_time_hr_min
        # print(end_time_hr_min, end_time)
        
        # total_endtime = (datetime.strptime(end_time, '%H:%M').time() + buffer_time).strftime('%H:%M')
        # total_endtime = str(total_endtime)

        existing_booking1 = Booking.objects.filter(
            selected_slot=selected_slot,
            # only depends on start time end time ma depend xaina, aile chai
            #  start time and end time format is not same
            
            start_time__lt=end_datetime ,
            total_endtime__gt=start_datetime
            # total_endtime=start_datetime

        ).exists()
        if existing_booking1:
            messages.error(request, "The selected slot is already booked for the chosen time. Please choose a different slot or time.")
            return redirect('bookfixed')
        
        payment_status = 'Paid'
        user = request.user
        booking_type_value = "fixed"
        # Saveing that data
        booking = Booking(
            user=user,
            full_name=fullname,
            phone=phone,
            # license_plate=licenseplate,
            location=location,
            selected_slot=selected_slot,
            start_time=start_datetime_str,
            end_time = end_datetime_str,
            booking_type = booking_type_value,
            buffer_time = buffer_time,
            total_endtime = total_endtime_str,
            payment = payment_status
        )
        booking.save()        
        return render(request, 'booking_success.html', {'booking': booking})
    return render(request, 'booking1.html')
    
@login_required
def bookflexible(request):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M')
    print(current_datetime)
    print(f"Current user: {request.user}")
    existing_booking_slot1 = Booking.objects.filter(
            selected_slot="Slot-1",
    ).exclude(Q(status = 'Ended')| Q(total_endtime__lt = formatted_datetime ) & Q(booking_type = 'fixed')).exists()
    existing_booking_slot2 = Booking.objects.filter(
            selected_slot="Slot-2",
            

    ).exclude(Q(status = 'Ended')| Q(total_endtime__lt = formatted_datetime ) & Q(booking_type = 'fixed')).exists()
    existing_booking_slot3 = Booking.objects.filter(
            selected_slot="Slot-3",
            

    ).exclude(Q(status = 'Ended')| Q(total_endtime__lt = formatted_datetime ) & Q(booking_type = 'fixed')).exists()
    existing_booking_slot4 = Booking.objects.filter(
            selected_slot="Slot-4",
            

    ).exclude(Q(status = 'Ended')| Q(total_endtime__lt = formatted_datetime ) & Q(booking_type = 'fixed')).exists()
    context = {
        'existing_booking_slot1': existing_booking_slot1,
        'existing_booking_slot2': existing_booking_slot2,
        'existing_booking_slot3': existing_booking_slot3,
        'existing_booking_slot4': existing_booking_slot4,
        # Include other context variables if needed
    }

    if request.method == 'POST':
        fullname = request.POST.get('name')
        phone = request.POST.get('phone')
        # licenseplate = request.POST.get('licensePlate')
        location = request.POST.get('location')
        selected_slot = request.POST.get('selected_slot')
        start_time_str = request.POST.get('startTime')
        print(fullname, phone, location, selected_slot, start_time_str, type(start_time_str))
        try:
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
        except ValueError:
            start_time = None
        # c= start_time# using to match the format of end time and start time
        # start_time = str(start_time)
        # current_date = datetime.today().date()
        # a= start_time# starttime in just hour and minute but in string 
        # b = current_date# current date in datetime
        # start_time = str(b)+ " " +a# make start time as desired format paila string concatination 
        # end_time = time(0,0)
        current_date = datetime.today().date()
        start_datetime = datetime.combine(current_date, start_time)
        start_datetime_str = str(start_datetime)
        end_datetime = datetime.combine(datetime.today(), time(0, 0, 0))
        # end_datetime_str = str(end_datetime) # no neddd
        # buffer_time = timedelta(minutes=15) #buffer time models.py mai default 0 xa
        total_endtime_str = str(end_datetime)
        


        
        
        
        existing_booking = Booking.objects.filter( #just kept this incase two user book simultaneosly
            selected_slot= selected_slot,
            
           

        ).exclude(Q(status = 'Ended')| Q(total_endtime__lt = formatted_datetime ) & Q(booking_type = 'fixed')).exists()
        if existing_booking:
            messages.error(request, "The selected slot is already booked for the chosen time. Please choose a different slot or time.")
            return redirect('bookflexible')
        

        user = request.user
        booking_type_value = "flexible"

        # Saveing that data
        booking = Booking(
            user=user,
            full_name=fullname,
            phone=phone,
            # license_plate=licenseplate,
            location=location,
            selected_slot=selected_slot,
            start_time=start_datetime_str,
            end_time = total_endtime_str,
            booking_type = booking_type_value,
        )
        booking.save()        
        return render(request, 'booking_success.html', {'booking': booking})
    return render(request, 'booking2.html', context)

 

def show_slot_availability(request):
    
    available_slots1 = Booking.objects.filter(selected_slot = "Slot-1")
    available_slots2 = Booking.objects.filter(selected_slot = "Slot-2")
    available_slots3 = Booking.objects.filter(selected_slot = "Slot-3")
    available_slots4 = Booking.objects.filter(selected_slot = "Slot-4")
    
    
    if available_slots1.exists():
        
        time_free = Booking.objects.filter(selected_slot = "Slot-1").order_by("start_time")
        list_for_slot1 = []
        for booking in time_free:
            start_time = booking.start_time
            end_time = booking.end_time
            time_range = f' Booked from{start_time} to {end_time}'
            list_for_slot1.append(time_range)
    elif not (available_slots1.exists()):
        list_for_slot1 = ["Slot is available for whole Duration"]
        

    if available_slots2.exists():
        
        time_free = Booking.objects.filter(selected_slot = "Slot-1").order_by("start_time")
        list_for_slot2 = []
        for booking in time_free:
            start_time = booking.start_time
            end_time = booking.end_time
            time_range = f' Booked from{start_time} to {end_time}'
            list_for_slot2.append(time_range)
    elif not (available_slots2.exists()):
        list_for_slot2 = ["Slot is available for whole Duration"]

    if available_slots3.exists():
        
        time_free = Booking.objects.filter(selected_slot = "Slot-1").order_by("start_time")
        list_for_slot3 = []
        for booking in time_free:
            start_time = booking.start_time
            end_time = booking.end_time
            time_range = f' Booked from{start_time} to {end_time}'
            list_for_slot3.append(time_range)
    elif not (available_slots3.exists()):
        list_for_slot3 = ["Slot is available for whole Duration"]

    if available_slots4.exists():
        
        time_free = Booking.objects.filter(selected_slot = "Slot-1").order_by("start_time")
        list_for_slot4 = []
        for booking in time_free:
            start_time = booking.start_time
            end_time = booking.end_time
            time_range = f' Booked from {start_time} to {end_time}'
            list_for_slot4.append(time_range)

    elif not (available_slots4.exists()):
        list_for_slot4 = ["Slot is available for whole Duration"]
    # elif available_slots2.exists():
    #     slot = available_slots2.first()
    #     time_range = f"{slot.start_time} - {slot.end_time}"
    # elif available_slots3.exists():
    #     slot = available_slots3.first()
    #     time_range = f"{slot.start_time} - {slot.end_time}"
    # elif available_slots4.exists():
    #     slot = available_slots4.first()
    #     time_range = f"{slot.start_time} - {slot.end_time}"
    # if not(available_slots1.exists() and available_slots2.exists() and available_slots3.exists() and available_slots4.exists()):
    #     time_range = "Slot is available for whole Duration"
    #     return JsonResponse({'list_for_slot1': time_range})
    return JsonResponse({'list_for_slot1': list_for_slot1,
                         'list_for_slot2': list_for_slot2,
                         'list_for_slot3': list_for_slot3,
                         'list_for_slot4': list_for_slot4})

def book_extend(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)
    return render(request, 'extend_file.html', {'bookings': bookings})

def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        if booking:
            if booking.payment == 'Paid':
                messages.error(request, "Payment for this booking has already been confirmed!")
                return redirect('bookinghistory')
            booking.payment = 'Paid'
            booking.save() 
            start = booking.start_time
            end = booking.end_time
            time_difference = end - start

# Get the difference in minutes
            difference_in_minutes = time_difference.total_seconds() / 60
            total = difference_in_minutes * 0.5
            
    return render(request, 'payment_success.html', {'booking': booking, 'total':total})

def save_license_plate_data(license_plate):
    cache.set('latest_license_plate', license_plate, timeout=60*5)  # Cache for 5 minutes

def fetch_latest_license_plate_data():
    return cache.get('latest_license_plate')

# @login_required
@csrf_exempt
@require_POST
def process_image(request):
    if request.method == 'POST':
        print('POST request detected')
        user_to_notify_1 = ' '
        current_time = datetime.now()
        reader = easyocr.Reader(['en'])
        final_text = " "
        if 'file' in request.FILES:
            image = request.FILES['file']
            img = Image.open(image)
            # text = pytesseract.image_to_string(img)
            final_text = " "
            text = reader.readtext(img)
            if text:
                
                for item in text:
                    final_text += (item[1]+" ")
                final_text = final_text.strip().upper()  # Standardize extracted text
                # final_text = re.sub(r'[^A-Z0-9]', '', final_text)


                active_booking = Booking.objects.filter(
                    selected_slot='Slot-1', 
                    status='Pending..', 
                    booking_type='fixed',
                    start_time__lte=current_time, 
                    end_time__gte=current_time
                ).first()
                active_booking_flex = Booking.objects.filter(
                    selected_slot='Slot-1', 
                    status='Pending..', 
                    booking_type='flexible',
                    start_time__lte=current_time, 
                    end_time=datetime.combine(datetime.today(), time(0, 0, 0)),
                ).first()
                active_booking1_flex = Booking.objects.filter(
                    selected_slot='Slot-1', 
                    status='Verified.', 
                    booking_type='flexible',
                    start_time__lte=current_time, 
                    end_time=datetime.combine(datetime.today(), time(0, 0, 0)),
                ).first()
                if active_booking_flex:
                    save_license_plate_data(active_booking_flex.license_plate)  #cache save rakhen
                    user_to_notify = active_booking_flex.user
                    
                    print(f'reached inside active_booking_flex{final_text}')
                    if user_to_notify and user_to_notify.is_authenticated:  # Ensure the user is logged in
                        print(f'User:{user_to_notify}')
                        print(f'reached inside auth active_booking_flex{final_text}')
                        active_booking_flex.license_plate = final_text
                        active_booking_flex.save()
                        user_to_notify_1 = user_to_notify.username
                        print({'temp_user': user_to_notify_1, 'final': final_text})

                        return JsonResponse({'temp_user': user_to_notify_1, 'final': final_text})
                        # return render(request, 'confirmation.html', {
                        #     'status': 'success',
                        #     'license_plate': final_text,
                        #     'booking': booking,
                        #     'message': 'Your car has been successfully identified'
                        # })
                        # return redirect('confirmationimage')  # Ensure this URL is correct and accessible

                elif active_booking:
                    save_license_plate_data(active_booking.license_plate)  #cache save rakhen
                    user_to_notify = active_booking.user
                    booking = active_booking
                    if user_to_notify and user_to_notify.is_authenticated:  # Ensure the user is logged in
                        print(f'User:{user_to_notify}')
                        print(f'reached inside auth active_booking_flex{final_text}')
                        active_booking.license_plate = final_text
                        active_booking.save()
                        user_to_notify_1 = user_to_notify.username
                        print({'temp_user': user_to_notify_1, 'final': final_text})

                        return JsonResponse({'temp_user': user_to_notify_1, 'final': final_text})
                        # return render(request, 'confirmation.html', {
                        #     'status': 'success',
                        #     'license_plate': final_text,
                        #     'booking': booking,
                        #     'message': 'Your car has been successfully identified'
                        # })
                    # return render(request, 'confirmation.html', {
                    #     'status': 'success',
                    #     'license_plate': final_text,
                    #     'booking': active_booking,
                    #     'message': 'Your car has been successfully identified'
                    # })
                elif active_booking1_flex:
                    user_to_notify = active_booking1_flex.user
                    booking = active_booking1_flex
                    if active_booking1_flex.license_plate == final_text:
                        return redirect(request.META.get('HTTP_REFERER') or '/')
                    else:
                        active_booking1_flex.end_time = current_time
                        active_booking1_flex.total_endtime = current_time
                        active_booking1_flex.status = 'End'
                        active_booking1_flex.save()
                        if user_to_notify and user_to_notify.is_authenticated:  # Ensure the user is logged in
                            print(f'User:{user_to_notify}')
                            print(f'reached inside auth active_booking_flex{final_text}')
                            user_to_notify_1 = user_to_notify.username
                            print({'temp_user': user_to_notify_1, 'final': final_text})

                            return JsonResponse({'temp_user': user_to_notify_1, 'finall': final_text})
                else:
                    return JsonResponse({'temp_user': user_to_notify_1, 'final': final_text})
            else:
                return JsonResponse({'status': 'error', 'message': 'No text found'})
        else:
            return JsonResponse({'temp_user': user_to_notify_1, 'final': final_text})
            # return JsonResponse({'status': 'error', 'message': 'No image uploaded', 'temp_user': 'none', 'final': 'none'})
    else:
        # if request.user == user_to_notify_1:
        #     return render(request, 'confirmation.html', {
        #                     'status': 'success',
        #                     'license_plate': final_text,
        #                     'message': 'Your car has been successfully identified'
        #                 })
        # print('helo')
        return JsonResponse({'temp_user': user_to_notify_1, 'final': final_text})
        # return JsonResponse({'status': 'error', 'message': 'No image uploaded', 'temp_user': 'none', 'final': 'none'})
    return JsonResponse({'temp_user': user_to_notify_1, 'final': final_text})

@csrf_exempt
@require_GET
def get_latest_license_plate(request):
    # Assuming you have a way to fetch the latest license plate data
    user = request.user
    current_time = datetime.now()
    active_booking = Booking.objects.filter(
                user=user, 
                selected_slot='Slot-1', 
                status='Pending..', 
                booking_type='fixed',
                start_time__lte=current_time, 
                end_time__gte=current_time
            ).first()
    active_booking_flex = Booking.objects.filter(
                    user=user, 
                    selected_slot='Slot-1', 
                    status='Pending..', 
                    booking_type='flexible',
                    start_time__lte=current_time, 
                    end_time=datetime.combine(datetime.today(), time(0, 0, 0)),
                ).first()
    active_booking_flex_end = Booking.objects.filter(
                    user=user, 
                    selected_slot='Slot-1', 
                    status='End', 
                    booking_type='flexible',
                    start_time__lte=current_time, 
                    # end_time=datetime.combine(datetime.today(), time(0, 0, 0)),
                ).first()
    if active_booking:

        latest_data = active_booking.license_plate  # Implement this function as needed
        if latest_data:
            return JsonResponse({'status': 'success', 'license_plate': latest_data})
    if active_booking_flex:

        latest_data = active_booking_flex.license_plate  # Implement this function as needed
        if latest_data:
            return JsonResponse({'status': 'success', 'license_plate': latest_data})
    if active_booking_flex_end:

        latest_data = ''  # Implement this function as needed
        print('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
        
        return JsonResponse({'status': 'ended', 'license_plate': latest_data})
    return JsonResponse({'status': 'error', 'message': 'No new data', 'license_plate': ''})


# @login_required
def confirmation_image(request):
    # Assuming you have a way to fetch the latest license plate data
    
    return render(request, 'confirmation.html')
@login_required
def finish_session(request):
    user = request.user
    current_time = datetime.now()
    active_booking_flex_end = Booking.objects.filter(
                    user=user, 
                    selected_slot='Slot-1', 
                    status='End', 
                    booking_type='flexible',
                    start_time__lte=current_time, 
                    # end_time=datetime.combine(datetime.today(), time(0, 0, 0)),
                ).first()
    active_booking_flex_end.status = 'Ended'
    active_booking_flex_end.save()
    return render(request, 'finish_session.html')

@login_required
def update_booking_status(request, status):
    # Assuming you have a way to fetch the latest license plate data
    user = request.user
    current_time = datetime.now()
    active_booking = Booking.objects.filter(
                user=user, 
                selected_slot='Slot-1', 
                status='Pending..', 
                booking_type='fixed',
                start_time__lte=current_time, 
                end_time__gte=current_time
            ).first()
    active_booking_flex = Booking.objects.filter(
                    user=user, 
                    selected_slot='Slot-1', 
                    status='Pending..', 
                    booking_type='flexible',
                    start_time__lte=current_time, 
                    end_time=datetime.combine(datetime.today(), time(0, 0, 0)),
                ).first()
    if active_booking and status == 'confirmed':
        active_booking.status = "Verified."
        # active_booking.license_plate = plate
        active_booking.save()
    if active_booking and status == 'cancel':
        # active_booking.status = "Verified."
        active_booking.license_plate = ''
        active_booking.save()
        # cache.set('latest_license_plate', '')
    if active_booking_flex and status == 'confirmed':
        active_booking_flex.status = "Verified."
        # active_booking_flex.license_plate = plate
        active_booking_flex.save()
    return redirect('book')

