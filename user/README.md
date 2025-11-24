# User Application - PookieCare

## Overview
This is a custom user application for the PookieCare Django project that handles user registration and authentication with a custom user model tailored for Bangladeshi users.

## Features

### 1. Custom User Model
- **User ID**: Automatically generated UUID (Primary Key)
- **Personal Information**:
  - First Name (Required)
  - Middle Name (Optional)
  - Last Name (Required)
- **Contact Information**:
  - Email Address (Required, Unique)
  - Phone Number (Required, Unique, Bangladeshi format validation)
- **Address Information**:
  - House Number (Required)
  - Road Number (Required)
  - Postal Code (Required)
  - District (Required)
  - Country (Fixed: Bangladesh)

### 2. Authentication
- Email-based authentication (login with email and password)
- Custom authentication backend
- Password validation and confirmation
- Session management

### 3. Phone Number Validation
- Validates Bangladeshi phone number format
- Format: 11 digits starting with '01'
- Example: 01999999999
- No need for +88 prefix

### 4. Admin Panel Integration
- Full admin interface for user management
- Custom admin forms with password confirmation
- Organized fieldsets for better UX
- List filters and search functionality

## URLs

The user app provides the following URLs:

- `/user/register/` - User registration page
- `/user/login/` - User login page
- `/user/logout/` - User logout
- `/user/profile/` - User profile page (requires authentication)

## Usage

### Creating a Superuser

To create a superuser for admin access, run:

```bash
python manage.py createsuperuser
```

You'll be prompted to enter:
- Email address
- Phone number (11 digits, e.g., 01999999999)
- First name
- Last name
- House number
- Road number
- Postal code
- District
- Password

### Accessing the Admin Panel

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Navigate to `http://127.0.0.1:8000/admin/`

3. Login with your superuser credentials

4. You can now manage users through the admin interface

### User Registration Flow

1. User visits `/user/register/`
2. Fills out the registration form with all required information
3. Password is validated and confirmed
4. Phone number is validated for Bangladeshi format
5. User account is created
6. User is redirected to login page

### User Login Flow

1. User visits `/user/login/`
2. Enters email and password
3. Authentication is performed using email (not username)
4. Successful login redirects to home page
5. Failed login shows error message

## Database Schema

### User Model Fields

| Field | Type | Required | Unique | Description |
|-------|------|----------|--------|-------------|
| user_id | UUID | Auto | Yes | Primary Key |
| first_name | CharField(100) | Yes | No | User's first name |
| middle_name | CharField(100) | No | No | User's middle name |
| last_name | CharField(100) | Yes | No | User's last name |
| email | EmailField(255) | Yes | Yes | Email address for login |
| phone_number | CharField(11) | Yes | Yes | Bangladeshi phone number |
| house_number | CharField(50) | Yes | No | House number |
| road_number | CharField(50) | Yes | No | Road number |
| postal_code | CharField(10) | Yes | No | Postal code |
| district | CharField(100) | Yes | No | District name |
| country | CharField(50) | No | No | Always "Bangladesh" |
| password | CharField | Yes | No | Hashed password |
| is_active | Boolean | No | No | User account status |
| is_staff | Boolean | No | No | Staff status |
| is_superuser | Boolean | No | No | Superuser status |
| date_joined | DateTime | Auto | No | Registration date |
| last_login | DateTime | Auto | No | Last login date |

## Files Structure

```
user/
├── __init__.py
├── admin.py              # Admin panel configuration
├── apps.py               # App configuration
├── backends.py           # Custom authentication backend
├── forms.py              # User registration form
├── models.py             # Custom User model
├── urls.py               # URL routing
├── views.py              # View functions
├── migrations/           # Database migrations
│   └── 0001_initial.py
└── templates/
    └── user/
        ├── register.html # Registration page
        ├── login.html    # Login page
        └── profile.html  # User profile page
```

## Configuration

### Settings (pookiecare/settings.py)

The following settings have been configured:

```python
# Add user app to INSTALLED_APPS
INSTALLED_APPS = [
    ...
    'user',
]

# Set custom user model
AUTH_USER_MODEL = 'user.User'

# Configure authentication backends
AUTHENTICATION_BACKENDS = [
    'user.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Configure login/logout URLs
LOGIN_URL = 'user:login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'user:login'
```

## Security Features

1. **Password Hashing**: Passwords are securely hashed using Django's default password hasher
2. **CSRF Protection**: All forms include CSRF tokens
3. **Email Uniqueness**: Prevents duplicate email registrations
4. **Phone Number Validation**: Ensures proper Bangladeshi phone number format
5. **Password Confirmation**: Requires password confirmation during registration

## Testing

To test the user registration and authentication:

1. Start the development server
2. Visit `http://127.0.0.1:8000/user/register/`
3. Fill out the registration form
4. Submit and verify redirection to login page
5. Login with the registered credentials
6. Verify successful authentication and profile access

## Customization

### Adding More Fields

To add more fields to the User model:

1. Edit `user/models.py` and add the field
2. Update `user/forms.py` to include the new field
3. Update `user/admin.py` to display the field in admin
4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Changing Phone Number Validation

Edit the `phone_regex` validator in `user/models.py` to change the validation pattern.

## Dependencies

- Django 5.2.7
- No additional packages required

## License

This is part of the PookieCare project.
