#  MeltnMunch - Handmade Confectionary Portal

> A beautiful, minimalist e-commerce platform for handmade bakery products built with Django.

##  Table of Contents

- [About](#about)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Database Models](#database-models)


##  About

MeltnMunch is a full-stack web application designed for the sale of handmade bakery products. The platform features a clean, minimalist design with a humbly functional UI. Users can browse products, add items to their cart, manage favorites, and complete purchases.

### Project Goals

- Create a simple framework for an E-Commerce site.
- Implement secure user authentication with built-in Django libraries.
- Provide product management capabilities.
- Build a responsive, mobile-friendly interface.
- Learn Django framework fundamentals.

##  Features

### User Features
-  **User Authentication**: Secure signup, login, and logout functionality
-  **Product Browsing**: View all available bakery products with images and descriptions
-  **Favorites System**: Save favorite products for quick access
-  **Shopping Cart**: Add products, adjust quantities, and manage cart items
-  **Responsive Design**: Fully mobile-optimized interface

### Admin Features
-  **Product Management**: Add, edit, and remove products
-  **Image Upload**: Support for product images
-  **User Management**: Track registered users
-  **Inventory Control**: Manage product availability

##  Technologies Used

### Backend
- **Django 5.2.8** - Web framework
- **Python 3.14** - Programming language
- **SQLite** - Database
- **Pillow** - Image processing

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling with custom design system
- **Django Template Engine** - Server-side rendering

##  Installation

### Prerequisites

- Python 3.14 or higher
- pip (Python package manager)
- Pipenv (recommended) or virtualenv

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/meltnmunch.git
   cd meltnmunch
   ```

2. **Install dependencies**
   
   Using Pipenv (recommended):
   ```bash
   pipenv install
   pipenv shell
   ```
   
   Or using pip:
   ```bash
   pip install django pillow
   ```

3. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set username, email, and password.

5. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

##  Usage

### For Users

1. **Sign Up**: Create an account using the signup page
2. **Browse Products**: View all available products on the dashboard
3. **Add to Favorites**: Click the heart icon to save products
4. **Add to Cart**: Click "Add to Cart" to add items to your shopping cart
5. **Manage Cart**: Adjust quantities or remove items from your cart
6. **Checkout**: Complete your purchase (checkout functionality coming soon)

### For Administrators

1. **Access Admin Panel**: Navigate to `/admin` and login with superuser credentials
2. **Add Products**: 
   - Go to Products → Add Product
   - Fill in name, description, price, and upload image
   - Set quantity and category
3. **Manage Users**: View and manage registered users
4. **View Orders**: Track customer orders and cart items

##  Project Structure

```
MNM/
│
├── app/                          # Main application
│   ├── migrations/               # Database migrations
│   ├── static/                   # Static files
│   │   ├── css/                  # Stylesheets
│   │   │   ├── cart.css
│   │   │   ├── dash.css
│   │   │   ├── style.css
│   │   │   └── stylee.css
│   │   └── images/               # Static images (logos, backgrounds)
│   ├── templates/                # HTML templates
│   │   ├── cart.html
│   │   ├── dash.html
│   │   ├── home.html
│   │   ├── login.html
│   │   └── signup.html
│   ├── admin.py                  # Admin configuration
│   ├── models.py                 # Database models
│   ├── urls.py                   # App URL routing
│   └── views.py                  # View functions
│
├── media/                        # User-uploaded files
│   └── products/                 # Product images
│
├── MeltnMunch/                   # Project configuration
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Main URL routing
│   └── wsgi.py                   # WSGI configuration
│
├── db.sqlite3                    # SQLite database
├── manage.py                     # Django management script
├── Pipfile                       # Dependencies (Pipenv)
└── README.md                     # This file
```

##  Database Models

### User (Django Built-in)
- username
- email
- password (hashed)
- date_joined

### Product
```python
- name: CharField (max 100 chars)
- description: TextField
- price: DecimalField (10 digits, 2 decimals)
- quantity: PositiveIntegerField
- category: CharField (choices: Cookies, Cakes, Breads, etc.)
- image: ImageField (optional)
- is_in_stock(): Method to check availability
```

### Favorite
```python
- user: ForeignKey (User)
- product: ForeignKey (Product)
- Unique together: (user, product)
```

### CartItem
```python
- user: ForeignKey (User)
- product: ForeignKey (Product)
- quantity: PositiveIntegerField
- date_added: DateTimeField
- Unique together: (user, product)
```

### Order (Future implementation)
```python
- customer_name: CharField
- created_at: DateTimeField
- total_amount: DecimalField
```

##  Configuration
```
##  Known Issues

- [ ] Checkout functionality not yet implemented
- [ ] Stock management needs enhancement
- [ ] Search functionality to be added
- [ ] Product filtering by category pending

## 🔮 Future Enhancements

- [ ] Payment gateway integration (Stripe/PayPal)
- [ ] Order history and tracking
- [ ] Email notifications
- [ ] Product reviews and ratings
- [ ] Advanced search and filtering
- [ ] Wishlist sharing
- [ ] Social media integration
- [ ] Multi-language support

##  Learning Notes

### What I Learned

1. **Django Fundamentals**
   - Models, Views, Templates (MVT) architecture
   - URL routing and view functions
   - Django ORM for database operations
   - Static and media files handling

2. **Authentication**
   - User registration and login
   - Login-required decorators
   - Password hashing and security

3. **Database Design**
   - One-to-many relationships (User → CartItem)
   - Many-to-many relationships (User ↔ Product via Favorite)
   - Database migrations

4. **Frontend Integration**
   - Django template language
   - Form handling with CSRF protection
   - Static files organization
   - Responsive CSS design

