# 🚗 ParkEase — Vehicle Parking App

**ParkEase** is a full-stack multi-user web application for managing **4-wheeler parking lots**, featuring **role-based access**, **real-time reservations**, **automated billing**, **analytics dashboards**, and **scheduled Celery background tasks**.

Built as part of **Modern Application Development II (MAD-II)**, the project adheres to the official *Vehicle Parking App V2* problem statement and milestones.

---

## 🧱 Tech Stack

**Backend:** Flask (Python), SQLAlchemy ORM, SQLite  
**Frontend:** Vue 3, Bootstrap 5  
**Background Tasks:** Celery + Redis (worker, beat)  
**Caching:** Redis  
**Visualization:** Chart.js  
**Environment:** Works locally (Flask API + Vue dev server)

---

## ✨ Features

- 🔐 **Admin & User roles** with JWT authentication  
- 🅿️ **Parking lot & spot management** (CRUD)  
- 🗕️ **Reservation & release flow** with cost computation  
- 📊 **Analytics dashboards** for both roles  
- ⚡ **Redis caching** for frequent queries  
- ⏰ **Celery jobs**:  
  - Daily user reminders (email/chat)  
  - Monthly activity reports  
  - On-demand CSV export (async)  
- 💾 SQLite database auto-created programmatically  
- 📈 Chart.js-based data visualization

---

## 🚀 Quick Start

### 🔹 Prerequisites
- Python 3.10+
- Node.js 16+ (recommended 18+)
- Redis 6+ (WSL/Local)

---

### **1️⃣ Backend Setup**

```bash
cd backend
python -m venv venv
venv\Scripts\activate    # On Windows
# source venv/bin/activate  (Linux/Mac)

pip install --upgrade pip
pip install -r requirements.txt
flask init-db
flask run
```

🗾 Default Admin Credentials  
- **Email:** admin@gmail.com  
- **Password:** Admin  

---

### **2️⃣ Frontend Setup**

```bash
cd frontend
npm install --legacy-peer-deps
npm run serve
```

Access frontend: [http://localhost:8080](http://localhost:8080)

Default API base: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

### **3️⃣ Redis (via WSL)**

```bash
sudo service redis-server start
```

---

### **4️⃣ Celery (Background Jobs)**

In **backend** folder, open **two terminals** with venv activated:

**Terminal 1 — Worker**
```bash
celery -A celery_worker.celery worker --loglevel=info --pool=solo
```

**Terminal 2 — Beat (Scheduler)**
```bash
celery -A celery_worker.celery beat --loglevel=info
```

🗂️ Generated CSV exports are stored in  
`backend/exports/`

---

### **5️⃣ Testing Celery Tasks (via Flask shell)**

```bash
flask shell
from tasks import *
send_daily_reminders.delay()
send_monthly_reports.delay()
export_user_history.delay(user_id=1)
```

---

## 🧠 Project Structure

```
.
├── backend/
│   ├── app.py
│   ├── auth.py
│   ├── config.py
│   ├── db.py
│   ├── models.py
│   ├── routes.py
│   ├── admin_routes.py
│   ├── user_routes.py
│   ├── cache.py
│   ├── tasks.py
│   ├── celery_worker.py
│   ├── celery_beat.py
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── router/
│       ├── services/api.js
│       ├── components/
│       └── views/
└── README.md
```

---

## 🧯 Milestones Overview

| Milestone | Description | Commit Tag |
|------------|--------------|-------------|
| 0 | GitHub Setup | `Milestone-0 VP-MAD2` |
| 1 | DB Models & Schema | `Milestone-VP-MAD2 DB-Relationship` |
| 2 | Auth & Role-based Access | `Milestone-VP-MAD2 Auth-RBAC-Token` |
| 3 | Admin Dashboard + CRUD | `Milestone-VP-MAD2 Admin-Dashboard-Management` |
| 4 | User Dashboard & Reservation | `Milestone-VP-MAD2 User-Dashboard-Management` |
| 5 | Reservation History & Cost Calc | `Milestone-VP-MAD2 Reservation-Cost-Calculation` |
| 6 | Charts & Analytics | `Milestone-VP-MAD2 Charts-Analytics` |
| 7 | Redis Caching | `Milestone-VP-MAD2 Redis-Caching` |
| 8 | Celery Jobs (Reminders, Reports, CSV) | `Milestone-VP-MAD2 Celery-Jobs` |
| — | Final Submission | `Milestone-VP-MAD2 Final-Submission` |

---

## 🤌 Recommended Enhancements
- Search for lots/spots/users  
- Responsive UI + PWA features  
- Advanced analytics & predictions (optional)

---

## 🧮 Development Notes
- Flask + Vue run independently; CORS enabled.
- SQLite default DB path: `backend/parkease.db`
- Change DB/Redis URLs via environment vars.
- All DB tables auto-create programmatically.

---

## 👨‍💻 Developer

**Shamanthak Reddy M**  
BS in Data Science and Applications  
IIT Madras Online Degree  
Grade: **A (Excellent)** in Project

---

## 📄 License

This project is for academic demonstration purposes only.

---
