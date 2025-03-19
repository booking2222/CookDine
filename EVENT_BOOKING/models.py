from django.db import models
from datetime import datetime, date, time, timedelta


# Create your models here.
class Event(models.Model):
    STATUS=(('applied','Applied'),('approved','Approved'),('reject','Reject'),)
    status=models.CharField(max_length=20,choices=STATUS,default='Applied')
    image=models.ImageField(upload_to='image/',null='True',blank='True')
    username=models.CharField(max_length=100)
    phone=models.IntegerField()
    email=models.EmailField(unique=True)
    address=models.CharField(max_length=255)
    password=models.CharField(max_length=128)
    place=models.CharField(max_length=128)
def __str__(self):
    return self.username



def __str__(self):
    return self.Event_name

class feedback(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    feedback_text = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating: {self.rating}, Feedback: {self.feedback_text[ :50]}..."

class Owner(models.Model):
    username=models.CharField(max_length=100)
    phone=models.IntegerField(null=True, blank=True)
    email=models.EmailField(unique=True)
    address=models.CharField(max_length=255)
    password=models.CharField(max_length=128)
    place=models.CharField(max_length=128)


class chef(models.Model):
    STATUS=(('applied','Applied'),('approved','Approved'),('reject','Reject'),)
    status=models.CharField(max_length=20,choices=STATUS,default='Applied')
    image = models.ImageField(upload_to='chefimages/', null=True, blank=True)
    username = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)  # Use CharField to accommodate international numbers
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
    place = models.CharField(max_length=128)
    languages_spoken = models.CharField(max_length=128)  # Can be a comma-separated list
    experience = models.CharField(max_length=128)  # Example: "5 years professional cooking"
    signature_dishes = models.CharField(max_length=500)  # Comma-separated names of dishes
    service_area = models.CharField(max_length=500)  # Radius or regions where they work
    primary_cuisines = models.CharField(max_length=300)  # E.g., "Italian"
    services_offered = models.CharField(max_length=500)  # E.g., "Private dining, Catering"
    certifications = models.FileField(upload_to='chef_certifications/', blank=True, null=True)  # Upload certifications
    work_hours_and_days = models.CharField(max_length=128)  # E.g., "Mon-Fri: 10 AM - 6 PM"



class Chefrecipe(models.Model):
    image=models.ImageField(upload_to='image/',null=True,blank=True)
    name=models.CharField(max_length=100)
    specializations=models.CharField(max_length=300)
    description=models.CharField(max_length=500)
    video=models.FileField(upload_to='video/', null=True, blank=True)    

# chef package
class eventsupdates(models.Model):
    category=models.CharField(max_length=60,null=True, blank=True)
    packagename=models.CharField(max_length=60,null=True, blank=True)
    chefname=models.CharField(max_length=60,null=True, blank=True)
    chefimage=models.ImageField(upload_to='image/', null=True,blank=True)
    chef=models.ForeignKey(chef,null=True,blank=True,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='image/', null=True,blank=True)
    details=models.CharField(max_length=300,null=True,blank=True)
    fromdate=models.DateField(null=True,blank=True)
    todate=models.DateField(null=True,blank=True)
    rentperday=models.IntegerField(null=True, blank=True)
    package=models.DateField(null=True,blank=True)
    
    
class icart(models.Model):
    user = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1,null=True,blank=True)
    products = models.ForeignKey('eventsupdates', on_delete=models.CASCADE)  # Adjust based on your model structure
    start = models.DateField()
    end = models.DateField()
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending',null=True,blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s cart - {self.products.packagename}"

# payments done of chef
class Transaction(models.Model):
    user=models.ForeignKey(Event,on_delete=models.CASCADE)
    products = models.ForeignKey(eventsupdates,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveBigIntegerField(default=1)
    order_id= models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)





    








from django.utils.timezone import now

class ChatMessage(models.Model):
    sender = models.CharField(max_length=100)  # Artist or Buyer username
    receiver = models.CharField(max_length=100)  # Receiver's username
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)
    media=models.FileField(upload_to='chat_media/',null=True,blank=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"
    
    
    

from django import forms
# from .models import decorations

class decorations(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    timeduration = models.IntegerField(null=True,blank=True)
    event = models.CharField(max_length=255,null=True,blank=True)
    amount=models.IntegerField(null=True, blank=True)
    image=models.ImageField(upload_to='decorimage/',null='True',blank='True')
    description = models.TextField(null=True, blank=True)
    
    # Add new fields for better utensil tracking
    UTENSIL_CHOICES = [
        ('chair', 'Chair'),
        ('table', 'Table'),
        ('light', 'Light'),
        ('generator', 'Generator'),
    ]
    
    # Store selected utensils as JSON
    selected_utensils = models.JSONField(default=dict, blank=True)
    # Add new fields for better utensil tracking
    UTENSIL_CHOICES = [
        ('chair', 'Chair'),
        ('table', 'Table'),
        ('light', 'Light'),
        ('generator', 'Generator'),
    ]
    
    # Store selected utensils as JSON
    selected_utensils = models.JSONField(default=dict, blank=True)

class deccart(models.Model):
    user=models.ForeignKey(Event,on_delete=models.CASCADE,null=True,blank=True)
    decoration=models.ForeignKey(decorations,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField()
    rdate = models.DateField()
    time = models.TimeField()
    amount=models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('refund', 'refund'), ('Rejected', 'Rejected')], default='Pending',null=True,blank=True)
    # Add new fields for better utensil tracking
    UTENSIL_CHOICES = [
        ('chair', 'Chair'),
        ('table', 'Table'),
        ('light', 'Light'),
        ('generator', 'Generator'),
    ]
    
    # Store selected utensils as JSON
    selected_utensils = models.JSONField(default=dict, blank=True)
    

class Paymentd(models.Model):
    user=models.ForeignKey(Event,on_delete=models.CASCADE,null=True,blank=True)
    utensils=models.ForeignKey(decorations,on_delete=models.CASCADE,null=True,blank=True)
    payment_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

class decorationtransaction(models.Model):
    user = models.ForeignKey(Event, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=20, default='Created')
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)




class Utensilsform(models.Model):
    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    user=models.ForeignKey(Event,on_delete=models.CASCADE,null=True,blank=True)
    address = models.CharField(max_length=255)
    email = models.EmailField(null=True,blank=True)
    date = models.DateField()
    rdate = models.DateField()
    time = models.TimeField()
    amount=models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Paid', 'paid'), ('refund', 'refund')], default='Pending')
    
    
    # Add new fields for better utensil tracking
    UTENSIL_CHOICES = [
        ('cutlery_sets', 'Cutlery Sets'),
        ('plates_bowls', 'Plates and Bowls'),
        ('serving_utensils', 'Serving Utensils'),
        ('specialty_tools', 'Specialty Tools'),
    ]
    
    # Store selected utensils as JSON
    selected_utensils = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"Rental by {self.name} on {self.date}"
        


# database of utensilform
class Payment(models.Model):
    user=models.ForeignKey(Event,on_delete=models.CASCADE,null=True,blank=True)
    utensils=models.ForeignKey(Utensilsform,on_delete=models.CASCADE,null=True,blank=True)
    payment_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20,choices=[('Pending', 'Pending'), ('Paid', 'paid'), ('refund', 'refund')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)    

class refund(models.Model):
    transact=models.ForeignKey(Payment,on_delete=models.CASCADE,null=True,blank=True)
    refdes=models.TextField()
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('refund', 'refund'), ('Rejected', 'Rejected')], default='Pending')
