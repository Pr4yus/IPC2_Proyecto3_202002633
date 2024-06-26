"""
URL configuration for empresa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from webapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    path('grabarConfiguracion/', views.grabarConfiguracion, name='grabarConfiguracion'),
    path('grabarTransacciones/', views.grabarTransaccion, name='grabarTransaccion'),
    path('devolverEstadoCuenta/', views.devolverEstadoCuenta, name='devolverEstadoCuenta'),
    path('devolverResumenPagos/', views.devolverResumenPagos, name='devolverResumenPagos'),
    path('borrarDatos/', views.borrarDatos, name='borrar datos'),
    path('ayuda/', views.ayuda, name= 'ayuda')

    # Otros patrones de URL aquí...

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
