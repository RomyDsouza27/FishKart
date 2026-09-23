# 🐟 FishKart – Online Fish Delivery Platform

FishKart is a full-stack web-based fish delivery platform that bridges the gap between local fish markets and digital convenience. It lets home cooks, restaurants, and seafood enthusiasts browse, select, and order fresh fish and seafood products online — with real-time inventory, secure payments, and order tracking.

Built solo as a final year B.Sc. Computer Science (Hons.) project at S.K. Somaiya College, Somaiya Vidyavihar University (2024–25).

## Features

- 🛒 Real-time inventory updates with dynamic product listings
- 👤 User registration/login with encrypted passwords, profile management
- 🧺 Smart cart management — add, update quantity, remove items
- 💳 Secure payment integration via **Razorpay** and **PayPal**
- 📦 Order tracking with estimated delivery times
- 📱 Fully responsive design across desktop and mobile
- 🛠️ Admin panel for managing orders, inventory, and user queries

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django (MVC-style: models, views, templates) |
| Frontend | HTML5, CSS3, Bootstrap, JavaScript |
| Database | MySQL / SQLite3 |
| Payments | Razorpay API, PayPal |
| Testing | Django `TestCase` (unit + integration testing) |
| Tooling | flake8, black (PEP8 formatting & linting) |

## Architecture

The app follows a modular MVC structure with these core modules:

- **User Module** — registration, login, encrypted passwords, profile management
- **Product Module** — dynamic fish listings with category filtering & search
- **Cart & Order Module** — add/edit/remove cart items, checkout, order summary
- **Payment Module** — Razorpay integration with secure transaction callbacks
- **Admin Module** — CRUD operations on products, orders, and users
- **Delivery Module** *(future scope)* — delivery tracking & route optimization

### Core Entities (Database)

- `User` (user_id, name, email, password_hash, role)
- `Product` (product_id, name, type, price, stock_quantity, vendor_id)
- `Order` (order_id, user_id, total_price, status, order_date)
- `OrderItem` (order_item_id, order_id, product_id, quantity, price)
- `Payment` (payment_id, order_id, payment_method, payment_status, transaction_id)

Schema is normalized to 3NF with primary/foreign key constraints, `CHECK` and `NOT NULL` constraints for data integrity.

## Security

- Encrypted passwords via Django's built-in authentication
- Role-based access control (User / Admin)
- CSRF protection on all form submissions
- ORM-based queries to prevent SQL injection
- PCI-DSS compliant payment flow via Razorpay

## Screenshots

*(Add screenshots of the homepage, login page, product detail page, cart, and checkout here — see project report for reference layouts.)*

## Setup

```bash
git clone https://github.com/RomyDsouza27/FishKart.git
cd FishKart
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/`

## Testing

Unit and integration tests were written using Django's `TestCase` class, covering:
- User registration & login flows
- Cart operations (add/edit/remove)
- End-to-end checkout → payment → order confirmation
- Admin CRUD operations
- Out-of-stock and payment-failure edge cases

## Future Enhancements

- Native mobile apps (Android/iOS) with push notifications
- AI-based product recommendations
- Real-time delivery tracking with maps
- Vendor analytics dashboard
- Multi-language support
- Two-Factor Authentication (2FA)

## Author

**Romy Francis D'souza**
B.Sc. Computer Science (Hons.), S.K. Somaiya College 
