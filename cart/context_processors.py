from .cart import Cart

#Create context processors so our cart can work on all page of the website

def cart(request):
    # Return the default data from our Cart
    return {'cart': Cart(request)}