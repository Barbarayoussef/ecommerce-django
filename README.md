# Ecommerce Django Project

A full-featured ecommerce web application built with Django, featuring product management, shopping cart functionality, payment processing, and shipping services.

## 🚀 Features

### Core Ecommerce Features
- **Product Management**: Add, edit, and manage products with inventory tracking
- **Shopping Cart**: Session-based shopping cart with quantity management
- **User Authentication**: Django's built-in user authentication system
- **Order Management**: Complete order processing and tracking
- **Payment Processing**: Integrated payment system for secure transactions

### Advanced Features
- **Shipping Service**: Intelligent shipping cost calculation based on product weight
- **Product Expiry Tracking**: Monitor product expiration dates
- **Inventory Management**: Real-time stock quantity tracking
- **User Profiles**: Extended user profiles with shipping addresses and balance tracking
- **Admin Interface**: Django admin panel for easy management

## 🛠️ Technology Stack

- **Backend**: Django 5.2.1
- **Database**: SQLite3 (development)
- **Frontend**: Django Templates with Bootstrap
- **Payment**: Custom payment processing system
- **Shipping**: Custom shipping service with weight-based calculations

## 📁 Project Structure

```
ecom/
├── ecom/                 # Main Django project settings
│   ├── settings.py      # Django configuration
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI configuration
├── store/               # Product and store management app
│   ├── models.py        # Product, Customer, Order models
│   ├── views.py         # Store views and logic
│   ├── forms.py         # Product and customer forms
│   └── templates/       # Store templates
├── cart/                # Shopping cart functionality
│   ├── cart.py          # Cart session management
│   ├── views.py         # Cart views
│   └── context_processors.py
├── payment/             # Payment and shipping processing
│   ├── models.py        # Order, ShippingAddress models
│   ├── views.py         # Payment processing views
│   ├── shipping_service.py  # Shipping calculations
│   └── forms.py         # Payment forms
├── static/              # Static files (CSS, JS, images)
├── media/               # User-uploaded files
├── manage.py            # Django management script
└── test_shipping.py     # Shipping service test script
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd ecom
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install django
```

### Step 4: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 📊 Database Models

### Store App Models
- **Product**: Products with name, price, quantity, expiry date, and shipping properties
- **Customer**: Customer information (first name, last name, phone, email)
- **Order**: Basic order tracking
- **Profile**: Extended user profiles with address and balance information

### Payment App Models
- **ShippingAddress**: Customer shipping addresses
- **Order**: Detailed order information with shipping status
- **OrderItem**: Individual items within orders

## 🛒 Key Features Explained

### Shopping Cart System
- Session-based cart management
- Add/remove items with quantity control
- Persistent cart across sessions
- Real-time cart total calculation

### Shipping Service
- Weight-based shipping cost calculation
- Support for both shippable and non-shippable items
- Automatic shipping date tracking
- Flexible shipping address management

### Product Management
- Product categorization and inventory tracking
- Expiry date monitoring for perishable items
- Weight tracking for shipping calculations
- Stock quantity management




## 🔧 Configuration

### Environment Variables
The project uses Django's default settings. For production, consider setting:
- `SECRET_KEY`: Change the default secret key
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Configure allowed hosts for production

### Database Configuration
Currently configured for SQLite3. For production, consider using PostgreSQL or MySQL.

## 📝 API Endpoints

### Store Endpoints
- `/` - Home page with products
- `/product/<id>/` - Product detail page
- `/register/` - User registration
- `/login/` - User login

### Cart Endpoints
- `/cart/` - Shopping cart view
- `/cart/add/<product_id>/` - Add item to cart
- `/cart/remove/<product_id>/` - Remove item from cart

### Payment Endpoints
- `/payment/` - Payment processing
- `/shipping/` - Shipping information
- `/order-confirmation/` - Order confirmation page

