from django.db import models
from accounts.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.

class Info(models.Model):
    name=models.CharField(max_length=255)
    slug=models.SlugField(max_length=255,unique=True)

    class Meta:
        abstract=True

    def __str__(self) -> str:
        return self.name

class Category(Info):
    sub=models.ForeignKey('self',on_delete=models.CASCADE,related_name='sub_cate',null=True,blank=True)
    is_sub=models.BooleanField(default=False)
    img_brand=models.ImageField(upload_to='imges/',null=True,blank=True)

class Select_IMG_Product(models.Model):
    name=models.CharField(max_length=255)
    select=models.ImageField(upload_to='imges/')

    def __str__(self) -> str:
        return self.name

class Product(Info):
    # name=models.CharField(max_length=255)
    # slug=models.SlugField(max_length=255,unique=True)
    category=models.ManyToManyField(Category,related_name='cate')
    img=models.ImageField()
    detail_img=models.ManyToManyField(Select_IMG_Product,related_name='select_img')
    description=models.TextField()
    price=models.IntegerField()
    is_avalable=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE ,related_name='user_order')
    paid=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    discount=models.IntegerField(default=None,null=True,blank=True)

    def __str__(self) -> str:
        return str(self.user)
    
    def get_total(self):
        total = sum( item.Total_Price() for item in self.item_user.all())
        if self.discount:
            get_discount=(self.discount / 100) * total
            return int(get_discount - total)
        return total
    
class OrderIten(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='item_user')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='pro_user')
    price=models.IntegerField()
    tedad=models.IntegerField(default=1)

    def __str__(self) -> str:
        return str(self.order)
    
    def Total_Price(self):
        return self.tedad * self.price
    
class Cupon(models.Model):
    code=models.CharField(max_length=50)
    start=models.DateTimeField()
    end=models.DateTimeField()
    discount=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(90)])
    is_active=models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.code
    
class CommentProduct(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_comment')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_comment')
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    is_sub=models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.user} Commented... {self.product}"
    