from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from provider_api.models import Provider, Product, COMMISSION_RATE, Order
from django.contrib.auth.decorators import login_required
from functools import wraps


def valid_provider_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if Provider.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)
        messages.add_message(request, messages.warning, '請先登入')
        return redirect('provider_system:login')
    return wrapper


@login_required(login_url='provider_system:login')
@valid_provider_required
def home_view(request):
    """
    提供商家管理功能（查看與修改商家資訊，查看、新增、修改與刪除商品資訊．）
    """
    provider = Provider.objects.get(user=request.user)
    products = Product.objects.filter(provider=provider)
 
    page_name = 'home'
    return render(request, 'home.html', locals())
    


def login_view(request):
    """
    提供商家登入功能
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and Provider.objects.filter(user=user).exists():
            login(request, user)
            return redirect('provider_system:home')  
        else:
            messages.add_message(request, messages.WARNING, '帳號或密碼錯誤')
    return render(request, 'login.html')


def register_view(request):
    """
    提供商家註冊功能
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        shop_name = request.POST['shop_name']
        phone = request.POST['phone']
        address = request.POST['address']
        img_url = request.POST['image_url']
        category = request.POST['category']
        
        if not username or not password or not password2 or not shop_name or not phone or not address or not img_url or not category:
            messages.add_message(request, messages.WARNING, '請填寫所有欄位')
            return redirect('provider_system:register')
        
        if password != password2:
            messages.add_message(request, messages.WARNING, '密碼不一致')
            return redirect('provider_system:register')
        
        try:
            if User.objects.filter(username=username).exists():
                messages.add_message(request, messages.WARNING, '帳號已存在')
                return redirect('provider_system:register')
        
        
            user = User.objects.create_user(username=username, password=password)
            provider = Provider.objects.create(user=user, shop_name=shop_name, phone=phone, address=address, image_url=img_url, category=category)
        except Exception as e:
            messages.add_message(request, messages.WARNING, '註冊失敗，請檢查資料是否符合格式')
            return redirect('provider_system:register')
        
        messages.add_message(request, messages.SUCCESS, '註冊成功')
        return redirect('provider_system:login')  
    return render(request, 'register.html')


@login_required(login_url='provider_system:login')
@valid_provider_required
def logout_view(request):
    """
    提供商家登出功能
    """
    logout(request)
    messages.add_message(request, messages.SUCCESS, '登出成功')
    return redirect('provider_system:login')


@login_required(login_url='provider_system:login')
@valid_provider_required
def profile_edit_view(request):
    """
    提供商家修改資訊功能
    """
    provider = Provider.objects.get(user=request.user)
    
    if request.method == 'POST':
        shop_name = request.POST['shop_name']
        phone = request.POST['phone']
        address = request.POST['address']
        img_url = request.POST['image_url']
        category = request.POST['category']
        
        if not shop_name or not phone or not address or not img_url or not category:
            messages.add_message(request, messages.WARNING, '請填寫所有欄位')
            return redirect('provider_system:profile_edit')
        
        try:
            provider.shop_name = shop_name
            provider.phone = phone
            provider.address = address
            provider.image_url = img_url
            provider.category = category
            provider.save()
            messages.add_message(request, messages.SUCCESS, '修改成功')
            return redirect('provider_system:home')
        except Exception as e:
            messages.add_message(request, messages.WARNING, '修改失敗，請檢查資料是否符合格式')   
    
    page_name = 'home'
    return render(request, 'profile_edit.html', locals())


@login_required(login_url='provider_system:login')
@valid_provider_required
def product_edit_view(request, product_id):
    """
    提供商家修改商品資訊功能
    """
    provider = Provider.objects.get(user=request.user)
    try:
        product = Product.objects.get(id=product_id, provider=provider)
    except Product.DoesNotExist:
        messages.add_message(request, messages.WARNING, '商品不存在')
        return redirect('provider_system:home')
    except Exception as e:
        messages.add_message(request, messages.WARNING, '讀取失敗')
        return redirect('provider_system:home')
    
    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST['price']
        description = request.POST['description']
        
        if not name or not price or not description:
            messages.add_message(request, messages.WARNING, '請填寫所有欄位')
            return redirect('provider_system:product_edit', product_id=product_id)
        
        try:
            product.name = name
            product.price = price
            product.description = description
            product.save()
            messages.add_message(request, messages.SUCCESS, '修改成功')
            return redirect('provider_system:home')
        except Exception as e:
            messages.add_message(request, messages.WARNING, '修改失敗，請檢查資料是否符合格式')
            return redirect('provider_system:product_edit', product_id=product_id)
    
    page_name = 'home'
    return render(request, 'product_edit.html', locals())


