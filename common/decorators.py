from django.http import HttpResponseRedirect 
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
                                      
def login_required(func) :

    def wrapper(request, *args, **kwargs):

            if 'customer' in request.session:

                return func (request, *args, **kwargs)

            else:

                return redirect('common:login')


    return wrapper