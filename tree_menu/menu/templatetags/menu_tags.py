from django import template
from ..models import MenuItem

register = template.Library()

@register.inclusion_tag('menu/menu_template.html')
def draw_menu(menu_name, current_path):
    menu_items = MenuItem.objects.filter(name=menu_name, parent=None)
    expanded_menu = find_expanded_menu(menu_items, current_path)
    return {'menu_items': menu_items, 'menu_name': menu_name, 'current_path': current_path, 'expanded_menu': expanded_menu}

@register.simple_tag
def is_active(item_url, current_path):
    return 'active' if current_path == item_url else ''

def find_expanded_menu(menu_items, current_path):
    for item in menu_items:
        item.expanded = False
        if current_path.startswith(item.url):
            item.expanded = True
            return menu_items
        item.children = find_expanded_menu(item.children.all(), current_path)
    return menu_items