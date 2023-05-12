from django.db import models
from ecommerceadmin.models import Products
from datetime import date

# Create your models here.


class Customer(models.Model):
    customer_name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    phone = models.BigIntegerField()
    password = models.CharField(max_length=10)
    address = models.CharField(max_length=100,default='')

    class Meta:
        db_table = 'customer'

class Cart(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)

    
    class Meta:
        db_table = 'cart'


class Order(models.Model):
    customer =models.ForeignKey(Customer,on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=20,default="pending")
    provider_order_id = models.CharField(max_length=40)
    payment_id = models.CharField(max_length=36)
    signature_id = models.CharField(max_length=128)

    class Meta:
        db_table = 'order_tb'



class Order_detail(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    productid = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=20,default="pending") #update after payment confirmed
    payment_type = models.CharField(max_length=20)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)


    class Meta:
        db_table = 'order_detail'


class Review(models.Model):
    name = models.CharField(max_length=50,default='')
    
    email = models.CharField(max_length=50)
    review = models.CharField(max_length=150)



    
    class Meta:
        db_table = 'review'
    