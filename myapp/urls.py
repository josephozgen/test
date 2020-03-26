from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('create', views.create),
    path('show/<int:id>', views.show),
    #path('edit/<int:id>', views.edit),
    path('delete/<int:id>', views.delete),
    path('join/<int:id>', views.join),
    path('cancel/<int:id>', views.cancel),
    # AJAX ROUTES
    path('validemail', views.validemail),
    path('validlogin', views.validlogin)

]
