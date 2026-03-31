from website.models import Product , Profile


class Cart():
    def __init__(self,request):
        self.session = request.session

        # get request
        self.request = request
        # get the current session key if it exists
        cart = self.session.get('session_key')
       
        # if the user is new ,no session key! create one !
        if 'session_key' not in request.session:
            cart = self.session['session_key']= {}

        # make sure cart is avalible on ALL pages of site
        self.cart = cart    
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
		# Logic
        if product_id in self.cart:
            pass
        else:
			#self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

		# Deal with logged in user
        if self.request.user.is_authenticated:
			# Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
            current_user.update(old_cart=str(carty))
    
    def add(self,product,quantity):
        product_id =str(product.id)
        product_qty=str(quantity)

        # logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price ': str(product.price)} 
            self.cart[product_id] =  int(product_qty)

        self.session.modified = True
        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
    
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("'", "\"")
    
            # Save carty to the Profile model
            current_user.update(old_cart=str(carty))



       



     #cart_quantity 
    def __len__(self):
        return len(self.cart)        
    



    def get_prods(self):
        #get id from cart
        product_ids =self.cart.keys()
        # use id to lookup products and database models
        products = Product.objects.filter(id__in=product_ids)
        # return the products
        return products
    

    # ?for quantity
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    # update product 
    def update(self,product,quantity):
        product_id=str(product)
        product_qty= int(quantity)

        #get cart 
        ourcart = self.cart
        #update dic/cart
        ourcart[product_id]= product_qty

        self.session.modified = True

        
          # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
    
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("'", "\"")
    
            # Save carty to the Profile model
            current_user.update(old_cart=str(carty))
        thing = self.cart    
        return thing
    
    def delete(self, product):
        product_id =str(product)
        # delete the dic /cart 
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True
          # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
    
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("'", "\"")
    
            # Save carty to the Profile model
            current_user.update(old_cart=str(carty))


    def cart_total(self):
        # get product_ids
        product_ids= self.cart.keys()
        #lookup those keys in database models
        products =Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        # get quantities
        quantities = self.cart
        # let start counting at 0
        total = 0      
        for  key, value in quantities.items():
            #convert key string into int key 
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total= total +(product.sale_price * value)
                    else:
                        total= total +(product.price * value)
        return total            