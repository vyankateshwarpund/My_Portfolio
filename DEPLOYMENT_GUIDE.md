# 🚀 Production Deployment Guide for Vyankateshwar Pund Portfolio

This Django portfolio is production-ready with Gunicorn, WhiteNoise static handling, Environment configuration, and Docker support.

---

## 🌟 Option 1: Deploy on Render.com (Recommended Free Tier)

Render supports Django apps out of the box with free PostgreSQL database and automatic SSL (https).

### Step 1: Push Code to GitHub
1. Create a public/private repository on GitHub: `vyankateshwar-portfolio`.
2. Initialize git and push your codebase:
```bash
git init
git add .
git commit -m "Production ready Django portfolio"
git branch -M main
git remote add origin https://github.com/vyankateshwarpund/vyankateshwar-portfolio.git
git push -u origin main
```

### Step 2: Create Web Service on Render
1. Sign up at [render.com](https://render.com).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub repository `vyankateshwar-portfolio`.
4. Configure settings:
   - **Name**: `vyankateshwar-portfolio`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python seed_data.py`
   - **Start Command**: `gunicorn portfolio_project.wsgi:application`

### Step 3: Add Environment Variables on Render
Under **Environment Variables**, add:
- `DEBUG` = `False`
- `SECRET_KEY` = `your-super-secret-django-production-key`
- `EMAIL_HOST_USER` = `pundvyankateshwar@gmail.com`
- `EMAIL_HOST_PASSWORD` = `your-16-character-gmail-app-password`

Click **Create Web Service**. Your site will be live at `https://vyankateshwar-portfolio.onrender.com`!

---

## 🐍 Option 2: Deploy on PythonAnywhere (Easiest Free Hosting)

PythonAnywhere is specifically built for Python and Django applications.

### Step 1: Sign Up
1. Register for a free account at [pythonanywhere.com](https://www.pythonanywhere.com).

### Step 2: Open Bash Console & Clone Project
```bash
git clone https://github.com/vyankateshwarpund/vyankateshwar-portfolio.git
cd vyankateshwar-portfolio
mkvirtualenv --python=/usr/bin/python3.10 portfolio-env
pip install -r requirements.txt
python manage.py migrate
python seed_data.py
python manage.py collectstatic --noinput
```

### Step 3: Configure Web App
1. Go to the **Web** tab -> **Add a new web app**.
2. Select **Manual Configuration** -> **Python 3.10**.
3. Set **Virtualenv path**: `/home/yourusername/.virtualenvs/portfolio-env`.
4. Set **Code path**: `/home/yourusername/vyankateshwar-portfolio`.
5. Edit the **WSGI configuration file**:
```python
import os
import sys

path = '/home/yourusername/vyankateshwar-portfolio'
if path not in sys.path:
    sys.path.append(path)
sys.path.insert(0, os.path.join(path, 'apps'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'portfolio_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
6. Click **Reload yourusername.pythonanywhere.com**. Your website is live!

---

## 🐳 Option 3: Deploy using Docker (VPS / DigitalOcean / AWS EC2)

If deploying to a VPS (Ubuntu / Linux instance):

```bash
# Build and run using Docker Compose
docker-compose up -d --build
```
This automatically boots Gunicorn app container and MySQL 8 database container.

---

## 📄 Post-Deployment Verification
- Test Contact form live email delivery to `pundvyankateshwar@gmail.com`.
- Verify PDF Resume downloading at `/resume/download/1/`.
- Access Admin dashboard at `/admin/` with your superuser credentials.
