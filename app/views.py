from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CartItem, Favorite, Product

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('dash')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html', {'error': 'Invalid username or password. Please try again.'})

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'signup.html', {'error': 'Username already exists. Please choose a different username.'})
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'signup.html', {'error': 'Email already registered. Please use a different email.'})
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'signup.html', {'error': f'Error creating account: {str(e)}'})
    else:
        return render(request, 'signup.html', {'error': 'Invalid request method'})

@login_required(login_url='login') 
@login_required(login_url='login') 
def dash(request):
    user = request.user
    current_view = request.GET.get('view', 'products')
    products = Product.objects.all()
    
    # Get user's favorite product IDs
    user_favorites = Favorite.objects.filter(user=user).values_list('product_id', flat=True)
    favorite_products = Product.objects.filter(id__in=user_favorites)
    
    if current_view == 'cart':
        return redirect('cart')
    
    context = {
        'user': user,
        'username': user.username,
        'email': user.email,
        'current_view': current_view,
        'products': products,
        'favorite_products': favorite_products,
        'user_favorites': list(user_favorites),  # For checking in template
    }
    
    return render(request, 'dash.html', context)

@login_required(login_url='login')
def toggle_favorite(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if not created:
            # If favorite already exists, remove it
            favorite.delete()
            message = f"Removed {product.name} from favorites"
        else:
            # If favorite was just created
            message = f"Added {product.name} to favorites"
        
        # Add message for user feedback
        messages.success(request, message)
        
        # Redirect back to the same view
        current_view = request.GET.get('view', 'products')
        return redirect(f'/dash/?view={current_view}')
    
    return redirect('dash')

@login_required(login_url='login')
def add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        
        if name and description and price:
            try:
                product = Product.objects.create(
                    name=name,
                    description=description,
                    price=float(price),
                    created_by=request.user
                )
                messages.success(request, 'Product added successfully!')
                return redirect('dash')
            except Exception as e:
                messages.error(request, f'Error adding product: {str(e)}')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return redirect('dash?view=add')

@login_required(login_url='login')
def cart(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    cart_total = sum(item.quantity * item.product.price for item in cart_items)
    for item in cart_items:
        item.total_price = item.quantity * item.product.price
    context = {
        'user': user,
        'username': user.username,
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        user=request.user,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')

@login_required(login_url='login')
def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, pk=item_id, user=request.user)
        action = request.POST.get('action')
        
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
    
    return redirect('cart')

def logout_view(request):
    logout(request)
    return redirect('login')