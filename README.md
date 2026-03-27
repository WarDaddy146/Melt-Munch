# MeltnMunch (MNM) — Full Project Documentation

This document is the comprehensive technical reference for the MeltnMunch project, based on the current codebase state in this workspace.

- Project type: Django monolith (single project + single app)
- Domain: E- Commerce Portal for Confectionaries.
- Primary stack: Django, SQLite, Django templates, custom CSS
- App architecture style: Server-rendered MVT (Model-View-Template)

---

## 1) Project Overview

MeltnMunch is a server-rendered e-commerce web application for showcasing and selling handmade bakery products. It implements:

- Public pages (home, login, signup)
- Authenticated shopping dashboard
- Favorites system
- Cart with quantity updates
- Admin-side product management

The application follows Django’s default structure:

- One Django project package: `MeltnMunch`
- One custom Django app: `app`
- SQLite database for persistence
- Media folder for uploaded product images

---

## 2) Architecture and Runtime Model

### 2.1 High-Level Runtime Flow

1. Browser sends HTTP request to Django.
2. URL resolver matches route in project-level URL config (`MeltnMunch/urls.py`).
3. Request is delegated to app routes (`app/urls.py`).
4. View function in `app/views.py` executes business logic.
5. ORM queries/updates models in `app/models.py` against SQLite.
6. Response is rendered via Django templates in `app/templates/`.
7. Static files are served from configured static paths.
8. Media files are served in development when `DEBUG=True`.

### 2.2 Core Components

- Configuration layer: `MeltnMunch/settings.py`
- URL routing layer: `MeltnMunch/urls.py`, `app/urls.py`
- Business logic layer: `app/views.py`
- Persistence layer: `app/models.py` + migrations
- Presentation layer: `app/templates/` + `app/static/css/`

### 2.3 Authentication Model

The project uses Django’s built-in auth system (`django.contrib.auth.models.User`) rather than a custom user model.

- Login: `authenticate` + `auth_login`
- Logout: `logout`
- Route protection: `@login_required(login_url='login')`

---

## 3) Repository Structure

```text
MNM/
├── manage.py
├── db.sqlite3
├── README.md
├── PROJECT_DOCUMENTATION.md
├── Pipfile
├── Pipfile.lock
├── requirement.txt
├── DESIGN_GUIDE.md
├── DESIGN_GUIDE_MNM.txt
├── MeltnMunch/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── app/
│   ├── __init__.py
│   ├── apps.py
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_cartitem_product_delete_user_cartitem_product.py
│   │   ├── 0003_rename_added_at_cartitem_date_added_and_more.py
│   │   ├── 0004_alter_product_name_favorite.py
│   │   ├── 0005_order_remove_product_created_by_product_category_and_more.py
│   │   └── 0006_alter_product_image.py
│   ├── templates/
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── dash.html
│   │   └── cart.html
│   └── static/
│       ├── css/
│       │   ├── stylee.css
│       │   ├── style.css
│       │   ├── dash.css
│       │   └── cart.css
│       ├── images/
│       │   ├── home_bg.jpg
│       │   ├── bgo.jpg
│       │   └── mnm_logo.jpg
│       └── js/
└── media/
    └── products/
```

Notes:
- `mnm/` in root is a local virtual environment folder.

---

## 4) Configuration Deep Dive

## 4.1 `MeltnMunch/settings.py`

### Installed apps
- Default Django contrib apps
- Custom app: `app`

### Template engine
- `APP_DIRS = True` (templates auto-discovered in app directories)
- `DIRS = []` (no project-level templates folder configured)

### Database
- Engine: SQLite3
- File: `BASE_DIR / 'db.sqlite3'`

### Static configuration
- `STATIC_URL = 'static/'`
- `STATICFILES_DIRS = [BASE_DIR / 'app' / 'static']`
- `STATIC_ROOT = BASE_DIR / 'staticfiles'` for collection/deployment

### Media configuration
- `MEDIA_URL = '/media/'`
- `MEDIA_ROOT = BASE_DIR / 'media'`
---

## 5) URL Routing Map

## 5.1 Project Routes (`MeltnMunch/urls.py`)

- `/admin/` → Django admin
- `/` and all app-defined routes are delegated via `include('app.urls')`
- Media URL serving in development only when `DEBUG=True`

## 5.2 App Routes (`app/urls.py`)

| Route | Name | View | Method(s) | Auth Required |
|---|---|---|---|---|
| `/` | `home` | `home` | GET | No |
| `/login/` | `login` | `login_view` | GET/POST | No |
| `/signup/` | `signup` | `signup` | GET/POST | No |
| `/dash/` | `dash` | `dash` | GET | Yes |
| `/add/` | `add` | `add` | POST | Yes |
| `/cart/` | `cart` | `cart` | GET | Yes |
| `/add-to-cart/<product_id>/` | `add_to_cart` | `add_to_cart` | GET/POST-style link action | Yes |
| `/update-cart/<item_id>/` | `update_cart` | `update_cart` | POST | Yes |
| `/toggle-favorite/<product_id>/` | `toggle_favorite` | `toggle_favorite` | POST | Yes |
| `/logout/` | `logout` | `logout_view` | GET | No |

