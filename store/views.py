from django.shortcuts import render , redirect
from .models import Product , Category , Profile
from .models import Adopted_pet 
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm , UpdateUserForm , ChangePasswordForm , UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms 
from django.db.models import Q
import json
from  cart.cart import Cart
# views.py
from django.core.exceptions import ObjectDoesNotExist

def adoption(request, pk=None):
    if request.method == 'POST':
        # Assuming you have a form for adoption with POST method
        # Handle the form data here and process adoption
        try:
            adopted_pet_id = request.POST.get('pet_id')
            adopted_pet = Adopted_pet.objects.get(pk=adopted_pet_id)
            
            if request.user.is_authenticated:
                user_email = request.user.email
                subject = f"Adoption Confirmation - {adopted_pet.name}"
                message = f"Dear User,\n\nThank you for adopting {adopted_pet.name}!\n\nDescription: {adopted_pet.description}\n\nBest regards,\nThe Animalia Team"

                send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])

                # You might want to add some logic here to handle successful adoption

            adopted_pets = Adopted_pet.objects.all()
            return render(request, 'adoption.html', {'adopted_pets': adopted_pets})
        
        except ObjectDoesNotExist:
            # Handle the case where the adopted pet does not exist
            # Redirect or show an error message
            messages.error(request, "The adopted pet does not exist.")
            return redirect('home')

    else:
        # This block handles GET requests to the adoption view
        # Here you might want to render the adoption page with available pets
        adopted_pets = Adopted_pet.objects.all()
        return render(request, 'adoption.html', {'adopted_pets': adopted_pets})

def search(request):
    #determine if they filled out the form
    if request.method == "GET":
        searched = request.GET.get('searched', '')
        # Query The Products DB Model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        #test for null
        if not searched :
            messages.success(request, "That Product Does Not Exist...Please Try Again")
            return render(request , "search.html", {})
        else:
            return render(request , "search.html", {'searched': searched })
    else:   
        return render(request , "search.html", {})






def update_info(request):
     if request.user.is_authenticated:
        #get current user
        current_user = Profile.objects.get(user__id = request.user.id)
        #get current user's shipping info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        #get original user form
        form = UserInfoForm(request.POST or None , instance= current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        #get user's shipping form
        if form.is_valid() or shipping_form.is_valid():
            #save original form
            form.save()
            #save shipping form
            shipping_form.save()

            messages.success(request, "Your Info Has Been Updated!!")
            return redirect('home')
        return render(request , "update_info.html", {'form': form, 'shipping_form':shipping_form})
     else:
        messages.success(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')



def update_password(request):
    if request.user.is_authenticated:
         current_user = request.user
         #did they fill out the form
         if request.method == 'POST':  #they are posting the form
            form = ChangePasswordForm(current_user , request.POST)
            # is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password has been Updated")
                #login(request, current_user)
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')

         else:
            form = ChangePasswordForm(current_user)
            return render(request , "update_password.html", {'form': form})
    else:
        messages.success(request, ("You Must Be Logged In To View That Page"))
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None , instance= current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Has Been Updated!!")
            return redirect('home')
        return render(request , "update_user.html", {'user_form': user_form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')



def category(request,foo):
    # Replace hyphens with spaces
    foo = foo.replace('-',' ')
    #grab the category from the url
    try:
        #look up the category
        category = Category.objects.get(name=foo )
        products =Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products,'category':category})
    except:
        messages.success(request, ("That Category Doesn't Exist ..."))
        return redirect('pets')


def product(request,pk):
    product =Product.objects.get(id=pk)
    return render(request, 'product.html',{'product':product})


def adopted_pet(request,pk):
    adopted_pet =Adopted_pet.objects.get(id=pk)
    return render(request, 'adopted_pet.html',{'adopted_pet':adopted_pet})


def home(request):
    return render(request,'home.html')
    

def adoption(request):
    adopted_pets = Adopted_pet.objects.all()
    return render(request,'adoption.html',{'adopted_pets' : adopted_pets})

def advice(request):
    return render(request,'advice.html')

def pets(request):
    products = Product.objects.all()
    return render(request,'pets.html', {'products':products})

def login_user(request):
    if request.method =="POST":
        username = request.POST['username']
        password  = request.POST['password']
        user = authenticate(request , username=username, password=password)
        if user is not None :
            login(request, user)

            #do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            #get their saved cart from database
            saved_cart = current_user.old_cart
            #convert database string to python dictionary
            if saved_cart:
                #convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                #add the laoded cart dictionary to our session 
                #get the cart
                cart = Cart(request)
                #look through the cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)



            messages.success(request , ("You have been logged In!"))
            return redirect('home')
        else:
            messages.success(request , ("There was an error , please try again"))
            return redirect('login')

    else:
        return render(request, 'login.html', {})
        

def shop(request):
    products = Product.objects.all()
    return render(request,'shop.html',{'products':products})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out ..."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form =SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #log in user
            user = authenticate(username=username , password=password )
            login(request , user)
            messages.success(request , ("Username Created - Please Fill Out Your User Info"))
            return redirect('update_info')
        else:
            messages.success(request , ("Whoops! There was a problem Registering please try again ... "))
            return redirect('register')
    else:
        return render(request,'register.html', {'form' : form})