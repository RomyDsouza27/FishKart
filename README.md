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

*<img width="1103" height="817" alt="image" src="https://github.com/user-attachments/assets/1d67e0a7-b8ca-48aa-a4fb-78297d9e185f" /> <img width="1117" height="579" alt="image" src="https://github.com/user-attachments/assets/b2a43182-2ac9-4e54-8567-c47cb5639c65" /> <img width="1093" height="1212" alt="image" src="https://github.com/user-attachments/assets/13b2e6ec-2c65-4a43-b136-d0fdc15b6204" /> <img width="1320" height="639" alt="image" src="https://github.com/user-attachments/assets/2fcf5385-29bd-473d-991b-38d544643da0" /> 
<img width="1152" height="745" alt="image" src="https://github.com/user-attachments/assets/2910de3b-609e-4da3-bed6-a1429d41a731" /> <img width="1245" height="740" alt="image" src="https://github.com/user-attachments/assets/c37f5153-6e80-4dae-ad7f-4e1e6fce786b" /> 
<img width="1131" height="645" alt="image" src="https://github.com/user-attachments/assets/c9dc41dc-09bd-49fc-aff2-b7eec94944e7" />




*

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
