from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product


def proccess_order(request):
    if request.POST:
        #get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        #get billing info from the last page 
        payment_form = PaymentForm(request.POST or None)
        #get shipping session data
        my_shipping = request.session.get('my_shipping')

        # gather order info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        #cerate shipping address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        #create an order
        if request.user.is_authenticated:
            #logged in
            user = request.user
            #create order
            create_oder = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_oder.save()

            #add order items

            #get the order id
            order_id = create_oder.pk
            #get product info
            for product in cart_products():
                #get product id
                product_id = product.id
                #get product price
                price = product.price
                #get quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        #create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()
        #delete our cart
        for key in list(request.session.keys()):
            if key == "session_key":
                #delete the key
                del request.session[key]


            messages.success(request,"Order Placed")
            return redirect('home')

        else:
            #not logged in
            #create order
            create_oder = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_oder.save()

            #add order items
            
            #get the order id
            order_id = create_oder.pk
            #get product info
            for product in cart_products():
                #get product id
                product_id = product.id
                #get product price
                price = product.price
                #get quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        #create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()

        #delete our cart
        for key in list(request.session.keys()):
            if key == "session_key":
                #delete the key
                del request.session[key]



            messages.success(request,"Order Placed")
            return redirect('home')


    else:
        messages.success(request,"Access Denied")
        return redirect('home')


def billing_info(request):
    if request.POST:
    #get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        #cerate a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        #check to see if user is logged in 
        if request.user.is_authenticated:
            #get thee billing form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products":cart_products , "quantities":quantities, "totals":totals , "shipping_info":request.POST, "billing_form":billing_form})

        else:
            #not logged in
            #get thee billing form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products":cart_products , "quantities":quantities, "totals":totals , "shipping_info":request.POST, "billing_form":billing_form})


        shipping_form = request.POST
        return render(request, "payment/billing_info.html", {"cart_products":cart_products , "quantities":quantities, "totals":totals , "shipping_form":shipping_form})
    else:
        messages.success(request,"Access Denied")
        return redirect('home')


def checkout(request):
     #get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        #checkout as logged in user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html", {"cart_products":cart_products , "quantities":quantities, "totals":totals , "shipping_form":shipping_form})

    else:
        #checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {"cart_products":cart_products , "quantities":quantities, "totals":totals , "shipping_form":shipping_form})


def payment_success(request):
    return render(request, "payment_success.html", {})
