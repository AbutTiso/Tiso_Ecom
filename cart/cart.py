from django.shortcuts import render
from my_store.models import Product, Profile


class Cart:
    def __init__(self, request):
        self.session = request.session
        #Get request
        self.request = request

        # get current session key
        cart = self.session.get("session_key")  # Retrieve from session
        # If session key is not present, initialize it
        if "session_key" not in request.session:
            # Initialize an empty cart if not present
            cart = self.session["session_key"] = {}  # Initialize if absent
        self.cart = cart  


    def db_add (self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {"price": str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True
        #Deal with logged in users
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #convert from ' to ""
            carty = str(self.cart)
            carty = carty.replace("\'" , "\"")
            #save our carty to the profile model
            current_user.update(old_cart=str(carty)) 

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {"price": str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True
        #Deal with logged in users
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #convert from ' to ""
            carty = str(self.cart)
            carty = carty.replace("\'" , "\"")
            #save our carty to the profile model
            current_user.update(old_cart=str(carty))  


    def cart_total(self):
        product_ids = self.cart.keys()
        #Lookup products in DB
        products = Product.objects.filter(id__in=product_ids)
        #get quantities
        quantities = self.cart
        #totals
        total = 0
        for key, value in quantities.items():
            # Convert key to int for comparison
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale and product.sale_price is not None:
                        total += product.sale_price * value
                    else:
                        total += product.price * value
        return total
        


    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # Get ids from cart
        product_ids = self.cart.keys()
        # use ids to look up products in DB
        product_ids = Product.objects.filter(id__in=product_ids)
        # Return products
        return Product.objects.filter(id__in=product_ids)

    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        # Get cart
        ourcart = self.cart
        # Update quantity/dictionary/cart
        ourcart[product_id] = product_qty
        # Save to session
        self.session.modified = True

        thing = self.cart
        return thing
    def delete(self, product):

       product_id = str(product)
       #Delete product from cart 
       if product_id in self.cart:
            del self.cart[product_id]
       self.session.modified = True
        


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    return render(request, "cart_summary.html", {"cart_products": cart_products})



