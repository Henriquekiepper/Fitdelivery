from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Assumindo que você tem um modelo Product - ajuste conforme necessário
# from .models import Product

def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')
        else:
            return render(request, 'register.html', {'user_form': user_form})
    else:
        user_form = UserCreationForm()
        return render(request, 'register.html', {'user_form': user_form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('supplement_list')
        else:
            login_form = AuthenticationForm()
    else:
        login_form = AuthenticationForm()
    return render(request, 'login.html', {'login_form': login_form})

def logout_view(request):
    logout(request)
    return redirect('supplement_list')

# ===== VIEWS DO CARRINHO =====

def cart_view(request):
    """
    Renderiza a página do carrinho
    O carrinho é gerenciado pelo localStorage no frontend
    """
    return render(request, 'cart.html')

def add_to_cart_session(request, product_id):
    """
    ALTERNATIVA: Adiciona produto ao carrinho usando sessões Django
    Use esta função se quiser gerenciar o carrinho no backend
    """
    if request.method == 'POST':
        # Descomente e ajuste estas linhas se você tiver um modelo Product
        # product = get_object_or_404(Product, id=product_id)
        
        # Para demonstração, vamos usar dados fictícios
        # Substitua por seus dados reais do produto
        product_data = {
            'id': product_id,
            'name': f'Produto {product_id}',  # Substitua pela consulta real
            'price': 99.99,  # Substitua pelo preço real
            'image': '/static/images/default.jpg'  # Substitua pela imagem real
        }
        
        # Inicializa o carrinho na sessão se não existir
        if 'cart' not in request.session:
            request.session['cart'] = {}
        
        cart = request.session['cart']
        
        # Adiciona ou atualiza o produto no carrinho
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            cart[str(product_id)] = {
                'name': product_data['name'],
                'price': product_data['price'],
                'image': product_data['image'],
                'quantity': 1
            }
        
        request.session['cart'] = cart
        request.session.modified = True
        
        # Se for uma requisição AJAX, retorna JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True, 
                'message': 'Produto adicionado ao carrinho!',
                'cart_count': sum(item['quantity'] for item in cart.values())
            })
        
        # Se não for AJAX, redireciona para o carrinho
        return redirect('cart')
    
    return redirect('supplement_list')

def get_cart_session(request):
    """
    ALTERNATIVA: Retorna dados do carrinho da sessão
    Use se estiver gerenciando o carrinho no backend
    """
    cart = request.session.get('cart', {})
    
    cart_items = []
    total = 0
    
    for product_id, item_data in cart.items():
        item_total = item_data['price'] * item_data['quantity']
        total += item_total
        
        cart_items.append({
            'id': int(product_id),
            'name': item_data['name'],
            'price': item_data['price'],
            'image': item_data['image'],
            'quantity': item_data['quantity'],
            'total': item_total
        })
    
    return JsonResponse({
        'cart_items': cart_items,
        'total': total,
        'count': sum(item['quantity'] for item in cart_items)
    })

def update_cart_session(request):
    """
    ALTERNATIVA: Atualiza quantidade de produto no carrinho (sessão)
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))
        quantity = int(data.get('quantity', 1))
        
        if 'cart' in request.session and product_id in request.session['cart']:
            if quantity > 0:
                request.session['cart'][product_id]['quantity'] = quantity
            else:
                del request.session['cart'][product_id]
            
            request.session.modified = True
            
            return JsonResponse({'success': True, 'message': 'Carrinho atualizado!'})
    
    return JsonResponse({'success': False, 'message': 'Erro ao atualizar carrinho'})

def remove_from_cart_session(request, product_id):
    """
    ALTERNATIVA: Remove produto do carrinho (sessão)
    """
    if 'cart' in request.session and str(product_id) in request.session['cart']:
        del request.session['cart'][str(product_id)]
        request.session.modified = True
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Produto removido!'})
        
        return redirect('cart')
    
    return redirect('cart')

def clear_cart_session(request):
    """
    ALTERNATIVA: Limpa todo o carrinho (sessão)
    """
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Carrinho limpo!'})
    
    return redirect('cart')

# ===== VIEW PARA LISTAR PRODUTOS (EXEMPLO) =====

def supplement_list(request):
    """
    Sua view de listagem de produtos
    Ajuste conforme seu modelo de dados
    """
    # Exemplo de produtos - substitua pela sua consulta real
    # products = Product.objects.all()
    
    # Para demonstração, produtos fictícios:
    products = [
        {
            'id': 1,
            'name': 'Whey Protein',
            'price': 89.99,
            'image': '/static/images/whey.jpg',
            'description': 'Proteína de alta qualidade'
        },
        {
            'id': 2,
            'name': 'Creatina',
            'price': 49.99,
            'image': '/static/images/creatina.jpg',
            'description': 'Melhora performance nos treinos'
        },
        {
            'id': 3,
            'name': 'BCAA',
            'price': 39.99,
            'image': '/static/images/bcaa.jpg',
            'description': 'Aminoácidos essenciais'
        }
    ]
    
    return render(request, 'supplement_list.html', {'products': products})

# ===== FUNÇÕES AUXILIARES =====

def get_cart_count(request):
    """
    Retorna a quantidade total de itens no carrinho
    Útil para mostrar no header/navbar
    """
    if 'cart' in request.session:
        return sum(item['quantity'] for item in request.session['cart'].values())
    return 0

# Context processor para mostrar contador do carrinho em todos os templates
def cart_context_processor(request):
    """
    Adicione esta função em settings.py em TEMPLATES['OPTIONS']['context_processors']
    para ter acesso ao contador do carrinho em todos os templates
    """
    return {
        'cart_count': get_cart_count(request)
    }

def cart(request):
    return render(request, 'cart.html')