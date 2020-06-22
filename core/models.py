from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=200 , blank=True)
    description = models.TextField(max_length=500, blank=True)
    main_image = models.ImageField(upload_to='products/')
    image1 = models.ImageField(upload_to='products/', blank=True)
    image2 = models.ImageField(upload_to='products/', blank=True)
    image3 = models.ImageField(upload_to='products/', blank=True)
    image4 = models.ImageField(upload_to='products/', blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    sale_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    weight = models.DecimalField(decimal_places=2, max_digits=10,default=0.5)
    availabe = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    

class Cart(models.Model):
    session = models.CharField(max_length=200)
    item = models.ForeignKey('Cart_item', on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)



        
    def __str__(self):
        return str(self.id)
    
    def cart_price(self):
        prices = []
        for c in self.cart_item_set.all():
            prices.append(c.total_price())
        return sum(prices)

    def cart_count(self):
        return self.cart_item_set.all().count()

class Cart_item(models.Model):
    shopping_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    time = models.DateTimeField(auto_now_add=True)
 

    def total_price(self):
        return self.qty * self.item.price

    def __str__(self):
        return self.item.title
    


class Customer(models.Model):
    name = models.CharField(max_length=100) 
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length= 100)
    def __str__(self):
        return str(self.name)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places= 2)
    timestamp = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    def __str__(self):
        return str(self.id)