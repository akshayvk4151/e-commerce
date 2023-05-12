from django.shortcuts import render,redirect
from .models import Customer , Cart , Order , Order_detail,Review
from ecommerceadmin.models import Products
from .decorators import login_required
from django.http import JsonResponse
from django.db.models import F,Q,Sum
import razorpay
from django.core import serializers
from django.conf import settings
from . serializer import productSerialize



# Create your views here.

def home(request):

    product =Products.objects.all()[0:4]

    return render(request,'common/home.html',{'products':product})

def about(request):
    return render(request,('common/about.html'))

def contact(request):

    if request.method == "POST":



        name = request.POST['name']
        email = request.POST['email']
        review = request.POST['review']




        reviews = Review(name = name , email = email , review = review )
        reviews.save()



    return render(request,'common/contact.html',{'msg':'added successfully'})

def order_details(request):
    try:
        pid=  int(request.GET['u'])
        product=Products.objects.get(id=pid)
        request.session['gt']=product.price
        
        customer=Customer.objects.get(id=request.session['customer'])
        return render(request,'common/order_details.html',{'customer':customer,'gtotal':product.price})
    except:
        # customer_details = Customer.objects.filter(id= request.session['customer']).values('customer_name','address','phone','email')
        # customer_name = customer_details[0]['customer_name']
        # phone  = customer_details[0]['phone']
        # email  = customer_details[0]['email']
        # address  = customer_details[0]['address']
        customer=Customer.objects.get(id=request.session['customer'])
        gtotal = request.session['gt']
        print("gt",gtotal)
        return render(request,'common/order_details.html',{'customer':customer,'gtotal':gtotal})

@login_required
def payment(request):

    name=Customer.objects.get(id=request.session['customer']).customer_name
    amount=request.session['gt']

    return render(request,'common/payment.html',{'name':name,'amount':amount})


@login_required

def order_payment(request):

    
    customer = request.session['customer']
    od=Order(customer_id=customer,amount=request.session['gt'],status='pending')
    od.save()
    request.session['oid']= od.id

   

    if request.method == "POST":
        customer = request.session['customer']
        amount = request.POST['total']
        
        print(amount)
        order_recipt="order_reciptid_11"
        notes={'shipping address':'bomalahalli,bangolre'}

        products= Order.objects.filter(customer_id=request.session['customer'],status='pending')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        payment = client.order.create(
            {"amount": float(amount) * 100, "currency": "INR", "payment_capture": "1",'notes':notes}
        )

        
        print(payment)



        request.session['oid']= od.id
        products=Cart.objects.filter(customer_id=customer) 


        for pro in products:

            print(pro.product_id)

            order=Order_detail(customer_id=customer,
                    productid_id=pro.product_id,
                    price=pro.product.price,
                    quantity=pro.qty,
                    status="order_pending",
                    payment_type="Razorpay",
                    order_id=od.id        
                    )
            order.save()
        products.delete()
        return JsonResponse(payment)

  
     

       



@login_required

def updatepayment(request):




    user_id=request.session['customer']
    Order.objects.filter(id=request.session['oid'],customer_id=user_id, status='pending').update(status="paid")
    pid=Order.objects.filter(id=request.session['oid'],customer_id=user_id, status='pending')
    print('hello')
    print(pid)
    customer_id=request.session['customer']
    products=Cart.objects.filter(customer_id=customer_id) 

    for pro in products:

        print(pro.product)

        order=Order_detail(customer_id=customer_id,
                    productid_id=pro.product,
                    price=pro.product.price,
                    quantity=pro.qty,
                    status="paid",
                    payment_type="Razorpay",
                    order_id= pid[0].id
        )
        order.save()
        products.delete()

    Order_detail.objects.filter(customer_id=user_id, status='order_pending',order_id=request.session['oid']).update(status='paid')
    return JsonResponse({'resp':'sucsses'})
  






def shop(request):
    error_msg =''

    products =Products.objects.all()


    if request.method == 'POST':

        pid = request.POST['pid']     #pid from hidden input tag
        customer = request.session['customer']



        record_exist = Cart.objects.filter( product = pid ,customer = customer ).exists()

        if not record_exist:


            cart = Cart(customer_id =customer ,product_id = pid )
            cart.save()
            return redirect('common:cart')

        else:

            error_msg = 'item is already in cart'



    return render(request,'common/shop.html',{'products':products,'error':error_msg})




def login(request):

    error_msg = ''

    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']

        try:
            customer = Customer.objects.get(email = email ,password = password)
            request.session['customer'] = customer.id
            return redirect('common:home')

        except:

            error_msg = 'email or password is incorrect'



    return render(request,'common/login.html',{'error_msg':error_msg})

def logout(request):
    del request.session['customer']
    request.session.flush()
    return redirect('common:home')




def signup(request):

    success_msg =''
    error_msg =''


    if request.method == 'POST':
        cname = request.POST['customer_name']
        cphone = request.POST['phone']
        cemail = request.POST['email']
        cpassword = request.POST['password']
        caddress = request.POST['address']


        email_exist = Customer.objects.filter(email = cemail).exists()

        if not email_exist:

            customer = Customer(customer_name = cname ,phone = cphone , email = cemail ,password = cpassword, address =caddress)
            customer.save()
            success_msg = 'you registered successfully'

        else:

            error_msg = 'email is already exist'




    return render(request,'common/signup.html',{'success_message':success_msg,'error_message':error_msg})




