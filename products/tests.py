from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from .models import Brand, Category, Product, Order, OrderItem

User = get_user_model()


class BrandModelTestCase(TestCase):
    """Test cases for the Brand model."""
    
    def test_create_brand(self):
        """Test creating a brand."""
        brand = Brand.objects.create(brand_name="CeraVe")
        self.assertEqual(brand.brand_name, "CeraVe")
        self.assertIsNotNone(brand.brand_id)
    
    def test_brand_str(self):
        """Test brand string representation."""
        brand = Brand.objects.create(brand_name="The Ordinary")
        self.assertEqual(str(brand), "The Ordinary")


class CategoryModelTestCase(TestCase):
    """Test cases for the Category model."""
    
    def test_create_category(self):
        """Test creating a category."""
        category = Category.objects.create(category_name="Moisturizers")
        self.assertEqual(category.category_name, "Moisturizers")
        self.assertIsNotNone(category.category_id)
    
    def test_category_str(self):
        """Test category string representation."""
        category = Category.objects.create(category_name="Serums")
        self.assertEqual(str(category), "Serums")


class ProductModelTestCase(TestCase):
    """Test cases for the Product model."""
    
    def setUp(self):
        """Set up test data."""
        self.brand = Brand.objects.create(brand_name="CeraVe")
        self.category = Category.objects.create(category_name="Moisturizers")
    
    def test_create_product(self):
        """Test creating a product."""
        product = Product.objects.create(
            product_name="CeraVe Moisturizing Cream",
            brand=self.brand,
            category=self.category,
            product_details="<p>Rich moisturizing cream</p>",
            price=Decimal("1250.00"),
            available_stock=50
        )
        self.assertEqual(product.product_name, "CeraVe Moisturizing Cream")
        self.assertEqual(product.price, Decimal("1250.00"))
        self.assertEqual(product.available_stock, 50)
        self.assertFalse(product.featured)
    
    def test_product_is_in_stock(self):
        """Test product stock checking."""
        product = Product.objects.create(
            product_name="Test Product",
            brand=self.brand,
            category=self.category,
            product_details="Test",
            price=Decimal("100.00"),
            available_stock=10
        )
        self.assertTrue(product.is_in_stock())
        
        product.available_stock = 0
        self.assertFalse(product.is_in_stock())
    
    def test_product_stock_status(self):
        """Test product stock status messages."""
        product = Product.objects.create(
            product_name="Test Product",
            brand=self.brand,
            category=self.category,
            product_details="Test",
            price=Decimal("100.00"),
            available_stock=20
        )
        self.assertEqual(product.get_stock_status(), "In Stock")
        
        product.available_stock = 5
        self.assertEqual(product.get_stock_status(), "Low Stock (5 left)")
        
        product.available_stock = 0
        self.assertEqual(product.get_stock_status(), "Out of Stock")


class OrderModelTestCase(TestCase):
    """Test cases for the Order model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            email="test@example.com",
            phone_number="01712345678",
            first_name="John",
            last_name="Doe",
            house_number="123",
            road_number="45",
            postal_code="1234",
            district="Dhaka",
            password="testpass123"
        )
        self.brand = Brand.objects.create(brand_name="CeraVe")
        self.category = Category.objects.create(category_name="Moisturizers")
        self.product = Product.objects.create(
            product_name="Test Product",
            brand=self.brand,
            category=self.category,
            product_details="Test",
            price=Decimal("500.00"),
            available_stock=50
        )
    
    def test_create_order(self):
        """Test creating an order."""
        order = Order.objects.create(user=self.user)
        self.assertEqual(order.user, self.user)
        self.assertTrue(order.in_cart)
        self.assertIsNone(order.completed_at)
    
    def test_order_total_items(self):
        """Test calculating total items in order."""
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=3,
            price_at_purchase=self.product.price
        )
        self.assertEqual(order.get_total_items(), 3)
    
    def test_order_total_price(self):
        """Test calculating total price of order."""
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            price_at_purchase=Decimal("500.00")
        )
        self.assertEqual(order.get_total_price(), Decimal("1000.00"))
    
    def test_complete_order(self):
        """Test completing an order and stock update."""
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=5,
            price_at_purchase=self.product.price
        )
        
        initial_stock = self.product.available_stock
        success = order.complete_order()
        
        self.assertTrue(success)
        self.assertFalse(order.in_cart)
        self.assertIsNotNone(order.completed_at)
        
        # Refresh product from database
        self.product.refresh_from_db()
        self.assertEqual(self.product.available_stock, initial_stock - 5)
    
    def test_complete_order_insufficient_stock(self):
        """Test order completion fails with insufficient stock."""
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=100,  # More than available
            price_at_purchase=self.product.price
        )
        
        success = order.complete_order()
        self.assertFalse(success)
        self.assertTrue(order.in_cart)  # Should still be in cart


class OrderItemModelTestCase(TestCase):
    """Test cases for the OrderItem model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            email="test@example.com",
            phone_number="01712345678",
            first_name="John",
            last_name="Doe",
            house_number="123",
            road_number="45",
            postal_code="1234",
            district="Dhaka",
            password="testpass123"
        )
        self.brand = Brand.objects.create(brand_name="CeraVe")
        self.category = Category.objects.create(category_name="Moisturizers")
        self.product = Product.objects.create(
            product_name="Test Product",
            brand=self.brand,
            category=self.category,
            product_details="Test",
            price=Decimal("300.00"),
            available_stock=50
        )
        self.order = Order.objects.create(user=self.user)
    
    def test_create_order_item(self):
        """Test creating an order item."""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price_at_purchase=self.product.price
        )
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price_at_purchase, Decimal("300.00"))
    
    def test_order_item_subtotal(self):
        """Test calculating order item subtotal."""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3,
            price_at_purchase=Decimal("300.00")
        )
        self.assertEqual(order_item.get_subtotal(), Decimal("900.00"))
    
    def test_order_item_auto_price(self):
        """Test automatic price setting on save."""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1
        )
        # Price should be automatically set from product
        order_item.refresh_from_db()
        self.assertEqual(order_item.price_at_purchase, self.product.price)
