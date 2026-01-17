# 🎓 Beginner's Guide to FOCUS

Welcome! This guide will help you understand the project structure even if you're new to Django.

## 📁 Project Structure (Simple View)

```
studyflow/                          # 📦 Your project folder
│
├── 🎯 manage.py                    # Command center - Run Django commands here
│
├── 📝 Core Files
│   ├── README.md                   # Project overview (start here!)
│   ├── requirements.txt            # Python packages needed
│   ├── db.sqlite3                  # Database file (stores all data)
│   └── PROJECT_STRUCTURE.md        # Detailed structure guide
│
├── 🚀 core/                        # Main app - Your code lives here
│   ├── README.md                   # ← Read this to understand the app
│   ├── models.py                   # Database tables (Assignment, Session, Note)
│   ├── views.py                    # Page logic (what happens when you visit a URL)
│   ├── urls.py                     # URL routing (maps /dashboard/ to views)
│   ├── admin.py                    # Admin panel configuration
│   ├── apps.py                     # App settings
│   └── migrations/                 # Database change history (auto-generated)
│
├── ⚙️ studyflow/                   # Project settings
│   ├── README.md                   # ← Read this to understand configuration
│   ├── settings.py                 # Main configuration (database, apps, security)
│   ├── urls.py                     # Root URL routing (includes core app URLs)
│   └── wsgi.py + asgi.py          # Server files (for deployment)
│
├── 🎨 templates/                   # HTML files - What you see
│   ├── README.md                   # ← Read this to understand templates
│   ├── base.html                   # Main layout (sidebar, navigation)
│   └── core/                       # Page templates
│       ├── dashboard.html          # Dashboard page
│       ├── assignments.html        # Treemap page
│       ├── study.html              # Timer page
│       ├── notes.html              # Notes page
│       ├── login.html              # Login page
│       └── signup.html             # Registration page
│
├── 💅 static/                      # CSS, JavaScript, images
│   ├── README.md                   # ← Read this to understand assets
│   ├── css/style.css               # All styling (colors, layout, etc.)
│   └── js/app.js                   # Interactive features (timer, treemap)
│
├── 📚 docs/                        # Documentation
│   ├── README.md                   # Guide to all docs
│   ├── QUICK_START.md              # Setup instructions
│   ├── PROJECT_WALKTHROUGH.md      # Detailed tour
│   ├── DESIGN_REFERENCE.md         # Design system
│   └── ...more docs
│
└── 🔧 scripts/                     # Utility scripts
    ├── README.md                   # Guide to scripts
    └── set_password.py             # Password reset tool
```

## 🎯 How Django Works (Simple Explanation)

### 1. User Visits a Page
```
User types: http://localhost:8000/dashboard/
```

### 2. Django Checks URLs
```python
# studyflow/urls.py includes core/urls.py
# core/urls.py maps '/dashboard/' to dashboard_view
```

### 3. View Function Runs
```python
# core/views.py
def dashboard_view(request):
    # Get data from database
    assignments = Assignment.objects.filter(user=request.user)
    # Render HTML with data
    return render(request, 'core/dashboard.html', {'assignments': assignments})
```

### 4. Template Displays
```html
<!-- templates/core/dashboard.html -->
{% for assignment in assignments %}
    <div>{{ assignment.title }}</div>
{% endfor %}
```

### 5. User Sees Page!
```
Beautiful dashboard with all their assignments
```

## 🗂️ Key Files Explained

### `manage.py` - Your Command Center
Run Django commands:
```bash
python manage.py runserver          # Start server
python manage.py migrate            # Update database
python manage.py createsuperuser    # Create admin account
python manage.py makemigrations     # Prepare database changes
```

### `models.py` - Database Structure
Defines what data you store:
```python
class Assignment(models.Model):
    title = models.CharField(max_length=200)
    deadline = models.DateTimeField()
    # Each line is a database column
```

### `views.py` - Page Logic
Functions that handle requests:
```python
def dashboard_view(request):
    # Get data, process it, return HTML
```

### `urls.py` - URL Routing
Maps URLs to views:
```python
path('dashboard/', dashboard_view, name='dashboard')
# When someone visits /dashboard/, run dashboard_view()
```

### `settings.py` - Configuration
Controls everything:
```python
DEBUG = True              # Show errors (turn off in production)
INSTALLED_APPS = [...]   # Apps your project uses
DATABASES = {...}        # Database connection
```

## 🚀 Common Tasks

### Start the Server
```bash
python manage.py runserver
# Visit: http://localhost:8000/
```

### Add a New Page
1. Create function in `core/views.py`
2. Add URL in `core/urls.py`
3. Create HTML in `templates/core/`
4. Done!

### Change How It Looks
Edit `static/css/style.css`

### Add JavaScript
Edit `static/js/app.js`

### Change Database
1. Edit `core/models.py`
2. Run: `python manage.py makemigrations`
3. Run: `python manage.py migrate`

### Create Admin User
```bash
python manage.py createsuperuser
# Visit: http://localhost:8000/admin/
```

## 📖 Learning Path

### Day 1: Orientation
1. Read this file (you're here!)
2. Read [README.md](README.md)
3. Read [docs/QUICK_START.md](docs/QUICK_START.md)
4. Run the project

### Day 2: Understand Structure
1. Read [core/README.md](core/README.md)
2. Read [templates/README.md](templates/README.md)
3. Read [static/README.md](static/README.md)
4. Explore the admin panel

### Day 3: Code Deep Dive
1. Open `core/models.py` - See database structure
2. Open `core/views.py` - See page logic
3. Open `templates/core/dashboard.html` - See HTML
4. Open `static/css/style.css` - See styling

### Day 4: Make Changes
1. Change a color in CSS
2. Add text to a template
3. Create a test assignment
4. Explore the features

### Day 5: Advanced
1. Read [docs/PROJECT_WALKTHROUGH.md](docs/PROJECT_WALKTHROUGH.md)
2. Read [studyflow/README.md](studyflow/README.md)
3. Try modifying a view function
4. Add a new feature

## 🆘 Help Resources

### README Files (Start Here!)
- Main: [README.md](README.md)
- Core App: [core/README.md](core/README.md)
- Templates: [templates/README.md](templates/README.md)
- Static: [static/README.md](static/README.md)
- Settings: [studyflow/README.md](studyflow/README.md)
- Docs: [docs/README.md](docs/README.md)
- Scripts: [scripts/README.md](scripts/README.md)

### Documentation
- Quick Start: [docs/QUICK_START.md](docs/QUICK_START.md)
- Project Tour: [docs/PROJECT_WALKTHROUGH.md](docs/PROJECT_WALKTHROUGH.md)
- Design Guide: [docs/DESIGN_REFERENCE.md](docs/DESIGN_REFERENCE.md)

### Django Resources
- [Official Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Django Girls Tutorial](https://tutorial.djangogirls.org/)

## 💡 Pro Tips

1. **Every folder has a README** - Start there when confused!
2. **Use the admin panel** - Great for testing: http://localhost:8000/admin/
3. **Check the terminal** - Errors show up there
4. **Ctrl+F5** - Hard refresh browser when CSS/JS changes don't show
5. **Comments are your friend** - Read the code comments
6. **Git commit often** - Save your progress frequently
7. **Test in browser console** - Press F12, test JavaScript there first

## 🎉 You're Ready!

Start with the main [README.md](README.md) and follow the setup instructions. Don't worry if things seem confusing at first - every README file in each folder will guide you!

**Remember**: Learning takes time. Be patient with yourself! 🌟
