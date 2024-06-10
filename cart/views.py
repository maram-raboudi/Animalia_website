from django.shortcuts import render, get_object_or_404
from .cart import Cart
from django.contrib import messages
from store.models import Product
from django.http import JsonResponse

def cart_summary(request):
    #get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products":cart_products , "quantities":quantities, "totals":totals })

def cart_add(request):
    # Get the cart
    cart = Cart(request) 
    # Test for POST
    if request.POST.get('action') == 'post':
        # Get product_id from POST data
        product_id = int(request.POST.get('product_id'))
        # Get product_qty from POST data, handle empty value
        product_qty_str = request.POST.get('product_qty', '')
        # Convert product_qty to integer, default to 1 if not provided or empty
        product_qty = int(product_qty_str) if product_qty_str else 1

        # Lookup product in DB
        product = get_object_or_404(Product, id=product_id)
   
        # Save to session 
        cart.add(product=product, quantity=product_qty)

        # Get cart quantity
        cart_quantity = cart.__len__()

        # Return response
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request , ("Product Added To Cart ..."))
        return response




    

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #get stuff
        product_id = int(request.POST.get('product_id'))
        #call delete function in cart
        cart.delete(product=product_id)

        response = JsonResponse({'product':product_id})
        messages.success(request , ("Item Deleted From Shopping Cart ..."))
        return response



def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty )
        response = JsonResponse({'qty':product_qty})
        messages.success(request , ("Your Cart Has Been Updated ..."))
        return response
        #return redirect('cart_summary')