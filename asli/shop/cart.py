from .models import Product

CART_SESSION_ID='cart'

class Cart:
    def __init__(self,request) -> None:
        self.session=request.session
        cart=self.session.get(CART_SESSION_ID)
        if not cart:
            cart=self.session[CART_SESSION_ID]={}
        self.cart=cart

    def __iter__(self):
        product_ins=self.cart.keys()
        products=Product.objects.filter(id__in=product_ins)
        cart=self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['total_price'] = int(item['price']) * item['tedad']
            yield item

    def __len__(self):
        return sum(item['tedad'] for item in self.cart.values())

    def Add_To_Cart(self,product,tedad):
        product_id=str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'tedad':0 , 'price':str(product.price)}
        self.cart[product_id]['tedad'] += tedad
        self.save()

    def Delete_in_Cart(self,product):
        product_id=str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def Total_Price(self):
        return sum(item['tedad'] * int(item['price']) for item in self.cart.values())
    
    def Clear_Cart(self):
        del self.session[CART_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified=True