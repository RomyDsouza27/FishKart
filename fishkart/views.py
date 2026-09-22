from django.shortcuts import  render, redirect
from .forms import NewCustomerForm, SearchForm
from django.contrib.auth import login, authenticate,  logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages #import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q, Prefetch
from .models import User, Fishlist, Cart, Customer, Restaurant, Orders
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.db.models import Sum
import json
import razorpay
from django.http import JsonResponse
from django.shortcuts import redirect
from django.conf import settings
from .models import Restaurant, Orders, Cart
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import constant_time_compare
import hmac
import hashlib
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import  Cart
from django.contrib import messages
from django.views.generic.edit import FormView
from django.urls import reverse



logging.basicConfig(level=logging.INFO)


class CustomerRegisterView(CreateView):
    model = User
    form_class=NewCustomerForm
    template_name = 'registerCustomer.html'
    def form_valid(self, form):
        user = form.save()
        return redirect('/')

def homeview(request):
    return Home.as_view()(request)

def loginview(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                print(f"Redirecting to: {reverse('fishkart:home')}")  # Debug
                return redirect('fishkart:home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="loginCustomer.html", context={"login_form": form})

def order_list_restaurant(request):
    if not request.user.is_restaurant:
        return redirect('/')
    orders = Orders.objects.filter(restaurant_id__user=request.user).select_related('customer_id')

    order_data = []
    for order in orders:
        order_data.append({
            'order_id': order.order_id,
            'customer_name': order.customer_id.cus_name,
            'address': order.shipping_info.get("address", "N/A") if isinstance(order.shipping_info, dict) else order.shipping_info,
        })

    return render(request, 'orderlist2.html', {'orders': order_data})
def track_delivery(request):
    if not request.user.is_authenticated or not request.user.is_delivery:
        return redirect('/')
    return render(request, 'trackDel.html')
class Fishlistlist( UserPassesTestMixin, ListView,LoginRequiredMixin):
    def test_func(self):
        return self.request.user.is_restaurant
    model=Fishlist
    template_name='orderlist2.html'
    def get_queryset(self):
        return Fishlist.objects.filter(restaurant_id=self.request.user)

class AddFood(UserPassesTestMixin, CreateView, LoginRequiredMixin):
    def test_func(self):
        return self.request.user.is_restaurant
    model = Fishlist
    fields = ['fish_name', 'description', 'fish_image', 'price']  # Corrected
    template_name = 'updatefood.html'
    def form_valid(self, form):
        form.instance.restaurant_id = self.request.user
        return super().form_valid(form)
    success_url = '/resthome'

class UpdateFood(UserPassesTestMixin, UpdateView, LoginRequiredMixin):
    def test_func(self):
        return self.request.user.is_restaurant
    model = Fishlist
    fields = ['fish_name', 'description', 'fish_image', 'price']  # Corrected
    template_name = 'updatefood.html'
    success_url = '/resthome'
class DeleteFood( UserPassesTestMixin, DeleteView, LoginRequiredMixin):
    def test_func(self):
        return self.request.user.is_restaurant
    model=Fishlist
    template_name='deletefood.html'
    success_url='/resthome'

class Home(UserPassesTestMixin, ListView, LoginRequiredMixin):
    def test_func(self):
        return self.request.user.is_customer

    model = Fishlist
    context_object_name = 'Fishlist_all'
    queryset = Fishlist.objects.all()
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['search'] = SearchForm(self.request.GET or None)
        context['search_res'] = None
        context['msg'] = ''

        # Search functionality
        food = self.request.GET.get('search', '')
        if food:
            if Fishlist.objects.filter(fish_name__icontains=food).exists():
                context['search_res'] = Fishlist.objects.filter(fish_name__icontains=food)
                context['msg'] = "Here's what we found for you: "
            else:
                context['msg'] = "Sorry! We could not find your dish :("

        # Categorized products
        context['main_products'] = Fishlist.objects.filter(main_product=True, sold_out=False)
        context['featured_products'] = Fishlist.objects.filter(featured=True, sold_out=False)
        context['sold_out_products'] = Fishlist.objects.filter(sold_out=True)

        return context
class DelHome( UserPassesTestMixin, LoginRequiredMixin, View):
    template_name='homeDel.html'
    def test_func(self):
        return self.request.user.is_delivery
    def get(self, request):
        return render(request, self.template_name, context={'msg': ""})
def takeorderview(request, q=None):
    if not request.user.is_authenticated or not request.user.is_delivery:
        return redirect('/')
    return render(request=request, template_name="deliveryinprocess.html", context={"orderid": q})

class DetailFood( UserPassesTestMixin, DetailView,LoginRequiredMixin):
    model=Fishlist
    template_name='Detail.html'
    def test_func(self):
        return self.request.user.is_customer

@login_required
def additemview(request, item_id):
    fishlist_item = get_object_or_404(Fishlist, id=item_id)
    
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            weight = int(request.POST.get('weight', 1000))
        except (ValueError, TypeError):
            messages.error(request, "Invalid quantity or weight")
            return redirect('fishkart:detail', pk=item_id)
        
        # Validate inputs
        if quantity < 1:
            messages.error(request, "Quantity must be at least 1")
            return redirect('fishkart:detail', pk=item_id)
        if weight not in [250, 500, 750, 1000]:
            messages.error(request, "Invalid weight")
            return redirect('fishkart:detail', pk=item_id)
        
        # Add to cart
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            fish_item=fishlist_item,
            weight=weight,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f"Added {fishlist_item.fish_name} ({weight} grams) to cart")
        return redirect('fishkart:mycart')
    else:
        messages.error(request, "Invalid request method")
        return redirect('fishkart:detail', pk=item_id)

class MyCart(UserPassesTestMixin, ListView, LoginRequiredMixin):
    def test_func(self):
        return self.request.user.is_customer
    template_name = "Cart.html"
    model = Cart

    def get_queryset(self):
        items = Cart.objects.filter(user=self.request.user).select_related('fish_item')
        object_list = []
        for ob in items:
            obj = ob.fish_item
            object_list.append({
                'food_name': obj.fish_name,
                'price': obj.price * ob.weight / 1000,  # Scale price by weight
                'quantity': ob.quantity,
                'weight': ob.weight,
                'id': ob.pk,
                'fish_image': obj.fish_image.url if obj.fish_image else None  # Add fish_image URL
            })
        return object_list
class CartDelete(UserPassesTestMixin, DeleteView, LoginRequiredMixin):
    def test_func(self):
        return self.request.user.is_customer
    template_name="Cart.html"
    model=Cart
    success_url='/mycart'
class PastOrderlist(UserPassesTestMixin, ListView, LoginRequiredMixin):
    def test_func(self):
        return self.request.user.is_customer
    model = Orders
    template_name = 'pastorders.html'
    def get_queryset(self):
        orders = Orders.objects.filter(customer_id=self.request.user).select_related('restaurant_id')
        res = []
        for o in orders:
            r = o.restaurant_id
            res.append({'order_id': o.order_id, 'rest_name': r.res_name, 'items': o.items})
        print(res)
        return res
def ordersummaryview(request):
    if not request.user.is_authenticated or not request.user.is_customer:
        return redirect('/')
    info = {}
    cust = Customer.objects.get(user=request.user)
    info['cust_id'] = request.user.pk
    info['cust_name'] = cust.cus_name
    cart_items = Cart.objects.filter(user=request.user).select_related('fish_item__restaurant_id')
    restaurants = {}
    total_amount = 0
    for cart in cart_items:
        fishlist_item = cart.fish_item
        restaurant_user = fishlist_item.restaurant_id
        try:
            restaurant = Restaurant.objects.get(user=restaurant_user)
        except Restaurant.DoesNotExist:
            print(f"Warning: No Restaurant found for User ID {restaurant_user.id}")
            continue
        restaurant_id = restaurant_user.pk
        if restaurant_id not in restaurants:
            restaurants[restaurant_id] = {
                'items': {},
                'rest_name': restaurant.res_name,
                'rest_id': restaurant_user.pk,
                'pickuplat': str(restaurant.latitude or 0.0),
                'pickuplong': str(restaurant.longitude or 0.0),
                'address': restaurant.addresses
            }
        item_price = (fishlist_item.price * cart.weight / 1000) * cart.quantity
        restaurants[restaurant_id]['items'][fishlist_item.fish_name] = {
            'price': item_price,
            'quantity': cart.quantity,
            'weight': cart.weight,
            'fish_image': fishlist_item.fish_image.url  # Add fish image URL
        }
        total_amount += item_price
    info['rest'] = bool(restaurants)
    if not restaurants:
        return render(request, 'order.html', {
            'info': info,
            'rests': {},
            'subtotal': '0.00',
            'total': '0.00',
            'total_amount_paise': 0,
            'razorpay_order_id': None,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID
        })
    total_amount_paise = int(total_amount * 100)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = client.order.create({
        'amount': total_amount_paise,
        'currency': 'INR',
        'payment_capture': 1
    })
    context = {
        'info': info,
        'rests': restaurants,
        'subtotal': f'{total_amount:.2f}',
        'total': f'{total_amount:.2f}',
        'total_amount_paise': total_amount_paise,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID
    }
    return render(request, 'order.html', context)
def restcheckorderview(request, q=None):
    if not request.user.is_authenticated or not request.user.is_restaurant:
        return redirect('/')
    return render(request=request, template_name="handleOrder.html", context={"orderid":q})
def trackordersview(request):
    if not request.user.is_authenticated or not request.user.is_customer:
        return redirect('/')
    orders = Orders.objects.filter(customer_id=request.user).select_related('restaurant_id')
    order_list = [
        {
            'order_id': order.order_id,
            'restaurant_name': order.restaurant_id.res_name,
            'items': order.items,
            'payment_method': order.payment_method,
            'shipping_info': order.shipping_info,
            'created_at': order.id
        } for order in orders
    ]
    return render(request, 'orderlist.html', {'orders': order_list})


@csrf_exempt
def successorderview(request):
    if not request.user.is_authenticated or not request.user.is_customer:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            logging.info("Received payload: %s", data)
            payment_method = data.get("payment_method", "razorpay")
            rests = data.get("rests", {})
            shipping_info = data.get("shipping_info", {})
            if not rests:
                logging.error("No items in order: %s", data)
                return JsonResponse({'error': 'No items in order'}, status=400)

            if payment_method == "razorpay":
                razorpay_payment_id = data.get("razorpay_payment_id")
                razorpay_order_id = data.get("razorpay_order_id")
                razorpay_signature = data.get("razorpay_signature")
                if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature]):
                    logging.error("Missing Razorpay fields")
                    return JsonResponse({'error': 'Missing Razorpay payment details'}, status=400)
                generated_signature = hmac.new(
                    settings.RAZORPAY_KEY_SECRET.encode(),
                    f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
                    hashlib.sha256
                ).hexdigest()
                if not constant_time_compare(generated_signature, razorpay_signature):
                    logging.error("Signature mismatch")
                    return JsonResponse({'error': 'Signature mismatch'}, status=400)

            for order_id, data in rests.items():
                restaurant_user = data['rest_id']
                try:
                    restaurant = Restaurant.objects.get(user=restaurant_user)
                    order = Orders.objects.create(
                        order_id=order_id,
                        restaurant_id=restaurant,
                        customer_id=request.user,
                        items=data['items'],
                        payment_method=payment_method,
                        shipping_info=shipping_info,
                        status=0  # Set initial status
                    )
                    # Sync to Firebase
                    ref = db.reference(f'Orders/{order_id}')
                    ref.set({
                        'cust_name': request.user.customer.cus_name,
                        'del_lat': float(shipping_info.get('latitude', 0.0)),
                        'del_long': float(shipping_info.get('longitude', 0.0)),
                        'curr_status': 0,
                        'item_list': data['items'],
                        'restaurant_id': str(restaurant_user.pk)
                    })
                    logging.info(f"Synced order {order_id} to Firebase: {data['items']}")
                except Restaurant.DoesNotExist:
                    logging.error("Restaurant not found: %s", data)
                    return JsonResponse({'error': f'Restaurant not found: {restaurant_user}'}, status=404)
                except Exception as e:
                    logging.error(f"Firebase sync error for order {order_id}: {str(e)}")
                    return JsonResponse({'error': f'Firebase sync failed: {str(e)}'}, status=500)

            Cart.objects.filter(user=request.user).delete()
            logging.info("Order placed successfully for user: %s", request.user)
            return JsonResponse({'status': 'success', 'message': 'Order placed successfully!'})
        except json.JSONDecodeError as e:
            logging.error("JSON parsing error: %s", str(e))
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
        except Exception as e:
            logging.error("Error in successorderview: %s", str(e))
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)






def order_status(request, order_id):
    order = Orders.objects.get(order_id=order_id, customer_id=request.user)
    return render(request, 'orderstatus.html', {'orderid': order.order_id})

def home_delivery(request):
    if not request.user.is_delivery:
        return redirect('/')
    return render(request, 'homeDel.html', {'msg': 'Available Orders'})


def handle_order(request):
    if not request.user.is_restaurant:
        return redirect('/')
    
    # Fetch all orders for the restaurant
    orders = Orders.objects.filter(restaurant_id__user=request.user).select_related('customer_id')
    
    # Prepare order data for the template
    order_data = [
        {
            'order_id': order.order_id,
            'customer_name': order.customer_id.cus_name,
            'shipping_info': order.shipping_info,
            'items': order.items,
            'status': order.status if hasattr(order, 'status') else 0
        }
        for order in orders
    ]
    
    print(f"Orders for restaurant {request.user.username}: {order_data}")  
    return render(request, 'handleOrder.html', {'orders': order_data})
def finishorderview(request, q=None):
    if data.status == 'success':
                return redirect('fishkart:home')  

def logout_request(request):
    logout(request)
    return redirect('/')




