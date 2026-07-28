# Hair Salon POS

A full-featured Point of Sale and business management system built beauty hair salons. Built with Django + PostgreSQL + Tailwind CSS.

---

## ✨ Features

### 🧾 Point of Sale (POS)
- Fast service & product checkout with real-time cart
- Assign a **worker/stylist** to each service at checkout
- **Beverage sales** (Coke, Sprite, Fanta etc.) with stock tracking
- Payment method selection — Cash, M-Pesa, Card
- Discount field per sale
- Walk-in and registered client support

### 📊 Dashboard
- Today / This Week / This Month revenue at a glance
- Recent sales activity feed
- Top performing workers leaderboard
- Beverage sales metrics

### 📈 Reports
- 30-day daily revenue bar chart
- Top services by revenue
- Worker performance table (jobs done + revenue generated)
- Top beverages sold
- Payment method breakdown (Cash vs M-Pesa vs Card)

### 👥 Clients
- Client directory with phone, email, birthday
- Preferred stylist per client
- Visit count and total spent per client
- **WhatsApp broadcast** — generate personal wa.me links for all clients with one message
- **Email newsletter** — compose and open in email app with all client emails pre-filled
- **Export contacts** as `.vcf` (Google Contacts / iPhone / Android) or `.csv` (Excel)

### ✂️ Services & Inventory
- Service categories and menu management
- Product inventory with stock tracking (retail + consumables)
- Stock movement log (in/out)
- Service-product usage linking

### 🥤 Beverages
- Beverage categories (Soda, Water, Juice etc.)
- Individual drink management with size and pricing
- Stock in/out tracking

### 👩‍💼 Staff Management
- Staff profiles with roles (Stylist, Colorist, Nail Tech etc.)
- Commission rate per staff member
- Active / Inactive / On Leave status
- Worker performance tracked per sale

### 🔐 Security & Auth
- Login required on all pages
- Role-based access — Staff uses POS frontend, Owner uses Admin panel
- Session auto-expiry after 8 hours
- Secrets managed via `.env` file (never committed to Git)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.x (Python) |
| Database | PostgreSQL |
| Frontend | Tailwind CSS (CDN), vanilla JS |
| Admin Panel | Django Admin + Jazzmin theme |
| Charts | Chart.js |
| Auth | Django built-in auth |

---

## 📁 Project Structure

```
salon_system/
├── core/               # Settings, URLs, WSGI
├── frontend/           # Main views, URLs, export/broadcast logic
├── sales/              # Sale, SaleItem, Payment models
├── clients/            # Client model + admin
├── staff/              # StaffMember model + admin
├── salon_services/     # Service + ServiceCategory models
├── inventory/          # Product + StockMovement models
├── beverages/          # Beverage + BeverageStock + BeverageCategory
├── salons/             # Salon model
├── templates/          # All HTML templates
│   ├── layout.html
│   ├── dashboard.html
│   ├── reports.html
│   ├── sales/
│   ├── clients/
│   ├── services/
│   └── inventory/
└── manage.py
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL
- Git

### 1. Clone the repository
```bash
git clone https://github.com/stickmanKE/salon_pos.git
cd salon_pos/salon_system
```

### 2. Create and activate virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install django psycopg2-binary django-jazzmin
```

### 4. Set up environment variables
Create a `.env` file in the `salon_system/` root:
```
SECRET_KEY=your_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=salon_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Create the PostgreSQL database
```sql
CREATE DATABASE salon_db;
```

### 6. Run migrations
```bash
python manage.py migrate salons
python manage.py migrate staff
python manage.py migrate clients
python manage.py migrate beverages
python manage.py migrate sales
python manage.py migrate
```

### 7. Create a superuser (Owner/Admin account)
```bash
python manage.py createsuperuser
```

### 8. Run the server
```bash
python manage.py runserver
```

Visit:
- **Staff POS:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

---

## 🖥️ Desktop Shortcuts (Windows)

Two `.bat` files are included for quick launch without opening a terminal:

| Shortcut | Opens | For |
|---|---|---|
| `HappyHair_Staff.bat` | `http://127.0.0.1:8000/` | Secretary / Receptionist |
| `HappyHair_Admin.bat` | `http://127.0.0.1:8000/admin/` | Salon Owner |

Double-click either file — the server starts minimized in the background and the correct page opens in the browser automatically.

---

## ⚙️ Initial Data Setup (After First Run)

Once the server is running, log into `/admin/` and add:

1. **Salon** → Salons → Add your salon name, phone, location
2. **Staff Members** → Staff → Add each worker with their role and status
3. **Service Categories** → Salon Services → e.g. Hair, Nails, Skin
4. **Services** → Add each service with price and category
5. **Beverage Categories** → Beverages → e.g. Soda, Water, Juice
6. **Beverages** → Add each drink (Coca-Cola 500ml, Sprite 500ml etc.) with price and stock
7. **Products** → Inventory → Add consumables and retail products

---

## 🔒 Security Notes

- Never commit the `.env` file — it is listed in `.gitignore`
- Change `DEBUG=False` before deploying to a live server
- The `SECRET_KEY` in `.env` should be a long random string — generate one at https://djecrety.ir
- All pages require login — no public access

---

## 📄 License



---

## 👨‍💻 Developer

Built and maintained by Mark Mgharo. Contact 0715197114.
