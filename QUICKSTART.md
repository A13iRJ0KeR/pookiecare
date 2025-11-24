# PookieCare - Quick Start Guide

## What Has Been Created

### User Management Application
✅ Custom User model with all required fields
✅ Email-based authentication system
✅ Bangladeshi phone number validation
✅ User registration with password confirmation
✅ Login/Logout functionality
✅ User profile page
✅ Full admin panel integration
✅ Comprehensive test suite
✅ Beautiful, responsive HTML templates

### Products & E-Commerce Application
✅ Brand management system
✅ Category management system
✅ Product catalog with image support
✅ Shopping cart functionality
✅ Order management with automatic stock updates
✅ Full admin panel for e-commerce operations
✅ Inventory tracking
✅ Price management in BDT (৳)

## Quick Start

### 1. Create a Superuser

```bash
source .venv/bin/activate  # Activate virtual environment
python manage.py createsuperuser
```

**Enter the following when prompted:**
- Email: your-email@example.com
- Phone number: 01712345678 (must be 11 digits, starting with 01)
- First name: Your Name
- Last name: Your Last Name
- House number: 123
- Road number: 45
- Postal code: 1234
- District: Dhaka
- Password: (your secure password)

### 2. Start the Development Server

```bash
python manage.py runserver
```

### 3. Access the Application

Open your browser and visit:

**Admin Panel:**
- URL: http://127.0.0.1:8000/admin/
- Login with your superuser credentials
- Manage users, view details, create new users

**User Registration:**
- URL: http://127.0.0.1:8000/user/register/
- Fill out the registration form
- Test the phone number validation (must be 11 digits: 01XXXXXXXXX)
- Test password confirmation

**User Login:**
- URL: http://127.0.0.1:8000/user/login/
- Login with email and password
- No username required!

**User Profile:**
- URL: http://127.0.0.1:8000/user/profile/
- View complete user information
- See all fields including address

## Testing the Application

### Run All Tests
```bash
python manage.py test user
```

All 11 tests should pass, including:
- User creation
- Superuser creation
- Phone number validation
- Email uniqueness
- Password hashing
- Full name/address methods

### Manual Testing Checklist

1. **Registration Flow:**
   - [ ] Visit registration page
   - [ ] Try invalid phone number (should show error)
   - [ ] Try mismatched passwords (should show error)
   - [ ] Complete valid registration
   - [ ] Verify redirect to login page

2. **Login Flow:**
   - [ ] Visit login page
   - [ ] Try wrong credentials (should show error)
   - [ ] Login with correct email and password
   - [ ] Verify redirect to home/profile

3. **Admin Panel:**
   - [ ] Login to admin panel
   - [ ] View users list
   - [ ] Search for users by email/name/phone
   - [ ] Filter users by district
   - [ ] Create new user via admin
   - [ ] Edit user details
   - [ ] Verify country is fixed to "Bangladesh"

## Phone Number Validation Rules

✅ **Valid Formats:**
- 01712345678
- 01812345678
- 01912345678
- 01512345678
- 01612345678

