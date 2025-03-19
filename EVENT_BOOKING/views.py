from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from . import models
from.models import Event
from.models import chef
from.models import feedback
from datetime import datetime
from django.core.mail import send_mail
from django.shortcuts import redirect
# from django.contrib.auth import logout
from django.urls import reverse

from.models import Owner
from.models import eventsupdates
from.models import Transaction
from.models import icart


# Create your views here.
def index(request):
    return render(request,'index.html')
def register(request):
    if request.method =='POST':
        image=request.FILES.get("image")
        name=request.POST.get("username")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        address=request.POST.get("address")
        password=request.POST.get("password")
        place=request.POST.get("place")
        if Event.objects.filter(email=email).exists():
            alert_message="<script>alert('Email already in use !! Please enter a valid Email'); window.location.href='/login';</script>"
            return HttpResponse(alert_message)
        # Event.objects.create(image=image, username=name, phone=phone, email=email, address=address, password=password, place=place)
        us=models.Event(image=image,username=name,phone=phone,email=email,address=address,password=password,place=place)
        us.save()
        return redirect('login')
    return render(request,'register.html')

def chefregister(request):
    if request.method =='POST':
        image=request.FILES.get("image")
        name=request.POST.get("username")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        address=request.POST.get("address")
        password=request.POST.get("password")
        place=request.POST.get("place")
        languages_spoken=request.POST.get("languages_spoken")
        experience=request.POST.get("experience")
        signature_dishes=request.POST.get("signature_dishes")
        service_area=request.POST.get("service_area")
        primary_cuisines=request.POST.get("primary_cuisines")
        services_offered=request.POST.get("services_offered")
        certifications=request.POST.get("certifications")
        work_hours_and_days=request.POST.get("work_hours_and_days")
        if chef.objects.filter(email=email).exists():
            alert_message="<script>alert('Email already in use !! Please enter a valid Email'); window.location.href='/chef_login';</script>"
            return HttpResponse(alert_message)
        # Event.objects.create(image=image, username=name, phone=phone, email=email, address=address, password=password, place=place)
        us=models.chef(image=image,username=name,phone=phone,email=email,address=address,password=password,place=place,languages_spoken=languages_spoken,experience=experience,signature_dishes=signature_dishes,service_area=service_area,primary_cuisines=primary_cuisines,services_offered=services_offered,certifications=certifications,work_hours_and_days=work_hours_and_days)
        us.save()
        return redirect('chef_login')
    return render(request,'chef_register.html')



def login(request):
    if request.method =='POST':
        email=request.POST.get("email")
        password=request.POST.get("password")
        us=Event.objects.get(email=email,password=password)
        if us:
            request.session['email']=us.email
            if us.status=='approved':
                request.session['email']=us.email
                return redirect('home')
            else:
                return render(request,'login.html',{'error':'your account is not yet approved.Please wait until the admin approves your registration.'})
        else:
            return render(request,'login.html',{'error':'Invalid email or password'})
    return render(request,'login.html')

def cheflogin(request):
    if request.method =='POST':
        email=request.POST.get("email")
        print(email)

        password=request.POST.get("password")
        print(password)
        us=chef.objects.get(email=email,password=password)
        if us:
            request.session['email']=us.email
            if us.status=='approved':
                request.session['email']=us.email
                return redirect('chefhome')
            else:
                return render(request,'chef_login.html',{'error':'your account is not yet approved.Please wait until the admin approves your registration.'})
        else:
            return render(request,'chef_login.html',{'error':'Invalid email or password'})
    return render(request,'chef_login.html')


def new(request):
    u = decorations.objects.all()
    
    # Get the email from the session
    email = request.session.get('email')

    user_type = None
    username = None

    if email:
        # Check if the user is an Event or Chef
        event_user = Event.objects.filter(email=email).first()
        chef_user = chef.objects.filter(email=email).first()

        if event_user:
            user_type = 'event'
            username = event_user.username
        elif chef_user:
            user_type = 'chef'
            username = chef_user.username

    return render(request, 'newhome.html', {
        'Event': u,
        'user_type': user_type,
        'username': username
    })


import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
def declist(request):
    u=decorations.objects.all()
    return render(request,'declist.html',{'Event':u})

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import decorations

def update_decoration(request, id):
    decoration = get_object_or_404(decorations, id=id)

    if request.method == 'POST':
        decoration.name = request.POST.get('name', decoration.name)
        decoration.description = request.POST.get('description', decoration.description)
        decoration.timeduration = request.POST.get('timeduration', decoration.timeduration)
        decoration.event = request.POST.get('event', decoration.event)
        decoration.amount = request.POST.get('amount', decoration.amount)

        if 'image' in request.FILES:
            decoration.image = request.FILES['image']

        decoration.save()
        return redirect('declist')

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def decorcart(request):
    email = request.session['email']
    cart_items = deccart.objects.filter(user__email=email)
    
    # Calculate total amount
    total_amount = sum(item.amount for item in cart_items)
    total_items = cart_items.count()
    
    # Use the API keys directly
    razorpay_key_id = 'rzp_test_X5OfG2jiWrAzSj'
    razorpay_key_secret = 'SsCovWWZSwB1TGd1rSoIiwF3'
    
    # Initialize Razorpay client
    client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))
    
    # Create order for the total amount (amount in paise)
    total_amount_paise = total_amount * 100
    order_data = {
        'amount': total_amount_paise,
        'currency': 'INR',
        'receipt': f'order_rcpt_{email}_{total_amount}'
    }
    
    try:
        order = client.order.create(data=order_data)
        order_id = order['id']
    except Exception as e:
        print(f"Razorpay order creation error: {str(e)}")
        order_id = None
    
    context = {
        'Event': cart_items,
        'total_items': total_items,

        'total_amount': total_amount,
        'total_amount_paise': total_amount_paise,
        'razorpay_key': razorpay_key_id,  # Use the direct variable
        'order_id': order_id
    }
    
    return render(request, 'carts.html', context)

