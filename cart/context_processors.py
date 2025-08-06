from .cart import Cart

#create a context processor to make the cart available in templates
def cart(request):
    #return the default data from our cart 
    return {'cart': Cart(request)}  # Return the cart instance to be used in templates


