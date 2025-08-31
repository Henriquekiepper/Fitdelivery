# urls.py
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from accounts import views as accounts_views

from suplements.views import (
    SupplementListView,
    NewSupplementCreateView,
    SupplementDetailView,
    SupplementUpdateView
)
from accounts.views import register_view, login_view, logout_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Redireciona '/' para '/supplements/'
    path('', RedirectView.as_view(url='/supplements/', permanent=False)),

    # Admin
    path('admin/', admin.site.urls),

    # Contas
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Suplementos
    path('supplements/', SupplementListView.as_view(), name='supplement_list'),
    path('new_supplement/', NewSupplementCreateView.as_view(), name='new_supplement'),
    path('supplement/<int:pk>/', SupplementDetailView.as_view(), name='supplement_detail'),
    path('supplement/<int:pk>/update/', SupplementUpdateView.as_view(), name='supplement_update'),

    # Carrinho
    path('carrinho/', accounts_views.cart, name='cart'),

]

# Serve arquivos estáticos em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)