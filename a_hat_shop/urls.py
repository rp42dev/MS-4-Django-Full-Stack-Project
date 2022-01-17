"""a_hat_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler400, handler403, handler404, handler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('allauth.urls')),
    path('', include('home.urls')),
    path('shop/', include('shop.urls')),
    path('cart/', include('cart.urls')),
    path('user/', include('customers.urls')),
    path('checkout/', include('checkout.urls')),
    path('review/', include('reviews.urls')),
    path('support/', include('support.urls')),
    path('manage/', include('administration.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'a_hat_shop.views.error_404'
handler500 = 'a_hat_shop.views.error_500'
handler403 = 'a_hat_shop.views.error_403'
handler400 = 'a_hat_shop.views.error_400'