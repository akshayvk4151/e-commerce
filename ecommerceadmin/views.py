from django.shortcuts import render,redirect
from .models import Admin,Products
from common.models import Customer , Review ,Order_detail
from .decorators import login_required
from django.http import JsonResponse


# Create your views here.
@login_required
def index(request):

    admin = Admin.objects.filter(id= request.session['admin']).values('admin_name')
    admin_name = admin[0]['admin_name']

    product_count =Products.objects.all().count()
    order_count =Order_detail.objects.all().count()
    customers_count = Customer.objects.all().count()


    # orders=Order_detail.objects.all().order_by('date')

    orders=Order_detail.objects.all().order_by('-date')[0:4]





    return render(request,'ecommerceadmin/index.html',{'name':admin_name,'orders':orders,'p_count':product_count,'o_count':order_count,'c_count':customers_count})
def login(request):

    error_msg = ''

    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']

        try:
            admin = Admin.objects.get(email = email ,password = password)
            request.session['admin'] = admin.id
            return redirect('ecommerceadmin:adminhome')

        except:

            error_msg = 'email or password is incorrect'

    return render(request,'ecommerceadmin/login.html',{'error':error_msg})


@login_required

def add_product(request):

    success_msg = ''
    error_msg = ''

    if request.method == 'POST':

        product_name = request.POST['product_name']
        description = request.POST['description']
        price = request.POST['product_price']
        stock = request.POST['product_stock']
        code = request.POST['product_code']
        product_image = request.FILES['product_image']
        

        product_exist = Products.objects.filter(code = code ,admin = request.session['admin']).exists()  #it returns false or true

        if not product_exist:            

            product = Products(product_name = product_name , description = description , price = price , stock = stock , image = product_image , code = code , admin_id = request.session['admin'])
            product.save()
            success_msg ='product added successfully'

        else:

            error_msg = 'product is already added'

    return render(request,'ecommerceadmin/add_product.html',{'success':success_msg,'error':error_msg})



def update_stock(request):

    pno=Products.objects.all()

    if request.method=='POST':
        pid = request.POST['pno']
        n_stock = int(request.POST['n_stock'])
        newstock = Products.objects.get(id=pid)
        newstock.stock = n_stock
        newstock.save()


    return render(request,'ecommerceadmin/update_stock.html',{'pno':pno})

def reviews(request):

    reviews = Review.objects.all()

    return render(request,'ecommerceadmin/reviews.html',{'reviews':reviews})


@login_required

def catalogue(request):

    products = Products.objects.filter(admin = request.session['admin'])
    
    return render(request,'ecommerceadmin/catalogue.html',{'products':products})

def order_history(request):

    order_history=Order_detail.objects.all()

    return render(request,'ecommerceadmin/order_history.html',{'order_history':order_history})


@login_required

def change_password(request):

    error_msg = ''
    success_msg = ''

    if request.method == 'POST':

        old_pass = request.POST['old_password']
        new_pass = request.POST['new_password']
        confirm_pass = request.POST['confirm_password']

        if new_pass == confirm_pass :

            if len(new_pass) >= 8 :

                customer = Admin.objects.get(id = request.session['admin'])

                if customer.password == old_pass :

                    # customer.password = new_pass
                    # customer.save()

                    Admin.objects.filter(id = request.session['admin']).update( password = new_pass )
                    success_msg = 'password changed successfully'

                else:
                    error_msg = 'old password is incorrect'

            else:

                error_msg = 'passwords should be 8 characters'


        else:
            error_msg = 'passwords doesn\'t match'
    return render(request,'ecommerceadmin/change_password.html',{'success':success_msg,'error':error_msg})


@login_required

def customers(request):

    customer = Customer.objects.all()
    return render(request,'ecommerceadmin/customers.html',{'customer_list':customer})

def signup(request):

    success_msg =''
    error_msg =''


    if request.method == 'POST':
        aname = request.POST['admin_name']
        aphone = request.POST['phone']
        aemail = request.POST['email']
        apassword = request.POST['password']

        email_exist = Admin.objects.filter(email = aemail).exists()

        if not email_exist:

            admin = Admin(admin_name = aname ,phone = aphone , email = aemail ,password = apassword)
            admin.save()
            success_msg = 'you registered successfully'

        else:

            error_msg = 'email is already exist'

    return render(request,'ecommerceadmin/signup.html',{'error':error_msg,'success':success_msg})

def logout(request):
    del request.session['admin']
    request.session.flush()
    return redirect('ecommerceadmin:login')

def get_product(request):
    pid = request.POST['pid']
    p_no=Products.objects.get(id=pid)
    return JsonResponse({'data':p_no.stock})

def delete_product(request,pid):
    product =Products.objects.get(id=pid)
    product.delete()
    return redirect('ecommerceadmin:catalogue')