---

## 6) Data Model Documentation

## 6.1 `Product`

Purpose: Catalog item shown in dashboard and cart.

Fields:
- `name` — `CharField(max_length=100)`
- `description` — `TextField`
- `price` — `DecimalField(max_digits=10, decimal_places=2)`
- `quantity` — `PositiveIntegerField(default=1)`
- `category` — `CharField(max_length=100, choices=...)`
- `image` — `ImageField(upload_to='products/', blank=True, null=True)`

Methods:
- `is_in_stock()` returns boolean (`quantity > 0`)
- `__str__()` returns product name

Category options:
- Cookies
- Cakes
- Breads
- Pastries
- Chocolates
- Celebrations

## 6.2 `Favorite`

Purpose: Many-to-many-like linking table between user and product for favorites.

Fields:
- `user` — FK to Django `User`
- `product` — FK to `Product`

Constraints:
- Unique pair (`user`, `product`) via `unique_together`

## 6.3 `Cart`

Purpose: Container model linking a user to many products.

Fields:
- `user` — FK to `User`
- `products` — M2M to `Product`
- `created_at` — `DateTimeField(default=timezone.now)`

Operational note:
- Current active cart logic uses `CartItem` instead of this model for cart operations.

## 6.4 `CartItem`

Purpose: Per-user, per-product quantity entry used by cart page and cart updates.

Fields:
- `product` — FK to `Product`
- `user` — FK to `User`
- `quantity` — `PositiveIntegerField(default=0)`
- `date_added` — `DateTimeField(auto_now_add=True)`

Constraints:
- Unique pair (`product`, `user`) via `unique_together`

## 6.5 `Order`

Purpose: Basic order header model.

Fields:
- `customer_name` — `CharField(max_length=200)`
- `created_at` — `DateTimeField(auto_now_add=True)`
- `total_amount` — `DecimalField(max_digits=10, decimal_places=2)`

Status:
- Present in model layer, not integrated into checkout flow yet.

## 6.6 `OrderItem`

Purpose: Order line item.

Fields:
- `order` — FK to `Order`
- `product` — FK to `Product`
- `quantity` — `PositiveIntegerField`

Custom behavior:
- Overrides `save()` to enforce stock availability.
- Decrements product stock on save.

Risk note:
- This stock decrement logic is not currently wrapped in transaction handling, and repeated saves could decrement stock multiple times.

---

## 7) View Layer Behavior (Function-by-Function)

## 7.1 `home(request)`
- Renders `home.html`.
- Public landing page.

## 7.2 `login_view(request)`
- GET: renders login form.
- POST: authenticates username/password.
- Success: logs user in, sets success message, redirects to dashboard.
- Failure: returns login with error message.

## 7.3 `signup(request)`
- GET: renders signup form.
- POST:
  - reads `username`, `email`, `password`
  - checks uniqueness of username and email
  - creates Django auth user
  - on success redirects to login
  - on failure returns form with error

## 7.4 `dash(request)`
- Requires authenticated user.
- Supports view switch via query string `?view=products` or `?view=myproducts`.
- Loads full product list and user favorites.
- If `view=cart`, redirects to cart route.
- Renders dashboard template with product and favorite data.

## 7.5 `toggle_favorite(request, product_id)`
- Requires authenticated user.
- POST-only mutation logic:
  - creates favorite if absent
  - removes favorite if already present
- Sets success message.
- Redirects back to dashboard preserving selected view query.

## 7.6 `add(request)`
- Intended to add products.
- Current implementation attempts to pass `created_by=request.user` to `Product.objects.create(...)`.
- Current `Product` model no longer has `created_by`, so this code path raises an exception and will not create product as written.

## 7.7 `cart(request)`
- Requires authenticated user.
- Loads `CartItem` rows for current user.
- Computes per-item total and full cart total in memory.
- Renders cart template.

## 7.8 `add_to_cart(request, product_id)`
- Requires authenticated user.
- Creates `CartItem` with quantity 1 if absent.
- Otherwise increments existing quantity.
- Redirects to dashboard.

## 7.9 `update_cart(request, item_id)`
- Requires authenticated user.
- POST action values:
  - `increase` → quantity +1
  - `decrease` → quantity -1 or delete row when quantity reaches 1
- Redirects to cart page.

## 7.10 `logout_view(request)`
- Logs user out.
- Redirects to login page.

---

## 8) Templates and UI Composition

## 8.1 `home.html`
- Uses `stylee.css`.
- Two CTA buttons: login and signup.
- Public hero-style landing layout.

