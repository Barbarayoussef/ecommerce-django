from django.shortcuts import redirect, render
from cart.cart import Cart
from payment.models import ShippingAddress, Order,OrderItem
from payment.forms import ShippingForm
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product,Profile
import datetime
from django.utils.timezone import now 
import decimal
from payment.shipping_service import ShippingService, collectShippableItems



def orders(request, pk):
   if request.user.is_authenticated and request.user.is_superuser:
    order=Order.objects.get(id=pk)
    #get the order items
    items=OrderItem.objects.filter(order=pk)

    if request.POST:
        status=request.POST['shipping_status']
        #check if true or false
        if status=="true":
            order=Order.objects.filter(id=pk)
            #update the status
            now=datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)
        else:
            order=Order.objects.filter(id=pk)
            order.update(shipped=False)
        success_msg = "Shipping Status Updated"
        messages.success(request, success_msg)
        log_message_to_console(request, success_msg, "SUCCESS")
        return redirect('home')

    
    return render(request,'orders.html',{"items":items,"order":order})

   else:
     error_msg = "Access denied"
     messages.success(request, error_msg)
     log_message_to_console(request, error_msg, "ERROR")
     return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders=Order.objects.filter(shipped= False)
        if request.POST:
            status=request.POST['shipping_status']
            num = request.POST['num']
            order=Order.objects.filter(id=num)
            #grab date and time
            now=datetime.datetime.now()
            #update order
            order.update(shipped=True, date_shipped=now)
            messages.success(request, "Shipping Status Updated")
            return redirect('home')
        return render(request,"not_shipped_dash.html",{"orders": orders})
    else:
        messages.success(request,"Access denied")
        return redirect('home')
    


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders=Order.objects.filter(shipped= True)
        if request.POST:
            status=request.POST['shipping_status']
            num = request.POST['num']
            order=Order.objects.filter(id=num)
            #grab date and time
            now=datetime.datetime.now()
            #update order
            order.update(shipped=False)
            messages.success(request, "Shipping Status Updated")
            return redirect('home')
        return render(request,"shipped_dash.html",{"orders": orders})
    else:
        messages.success(request,"Access denied")
        return redirect('home')



