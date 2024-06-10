from .cart import Cart

#create context processors so our cart can work on all pages
def cart(request):
    # Retuen the default data from our Cart 
    return {'cart': Cart(request)}