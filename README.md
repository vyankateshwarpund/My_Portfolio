# Production Personal Portfolio Website - Vyankateshwar Santosh Pund

A high-performance, recruiter-grade Personal Portfolio Application built with **Django 6**, **Django REST Framework (DRF)**, **MySQL**, **HTML5**, **Vanilla CSS3 (Glassmorphism & Gradients)**, **Bootstrap 5**, and **JavaScript (ES6+)**.

Designed specifically to impress tech recruiters and engineering leaders from **Google, Microsoft, Amazon, Adobe, Atlassian, Zoho, TCS Digital, Infosys, Accenture, Deloitte, Capgemini**, and top startups.

---

## 🌟 Key Features

1. **Recruiter Persona & Personal Branding**: Focused on Python Backend Development, REST API Design, Django ORM, and MySQL schema optimization.
2. **Glassmorphism & Gradient Dark/Light Mode**: Smooth theme toggling with CSS variables and `localStorage` persistence.
3. **Interactive Hero Section**: Animated introduction, particle network canvas background, live GitHub API stats counter, floating tech stack badges.
4. **Recruiter Analytics Dashboard (`/dashboard/`)**: Built with **Chart.js** displaying real-time page visits timeline, unique IP tracking, top viewed projects, and unread contact message inbox.
5. **Django REST Framework (DRF) APIs**: Production endpoints for `/api/projects/`, `/api/skills/`, `/api/blogs/`, `/api/experiences/`, `/api/contact/`.
6. **Dynamic Blog Engine**: Supports Markdown content, reading time estimates, category filters, tags, and reader comment threads.
7. **PWA Support**: Offline service worker caching (`sw.js`) and web application manifest (`manifest.json`).
8. **Contact & Email System**: AJAX form handling with database persistence and auto-reply email notifications.
9. **Deployment Ready**: Fully prepared with `Procfile`, `Dockerfile`, `docker-compose.yml`, and `.env` support for Render, Railway, PythonAnywhere, AWS EC2, and Docker.

---

## 🛠️ Tech Stack & Architecture

- **Backend**: Python 3.14 / 3.11, Django 6.0, Django REST Framework, PyMySQL
- **Database**: MySQL (Default in production) / SQLite (Fallback for quick local testing)
- **Frontend**: HTML5, CSS3 Glassmorphism, Bootstrap 5.3, JavaScript (ES6+), Chart.js
- **Tools & Utilities**: Git, Gunicorn, Docker, Markdown, PWA Service Workers

---

## 🚀 Quick Setup & Installation Guide

### Step 1: Clone Repository & Navigate to Folder
```bash
cd portfolio_project
```

### Step 2: Create Virtual Environment & Activate
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database & Environment
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Optionally set `USE_MYSQL=True` and configure your MySQL credentials in `.env`)*

### Step 5: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Seed Database with Initial Data
Run the custom seed script to populate Vyankateshwar Pund's projects, experience, skills, and admin account (`admin` / `admin123`):
```bash
python seed_data.py
```

### Step 7: Start Development Server
```bash
python manage.py runserver
```

Open your browser and visit:
- **Portfolio Website**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Recruiter Analytics Dashboard**: [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)
- **Django Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **REST APIs**: [http://127.0.0.1:8000/api/projects/](http://127.0.0.1:8000/api/projects/)

---

## 🐳 Docker Deployment Setup

Run the entire application stack (Django + MySQL database) via Docker Compose:
```bash
docker-compose up --build -d
```

---

## 🧑‍💻 Author Information

- **Name**: Vyankateshwar Santosh Pund
- **Role**: Junior Software Engineer | Python Developer | Django Backend Developer
- **Email**: pundvyankateshwar@gmail.com
- **Phone**: +91 8263986554
- **LinkedIn**: [https://linkedin.com/in/vyankateshwar-pund-7a654632b](https://linkedin.com/in/vyankateshwar-pund-7a654632b)
- **GitHub**: [https://github.com/vyankateshwarpund](https://github.com/vyankateshwarpund)
