# ParkEase — Vehicle Parking App

ParkEase is a multi-user web app for managing 4-wheeler parking lots with role-based access, reservations, billing, and analytics.

Tech stack: Flask API, Vue 3 UI, Bootstrap, SQLite (default), Redis cache, Celery (worker + beat)

## Features
- Admin and User roles with JWT auth
- Parking lot and spot management (CRUD)
- Spot reservation and release flow with cost calculation
- User and Admin dashboards with analytics and charts
- Redis-backed caching for common queries
- Scheduled emails and CSV exports via Celery

---

## Quick Start

Prerequisites
- Python 3.10+
- Node.js 16+ (recommend 18+), npm
- Redis 6+

### 1) Backend (Flask API)

From the repo root:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r backend/requirements.txt

# Initialize DB and seed default Admin user
flask --app backend/app.py init-db

# Run the API (http://127.0.0.1:5000)
flask --app backend/app.py run    # or: python backend/app.py
```

Default Admin (seeded by `init-db`)
- Email: `admin@gmail.com`
- Password: `Admin`

Environment variables (optional; sensible defaults exist)
- `SECRET_KEY`: Flask secret
- `JWT_SECRET_KEY`: JWT signing key
- `DATABASE_URL`: SQLAlchemy URL (default: SQLite at `backend/parkease.db`)
- `REDIS_URL`: Redis for cache (default: `redis://localhost:6379/1`)
- `CELERY_BROKER_URL`: Celery broker (default: `redis://localhost:6379/0`)
- `CELERY_RESULT_BACKEND`: Celery result backend (default: `redis://localhost:6379/0`)
- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USE_SSL`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER`

If using the `flask` CLI, you can also set `export FLASK_APP=backend/app.py`.

### 2) Celery (background tasks)

Open new terminals with the same virtualenv activated:

```bash
# Worker
celery -A backend.celery_worker.celery worker --loglevel=info

# Beat (schedules daily reminders + monthly reports)
celery -A backend.celery_worker.celery beat --loglevel=info
```

Exports (CSV) land in: `backend/exports/`

### 3) Frontend (Vue 3)

```bash
cd frontend
npm install

# (optional) configure the API base URL; default is http://127.0.0.1:5000
echo "VUE_APP_API_BASE_URL=http://127.0.0.1:5000" > .env.development

npm run serve   # http://localhost:8080
```

The frontend automatically attaches `Authorization: Bearer <token>` if a token exists in `localStorage` under `access_token`.

---

## API Overview

Auth
- `POST /auth/register` — body: `{ email, password, full_name?, address?, pin_code? }`
- `POST /auth/login` — body: `{ email, password }` → `{ access_token, role }`

User (JWT with role=user)
- `GET /user/lots?location=&pin_code=` — list available lots with availability
- `POST /user/reserve` — `{ lot_id, vehicle_number }` → create reservation
- `GET /user/reservations` — list user reservations (history + ongoing)
- `POST /user/reservations/{id}/release` — release and compute cost
- `GET /user/summary` — totals and by-month spend

Admin (JWT with role=admin)
- `GET /admin/lots` — list lots
- `POST /admin/lots` — create lot `{ name, address, price_per_hour, total_spots, pin_code? }`
- `GET /admin/lots/{lot_id}` — lot details + spots
- `PUT /admin/lots/{lot_id}` — update lot, auto-add/remove spots
- `DELETE /admin/lots/{lot_id}` — delete lot
- `GET /admin/lots/{lot_id}/spots` — list spots for lot
- `GET /admin/spots/{spot_id}` — spot details
- `DELETE /admin/spots/{spot_id}` — delete available spot
- `GET /admin/users` — list users
- `GET /admin/summary` — revenue and occupancy aggregates

Auth header
```http
Authorization: Bearer <JWT>
```

---

## Project Structure

```
.
├── backend/
│   ├── app.py                # Flask app factory + CLI (init-db)
│   ├── auth.py               # Auth routes and role_required
│   ├── config.py             # Config + env vars
│   ├── db.py                 # SQLAlchemy init
│   ├── models.py             # User, ParkingLot, ParkingSpot, Reservation
│   ├── routes.py             # Root + role-gated sample routes
│   ├── admin_routes.py       # Admin CRUD + analytics
│   ├── user_routes.py        # User flows: search, reserve, release, summary
│   ├── cache.py              # Flask-Caching (Redis)
│   ├── tasks.py              # Celery tasks (email, CSV export)
│   ├── celery_worker.py      # Celery app
│   ├── celery_beat.py        # Beat schedule (optional entrypoint)
│   └── requirements.txt
├── frontend/
│   └──src/
│       ├── main.js                    # Vue app bootstrap
│       ├── App.vue                    # Root component
│       ├── router/
│       │   └── index.js               # Route definitions and guards
│       ├── services/
│       │   └── api.js                 # Axios instance (reads VUE_APP_API_BASE_URL)
│       ├── components/
│       │   ├── AdminLayout.vue        # Shell/layout for admin pages
│       │   ├── UserLayout.vue         # Shell/layout for user pages
│       │   ├── BarChart.vue           # Chart.js bar wrapper
│       │   ├── LineChart.vue          # Chart.js line wrapper
│       │   └── DoughnutChart.vue      # Chart.js doughnut wrapper
│       └── views/
│           ├── HomeView.vue          # Landing page
│           ├── Login.vue             # User login
│           ├── Signup.vue            # User registration
│           ├── UserDashboard.vue     # User dashboard overview
│           ├── UserSummaryView.vue   # Spending summary (charts)
│           ├── SearchLotsView.vue    # Search lots by pin/location
│           ├── SearchView.vue        # Search view (alternate)
│           ├── BookSpotView.vue      # Reserve a spot
│           ├── ReleaseSpotView.vue   # Release ongoing reservation
│           ├── AdminDashboard.vue    # Admin dashboard overview
│           ├── AdminSummaryView.vue  # Admin analytics (revenue/occupancy)
│           ├── UsersView.vue         # Manage user accounts
│           ├── AddLot.vue            # Create a parking lot
│           ├── EditLot.vue           # Edit a parking lot
│           ├── LotSpots.vue          # View/manage spots in a lot
│           └── AdminSpotView.vue     # Spot details (admin)
└── README.md

```

---

## Development Tips
- CORS is enabled; frontend dev server at `:8080` can call API at `:5000`.
- Default DB is SQLite at `backend/parkease.db`; use `DATABASE_URL` to switch engines.
- If `pip` complains about encoding on `backend/requirements.txt`, re-save the file as UTF-8 and retry.

---

## License
No license specified. Add one if you plan to distribute.
