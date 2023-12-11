from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import loader
from .models import MenuItem


def home(request):
    main_menu_items = MenuItem.objects.filter(name='main_menu', parent=None)
    return render(request, 'menu/home.html', {'main_menu_items': main_menu_items})


def draw_menu_view(request, menu_name):
    menu_items = MenuItem.objects.filter(name=menu_name, parent=None)
    context = {'menu_items': menu_items, 'menu_name': menu_name}
    return render(request, 'menu/draw_menu.html', context)
