from django.conf import settings
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView, DetailView,View
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, OrderItem ,Order, BillingAddress
from .forms import CheckoutForm
# Create your views here.

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class StoreView(ListView):
    model=Item
    template_name="store/store.html"


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            
            context={
                'object':order
            }
            
            return render(self.request, 'store/cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You dont have an active order")
            return redirect("/")

def product(request):
    context={}
    return render(request,'store/product.html',context)

class ProductDetailView(DetailView):
    model=Item
    template_name='store/product.html'

def cart(request):
    context={}
    return render(request, 'store/cart.html', context)

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        template_name = 'store/checkout.html'
        context = {
            'form': form
        }
        return render(self.request, template_name , context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address=form.cleaned_data.get('street_address')
                apartment_address=form.cleaned_data.get('apartment_address')
                country=form.cleaned_data.get('country')
                zip=form.cleaned_data.get('zip')
                #TODO: add functionality for these fields
                # same_shipping_address=form.cleaned_data.get('same_billing_address')
                # save_info=form.cleaned_data.get('save_info')
                payment_option=form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO: add redirect to the selected payment option
                return redirect('store:checkout')
            messages.warning(self.request, "Failed checkout")
            return redirect('store:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect('store:checkout')
        
class Payment(View):
    def get(self, *args, **kwargs):
        template_name = 'store/payment.html'
        return render(self.request, template_name)
    
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripToken')
        stripe.Charge.create(
            amount = order.get_total() *100, #cents
            currency = "ksh", 
            source=token, #obtained with strip.js
        )

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item,
                                                 user=request.user, 
                                                 ordered=False
                                                 )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1 
            order_item.save()
            messages.info(request, "Item quantity was updated") 
            return redirect ("store:cart")
            
        else:
            messages.info(request, "Item was added to cart")
            order.items.add(order_item)
            return redirect ("store:cart")
            
    else:
        ordered_date = timezone.now()
        order=Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item was added to cart")
        
    return redirect ("store:product")

@login_required
def remove_from_cart(request, slug):
    item=get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item= OrderItem.objects.filter(
                item=item,
                user=request.user, 
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "Item was removed from your cart")
            return redirect ("store:cart")

        else:
            # add message saying order doesnt contain the item
            messages.info(request, "order does not contain the item")
            return redirect ("store:product", slug=slug)
            
    else:
        # add message saying user doesnt have an order
        messages.info(request, "You do not have an order")
        return redirect ("store:product", slug=slug)
    return redirect ("store:product", slug=slug)
            
@login_required
def remove_single_item_from_cart(request, slug):
    item=get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item= OrderItem.objects.filter(
                item=item,
                user=request.user, 
                ordered=False
            )[0]
            if order_item.quantity >1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "Item quantity was updated")
            return redirect('store:cart')

        else:
            # add message saying order doesnt contain the item
            messages.info(request, "order doesnt contain the item")
            return redirect ("store:product", slug=slug)
            
    else:
        # add message saying user doesnt have an order
        messages.info(request, "You do not have an order")
        return redirect ("store:product", slug=slug)
    return redirect ("store:product", slug=slug)
                  
    
# def store(request):
#     context={
#         'items': Item.objects.all()
#     }
#     return render(request,'store/store.html',context)

