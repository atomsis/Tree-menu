from django.test import TestCase
from .models import MenuItem
from django.template import Context, Template
from .templatetags.menu_tags import draw_menu
from django.urls import reverse
from .forms import MenuItemForm

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class MenuItemModelTest(TestCase):
    def test_str_representation(self):
        menu_item = MenuItem(title='Test Item')
        self.assertEqual(str(menu_item), 'Test Item')

    def test_menu_item_creation(self):
        menu_item = MenuItem.objects.create(title='Test Item', url='/test/')
        self.assertEqual(menu_item.title, 'Test Item')
        self.assertEqual(menu_item.url, '/test/')


class DrawMenuTagTest(TestCase):
    def setUp(self):
        self.menu = MenuItem.objects.create(title='Test Menu', url='/menu/')
        self.child_item = MenuItem.objects.create(title='Child Item', url='/child/', parent=self.menu)

    def test_draw_menu_tag(self):
        template = Template("{% load menu_tags %}{% draw_menu 'Test Menu' %}")
        context = Context()
        rendered = template.render(context)
        self.assertInHTML('<a href="/menu/">Test Menu</a>', rendered)
        self.assertInHTML('<a href="/child/">Child Item</a>', rendered)


class MenuViewsTest(TestCase):
    def setUp(self):
        self.menu = MenuItem.objects.create(title='Test Menu', url='/menu/')
        self.child_item = MenuItem.objects.create(title='Child Item', url='/child/', parent=self.menu)

    def test_menu_detail_view(self):
        response = self.client.get(reverse('menu_detail', args=[self.menu.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Menu')
        self.assertContains(response, 'Child Item')

class MenuItemFormTest(TestCase):
    def test_menu_item_form_valid_data(self):
        form_data = {'title': 'Test Item', 'url': '/test/'}
        form = MenuItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_menu_item_form_invalid_data(self):
        form_data = {'title': '', 'url': '/test/'}
        form = MenuItemForm(data=form_data)
        self.assertFalse(form.is_valid())

class MenuIntegrationTest(StaticLiveServerTestCase):
    def setUp(self):
        self.menu = MenuItem.objects.create(title='Test Menu', url='/menu/')
        self.child_item = MenuItem.objects.create(title='Child Item', url='/child/', parent=self.menu)

        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_menu_integration(self):
        self.browser.get(self.live_server_url + reverse('menu_detail', args=[self.menu.id]))
        self.assertIn('Test Menu', self.browser.title)
        self.assertIn('Child Item', self.browser.page_source)