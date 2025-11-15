from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import User


class UserModelTestCase(TestCase):
    """Test cases for the User model."""
    
    def setUp(self):
        """Set up test data."""
        self.user_data = {
            'email': 'test@example.com',
            'phone_number': '01712345678',
            'first_name': 'John',
            'last_name': 'Doe',
            'house_number': '123',
            'road_number': '45',
            'postal_code': '1234',
            'district': 'Dhaka',
            'password': 'testpass123'
        }
    
    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(**self.user_data)
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.phone_number, '01712345678')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.country, 'Bangladesh')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(**self.user_data)
        
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    
    def test_user_full_name(self):
        """Test getting user's full name."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.get_full_name(), 'John Doe')
        
        # Test with middle name
        user.middle_name = 'Middle'
        self.assertEqual(user.get_full_name(), 'John Middle Doe')
    
    def test_user_short_name(self):
        """Test getting user's short name."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.get_short_name(), 'John')
    
    def test_user_full_address(self):
        """Test getting user's full address."""
        user = User.objects.create_user(**self.user_data)
        expected_address = "House: 123, Road: 45, Postal Code: 1234, Dhaka, Bangladesh"
        self.assertEqual(user.get_full_address(), expected_address)
    
    def test_email_required(self):
        """Test that email is required."""
        data = self.user_data.copy()
        data['email'] = ''
        
        with self.assertRaises(ValueError):
            User.objects.create_user(**data)
    
    def test_phone_number_required(self):
        """Test that phone number is required."""
        data = self.user_data.copy()
        data['phone_number'] = ''
        
        with self.assertRaises(ValueError):
            User.objects.create_user(**data)
    
    def test_email_unique(self):
        """Test that email must be unique."""
        User.objects.create_user(**self.user_data)
        
        # Try to create another user with the same email
        data = self.user_data.copy()
        data['phone_number'] = '01812345678'  # Different phone
        
        with self.assertRaises(Exception):
            User.objects.create_user(**data)
    
    def test_phone_number_validation(self):
        """Test phone number validation."""
        # Invalid: Less than 11 digits
        data = self.user_data.copy()
        data['phone_number'] = '0171234567'
        data['email'] = 'test2@example.com'
        user = User(**data)
        
        with self.assertRaises(ValidationError):
            user.full_clean()
        
        # Invalid: Doesn't start with 01
        data['phone_number'] = '12345678901'
        data['email'] = 'test3@example.com'
        user = User(**data)
        
        with self.assertRaises(ValidationError):
            user.full_clean()
        
        # Invalid: Contains non-digits
        data['phone_number'] = '0171234567a'
        data['email'] = 'test4@example.com'
        user = User(**data)
        
        with self.assertRaises(ValidationError):
            user.full_clean()
    
    def test_country_default(self):
        """Test that country defaults to Bangladesh."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.country, 'Bangladesh')
    
    def test_user_str_representation(self):
        """Test string representation of user."""
        user = User.objects.create_user(**self.user_data)
        expected = f"John Doe (test@example.com)"
        self.assertEqual(str(user), expected)

