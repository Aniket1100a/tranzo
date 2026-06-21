# 🚀 TRANZO Hosting Guide (Free Tier)

This document tracks the deployment status and provides instructions for hosting the TRANZO project for free.

## 🏗️ Architecture
- **Frontend:** React (Vite) hosted on **Vercel**
- **Backend:** Django (DRF) hosted on **Render**
- **Database:** PostgreSQL hosted on **Neon.tech**
- **Media Storage:** (Optional) Cloudinary or AWS S3 (Free Tier)

---

## 🛠️ Step-by-Step Deployment

### 1. Database Setup (Neon.tech)
1. Sign up at [Neon.tech](https://neon.tech/).
2. Create a new project named `tranzo-db`.
3. Copy the **Connection String** (Direct connection). It looks like:
   `postgres://alex:password@ep-cool-darkness-123456.us-east-2.aws.neon.tech/neondb`
4. Keep this safe; you'll need it for the Backend setup.

### 2. Backend Deployment (Render.com)
1. Sign up at [Render.com](https://render.com/).
2. Click **New +** > **Web Service**.
3. Connect your GitHub repository.
4. Set the following configurations:
   - **Name:** `tranzo-backend`
   - **Root Directory:** `backend`
   - **Environment:** `Python 3`
   - **Build Command:** `./build.sh` (I have already created this file for you)
   - **Start Command:** `gunicorn config.wsgi:application`
5. Click **Advanced** and add **Environment Variables**:
   - `DATABASE_URL`: (Paste your Neon.tech string)
   - `SECRET_KEY`: (Generate a random string)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `tranzo-backend.onrender.com` (Replace with your actual Render URL once assigned)
   - `FRONTEND_URL`: `https://your-frontend-url.vercel.app`

### 3. Frontend Deployment (Vercel)
1. Sign up at [Vercel](https://vercel.com/).
2. Click **Add New** > **Project**.
3. Import your GitHub repository.
4. Set **Root Directory** to `frontend`.
5. Vercel will auto-detect **Vite**.
6. Add **Environment Variables**:
   - `VITE_API_URL`: `https://tranzo-backend.onrender.com` (Your Render URL)
7. Click **Deploy**.

---

## 📝 Maintenance & Updates

### How to update the site?
Simply `git push` to your `main` branch.
- Vercel will automatically rebuild the frontend.
- Render will automatically rebuild the backend, run migrations, and collect static files.

### Current Status
| Component | Provider | URL | Status |
| :--- | :--- | :--- | :--- |
| Frontend | Vercel | *TBD* | ⚪ Not Started |
| Backend | Render | *TBD* | ⚪ Not Started |
| Database | Neon | *TBD* | ⚪ Not Started |

### Troubleshooting
- **Backend slow to start?** Render's free tier spins down after 15 mins of inactivity. The first request might take ~30 seconds.
- **CSRF Errors?** Ensure `CSRF_TRUSTED_ORIGINS` in `backend/config/settings.py` includes your frontend URL.
