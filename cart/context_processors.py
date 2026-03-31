from .cart import Cart
# create context processes so our cart can work all pages
def cart(request):
    #return the defualt data from our cart
    return {'cart': Cart(request)}