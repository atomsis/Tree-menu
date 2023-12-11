from django.urls import path
from .views import home, draw_menu_view

urlpatterns = [
    path('', home, name='home'),
    path('draw_menu/<str:menu_name>/', draw_menu_view, name='draw_menu'),
]