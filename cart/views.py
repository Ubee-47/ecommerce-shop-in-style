from django.shortcuts import render, get_object_or_404
from .cart import Cart
from website.models import Product
from django.http import JsonResponse
from django.contrib import messages 


# Create your views here.
def cart_summary(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities= cart.get_quants
    totals= cart.cart_total()
    return render(request, 'cart_summary.html',{'cart_products':cart_products,"quantities":quantities,"totals":totals })

def cart_add(request):
    # get the cart
    cart = Cart(request)
    # test about post
    if request.POST.get('action') == 'post':
        #get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        #lookup product from db
        product =get_object_or_404(Product, id =product_id)
        #add session
        cart.add(product=product, quantity=product_qty)


        # get cart quantity
        cart_quantity = cart.__len__()
        # return responce
        # response = JsonResponse({'Product name:' :product.name})
        response = JsonResponse({'qty ':cart_quantity})
        messages.success(request,("Product Added To cart...!"))

        return response

    return render(request, 'cart_add.html',{})



def cart_delete(request):
    if request.method == 'POST' and request.POST.get('action') == 'POST':
        cart = Cart(request)
        product_id = int(request.POST.get('product_id'))
        
        # Call the delete function in the cart class
        cart.delete(product_id)

        response=JsonResponse({ 'product_id': product_id})
        messages.success(request,("Item deleted from shopping cart...!"))
    return response

    


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'POST':
        #get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        #update cart
        cart.update(product= product_id, quantity= product_qty )
        response =JsonResponse({'qty':product_qty})
        messages.success(request,("Your cart has been  Updated...!"))

        return response
    

    return render(request, 'cart_update.html',{})