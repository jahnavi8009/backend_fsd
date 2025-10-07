from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from website.models import Product, Cart, CartItem
from website.forms import AuthUserCreationForm

User = get_user_model()

# -------------------------------
# Home Page
# -------------------------------
def home(request):
    return redirect('login')


# -------------------------------
# Authentication Views
# -------------------------------
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import redirect_to_login
from django.conf import settings
from django.http import HttpResponseRedirect

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            # Use next param or LOGIN_REDIRECT_URL
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            from django.urls import reverse
            return redirect(settings.LOGIN_REDIRECT_URL if hasattr(settings, 'LOGIN_REDIRECT_URL') else reverse('product_list'))
        else:
            return render(request, "website/login.html", {"error": "Invalid credentials"})
    return render(request, "website/login.html")


def logout_view(request):
    logout(request)
    return redirect('login')


def signup_view(request):
    if request.method == "POST":
        form = AuthUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
        else:
            return render(request, "website/signup.html", {"form": form})
    else:
        form = AuthUserCreationForm()
    return render(request, "website/signup.html", {"form": form})


# -------------------------------
# Product Views
# -------------------------------
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = "website/product_list.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = "website/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'price']
    template_name = "website/product_form.html"
    success_url = reverse_lazy('product_list')


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'description', 'price']
    template_name = "website/product_form.html"
    success_url = reverse_lazy('product_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "website/product_confirm_delete.html"
    success_url = reverse_lazy('product_list')


# -------------------------------
# Cart Views
# -------------------------------
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("cart_view")


@login_required
def remove_from_cart(request, pk):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=pk)
    cart_item.delete()
    return redirect("cart_view")


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    
    cart_items = []
    total_price = 0
    for item in items:
        subtotal = item.product.price * item.quantity
        total_price += subtotal
        cart_items.append({
            "product": item.product,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return render(request, "website/cart.html", {
        "items": cart_items,
        "total_price": total_price
    })
