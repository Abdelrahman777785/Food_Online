import datetime
from django.shortcuts import get_object_or_404, render ,redirect
from django.http.response import HttpResponse

from orders.models import Order
from vendor.forms import VendorForm
from .forms import UserForm, UserPasswordChangeForm
from .models import User, UserProfile
from django.contrib import messages, auth
from .utils import detectUser, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash

from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from vendor.models import Vendor
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator





# Restrict the vendor from accessing the customer page.
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page.
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied



def registerUser(request):# --> urls.py
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():

            # Create the user using the form
            #password = form.cleaned_data['password']
            #user = form.save(commit=False)
            #user.set_password(password)
            #user.role = User.CUSTOMER
            #user.save()

            # Create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()


            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)# --> utils.py
            messages.success(request, 'Your account has been registered successfully!')               #notifications
            return redirect('registerUser')
        
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/registerUser.html', context)



def registerVendor(request):# --> urls.py
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user 
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_name = slugify(vendor_name)+'-'+str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Your account has been registered successfully! please wait for the approval.')
            return redirect('registerVendor')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()


        context = {
            'form' : form,
            'v_form':v_form,
        }
    return render(request, 'accounts/registerVendor.html',context)


def activate(request, uidb64, token):# --> urls.py
    #Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activate.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('myAccount')


# # # # # # # # # # # # # # # # # #
          # Login #
# # # # # # # # # # # # # # # # # #

def login(request):# --> urls.py
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')

# # # # # # # # # # # # # # # # # #
          # Logout #
# # # # # # # # # # # # # # # # # #

def logout(request):# --> urls.py
    auth.logout(request)
    messages.info(request, 'Your are logged out.')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):# --> urls.py
    user = request.user
    redirectUrl = detectUser(user)# --> utils.py
    return redirect(redirectUrl)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')# --> models.py

    # إعداد الترقيم
    page_size = 5  # عدد الطلبات في كل صفحة
    paginator = Paginator(orders, page_size)
    page = request.GET.get('page', 1)

    try:
        page = int(page)
    except ValueError:
        page = 1  # الرجوع للصفحة الأولى في حال وجود خطأ

    page_obj = paginator.get_page(page)  # جلب الصفحة المطلوبة

    context = {
        'orders': orders,  # جميع الطلبات (إذا كنت تحتاجها في أماكن أخرى)
        'orders_count': orders.count(),
        'recent_orders': page_obj.object_list,  # الطلبات في الصفحة الحالية فقط
        'page_obj': page_obj,  # الكائن الخاص بالترقيم (يحتوي على مزيد من المعلومات)
    }
    return render(request, 'accounts/custDashboard.html', context)

 
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):# --> urls.py
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('-created_at')
    # إعداد الترقيم
    page_size = 5
    paginator = Paginator(orders, page_size)
    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except ValueError:
        page = 1
    page_obj = paginator.get_page(page)
    # current month's revenue
    current_month = datetime.datetime.now().month
    current_month_orders = orders.filter(vendors__in=[vendor.id],created_at__month=current_month)
    current_month_revenue = 0
    for i in current_month_orders:
        current_month_revenue += i.get_total_by_vendor()['grand_total']

    # total revenue
    total_revenue = 0
    for i in orders:
        total_revenue += i.get_total_by_vendor()['grand_total']

    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': page_obj.object_list,
        'page_obj': page_obj,
        'total_revenue': total_revenue,
        'current_month_revenue': current_month_revenue,
    }
    return render(request, 'accounts/vendorDashboard.html', context)



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():   #check email in database
            user = User.objects.get(email__exact=email)

            # send rest password email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')



# # # # # # # # # # # # # # # # # #
       # Reset Password #
# # # # # # # # # # # # # # # # # #

def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')



# # # # # # # # # # # # # # # # # #
    # Change Password #
# # # # # # # # # # # # # # # # # #

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def change_password(request):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        form = UserPasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserPasswordChangeForm(user)

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'accounts/change_password.html', context)

