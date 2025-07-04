from .cart import Cart

# context processors to make our cart work on all page of the website

def cart(request):
    # Return the default data from our Cart
    cart_instance = Cart(request)
    # Force clean cart count
    cart_count = len(cart_instance.cart) if cart_instance.cart else 0
    
    return {
        'cart': cart_instance,
        'cart_count': cart_count
    }