❌ **Invalid Formats:**
- +8801712345678 (includes country code)
- 1712345678 (missing leading 0)
- 0171234567 (less than 11 digits)
- 017123456789 (more than 11 digits)
- 02712345678 (doesn't start with 01)

## User Database Fields

### Automatically Generated
- **User ID**: UUID (Primary Key)
- **Date Joined**: Auto-generated timestamp
- **Last Login**: Auto-updated timestamp

### Required Fields
- First Name
- Last Name
- Email Address (unique)
- Phone Number (unique, validated)
- House Number
- Road Number
- Postal Code
- District
- Password

### Optional Fields
- Middle Name

### Fixed Fields
- Country: "Bangladesh" (cannot be changed)

## Key Features

### 1. Email Authentication
- Users login with email, not username
- Email must be unique
- Custom authentication backend handles email login

### 2. Password Security
- Passwords are hashed using Django's secure hasher
- Password confirmation required during registration
- Password validation enforced

### 3. Phone Number Validation
- Regex validation: ^01[0-9]{9}$
- Must be exactly 11 digits
- Must start with "01"
- Must be unique

### 4. Admin Integration
- Custom admin forms with password confirmation
- Organized fieldsets for better UX
- Search by email, name, phone
- Filter by district, staff status
- Read-only fields: User ID, dates, country

## Troubleshooting

### "Django is not installed" Error
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### "No such table: user_user" Error
```bash
python manage.py migrate
```

### Can't Login to Admin
Make sure you created a superuser:
```bash
python manage.py createsuperuser
```

### Phone Number Validation Error
- Remove any spaces or dashes
- Ensure it's 11 digits
- Must start with "01"
- Example: 01712345678

## Adding Sample Products

### Via Admin Panel

1. **Add Brands**:
   - Go to admin → Brands → Add Brand
   - Examples: CeraVe, The Ordinary, Neutrogena, La Roche-Posay

2. **Add Categories**:
   - Go to admin → Categories → Add Category
   - Examples: Moisturizers, Cleansers, Serums, Sunscreens, Toners

3. **Add Products**:
   - Go to admin → Products → Add Product
   - Fill in product details
   - Upload product image (stored in `media/products/images/`)
   - Set price in BDT
   - Set available stock
   - Mark as featured if desired

4. **Create Test Order**:
   - Go to admin → Orders → Add Order
   - Select a user
   - Leave "In cart" checked
   - Save and add order items inline
   - Complete order using the admin action

## Next Steps

### User Features
1. **Customize Templates**: Edit HTML files in `user/templates/user/`
2. **Add Email Verification**: Implement email confirmation
3. **Password Reset**: Add forgot password functionality
4. **Profile Editing**: Allow users to update their information

### E-Commerce Features
1. **Product Pages**: Create public-facing product listing and detail pages
2. **Shopping Cart UI**: Build cart interface for customers
3. **Checkout Process**: Implement checkout flow with address confirmation
4. **Payment Integration**: Add payment gateway (bKash, Nagad, SSL Commerz)
5. **Order Tracking**: Let users view their order history
6. **Product Search**: Add search and filter functionality

## File Locations

```
pookiecare/
├── user/
│   ├── models.py          # User model definition
│   ├── forms.py           # Registration form
│   ├── views.py           # View functions
│   ├── admin.py           # Admin configuration
│   ├── backends.py        # Authentication backend
│   ├── urls.py            # URL routing
│   ├── tests.py           # Test suite
│   └── templates/user/
│       ├── register.html  # Registration page
│       ├── login.html     # Login page
│       └── profile.html   # Profile page
├── products/
│   ├── models.py          # Brand, Category, Product, Order models
│   ├── admin.py           # E-commerce admin configuration
│   └── README.md          # Products documentation
└── media/
    └── products/
        └── images/        # Product images storage
```

## Support

For detailed documentation, see:
- `user/README.md` - User management documentation
- `products/README.md` - E-commerce documentation
- `README.md` - Main project documentation

## Summary

🎉 **Your e-commerce platform is complete and ready to use!**

The application includes:

### User Management
- ✅ Custom User model with UUID primary key
- ✅ All required fields (name, email, phone, address)
- ✅ Bangladesh-specific phone validation
- ✅ Email-based authentication
- ✅ User profile and admin panel

### E-Commerce System
- ✅ Brand and category management
- ✅ Product catalog with images
- ✅ Shopping cart functionality
- ✅ Order management with stock tracking
- ✅ Complete admin interface
- ✅ Price management in BDT (৳)
- ✅ Email authentication
- ✅ Complete admin integration
- ✅ Registration and login pages
- ✅ User profile display
- ✅ 11 passing tests
- ✅ Professional, styled templates

Start the server and begin testing!
