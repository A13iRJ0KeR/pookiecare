# PookieCare - Skincare E-Commerce Platform

A Django-based e-commerce platform for selling skincare products in Bangladesh.

## Project Structure

```
pookiecare/
├── manage.py
├── requirements.txt
├── README.md
├── media/                   # User-uploaded files (product images)
│   └── products/
│       └── images/
├── pookiecare/              # Main project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── user/                    # User management application
│   ├── models.py            # Custom User model
│   ├── views.py             # Authentication views
│   ├── forms.py             # Registration forms
│   ├── admin.py             # Admin configuration
│   ├── backends.py          # Email authentication backend
│   └── templates/           # User templates
└── products/                # Products & orders application
    ├── models.py            # Product, Brand, Category, Order models
    ├── admin.py             # E-commerce admin configuration
    └── README.md            # Products documentation
```

## Applications

### User Application

A custom user authentication system with the following features:

- **User Registration** with comprehensive user information
- **Email-based Authentication** (login with email instead of username)
- **Bangladeshi Phone Number Validation** (11-digit format: 01XXXXXXXXX)
- **Address Management** with Bangladesh-specific fields
- **Admin Panel Integration** for user management

For detailed documentation, see [user/README.md](user/README.md)

### Products Application

A comprehensive e-commerce system for managing skincare products:

- **Brand Management** - Organize products by brands
- **Category Management** - Categorize skincare products (e.g., Moisturizers, Cleansers, Serums)
- **Product Catalog** - Complete product information with images, prices, and inventory
- **Shopping Cart** - Add products to cart with quantity management
- **Order Management** - Track orders and automatic stock updates
- **Featured Products** - Highlight products on the homepage

For detailed documentation, see [products/README.md](products/README.md)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd pookiecare
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```
   
   You'll need to provide:
   - Email address
   - Phone number (e.g., 01999999999)
   - First name and last name
   - Full address (house, road, postal code, district)
   - Password

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - User registration: http://127.0.0.1:8000/user/register/
   - User login: http://127.0.0.1:8000/user/login/

## Features

### User Management
- ✅ Custom user model with UUID primary key
- ✅ Email-based authentication
- ✅ Bangladeshi phone number validation
- ✅ Comprehensive address fields for delivery
- ✅ Admin panel integration
- ✅ User profile page
- ✅ Registration and login forms

### Product Management
- ✅ Brand and category organization
- ✅ Product catalog with images
- ✅ HTML-supported product descriptions
- ✅ Price management in BDT (৳)
- ✅ Inventory/stock tracking
- ✅ Featured products flag
- ✅ Image storage system

### Shopping & Orders
- ✅ Shopping cart functionality
- ✅ Multiple products per order
- ✅ Quantity management
- ✅ Price snapshot at purchase time
- ✅ Automatic stock updates on order completion
- ✅ Order history tracking
- ✅ Admin order management tools

### User Fields
- User ID (Auto-generated UUID)
- First Name, Middle Name (optional), Last Name
- Email Address (unique)
- Phone Number (Bangladeshi format, unique)
- Address: House Number, Road Number, Postal Code, District
- Country: Bangladesh (fixed)
- Password with confirmation

## Technology Stack

- **Framework**: Django 5.2.7
- **Database**: SQLite3 (development)
- **Python**: 3.x
- **Image Processing**: Pillow 11.0.0
- **Authentication**: Custom email-based authentication

## Configuration

### Settings

Key settings in `pookiecare/settings.py`:

```python
# Custom User Model
AUTH_USER_MODEL = 'user.User'

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'user.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Login/Logout URLs
LOGIN_URL = 'user:login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'user:login'
```

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
```

### Applying Migrations
```bash
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## Admin Panel

Access the admin panel at `/admin/` to manage:

### User Management
- Users (view, create, edit, delete)
- User permissions and groups
- Custom user creation form with password confirmation
- Search and filter by email, name, phone, district

### Product Management
- Brands and categories
- Products with image previews
- Color-coded stock status (Red: Out of Stock, Orange: Low Stock, Green: In Stock)
- Price display in BDT (৳)
- Featured products management

### Order Management
- View all orders (cart and completed)
- Color-coded order status (🛒 In Cart, ✓ Completed)
- Inline order items editing
- Automatic stock validation
- Bulk order completion actions
- Order history and analytics

## Security Features

- CSRF protection on all forms
- Password hashing using Django's secure hasher
- Email and phone number uniqueness validation
- Bangladeshi phone number format validation
- Session-based authentication

## Future Enhancements

### User Features
- [ ] Password reset functionality
- [ ] Email verification
- [ ] User profile editing
- [ ] Order history page for users
- [ ] Wishlist functionality

### E-Commerce Features
- [ ] Product search and filtering
- [ ] Product reviews and ratings
- [ ] Payment gateway integration
- [ ] Order tracking
- [ ] Discount codes and promotions
- [ ] Product recommendations
- [ ] Public-facing product pages
- [ ] Checkout process

### Technical
- [ ] API endpoints for mobile app
- [ ] Email notifications for orders
- [ ] SMS notifications (Bangladesh)
- [ ] Advanced analytics dashboard

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Notes

- This platform is specifically designed for Bangladesh market
- Phone numbers must follow the format: 01XXXXXXXXX (11 digits)
- Country field is fixed to "Bangladesh"
- All prices are in BDT (Bangladeshi Taka - ৳)
- Product images are stored locally in `media/products/images/`
- All primary keys use UUID for better security and scalability
- Shopping cart is implemented as orders with `in_cart=True`
- Stock is automatically updated when orders are completed
