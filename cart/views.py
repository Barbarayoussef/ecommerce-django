from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    #get the cart
    cart= Cart(request)
    cart_products=cart.get_products()
    quantities=cart.get_quants()
    totals = cart.cart_total()
    return render(request,"cart_summary.html",{"cart_products" : cart_products, "quantities": quantities,"totals": totals})

def cart_add(request):
    # Get the cart
    cart= Cart(request)
    #test for post
    if request.POST.get('action')=='post':
        #get stuff
        product_id= int(request.POST.get('product_id'))
        product_qty=int(request.POST.get('product_qty'))
         #lookup product in DB
        product=get_object_or_404(Product,id=product_id)
        #Save to session
        result= cart.add(product=product, quantity=product_qty)
        #get cart quantity
        if result['success']:
         cart_quantity=cart.__len__()
         #Return response
         response=JsonResponse({'qty': cart_quantity})
         messages.success(request, result['message'])
         #response=JsonResponse({'Product Name': product.name})
        else:  
            response=JsonResponse({'error': result['message']}, status=400)
        return response

def cart_delete(request):
    cart=Cart(request)
    if request.POST.get('action')=='post':
        product_id= int(request.POST.get('product_id'))
        #call delete function in cart
        cart.delete(product=product_id)
        cart_quantity = cart.__len__()
        response= JsonResponse({'product': product_id, 'qty': cart_quantity})
        messages.success(request, "Item deleted successfully!")
        return response
    

def cart_update(request):
    cart=Cart(request)
    if request.POST.get('action')=='post':
        product_id= int(request.POST.get('product_id'))
        product_qty=int(request.POST.get('product_qty'))

        result = cart.update(product=product_id, quantity=product_qty)
        cart_quantity = cart.__len__()
        response= JsonResponse({'qty': cart_quantity})
        messages.success(request, "Your cart has been updated")
        return response
