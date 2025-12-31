# StudyFlow Configuration

This folder contains the main Django project configuration files.

## 📁 Files Overview

### `settings.py` - Main Configuration
Controls everything about your Django project:

- **Database**: SQLite connection settings
- **Apps**: Registered Django apps (core, admin, auth, etc.)
- **Templates**: Template directory locations
- **Static Files**: CSS/JS file locations
- **Security**: Secret key, debug mode, allowed hosts
- **Timezone**: Default timezone settings
- **Authentication**: Login URLs and redirects

### Important Settings:
```python
DEBUG = True                    # Development mode (set False for production)
ALLOWED_HOSTS = []             # Add your domain for production
STATIC_URL = '/static/'        # URL prefix for static files
LOGIN_URL = '/login/'          # Redirect here if not logged in
```

### `urls.py` - Root URL Configuration
Maps URLs to apps:

```python
/                  → Login page
/signup/           → Registration
/dashboard/        → Dashboard (requires login)
/study/            → Study timer
/assignments/      → Assignment treemap
/notes/            → Notes page
/admin/            → Django admin panel
```

### `wsgi.py` & `asgi.py`
Server deployment files - used when deploying to production.

- **WSGI**: Synchronous server interface (most common)
- **ASGI**: Asynchronous server interface (for websockets, etc.)

### `__init__.py`
Makes this folder a Python package. Usually empty.

## 🔧 Common Modifications

### Add a New App:
1. Create app: `python manage.py startapp newapp`
2. Add to `INSTALLED_APPS` in `settings.py`
3. Include URLs in `urls.py`

### Change Database:
Edit `DATABASES` in `settings.py` (default is SQLite)

### Add Environment Variables:
1. Create `.env` file in root
2. Install `python-decouple`
3. Use in `settings.py`: `from decouple import config`

### Configure Static Files for Production:
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```
Then run: `python manage.py collectstatic`

## ⚠️ Security Notes

- Never commit `SECRET_KEY` to version control
- Set `DEBUG = False` in production
- Configure `ALLOWED_HOSTS` for production
- Use environment variables for sensitive data