def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        
        # ===== VALIDATION CHECKS =====
        
        # 1. Check if cart is empty
        if len(cart_products) == 0:
            error_msg = "Cart is empty. Please add items before checkout."
            messages.error(request, error_msg)
            print("\n" + "="*50)
            print("CHECKOUT VALIDATION ERROR")
            print("="*50)
            print(f"❌ {error_msg}")
            print(f"Customer: {request.user.username if request.user.is_authenticated else 'Guest'}")
            print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*50 + "\n")
            return redirect('cart_summary')
        
        # 2. Check stock and expiry for all products
        for product in cart_products:
            product_qty = quantities.get(str(product.id), 0)
            
            # Check if product is out of stock
            if product.quantity < product_qty:
                error_msg = f"Product '{product.name}' is out of stock. Only {product.quantity} items available."
                messages.error(request, error_msg)
                print("\n" + "="*50)
                print("CHECKOUT VALIDATION ERROR")
                print("="*50)
                print(f"❌ Product is out of stock or expired")
                print(f"Product: {product.name}")
                print(f"Requested Quantity: {product_qty}")
                print(f"Available Quantity: {product.quantity}")
                print(f"Customer: {request.user.username if request.user.is_authenticated else 'Guest'}")
                print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("="*50 + "\n")
                return redirect('cart_summary')
            
            # Check if product is expired
            if product.is_expirable and product.expiry_date and product.expiry_date < datetime.date.today():
                error_msg = f"Product '{product.name}' has expired and cannot be purchased."
                messages.error(request, error_msg)
                print("\n" + "="*50)
                print("CHECKOUT VALIDATION ERROR")
                print("="*50)
                print(f"❌ Product is out of stock or expired")
                print(f"Product: {product.name}")
                print(f"Expiry Date: {product.expiry_date}")
                print(f"Current Date: {datetime.date.today()}")
                print(f"Customer: {request.user.username if request.user.is_authenticated else 'Guest'}")
                print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("="*50 + "\n")
                return redirect('cart_summary')
        
        # 3. Check customer balance (only for authenticated users)
        shipping_fees = decimal.Decimal('10.00')  # Fixed shipping fee
        total_with_shipping = totals + shipping_fees
        
        if request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user=request.user)
                if user_profile.balance < total_with_shipping:
                    error_msg = f"Insufficient balance. You have ${user_profile.balance:.2f}, but need ${total_with_shipping:.2f} (including ${shipping_fees:.2f} shipping)."
                    messages.error(request, error_msg)
                    print("\n" + "="*50)
                    print("CHECKOUT VALIDATION ERROR")
                    print("="*50)
                    print(f"❌ Customer's balance is insufficient")
                    print(f"Customer: {request.user.username}")
                    print(f"Current Balance: ${user_profile.balance:.2f}")
                    print(f"Required Amount: ${total_with_shipping:.2f}")
                    print(f"Shortfall: ${(total_with_shipping - user_profile.balance):.2f}")
                    print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    print("="*50 + "\n")
                    return redirect('cart_summary')
            except Profile.DoesNotExist:
                error_msg = "User profile not found. Please contact support."
                messages.error(request, error_msg)
                print("\n" + "="*50)
                print("CHECKOUT VALIDATION ERROR")
                print("="*50)
                print(f"❌ {error_msg}")
                print(f"Customer: {request.user.username}")
                print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("="*50 + "\n")
                return redirect('cart_summary')
        
        # SHIPPING SERVICE INTEGRATION 
        shipping_service = ShippingService()
        shippable_items = collectShippableItems(cart_products, quantities)
        shipping_details = shipping_service.getShippingDetails(shippable_items)
        
        # CONSOLE LOGGING
        print("\n" + "="*50)
        print("CHECKOUT DETAILS")
        print("="*50)
        print(f"Customer: {request.user.username if request.user.is_authenticated else 'Guest'}")
        print(f"Order Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n--- ORDER ITEMS ---")
        
        for product in cart_products:
            qty = quantities.get(str(product.id), 0)
            item_total = product.price * qty
            print(f"• {product.name} x{qty} @ ${product.price:.2f} = ${item_total:.2f}")
        
        print(f"\nSubtotal: ${totals:.2f}")
        print(f"Shipping Fees: ${shipping_fees:.2f}")
        print(f"Total Amount: ${total_with_shipping:.2f}")
        
        # Shipping service details
        if shippable_items:
            print(f"\n--- SHIPPING DETAILS ---")
            print(f"Shippable Items: {shipping_details['item_count']}")
            print(f"Total Weight: {shipping_details['total_weight']} kg")
            print(f"Calculated Shipping Cost: ${shipping_details['shipping_cost']:.2f}")
            print("\nShippable Items:")
            for item in shipping_details['items']:
                print(f"  • {item['name']}: {item['weight']} kg")
        else:
            print(f"\n--- SHIPPING DETAILS ---")
            print("No shippable items in this order")
        
        if request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user=request.user)
                print(f"\nCustomer Balance Before: ${user_profile.balance:.2f}")
                print(f"Customer Balance After: ${(user_profile.balance - total_with_shipping):.2f}")
            except Profile.DoesNotExist:
                print("\nCustomer Balance: Profile not found")
        else:
            print("\nCustomer Balance: Guest checkout")
        
        print("="*50 + "\n")
        
        # PROCESS ORDER
        my_shipping = request.session.get('my_shipping')

        # Gather order info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
        amount_paid = total_with_shipping  # Include shipping fees

        # Create the order
        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Update user balance
            user_profile = Profile.objects.get(user=request.user)
            user_profile.balance -= total_with_shipping
            user_profile.save()

            # Add order items
            order_id = create_order.pk
            for product in cart_products:
                product_id = product.id
                price = product.price
                
                for key, value in quantities.items(): 
                    if int(key) == product.id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()

            # Clear session and cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            # Delete cart from db
            current_user = Profile.objects.filter(user__id=request.user.id)
            current_user.update(old_cart="")

            # Process shipping order
            if shippable_items:
                customer_info = {
                    'full_name': full_name,
                    'email': email,
                    'shipping_address': shipping_address
                }
                shipping_order = shipping_service.processShippingOrder(shippable_items, customer_info)
                
                print("\n" + "="*50)
                print("SHIPPING ORDER PROCESSED")
                print("="*50)
                print(f"Tracking Number: {shipping_order['tracking_number']}")
                print(f"Customer: {shipping_order['customer_name']}")
                print(f"Email: {shipping_order['customer_email']}")
                print(f"Total Weight: {shipping_order['total_weight']} kg")
                print(f"Shipping Cost: ${shipping_order['shipping_cost']:.2f}")
                print(f"Status: {shipping_order['status']}")
                print("="*50 + "\n")

            messages.success(request, f"Order placed successfully! Total: ${total_with_shipping:.2f}")
            return redirect('home')

        else:
            # Guest checkout
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            # Add order items
            order_id = create_order.pk
            for product in cart_products:
                product_id = product.id
                price = product.price
                
                for key, value in quantities.items(): 
                    if int(key) == product.id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()
            
            # Delete cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            messages.success(request, f"Order placed successfully! Total: ${total_with_shipping:.2f}")
            return redirect('home')
    else:
        messages.success(request, "Access Denied")
        return redirect('home')






   




def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    shipping_fees = decimal.Decimal('10.00')  # Fixed shipping fee
    total_with_shipping = totals + shipping_fees
    
    # Checkout as a user
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "checkout.html", {
            "cart_products": cart_products, 
            "quantities": quantities,
            "totals": totals, 
            "shipping_fees": shipping_fees,
            "total_with_shipping": total_with_shipping,
            "shipping_form": shipping_form
        })
    # Checkout as a guest
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "checkout.html", {
            "cart_products": cart_products, 
            "quantities": quantities,
            "totals": totals, 
            "shipping_fees": shipping_fees,
            "total_with_shipping": total_with_shipping,
            "shipping_form": shipping_form
        })
    
    




def payment_success(request):
    return render(request, 'payment_success.html',{})