@login_required
def change_password(request):

    success_msg = ''
    error_msg = ''


    if request.method == 'POST':

        old_pass = request.POST['old_password']
        new_pass = request.POST['new_password']
        confirm_pass = request.POST['confirm_password']

        if new_pass == confirm_pass :

            if len(new_pass) >= 8 :

                customer = Customer.objects.get(id = request.session['customer'])

                if customer.password == old_pass :

                    # customer.password = new_pass
                    # customer.save()

                    Customer.objects.filter(id = request.session['customer']).update( password = new_pass )

                    success_msg = 'password changed successfully'

                else:
                    error_msg = 'old password is incorrect'

            else:

                error_msg = 'passwords should be 8 characters'


        else:
            error_msg = 'passwords doesn\'t match'
    return render(request,'common/change_password.html',{'success_msg':success_msg,'error_msg':error_msg})



@login_required

def cart(request):

    cart = Cart.objects.filter(customer = request.session['customer']).annotate(total_price = F('product__price') * F('qty'))
    sum=0
    for i in cart:
        sum = sum + i.total_price
    
   
    request.session['gt']=sum


    return render(request,'common/cart.html',{'cart_items':cart,'Gtotal':sum})


def change_qty(request):
 
    quantity = int(request.POST['quantity'])
    p_id = request.POST['p_id']
    print(p_id,quantity)
    customer = Customer.objects.get(id = request.session['customer'])
   

    
    stock = Products.objects.get(id=p_id)
    print(stock.stock)

    if stock.stock > quantity:

        changeqty = Cart.objects.get(product_id=p_id,customer_id=request.session['customer'])
        print(changeqty.qty)
        changeqty.qty=quantity        #qty is from model cart
        changeqty.save()
        status=True
        cart2=Cart.objects.filter(product_id=p_id,customer_id=request.session['customer']).annotate(total_price = F('product__price') * F('qty')) #product__price is a method 
        sum=0
        for i in cart2:
            sum = sum + i.total_price
        print("hhhhh",sum)  
        request.session['gt']=sum  

        msg="qty update successfully"
    
        return JsonResponse({'data':sum ,'status':status})
    
    else:
        print(sum)
        status=False
        return JsonResponse({'status':status})


    
def product_detailes(request,pid):

    error_msg = ''
    qtys = 1

    product = Products.objects.get( id = pid )
    try:
        cartitems=Cart.objects.get(product_id=pid,customer_id = request.session['customer'])
        qtys=cartitems.qty
    except:
        pass    

    if request.method == 'POST':

        customer = request.session['customer']
        qty=request.POST['quantity']
        qty=int(qty)

        print(type(qty))

        record_exist = Cart.objects.filter( product = pid ,customer = customer ).exists()

        if not record_exist:

            cart = Cart(customer_id =customer ,product_id = pid,qty=qty )
            cart.save()
            return redirect('common:cart')

        else:
            carts = Cart.objects.get( product = pid ,customer = customer )
            if carts.qty != qty:
                carts.qty=qty
                carts.save()
                qts=carts.qty
                return render(request,'common/product_detailes.html',{ 'product_detailes':product,'error':error_msg,'quantity':qts })
                
            else:
                error_msg = 'item already added in cart'

       
    return render(request,'common/product_detailes.html',{ 'product_detailes':product,'error':error_msg,'quantity':qtys })


@login_required   
def removecart(request,customer):
    cart_item = Cart.objects.get(id = customer)
    cart_item.delete()
    return redirect('common:cart')



@login_required

def profile(request):

    customer_D=Customer.objects.get(id=request.session['customer'])      

    
    return render(request,'common/profile.html',{'customer_details':customer_D})



@login_required


def edit_profile(request):

    success_msg = ''


    if request.method == 'POST':

        cname = request.POST['customer_name']
        cphone = request.POST['phone']
        cemail = request.POST['email']
        cpassword = request.POST['password']
        caddress = request.POST['address']


        customer = Customer.objects.get(id = request.session['customer'])

        Customer.objects.filter(id = request.session['customer']).update(customer_name = cname ,phone = cphone , email = cemail ,password = cpassword, address =caddress )

        success_msg = 'saved successfully'

    
    return render(request,'common/edit_profile.html',{'success_msg':success_msg})


@login_required

def my_orders(request):

    orders=Order_detail.objects.filter(customer_id=request.session['customer'])


    return render(request,'common/my_orders.html',{'orders':orders})


def cancel_order(request,o_id):
    ordered_item = Order_detail.objects.get(id =o_id )
    ordered_item.status='cancelled'
    ordered_item.save()
    return redirect('common:my_orders')



def search_product(request):

    search_word =request.POST['searchdata']

    results = Products.objects.filter(Q(product_name__icontains=search_word))
    print(results)
    result_list =productSerialize(results,many=True)
    print(result_list)
    return JsonResponse({'results':result_list.data})

    



