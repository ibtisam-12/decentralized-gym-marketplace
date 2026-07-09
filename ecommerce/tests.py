from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product, Category, Cart, CartItem, Order

class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Equipment')

    def test_product_creation(self):
        product = Product.objects.create(
            name='Dumbbell Set',
            price=99.99,
            category=self.category,
            stock=10,
            is_active=True
        )
        self.assertEqual(str(product), 'Dumbbell Set')
        self.assertTrue(product.is_active)

    def test_product_slug_generated(self):
        product = Product.objects.create(
            name='Barbell 20kg',
            price=149.99,
            category=self.category,
            stock=5,
            is_active=True
        )
        self.assertTrue(product.slug)

class CartModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.category = Category.objects.create(name='Supplements')
        self.product = Product.objects.create(
            name='Whey Protein', price=49.99, category=self.category, stock=20, is_active=True
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_cart_item_subtotal(self):
        self.assertEqual(self.cart_item.subtotal, 99.98)

    def test_cart_total(self):
        p2 = Product.objects.create(
            name='Creatine', price=29.99, category=self.category, stock=15, is_active=True
        )
        CartItem.objects.create(cart=self.cart, product=p2, quantity=1)
        self.assertEqual(self.cart.total, 129.97)