# New view to handle buying all decorations
@csrf_exempt
@csrf_exempt
def buy_all_decorations(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        
        # Verify payment with Razorpay
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        try:
            # Fetch payment details
            payment = client.payment.fetch(payment_id)
            
            if payment['status'] == 'captured':
                # Get cart items
                email = request.session['email']
                user = Event.objects.filter(email=email)
                cart_items = deccart.objects.filter(user__email=email)
                
                # Create transaction records for each cart item
                for cart_item in cart_items:
                    # Create transaction record
                    transaction = decorationtransaction.objects.create(
                        cart=user,
                        razorpay_order_id=order_id,
                        razorpay_payment_id=payment_id,
                        amount=cart_item.amount,
                        status='Paid'
                    )
                
                # Delete all cart items after saving transactions
                cart_items.delete()
                
                # Redirect to success page
                return redirect('carts')
            else:
                # Payment failed
                return redirect('payment_failed')
        
        except Exception as e:
            # Handle error
            print(f"Payment processing error: {str(e)}")
            return redirect('payment_failed')
    
    # If not POST request, redirect to cart
    return redirect('carts')

# Add these views if you don't have them already
def payment_success(request):
    return render(request, 'payment_success.html')

def payment_failed(request):
    return render(request, 'payment_failed.html')
def userlist(request):
    u=Event.objects.all()
    return render(request,'userlist.html',{'Event':u})

def Owner_list(request):
    u=Event.objects.all()
    return render(request,'Owner_list.html',{'Event':u})

def decoration_detail(request, pk):
    decoration = get_object_or_404(decorations, pk=pk)
    return render(request, 'decoration_detail.html', {'decoration': decoration})

def delete_decoration(request, id):
    decoration = get_object_or_404(decorations, id=id)

    if request.method == 'POST':
        decoration.delete()
        return redirect('declist')

    return redirect('declist')


def chefdatabase(request):
    u=chef.objects.all()
    return render(request,'chefdb.html',{'chef':u})

def deleteuser(request,id):
    d=Event.objects.get(id=id)
    d.delete()
    return redirect('userlist')

def deleteowner(request,id):
    d=models.Owner.objects.get(id=id)
    d.delete()
    return redirect('Owner_list')

def deletechefuser(request,id):
    d=chef.objects.get(id=id)
    d.delete()
    return redirect('chefdb')

def userprofile(request):

    email=request.session['email']
    cr=Event.objects.get(email=email)
    image=cr.image
    username=cr.username
    phone=cr.phone
    email=cr.email
    address=cr.address
    password=cr.password
    place=cr.place
    return render(request,'profile.html',{'image':image,'username':username,'phone':phone,'email':email,'address':address,'password':password,'place':place})

def owner_profile(request):

    email=request.session['email']
    cr=Event.objects.get(email=email)
    image=cr.image
    username=cr.username
    phone=cr.phone
    email=cr.email
    address=cr.address
    password=cr.password
    place=cr.place

    return render(request,'owner_profile.html',{'image':image,'username':username,'phone':phone,'email':email,'address':address,'password':password,'place':place})

def delete_decoration(request, id):
    decoration = get_object_or_404(decorations, id=id)

    if request.method == 'POST':
        decoration.delete()
        return redirect('declist')

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def chefprofile(request):

    email=request.session['email']
    cr=chef.objects.get(email=email)
    image=cr.image
    username=cr.username
    phone=cr.phone
    email=cr.email
    address=cr.address
    password=cr.password
    place=cr.place
    languages_spoken=cr.languages_spoken
    experience=cr.experience
    signature_dishes=cr.signature_dishes
    service_area=cr.service_area
    primary_cuisines=cr.primary_cuisines
    services_offered=cr.services_offered
    certifications=cr.certifications
    work_hours_and_days=cr.work_hours_and_days

    return render(request,'chef_profile.html',{'image':image,'username':username,'phone':phone,'email':email,'address':address,'password':password,'place':place,"languages_spoken":languages_spoken,"experience":experience,"signature_dishes":signature_dishes,"service_area":service_area,"primary_cuisines":primary_cuisines,"services_offered":services_offered,"certifications":certifications,"work_hours_and_days":work_hours_and_days})


def selection(request):
    if request.method =='POST':
        Event_name=request.POST.get("Event_name")
        Date=request.POST.get("Date")
        Time=request.POST.get("Time")
        Location=request.POST.get("Location")
        No_of_members=request.POST.get("No_of_members")
        Duration=request.POST.get("Duration")
        Event_organizer=request.POST.get("Event_organizer")
        Additional_requirements=request.POST.get("Additional_requirements")
        us=models.Event_selection(Event_name=Event_name,Date=Date,Time=Time,Location=Location,No_of_members=No_of_members,Duration=Duration,Event_organizer=Event_organizer,Additional_requirements=Additional_requirements)
        us.save()
        return redirect('adminhome')
    return render(request,'selection.html')

def update_profile(request):
    email = request.session['email']
    try:
        cr = Event.objects.get(email=email)
        user_info = {
            'username': cr.username,
            'phone': cr.phone,
            'email': cr.email,
            'address': cr.address,
            'password':cr.password,
            'place': cr.place,
            'image': cr.image.url if cr.image else None,  # Add image URL if it exists
        }
        return render(request, 'update_profile.html', user_info)
    except Event.DoesNotExist:
        return render(request, 'update_profile.html')
    
def chef_update(request):
    email = request.session['email']
    try:
        cr = chef.objects.get(email=email)
        user_info = {
            'username': cr.username,
            'phone': cr.phone,
            'email': cr.email,
            'address': cr.address,
            'password':cr.password,
            'place': cr.place,
            'languages_spoken':cr.languages_spoken,
            'experience':cr.experience,
            'signature_dishes':cr.signature_dishes,
            'service_area':cr.service_area,
            'primary_cuisines':cr.primary_cuisines,
            'services_offered':cr.services_offered,
            'certifications':cr.certifications,
            'work_hours_and_days':cr.work_hours_and_days,
            'image': cr.image.url if cr.image else None,  # Add image URL if it exists
        }
        return render(request, 'chef_update.html', user_info)
    except chef.DoesNotExist:
        return render(request, 'chef_update.html')

def update_pro(request):
    email = request.session['email']
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password = request.POST.get('password')
        place = request.POST.get('place')
        image = request.FILES.get('image')  # Get the uploaded image file

        try:
            data = Event.objects.get(email=email)
            data.username = username
            data.phone = phone
            data.email = email
            data.address = address
            data.password = password
            data.place = place
            
            if image:  # Check if an image is uploaded
                data.image = image
            
            data.save()
            # Redirect to the profile update page or any success page
            return userprofile(request)  # Re-render with updated information

        except Event.DoesNotExist:
            return render(request, 'update_profile.html')

    return render(request, 'update_profile.html')

def chefupdate_pro(request):
    email = request.session.get('email')

    if not email:
        messages.error(request, "You need to be logged in to update your profile.")
        return redirect('chef_login')  # Redirect to login if no session email is found

    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password = request.POST.get('password')
        place = request.POST.get('place')
        languages_spoken = request.POST.get('languages_spoken') # Get the uploaded image file
        experience = request.POST.get('experience')
        signature_dishes = request.POST.get('signature_dishes')
        service_area = request.POST.get('service_area')
        primary_cuisines = request.POST.get('primary_cuisines')
        services_offered = request.POST.get('services_offered')
        certifications = request.POST.get('certifications') 
        work_hours_and_days = request.POST.get('work_hours_and_days')
        image = request.POST.get('image')

        try:
            data = chef.objects.get(email=email)
            data.username = username
            data.phone = phone
            data.email = email
            data.address = address
            data.password = password
            data.place = place
            data.languages_spoken = languages_spoken
            data.experience = experience
            data.signature_dishes = signature_dishes
            data.service_area = service_area
            data.primary_cuisines = primary_cuisines
            data.services_offered = services_offered
            data.certifications = certifications
            data.work_hours_and_days = work_hours_and_days
            data.image = image # Check if an image is uploaded

            
            data.save()
            # Redirect to the profile update page or any success page
            return redirect('chef_profile')  # Re-render with updated information

        except chef.DoesNotExist:
            return render(request, 'chef_update.html')

    return render(request, 'chef_update.html')

def adminhome(request):
    return render(request,'adminhome.html')

def feedback_view(request):
    if request.method == "POST":
        feedback_text = request.POST.get('feedback_text')
        rating = request.POST.get('rating')
        
        if not feedback_text or not rating:
            # Handle missing fields
            alert_message = "<script>alert('Please fill in all required fields.'); window.location.href='/feedback_rate';</script>"
            return HttpResponse(alert_message)
        
        try:
            rating = int(rating)
            if rating not in [1, 2, 3, 4, 5]:
                raise ValueError("Invalid rating value")
        except (ValueError, TypeError):
            # Handle invalid rating
            alert_message = "<script>alert('Invalid rating value. Please select a valid rating.'); window.location.href='/feedback_rate';</script>"
            return HttpResponse(alert_message)

        # Create and save the Feedback instance
        feedbacks = feedback(
            feedback_text=feedback_text,
            rating=rating
        )
        feedbacks.save()

        # Redirect to a success page
        return redirect('feedback_success')
    
    else:
        # Render the feedback form
        return render(request, 'feedback_rate.html')
    
def feedback_success(request):
    return render(request, 'feedback_success.html')

def feedbacklist(request):
    u=feedback.objects.all()
    return render(request,'feedbacklist.html',{'Event':u})

def deletefeedback(request,id):
    d=feedback.objects.get(id=id)
    d.delete()
    return redirect('feedbacklist')

# def selectionlist(request):
#     u=Event_selection.objects.all()
#     return render(request,'selectionlist.html',{'Event':u})

# def deleteselection(request,id):
#     d=Event_selection.objects.get(id=id)
#     d.delete()
#     return redirect('selectionlist')
    




def Owner_login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            # Check if the Owner exists with the given email and password
            us = models.Owner.objects.get(email=email, password=password)
            # Set session data if user exists
            request.session['email'] = us.email
            return redirect('Owner_list')
        except models.Owner.DoesNotExist:
            # Handle case where no user is found
            messages.error(request, "Invalid email or password.")
            return redirect('owner_home')
    return render(request, 'Owner_login.html')

def Owner_register(request):
    if request.method =='POST':
        name=request.POST.get("username")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        address=request.POST.get("address")
        password=request.POST.get("password")
        place=request.POST.get("place")
        if Owner.objects.filter(email=email).exists():
            alert_message="<script>alert('Email already in use !! Please enter a valid Email'); window.location.href='/Owner_register';</script>"
            return HttpResponse(alert_message)
        
        us=models.Owner(username=name,phone=phone,email=email,address=address,password=password,place=place).save()
        return redirect('Owner_login')
    return render(request,'Owner_register.html')

def Owner_list(request):
    u=models.Owner.objects.all()
    return render(request,'Owner_list.html',{'u':u})


def admin_dash(request):
    return render(request,'admin_dashboard.html')

def update_status(request):
    if request.method=='POST':
        email=request.POST.get("email")
        status=request.POST.get("status")
        if not email or not status:
            return redirect('userlist')
        if status not in ['applied','approved','rejected']:
            return redirect('userlist')
        constr=get_object_or_404(Event,email=email)
        constr.status=status
        constr.save()
        return redirect(userlist)
    return render(request,'userlist.html')


def chef_status(request):
    if request.method=='POST':
        email=request.POST.get("email")
        status=request.POST.get("status")
        if not email or not status:
            return redirect('chefdb')
        if status not in ['applied','approved','rejected']:
            return redirect('chefdb')
        constr=get_object_or_404(chef,email=email)
        constr.status=status
        constr.save()
        return redirect('chefdb')
    return render(request,'chefdb.html')


def category(request):
    if request.method =='POST':
        Weddings=request.FILES.get("Weddings")
        Birthdays=request.POST.get("Birthdays")
        Anniversary=request.POST.get("Anniversary")
        Family_Gathering=request.POST.get("Family_Gathering")
        Babyshower=request.POST.get("Babyshower")
        Baptism=request.POST.get("Baptism")
        Holiday_Parties=request.POST.get("Holiday_Parties")
        Graduation=request.POST.get("Graduation")
        Retirement=request.POST.get("Retirement")
        Reunion=request.POST.get("Reunion")
        us=models.category(Weddings=Weddings,Birthdays=Birthdays,Anniversary=Anniversary,Family_Gathering=Family_Gathering,Babyshower=Babyshower,Baptism=Baptism,Holiday_Parties=Holiday_Parties,Graduation=Graduation,Retirement=Retirement,Reunion=Reunion)
        us.save()
    return render(request,'register.html')


def logout(request):
    request.session.flush()
    return redirect('index')


def adminlogin(request):

    admin_username = 'admin'
    admin_password = 'password123'

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == admin_username and password == admin_password:
            request.session['admin'] = username
            return redirect('admin_dashboard')
        else:
            
            return render(request, 'adminlogin.html', {'error': 'Invalid username or password'})

    return render(request, 'adminlogin.html')

def chefpage(request):
    return render(request,'chefhome.html')

# from datetime import datetime
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib import messages
# from .models import eventsupdates, icart, Event  # Ensure your models are correctly imported

def chefbookingform(request, chef_id):
    email = request.session.get('email')
    
    # Ensure we get the correct user
    chefd = get_object_or_404(Event, email=email)

    # Get chef event
    chef_event = get_object_or_404(eventsupdates, id=chef_id)

    if request.method == 'POST':
        print("✅ POST request received!")
        event_time = request.POST.get('event_time')
        location = request.POST.get('location')
        quantity = request.POST.get('quantity')
        start_date = request.POST.get('start')
        end_date = request.POST.get('end')
        total_price = request.POST.get('total_price')  # Get total price from form

        # Ensure total_price is a valid number before saving
        try:
            total_price = float(total_price)
        except (TypeError, ValueError):
            messages.error(request, "Invalid total price value. Please try again.")
            return redirect('chefbookingform', chef_id=chef_id)

        # Save booking details in the cart
        chef_booking, created = icart.objects.get_or_create(
            user=chefd,
            products=chef_event,
            defaults={
                'location': location,
                'quantity': quantity,
                'event_time': event_time,
                'start': start_date,
                'end': end_date,
                'total_price': total_price,
                'status': 'Pending',
            }
        )

        if not created:
            chef_booking.start = start_date
            chef_booking.end = end_date
            chef_booking.total_price = total_price
            chef_booking.status = 'Pending'
            chef_booking.save()

        messages.success(request, f'Chef booked successfully and added to cart! Total: ${total_price}')
        return redirect('chef_carts')

    return render(request, 'chefbookingform.html', {'chef_event': chef_event, 'chefd': chefd})

from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from django.core.exceptions import ValidationError

def Chefrecipe(request):
    if request.method == 'POST':
        chefname = request.POST.get("chefname")
        profile = request.POST.get("profile")
        image = request.FILES.get("image")  
        video = request.FILES.get("video")  
        name = request.POST.get("name")
        specializations = request.POST.get("specializations")
        description = request.POST.get("description")
        try:
            us = models.Chefrecipe(
                chefname=chefname,
                profile=profile,
                image=image,
                name=name,
                specializations=specializations,
                description=description,
                video=video
            )
            us.save()  
            alert = "<script>alert('Recipe added successfully!');window.location.href='/chefhome/';</script>"
            return HttpResponse(alert)
        
        except ValidationError as e:
            alert = f"<script>alert('Error: {e.message}');window.location.href='/chefhome/';</script>"
            return HttpResponse(alert)
    else:
        return render(request, 'chefrecipe.html')


def viewrecipe(request):
    uf=models.Chefrecipe.objects.all()
    return render(request,'viewrecipe.html',{'ae':uf})


from django.shortcuts import render, redirect
from . import models

def addevents(request):
    chefs = models.chef.objects.all()  # Get all chefs for dropdown

    if request.method == 'POST':
        category = request.POST.get('category')
        packagename = request.POST.get('packagename')
        chefname = request.POST.get('packagename')
        chefimage = request.FILES.get('image')
        image = request.FILES.get('image')
        details = request.POST.get('details')
        eventdate = request.POST.get('eventdate')
        enddate = request.POST.get('eventdate')
        amount = request.POST.get('amount')
        package = request.POST.get('package')
        chef_id = request.POST.get('chef_id')  # Get chef_id from form input

        # Fetch the selected chef instance
        chef_instance = models.chef.objects.get(id=chef_id) if chef_id else None

        # Save event details
        data = models.eventsupdates(
            category=category,
            packagename=packagename,
            chefname=chefname,
            chefimage=chefimage,
            image=image,
            details=details,
            fromdate=eventdate,
            todate=enddate,
            rentperday=amount,
            package=package,
            chef=chef_instance  # Assign chef instance
        )
        data.save()
        return redirect('chefhome')

    return render(request, 'organizereventcreate.html', {'chefs': chefs})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import eventsupdates  # Import your model

def delete_package(request, package_id):
    package = get_object_or_404(eventsupdates, id=package_id)
    
    if request.method == "POST":
        package.delete()
        messages.success(request, "Package deleted successfully!")
        return redirect('chefcard')  # Redirect to package list page
    
    return redirect('chefcard')  # Fallback redirect

def list(request):
    var=models.eventsupdates.objects.all()
    return render(request, 'chefcard.html', {'chefs': var})



from decimal import Decimal


def add_cart(request,pid):
    if 'email' in request.session:
        email=request.session.get('email')
        us=Event.objects.get(email=email)
        products=eventsupdates.objects.get(id=pid)
        
        

        if request.method == "POST":
            quantity = request.POST.get('quantity')
            quantity=int(quantity)
            total_price = Decimal(request.POST.get('total'))
            start = request.POST.get('start')
            end = request.POST.get('end')
            cart_item,created=icart.objects.get_or_create(user=us,products=products,defaults={'quantity':quantity,'total_price':total_price,'start': start, 'end': end} )
            if not created:
                cart_item.quantity = quantity
                cart_item.total_price=total_price
                cart_item.start=start
                cart_item.end=end
                cart_item.save()

                return redirect('cart_list')
            return redirect('cart_list')
            
        
        else:
            return render(request,'cart.html',{'prd':products})
    else:
        return redirect('login')
    
# from django.contrib.auth import logout
import razorpay # type: ignore
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.conf import settings
# from razorpay.errors import BadRequestError
from django.views.decorators.csrf import csrf_exempt

# from razorpay.errors import BadRequestError
from django.views.decorators.csrf import csrf_exempt







def initiate_payment(request,id):
    email = request.session['email']
    if email:
        crt=icart.objects.get(id=id)
        am=crt.total_price
        amount = int(am)*100 
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment_order = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        order_id = payment_order['id']
        juser = Event.objects.get(email=email)
        buyer_data = {
            'buyer': {
                'id': juser.id,
                'name': juser.username,
                'email': juser.email,
                'phone': juser.phone,
                # Add other fields as needed
            }
        }
        response_data = {'order_id': order_id, 'amount': amount}
        response_data.update(buyer_data)
        return JsonResponse(response_data, encoder=DjangoJSONEncoder)
    else:
        return redirect('log')
    

@csrf_exempt
def confirm_payment(request, order_id, payment_id, crti_id):
    try:
        # Get session email instead of relying on payment data
        email = request.session.get('email')
        if not email:
            return redirect('log')
            
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment = client.payment.fetch(payment_id)
        
        if payment['order_id'] == order_id and payment['status'] == 'captured':
            # Get user and cart item
            user = Event.objects.get(email=email)
            cart_item = icart.objects.get(id=crti_id)
            
            # Create transaction record
            trns = Transaction(
                user=user,
                products=cart_item.products,
                amount=cart_item.total_price,
                quantity=cart_item.quantity,
                order_id=order_id
            )
            trns.save()
            
            # Get chef data
            chef = cart_item.products.chef
            
            # Send email notification
            try:
                send_mail(
                    subject='Your Chef Appointment Details',
                    message=(
                        f"Hello {chef.username},\n\n"
                        f"Your appointment has been approved. Here are the details:\n"
                        f"Date: {cart_item.start} to {cart_item.end} \n"
                        f"Amount: {cart_item.total_price}\n"
                        f"User: {user.username}\n\n"
                        "Thank you for choosing our services."
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[chef.email],
                    fail_silently=False
                )
                
                # Also send confirmation to customer
                send_mail(
                    subject='Your Chef Booking Confirmation',
                    message=(
                        f"Hello {user.username},\n\n"
                        f"Your chef booking has been confirmed. Here are the details:\n"
                        f"Chef: {chef.username}\n"
                        f"Date: {cart_item.start} to {cart_item.end} \n"
                        f"Amount: {cart_item.total_price}\n\n"
                        "Thank you for choosing our services."
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False
                )
            except Exception as e:
                print(f"Email error: {e}")
            
            # Remove item from cart after successful purchase
            cart_item.delete()
            
            # Redirect to success page instead of using alert
            return redirect('home')
        else:
            return redirect('home')
    except Exception as e:
        print(f"Payment confirmation error: {e}")
        return redirect('payment_failed')
    
def chef_carts(request):
    email = request.session['email']
    user = Event.objects.get(email=email)
    cart_items = icart.objects.filter(user=user)  # Filter cart items by logged-in user
    return render(request, 'chef_carts.html', {'cart_items': cart_items})

def chef_carts(request):
    # Your cart logic here
    return render(request, 'chef_carts.html')


# View to display details of a specific cart item

# def chef_cart_detail(request, pk):
#     cart_item = get_object_or_404(icart, pk=pk, user=request.user)  # Ensure only the user's item is retrieved
#     return render(request, 'cart_detail.html', {'cart_item': cart_item})    


def cart_list(request):
    # Fetch the user's cart items
    if 'email' in request.session:
        email = request.session['email']
        juser = Event.objects.get(email=email)
        cart_items = icart.objects.filter(user=juser)

        return render(request, 'cart_list.html', {'cart_items': cart_items})
    else:
        return redirect('login')




from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Utensilsform
from django.views.decorators.csrf import csrf_exempt

# Price constants
UTENSIL_PRIC = {
    'Serving Utensils': 1000,
    'Specialty Tools': 100,
    'Plates and Bowls': 100,
    'Cutlery Sets': 10
}

def calculate_amount(utensil_selections):

    """Calculate total amount based on selected utensils and their quantities"""
    total = 0
    for utensil, quantity in utensil_selections.items():
        # Get price for the utensil type
        price = UTENSIL_PRIC.get(utensil, 0)
        total += price * int(quantity)
        print("hi",total)
    return total

@csrf_exempt
def utensils(request):
    email=request.session.get('email')
    us=Event.objects.get(email=email)
    print(us)
    if request.method == 'POST':
        try:
            # Process utensil selections
            selected_utensils = {}
            for key in request.POST:
                if key.startswith('Quantity_'):
                    utensil_name = key.replace('Quantity_', '')
                    quantity = request.POST.get(key)
                    if quantity and int(quantity) > 0:
                        selected_utensils[utensil_name] = int(quantity)
                        
            
            # Calculate total amount
            total_amount = calculate_amount(selected_utensils)
         
            # Create the rental object
            rental = Utensilsform.objects.create(
                name=request.POST.get("Name"),
                phone=request.POST.get("Phone"),
                user=us,
                address=request.POST.get("Address"),
                date=request.POST.get("Date"),
                rdate=request.POST.get("RDate"),
                time=request.POST.get("Time"),
                amount=total_amount  # Save calculated amount
            )
            rental.selected_utensils = selected_utensils
            rental.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Rental request submitted successfully',
                'amount': total_amount
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
        
    
    return render(request, 'utensils.html')


def utensils_list(request):
    # Fetch the user's cart items
    if 'email' in request.session:
        
        email = request.session['email']
        juser = Event.objects.get(email=email)
        cart_items = Utensilsform.objects.filter(user=juser)

        return render(request, 'utensils_list.html', {'cart_items': cart_items})
    else:
        return redirect('decorcart')


    

import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def create_order(request):
    if request.method == "POST":
        amount = int(request.POST.get("amount")) * 100  # Convert to paise
        order_data = {
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1",
        }
        order = client.order.create(order_data)
        return JsonResponse(order)  # Send order details to frontend
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Payment, Utensilsform

@csrf_exempt
def save_payment(request):
    email = request.session['email']
    juser = Event.objects.get(email=email)
    if request.method == "POST":
        data = json.loads(request.body)
        utensil_id = data.get("utensil_id")  # Get utensil ID from request
        
        try:
            utensi = Utensilsform.objects.get(id=utensil_id)
            utensi.status='paid'
            utensi.save()
            payment = Payment.objects.create(
                user=juser,
                payment_id=data["payment_id"],
                amount=data["amount"],  # Convert paise to rupees
                 # Convert paise to rupees
                status="Completed",
                utensils=utensi
            )
            try:

            # Update appointment details
                    if email:
                        # Send email notification
                        send_mail(
                            subject='Your utensil Details',
                            message=(
                                f"Hello admin ,\n\n"
                                f"You have an utensil update:\n"
                                f"Date: {utensi.date} to {utensi.rdate} \n"
                                f"Amount: {utensi.amount}\n"
                                f"utensils: {utensi.selected_utensils}\n"
                                f"user: {juser.username}\n\n"
                                "Thank you for choosing our services."
                            ),
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=['elnafracis11@gmail.com'],
                            
                        )
                        
                        return JsonResponse({"status": "success"})
            except Exception as e:
                    print(e)
             # Link utensil to payment
            return JsonResponse({"status": "success"})
        except Utensilsform.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invalid utensil ID"}, status=400)






from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, chef, ChatMessage

def chat_list(request):
    cheffs = chef.objects.all()
    events = Event.objects.all()
    return render(request, 'chat_list.html', {'cheffs': cheffs, 'events': events})





def chat_detail(request, user_type, username):
    sender_email = request.session.get('email')
    print('erf',sender_email)  # Assuming email is stored in the session

    if not sender_email:
        return redirect('login')  # Redirect to login if email is not in session

    # Determine the sender user type (Artist or Buyer)
    sender = None
    if Event.objects.filter(email=sender_email).exists():
        sender = Event.objects.get(email=sender_email)
    elif chef.objects.filter(email=sender_email).exists():
        sender = chef.objects.get(email=sender_email)

    if not sender:
        return redirect('login')  # Redirect if sender cannot be identified

    # Determine the receiver
    if user_type == 'event':
        receiver = get_object_or_404(Event, username=username)
    else:
        receiver = get_object_or_404(chef, username=username)
    print(f"Sender: {sender.username}, Receiver: {receiver.username}")
    print(f"URL username parameter: {username}")
    print(f"Sender detected from session: {sender.username}")


    # Fetch chat messages between the sender and receiver
    messages = ChatMessage.objects.filter(
        sender__in=[sender.username, username],
        receiver__in=[sender.username, username]
    ).order_by('timestamp')

    # Handle sending a message
    if request.method == 'POST':
        content = request.POST.get('content')
        media = request.FILES.get('media')  # Fetch the media file from the form

        if content.strip() or media:
            # Create a new chat message
            ChatMessage.objects.create(
                sender=sender.username,
                receiver=username,
                content=content,
                media=media if media else None
            )

            # Add a notification for the sender (pop-up message after sending)
            notification = "Message sent successfully!"

            # Redirect back to the chat without passing notification in the URL
            return redirect('chat_detail', user_type=user_type, username=username)
        if not username:
            return redirect('home')  # Redirect to a safe page if username is missing

    # Process media types for display
    for message in messages:
        if message.media:
            if message.media.name.endswith(('.jpg', '.jpeg', '.png')):
                message.media_type = 'image'
            elif message.media.name.endswith(('.mp4', '.avi', '.mov')):
                message.media_type = 'video'
            else:
                message.media_type = 'unknown'

    return render(request, 'chat_detail.html', {
        'receiver': receiver,
        'messages': messages,
        'sender': sender,
        'notification': "Message sent successfully!" if 'notification' in request.GET else '',
    })




from django.shortcuts import get_object_or_404, redirect
from .models import ChatMessage

def delete_message(request, message_id):
    message = get_object_or_404(ChatMessage, id=message_id)

    # Ensure that the sender is the user who is trying to delete
    if message.sender == request.user.username:
        message.delete()
        # Optional: Add a notification after successful deletion
        return redirect('chat_detail', user_type='cheff', username=message.receiver.username, notification="Message deleted successfully!")

    # If not the sender, redirect with a failure message or simply an error
    return redirect('chat_detail', user_type='cheff', username=message.receiver.username, notification="You can only delete your own messages!")

def myutensilslist(request):
    email = request.session['email']
    u=Utensilsform.objects.filter(user__email=email)
    return render(request,'myutensilslist.html',{'Event':u})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Utensilsform
from django.http import Http404

def edit_utensils(request, utensil_id):
    # Get the utensil object based on the ID and make sure the user owns it
    utensil = get_object_or_404(Utensilsform, id=utensil_id, user__email=request.session['email'])

    if request.method == 'POST':
        # Manually updating the fields from the request.POST
        utensil.name = request.POST.get('name', utensil.name)
        utensil.phone = request.POST.get('phone', utensil.phone)
        utensil.address = request.POST.get('address', utensil.address)
        utensil.date = request.POST.get('date', utensil.date)
        utensil.rdate = request.POST.get('rdate', utensil.rdate)
        utensil.time = request.POST.get('time', utensil.time)
        utensil.amount = request.POST.get('amount', utensil.amount)

        # Handle the selected utensils as a JSON object (ensure to save the updated data as a JSON field)
        selected_utensils = request.POST.getlist('selected_utensils')
        utensil.selected_utensils = {key: value for key, value in zip(selected_utensils, selected_utensils)}

        # Save the updated object
        utensil.save()

        # Redirect after saving
        return redirect('myutensilslist')  # Redirect to the list page after saving
    else:
        # If it's a GET request, just display the existing data in the form
        return render(request, 'edit_utensils.html', {'utensil': utensil})
    
    from django.shortcuts import render, redirect, get_object_or_404
from .models import Utensilsform

def delete_utensils(request, utensil_id):
    # Get the utensil object based on the ID and make sure the user owns it
    utensil = get_object_or_404(Utensilsform, id=utensil_id, user__email=request.session['email'])
    
    if request.method == 'POST':
        # Delete the utensil
        utensil.delete()
        return redirect('myutensilslist')  # Redirect to the list page after deletion

    # If it's not a POST request, simply redirect or show a confirmation page
    return redirect('myutensilslist')
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Payment, refund

def mytransutensilslist(request):
    email = request.session['email']
    
    # Get all payments for the user
    payments = Payment.objects.filter(user__email=email)

    # Check if a refund has been requested for each payment
    for payment in payments:
        # Check if any refund request exists with 'Pending' status
        payment.refund_requested = refund.objects.filter(transact=payment, status='Pending').exists()
    
    # Pass payments and refund status to the template
    return render(request, 'mytransutensilslist.html', {'Event': payments})

# def mytransutensilslist(request):
#     email = request.session['email']
    
#     # Get all payments for the user
#     payments = chef.objects.filter(user__email=email)

#     # Check if a refund has been requested for each payment
#     for payment in payments:
#         # Check if any refund request exists with 'Pending' status
#         payment.refund_requested = refund.objects.filter(transact=payment, status='Pending').exists()
    
#     # Pass payments and refund status to the template
#     return render(request, 'mytransutensilslist.html', {'Event': payments})




from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Payment, refund

# View for handling refund submission
def request_refund(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        refund_reason = request.POST.get('refund_reason')
        
        # Get the payment object based on the payment_id
        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            return HttpResponse("Payment not found", status=404)

        # Check if a refund has already been requested for this payment
        if refund.objects.filter(transact=payment, status='Pending').exists():
            return HttpResponse("Refund has already been requested for this payment.", status=400)

        # Create a new refund request
        refnd = refund.objects.create(
            transact=payment,
            refdes=refund_reason,
            status='Pending'
        )

        # Optionally, you can update the payment status to "Refund Requested"
        payment.status = 'Refund Requested'
        payment.save()

        # Redirect to the same page or a confirmation page
        return redirect('mytransutensilslist')  # Replace with the correct URL for your view
    return HttpResponse("Invalid request", status=400)


def refreq(request):
    payments=refund.objects.all()
    return render(request, 'ref.html', {'Event': payments})
    
import razorpay
from django.shortcuts import render, redirect
from django.conf import settings
from .models import refund, Paymentd

import razorpay
from django.shortcuts import render, redirect
from django.conf import settings
from .models import refund, Paymentd

def approve_refund(request, refund_id):
    # # Initialize Razorpay client
    email = request.session['email']

    if not email:
        return HttpResponse("email not found in session.", status=400)
    
    # Get all payments for the user
    userd = Event.objects.filter(email=email)
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    
    # Get the refund object
    refun = refund.objects.get(transact=refund_id)
    refunds = Payment.objects.get(id=refund_id)
    refunds.status='refund'
    refunds.save()
    hlo=refunds.status
    refun.status='refund'
    refun.save()
    print(hlo)
    
    # Calculate the payment amount (convert Decimal to integer paise)
    amount = int(refun.transact.amount * 100)  # Convert to paise (integer)
    
    # Create a Razorpay order
    order_data = {
        'amount': amount,  # Amount in paise (integer)
        'currency': 'INR',
        'payment_capture': '1'  # Automatic capture
    }
    
    order = client.order.create(data=order_data)
    
    # Save the payment transaction in the database
    payment = Paymentd.objects.create(
        user=refun.transact.user,  # Associate with the user of the refund
        payment_id=order['id'],  # Save Razorpay order ID
        amount=refun.transact.amount,  # Save original amount (Decimal)
        status='Pending',  # Initially set to Pending
    )
    
    # Redirect to the frontend to complete the payment
    return redirect(f'/payment/{payment.payment_id}/')



def reject_refund(request, refund_id):
    refun = get_object_or_404(refund, id=refund_id)
    refun.status = 'Rejected'  # Set status to 'Rejected'
    refun.save()
    return redirect('refreq')  # Redirect to the refund list page


from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import Paymentd

def payment_success(request, order_id, payment_id):
    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

    try:
        # Verify the payment by checking the payment status
        payment = client.payment.fetch(payment_id)
        if payment['status'] == 'captured':
            # Update the payment status in the database
            payment_record = Paymentd.objects.get(payment_id=order_id)
            payment_record.status = 'refund'  # Set status to Completed
            payment_record.save()
            return JsonResponse({'message': 'Payment successful!'})
        else:
            return JsonResponse({'error': 'Payment failed!'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
from django.shortcuts import render, get_object_or_404
from .models import Paymentd

def payment_page(request, payment_id):
    # Fetch the payment record from the database
    payment = get_object_or_404(Paymentd, payment_id=payment_id)

    # Convert amount to paise (integer) in the view
    amount_in_paise = int(payment.amount * 100)  # Convert to paise

    # Pass the Razorpay key, payment details, and the calculated amount to the template
    context = {
        'RAZOR_KEY_ID': settings.RAZOR_KEY_ID,
        'payment': payment,
        'amount_in_paise': amount_in_paise,  # Pass the calculated amount
    }
    
    return render(request, 'payment.html', context)



from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import decorations

def createdecoration(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        timeduration = request.POST.get('timeduration', None)
        event = request.POST.get('event', None)
        amount = request.POST.get('amount', None)

        # Collect selected utensils
        selected_utensils = {
            'chair': request.POST.get('chair', 0),
            'table': request.POST.get('table', 0),
            'light': request.POST.get('light', 0),
            'generator': request.POST.get('generator', 0)
        }

        # Handle image upload if present
        image = request.FILES.get('image', None)
        
        # Create the decoration object
        decorations.objects.create(
            name=name,
            timeduration=timeduration,
            event=event,
            amount=amount,
            selected_utensils=selected_utensils,
            image=image
        )

        # Redirect or send success response
        return redirect('home')
    
    return render(request, 'createdecoration.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import decorations, deccart
from django.contrib import messages

UTENSIL_PRICES = {
    'chair': 80,
    'table': 80,
    'light': 90,
    'generator': 90
}


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Event, decorations, deccart

def book_decoration(request, decoration_id):
    email = request.session['email']
    usrd = get_object_or_404(Event, email=email)
    decoration = get_object_or_404(decorations, id=decoration_id)

    if request.method == 'POST':
        date = request.POST.get('date')
        rdate = request.POST.get('rdate')
        time = request.POST.get('time')

        # Calculate extra utensils cost
        selected_utensils = {}
        total_amount = decoration.amount

        for utensil, price in UTENSIL_PRICES.items():
            quantity = request.POST.get(f"Quantity_{utensil}")
            if quantity:
                quantity = int(quantity)
                selected_utensils[utensil] = quantity
                total_amount += price * quantity

        # Check if booking already exists for this user and decoration
        deccart_item, created = deccart.objects.get_or_create(
            user=usrd,
            decoration=decoration,
            defaults={
                'date': date,
                'rdate': rdate,
                'time': time,
                'amount': total_amount,
                'selected_utensils': selected_utensils
            }
        )

        if not created:
            # If it already exists, update the fields
            deccart_item.date = date
            deccart_item.rdate = rdate
            deccart_item.time = time
            deccart_item.amount = total_amount
            deccart_item.selected_utensils = selected_utensils
            deccart_item.save()

        messages.success(request, 'Booking confirmed successfully!')
        return redirect('carts')

    return render(request, 'book_decoration.html', {'decoration': decoration,'usrd':usrd} )

def dcarts(request):
    obj=models.decorations.objects.all()
    return render(request,'dcarts.html',{'obj':obj})

def chef_carts(request):
    obj=models.icart.objects.all()
    return render(request,'chef_carts.html',{'obj':obj})




import razorpay
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import deccart, decorations, decorationtransaction

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Display Cart


# Buy Decoration and Start Payment
from django.db.models import F

def buy_decoration(request, decoration_id):
    email = request.session['email']
    user = Event.objects.get(email=email)
    cart_item, created = deccart.objects.get_or_create(
        decoration_id=decoration_id, user=user
    )

    UTENSIL_PRICES = {
        'chair': 80,
        'table': 80,
        'light': 80,
        'generator': 90
    }

    # Update selected utensils if already in cart
    new_selected_utensils = request.POST.get("selected_utensils", {})  # Get utensils from form
    for key, quantity in new_selected_utensils.items():
        cart_item.selected_utensils[key] = cart_item.selected_utensils.get(key, 0) + int(quantity)

    # Update total amount based on utensils
    total_amount = cart_item.amount or 0
    for key, quantity in cart_item.selected_utensils.items():
        total_amount += UTENSIL_PRICES.get(key, 0) * quantity

    # Update the cart item
    cart_item.amount = total_amount
    cart_item.save()
    user = Event.objects.filter(email=email)
    # Create Razorpay Order
    DATA = {
        "amount": total_amount * 10,  # Convert to paisa
        "currency": "INR",
        "receipt": f"order_rcptid_{cart_item.id}",
        "payment_capture": 1
    }
    order = razorpay_client.order.create(data=DATA)

    # Check if a transaction exists, update it instead of creating a new one
    transaction, trans_created = decorationtransaction.objects.update_or_create(
        user=user,
        defaults={"razorpay_order_id": order['id'], "amount": total_amount}
    )
    try:
    # Send email notification
        send_mail(
            subject='Your Utensil Details',
            message=(
                f"Hello Admin,\n\n"
                f"You have an updated utensil order:\n"
                f"Date: {cart_item.date} to {cart_item.rdate}\n"
                f"Amount: {cart_item.amount}\n"
                f"Utensils: {cart_item.selected_utensils}\n"
                f"User: {cart_item.user.username}\n\n"
                "Thank you for choosing our services."
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['elnafrancis11@gmail.com'],
        )

        context = {
            'order_id': order['id'],
            'razorpay_key': settings.RAZOR_KEY_ID,
            'amount': total_amount,
            'cart_item': cart_item,
        }
        return render(request, 'buy_decoration.html', context)
    except Exception as e:
        print(e)

def decoration_payment_success(request, cart_id):
    cart_item = get_object_or_404(deccart, id=cart_id)

    decorationtransaction.objects.filter(cart=cart_item).update(status='Paid')
    cart_item.delete()
    return render(request, 'decoration_payment_success.html', {'cart_item': cart_item})


from django.shortcuts import render, get_object_or_404, redirect
from .models import decorations

def edit_decoration(request, id):
    decoration = get_object_or_404(decorations, id=id)

    if request.method == 'POST':

        decoration.name = request.POST['name']
        decoration.description = request.POST['description']
        decoration.event = request.POST['event']
        decoration.timeduration = request.POST['timeduration']
        decoration.amount = request.POST['amount']

        # Handle image upload
        if 'image' in request.FILES:
            decoration.image = request.FILES['image']

        # Handle selected utensils (checkboxes)
        selected_utensils = request.POST.getlist('selected_utensils')
        decoration.selected_utensils = {ut: True for ut in selected_utensils}

        decoration.save()
        return redirect('declist')

    return render(request, 'edit_decoration.html', {'decoration': decoration})


def chef_events(request):
    email = request.session.get('email')
    print("Session Email:", email)  # Debugging

    if not email:
        return HttpResponse("User not logged in", status=401)

    user = chef.objects.filter(email=email).first()
    print("Chef Retrieved:", user)  # Debugging

    if not user:
        return HttpResponse("Chef not found", status=404)

    # Find all event updates created by this chef
    chef_events = eventsupdates.objects.filter(chef=user)
    print("Chef's Event Updates:", chef_events)  # Debugging

    # Find all transactions where the purchased product is one of the chef's event updates
    transactions = Transaction.objects.filter(products__in=chef_events)
    print("Transactions for this Chef's Events:", transactions)  # Debugging

    # Extract the events purchased from those transactions
    event_updates = eventsupdates.objects.filter(id__in=transactions.values_list('products', flat=True))
    print("Event Updates Retrieved:", event_updates)  # Debugging

    return render(request, 'chef_events.html', {'event_updates': event_updates})
from django.shortcuts import render
from .models import Utensilsform, decorations

def owner_home(request):
    # Fetch all utensils and decorations from the database
    Utensil = Utensilsform.objects.all()
    decor = decorations.objects.all()

    # Render the ownerhome.html template with the retrieved data
    return render(request, 'Ownerhome.html', {
        'Utensilsform': Utensil,
        'decorations': decor
    })



# def book_utensils(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         name = request.POST.get("name")
#         utensils = request.POST.get("utensils")

#         # Update the existing entry or create a new one
#         obj, created = Utensilsform.objects.update_or_create(
#             email=email,  # Search by email
#             defaults={"name": name, "utensils": utensils}  # Update if exists
#         )

#         message = "Booking updated!" if not created else "Booking created!"
#         return render(request, "utensils.html", {"message": message})

#     return render(request, "utensils.html")


def user_cart(request):
    email = request.session.get('email')  # Assuming user is identified by email
    user = get_object_or_404(Event, email=email)  # Get user instance

    # Fetch cart items related to this user
    chef_cart_items = icart.objects.filter(user=user)
    decoration_cart_items = deccart.objects.filter(user=user)
    utensil_cart_items = Utensilsform.objects.filter(user=user)

    return render(request, 'user_cart.html', {
        'chef_cart_items': chef_cart_items,
        'decoration_cart_items': decoration_cart_items,
        'utensil_cart_items': utensil_cart_items,
    })



# Helper 
# views for utensil cart






def list_utensils(request):
    utensils = Utensilsform.objects.all()
    return render(request, 'list_utensils.html', {'utensils': utensils})

from django.shortcuts import render
from .models import Transaction, Payment, decorationtransaction

def user_transactions(request):
    email = request.session.get('email')
    
    
    transactions = Transaction.objects.filter(user__email=email)
    payments = Payment.objects.filter(user__email=email)
    decorations = decorationtransaction.objects.filter(user__email=email)

    return render(request, 'user_transactions.html', {
        'transactions': transactions,
        'payments': payments,
        'decorations': decorations,
    })



def utidectransactions(request):
    email = request.session.get('email')
    
    
    
    payments = Payment.objects.all()
    decorations = decorationtransaction.objects.all()

    return render(request, 'utidectransactions.html', {
        
        'payments': payments,
        'decorations': decorations,
    })


def decorsview(request):
    paid_transactions = decorationtransaction.objects.filter(status="Paid")
    utensil_transaction=Payment.objects.filter(status="Paid")

    context = {
        "paid_transactions": paid_transactions,
        "utensil_transaction":utensil_transaction
    }
    return render(request, "decorsview.html", context)



def cheftransactions(request):
    email = request.session.get('email')
    
    
    
    transactions = Transaction.objects.filter(products__chef__email=email)

    return render(request, 'cheftransactions.html', {
        
        'transactions': transactions,
        
    })
