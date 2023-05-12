from django.db import models

# Create your models here.



class Admin(models.Model):
    admin_name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    phone = models.BigIntegerField()
    password = models.CharField(max_length=10)

    class Meta:
        db_table = 'admin'


class Products(models.Model):
    product_name = models.CharField(max_length=20)
    admin = models.ForeignKey(Admin,on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    stock = models.IntegerField()
    image = models.ImageField(upload_to = 'products/')
    price = models.FloatField()
    code = models.CharField(max_length=10)


    class Meta:
        db_table = 'product' 