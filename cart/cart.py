from store.models import Product,Profile
class Cart():
    def __init__(self,request):
        self.session=request.session
        # Get request
        self.request=request

        #Get the current session key if it exists
        cart=self.session.get('session_key')

        #if the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart=self.session['session_key']={}

        #Make sure cart is available on all pages of site
        self.cart = cart if cart is not None else {}



    def db_add(self, product,quantity):
       product_id=str(product)
       product_qty=str(quantity)

       if product_id in self.cart:
        pass
       else:
        self.cart[product_id]=int(product_qty)
        #self.cart[product_id]={'price': str(product.price)}
       self.session.modified=True
      # deal with logged in user
       if self.request.user.is_authenticated:
         current_user= Profile.objects.filter(user__id=self.request.user.id)
         # {'3' : 1, '2' : 4} to {"3":1,"2":4}
         carty=str(self.cart)
         carty=carty.replace("\'","\"")
         #save carty to the profile model
         current_user.update(old_cart=str(carty))

    def add(self, product,quantity):
      product_id=str(product.id)
      product_qty=int(quantity)

      if product.quantity < product_qty:
         return {'success': False, 'message': f"Only {product.quantity} items available."}

      if product_id in self.cart:
          return {'success': False, 'message': "Item already in cart."}  # Prevent duplicate add

      # Reduce stock and save
      product.quantity -= product_qty
      product.save()
      self.cart[product_id]=int(product_qty)
      #self.cart[product_id]={'price': str(product.price)}
      self.session.modified=True
      # deal with logged in user
      if self.request.user.is_authenticated:
         current_user= Profile.objects.filter(user__id=self.request.user.id)
         # {'3' : 1, '2' : 4} to {"3":1,"2":4}
         carty=str(self.cart)
         carty=carty.replace("\'","\"")
         #save carty to the profile model
         current_user.update(old_cart=str(carty))
      return {'success': True, 'message': "Product added to cart."}

    
    def __len__(self):
       return len(self.cart)
    
    def get_products(self):
       #get ids from cart
       product_ids=self.cart.keys()
       #use ids to looup products in database model
       products=Product.objects.filter(id__in=product_ids)
       return products
    
    def get_quants(self):
       quantities=self.cart
       return quantities
    
    def update(self, product,quantity):
       product_id=str(product)
       new_qty=int(quantity)

         # Get the current quantity in cart
       old_qty = self.cart.get(product_id, 0)
        # Fetch the product from DB
       prod_instance = Product.objects.get(id=int(product_id))
       # Calculate how much to adjust stock
       qty_change = new_qty - old_qty

        # If increasing cart qty, check stock availability
       if qty_change > 0 and prod_instance.quantity < qty_change:
        return {'success': False, 'message': f"Only {prod_instance.quantity} items available."}
       
        # Adjust product stock
       prod_instance.quantity -= qty_change
       prod_instance.save()

       # Update cart
       self.cart[product_id] = new_qty
       self.session.modified = True


       # Save cart to profile if logged in
       if self.request.user.is_authenticated:
        current_user = Profile.objects.filter(user__id=self.request.user.id)
        carty = str(self.cart).replace("\'", "\"")
        current_user.update(old_cart=str(carty))

       return {'success': True, 'message': "Cart updated successfully."}

    def delete(self,product):
       product_id=str(product)
       # delete from dictinary/cart
       if product_id in self.cart:
           qty_removed = self.cart[product_id]
           # Restore quantity
           prod_instance = Product.objects.get(id=int(product_id))
           prod_instance.quantity += qty_removed
           prod_instance.save()

           del self.cart[product_id]
        
       self.session.modified = True
       if self.request.user.is_authenticated:
         current_user= Profile.objects.filter(user__id=self.request.user.id)
         # {'3' : 1, '2' : 4} to {"3":1,"2":4}
         carty=str(self.cart)
         carty=carty.replace("\'","\"")
         #save carty to the profile model
         current_user.update(old_cart=str(carty))
    
    def cart_total(self):
       #get products id
       product_id= self.cart.keys()
       #lookup those keys in our products database model
       products=Product.objects.filter(id__in=product_id)
       #get quantities
       quantities=self.cart
       #start counting at 0
       total = 0
       for key, value in quantities.items():
           key=int(key)
           for product in products:
             if product.id == key:
                 total = total + (product.price * value)
       return total

    def clear_cart(self):
        #Clear all items from cart
        self.cart.clear()
        self.session.modified = True
        # Clear from profile if logged in
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            current_user.update(old_cart="")



       



