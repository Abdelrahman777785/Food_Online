import simplejson as json
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.forms import UserInForm, UserProfileForm
from accounts.models import UserProfile
from marketplace.models import Cart
from orders.models import Order, OrderedFood
from django.core.paginator import Paginator ,EmptyPage


@login_required(login_url='login')
def cprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile updated')
            return redirect('cprofile')
        else:
            print(profile_form.errors)
            print(user_form.errors)

    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInForm(instance=request.user)

    

    context = {
        'profile_form':profile_form,
        'user_form':user_form,
        'profile':profile,
    }
    return render(request, 'customers/cprofile.html', context)


def my_orders(request):
    orders_list = Order.objects.filter(user=request.user).order_by('-created_at')

    page_size = 9  # عدد الطلبات في كل صفحة
    paginator = Paginator(orders_list, page_size)
    page = request.GET.get('page', 1)

    try:
        page = int(page)
    except ValueError:
        page = 1

    try:
        page_obj = paginator.get_page(page)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'orders_count': orders_list.count(),
        'recent_orders': page_obj.object_list,
        'page_obj': page_obj,
    }
    return render(request, 'customers/my_orders.html', context)

def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        
        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price * item.quantity)

        tax_data = json.loads(order.tax_data)
        context = {
            'order':order,
            'ordered_food':ordered_food,
            'subtotal':subtotal,
            'tax_data':tax_data,
        }
        
        return render(request, 'customers/order_detail.html', context)
    except:
        return redirect('customer')

    