## 8.2 `login.html`
- Uses `style.css`.
- Form fields: username, password.
- Displays Django messages and explicit `error` context.

## 8.3 `signup.html`
- Uses `style.css`.
- Form fields: email, username, password.
- Displays explicit `error` context.

## 8.4 `dash.html`
- Uses `dash.css`.
- Header with logo, greeting, cart and logout links.
- View toggle between:
  - all products
  - favorite products
- Product card supports favorite toggling and add-to-cart actions.

## 8.5 `cart.html`
- Uses `cart.css`.
- Displays user cart items, item totals, and cart total.
- Quantity update form with increment/decrement controls.
- Checkout button currently displays placeholder alert.

---

## 9) Styling and Design System Implementation

The implemented styles align with the design guide files (`DESIGN_GUIDE.md`, `DESIGN_GUIDE_MNM.txt`) and are built around:

- Warm neutral palette (`soft-cream`, `warm-beige`, `dusty-brown`, etc.)
- Glassmorphism-style cards using backdrop blur
- Soft rounded corners and subtle shadows
- Responsive breakpoints for mobile widths

Primary CSS files:
- `app/static/css/stylee.css` (home)
- `app/static/css/style.css` (login/signup)
- `app/static/css/dash.css` (dashboard)
- `app/static/css/cart.css` (cart)

Image assets in use:
- `app/static/images/home_bg.jpg`
- `app/static/images/bgo.jpg`
- `app/static/images/mnm_logo.jpg`

---

## 10) Admin Configuration

`app/admin.py` registers `Product` with:

- `list_display`: name, category, price, quantity
- `list_filter`: category
- `search_fields`: name

Only `Product` is currently registered in admin; other models are not exposed there by default.

---

## 11.2 Important implication

Because `created_by` was removed in migration `0005`, any code still trying to set `created_by` on product creation is stale and non-functional.

---

## 12) Dependency and Environment Documentation

## 12.1 Declared dependencies

From `Pipfile`:
- django
- python-dotenv

From `requirement.txt`:
- Django==5.2.7
- asgiref==3.10.0
- python-dotenv==1.2.1
- sqlparse==0.5.3
- tzdata==2025.2
- pillow-12.1.1

## 12.2 Python version
- `Pipfile` requires Python `3.14`.

---

## 13) Setup, Run, and Operational Guide

## 13.1 Local setup (venv + pip)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
pip install pillow
```

## 13.2 Local setup (pipenv)

```bash
pipenv install
pipenv shell
pip install pillow
```

## 13.3 Environment file

Create `.env` in project root:

```env
SECRET_KEY=your-development-secret-key
DEBUG=True
```

## 13.4 Database and server

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 13.5 Access points

- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

---

## 14) Feature-by-Feature Functional Specs

## 14.1 Authentication
- Signup creates user after uniqueness checks.
- Login authenticates against Django auth backend.
- Logout ends authenticated session.

## 14.2 Product browsing
- Dashboard shows all products by default.
- Cards include image fallback when image absent.

## 14.3 Favorites
- User can toggle favorite per product.
- Favorites view (`?view=myproducts`) filters to liked products only.

## 14.4 Cart
- Add-to-cart creates or increments a `CartItem`.
- Cart page computes line total and grand total dynamically.
- Quantity controls mutate item count and remove item when decremented below 1.

## 14.5 Orders
- Order models exist but there is no checkout persistence path from cart to order currently.

---

## 16) Security and Production Readiness Notes

Before production deployment:

- Set strong `SECRET_KEY` securely via environment
- Set `DEBUG=False`
- Configure `ALLOWED_HOSTS`
- Use production DB (if scaling beyond prototype)
- Serve static/media via proper web server/CDN setup
- Add CSRF-safe POST forms for all state mutations
- Add transactional safety for stock operations (order creation)
- Add input validation and error monitoring

---

## 17) Testing Status and Recommendations

Suggested test modules:
- Auth flow tests (signup/login/logout)
- Favorite toggle behavior
- Cart add/update/remove logic
- OrderItem stock decrement behavior
- Access control tests for protected routes

---

## 18) Developer Workflow Reference

Common commands:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py shell
python manage.py collectstatic
```

If using Pipenv:

```bash
pipenv shell
python manage.py runserver
```

---

## 19) Suggested Near-Term Improvement Backlog

Priority 1 (stability):
- Fix product creation view to match current `Product` schema
- Add Pillow to dependency files
- Replace add-to-cart links with POST forms

Priority 2 (feature completeness):
- Implement checkout flow creating `Order` and `OrderItem`
- Add stock validation in cart updates and checkout finalization

Priority 3 (quality):
- Add unit/integration tests
- Register remaining models in admin
- Introduce logging and error tracking

---

## 20) Cross-Reference Documents

- `README.md` — project introduction and basic setup
- `DESIGN_GUIDE.md` — deep UI/UX design blueprint