@login_required(login_url='provider_system:login')
@valid_provider_required
def product_create_view(request):
    """
    提供商家新增商品功能
    """
    provider = Provider.objects.get(user=request.user)
    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST['price']
        description = request.POST['description']
        
        if not name or not price or not description:
            messages.add_message(request, messages.WARNING, '請填寫所有欄位')
            return redirect('provider_system:product_create')
        
        try:
            provider = Provider.objects.get(user=request.user)
            product = Product.objects.create(provider=provider, name=name, price=price, description=description)
        except Exception as e:
            messages.add_message(request, messages.WARNING, '新增失敗，請檢查資料是否符合格式')
            return redirect('provider_system:product_create')

        messages.add_message(request, messages.SUCCESS, '新增成功')
        return redirect('provider_system:home')
    
    page_name = 'home'
    return render(request, 'product_create.html', locals())


@login_required(login_url='provider_system:login')
@valid_provider_required
def product_delete_view(request, product_id):
    """
    提供商家刪除商品功能
    """
    try:
        provider = Provider.objects.get(user=request.user)
        product = Product.objects.get(id=product_id, provider=provider)
        product.delete()
        messages.add_message(request, messages.SUCCESS, '刪除成功')
    except Product.DoesNotExist:
        messages.add_message(request, messages.WARNING, '商品不存在')
    except Exception as e:
        messages.add_message(request, messages.WARNING, '刪除失敗')
    
    return redirect('provider_system:home')


@login_required(login_url='provider_system:login')
@valid_provider_required
def orders_manage_view(request):
    """
    提供訂單管理功能
    """
    provider = Provider.objects.get(user=request.user)
    orders = provider.order_set.filter(status__in=[0, 1, 2]).order_by('-created_at')
    commission_rates = {"Deliver": int(COMMISSION_RATE * 100), "Provider": int((1 - COMMISSION_RATE) * 100)}
    
    page_name = 'orders'
    return render(request, 'orders_manage.html', locals())


@login_required(login_url='provider_system:login')
@valid_provider_required
def order_detail_view(request, order_id):
    """
    提供訂單明細功能
    """
    try:
        provider = Provider.objects.get(user=request.user)
        order = Order.objects.get(id=order_id)
        detail = order.orderdetail_set.all()
    except Order.DoesNotExist:
        messages.add_message(request, messages.WARNING, '訂單不存在')
        return redirect('provider_system:orders_manage')
    except Exception as e:
        messages.add_message(request, messages.WARNING, '讀取失敗')
        return redirect('provider_system:orders_manage')
    
    page_name = 'orders'
    return render(request, 'order_detail.html', locals())



@login_required(login_url='provider_system:login')
@valid_provider_required
def order_ready_view(request, order_id):
    """
    提供訂單準備完成功能
    """
    try:
        order = Order.objects.get(id=order_id)
        order.status = 1
        order.save()
        messages.add_message(request, messages.SUCCESS, f'訂單編號 {order.id} 已準備完成')
    except Order.DoesNotExist:
        messages.add_message(request, messages.WARNING, '訂單不存在')
    except Exception as e:
        messages.add_message(request, messages.WARNING, '操作失敗')
    
    return redirect('provider_system:orders_manage')


@login_required(login_url='provider_system:login')
@valid_provider_required
def history_view(request):
    """
    提供歷史訂單查詢功能
    """
    provider = Provider.objects.get(user=request.user)
    orders = provider.order_set.filter(status=3).order_by('-created_at')
    
    page_name = 'orders'
    return render(request, 'history.html', locals())


@login_required(login_url='provider_system:login')
@valid_provider_required
def income_view(request):
    """
    提供收入查詢功能
    """
    provider = Provider.objects.get(user=request.user)
    orders = provider.order_set.filter(status=3).order_by('-created_at')
    total_income = sum([order.provider_fee for order in orders])
    total_orders = orders.count()
    
    page_name = 'income'
    return render(request, 'income.html', locals())