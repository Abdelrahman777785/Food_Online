from datetime import date, datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import UserProfile

from .context_processors import get_cart_amounts, get_cart_counter

from menu.models import Category, FoodItem

from vendor.models import Vendor ,OpeningHour
from django.db.models import Prefetch
from .models import Cart
from django.contrib.auth.decorators import login_required
from orders.forms import OrderForm
from django.core.paginator import Paginator ,EmptyPage



def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    # Filter vendors based on the search query ?

    # paginator #
    # Create a Paginator object with the list of vendors and the desired page size
    page_size = 5  # عدد الطلبات في كل صفحة
    paginator = Paginator(vendors, page_size)
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
        'vendors': page_obj.object_list,
        'vendor_count':vendor_count,
        'page_obj': page_obj,
    }
    return render(request, 'marketplace/listings.html', context)

 


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)

    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset= FoodItem.objects.filter(is_available=True)
        )
    )

    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day','-from_hour')
    
    # Check current day's opening hours.
    today_date = date.today()
    today = today_date.isoweekday()

    current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=today)
   
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
        'opening_hours': opening_hours,
        'current_opening_hours': current_opening_hours,
        
    }
    return render(request, 'marketplace/vendor_detail.html', context)



def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            # Check if the food item exists.
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'success', 'message': 'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    # Create a new entry in the cart table for this user and food item
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'success', 'message': 'Added the food to the cart.', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
                
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    
    else: 
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue.'})
    

def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            # Check if the food item exists.
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkCart.quantity > 1:
                        # Decrease the cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
                
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    
    else: 
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue.'})

@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        "cart_items": cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


def delete_from_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                cart_item = Cart.objects.get(user=request.user,id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({"status":"success","message":"Deleted from cart!", 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request!'})


def search(request):
    # address = request.GET['address']
    radius = request.GET['radius']
    keyword = request.GET['keyword']

    vendors = Vendor.objects.filter(vendor_name__icontains=keyword, is_approved=True, user__is_active=True)
    print(vendors)
    return render(request,'marketplace/listings.html')


 
@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    
    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address,
        'city': user_profile.city,
        'state': user_profile.state,
        'country': user_profile.country,
        'pin_code': user_profile.pin_code,
    }
    form = OrderForm(initial=default_values)
    context = {
        "form" : form,
        "cart_items" : cart_items,
        
    }
    return render(request, 'marketplace/checkout.html', context)