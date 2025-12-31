# 🔄 StudyFlow - How It Works

Visual guide to understand how the application flows from user action to result.

## 📱 Application Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                                 │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  User types URL: http://localhost:8000/dashboard/            │   │
│  └──────────────────────────┬──────────────────────────────────┘   │
└─────────────────────────────┼────────────────────────────────────────┘
                              │ HTTP Request
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DJANGO SERVER                                   │
│                                                                      │
│  ┌────────────────────────────────────────────────────────┐         │
│  │  1. studyflow/urls.py checks root URL patterns         │         │
│  │     → Finds: include('core.urls')                      │         │
│  └─────────────────┬──────────────────────────────────────┘         │
│                    │                                                 │
│  ┌─────────────────▼──────────────────────────────────────┐         │
│  │  2. core/urls.py checks app URL patterns               │         │
│  │     → Finds: path('dashboard/', dashboard_view)        │         │
│  └─────────────────┬──────────────────────────────────────┘         │
│                    │                                                 │
│  ┌─────────────────▼──────────────────────────────────────┐         │
│  │  3. core/views.py → dashboard_view() function          │         │
│  │     ┌──────────────────────────────────────────┐       │         │
│  │     │ def dashboard_view(request):             │       │         │
│  │     │   # Query database                       │       │         │
│  │     │   assignments = Assignment.objects...    │       │         │
│  │     │   sessions = StudySession.get_weekly...  │       │         │
│  │     │   # Prepare data                         │       │         │
│  │     │   context = {'assignments': ..., }       │       │         │
│  │     │   # Render template                      │       │         │
│  │     │   return render(..., context)            │       │         │
│  │     └──────────────┬───────────────────────────┘       │         │
│  └────────────────────┼───────────────────────────────────┘         │
│                       │                                              │
│  ┌────────────────────▼───────────────────────────────────┐         │
│  │  4. core/models.py queries SQLite database             │         │
│  │     ┌────────────────────────────────────────┐         │         │
│  │     │  Assignment.objects.filter(user=...)   │         │         │
│  │     │  StudySession.get_weekly_data(user)    │         │         │
│  │     └────────────────────────────────────────┘         │         │
│  │                    │                                    │         │
│  │     ┌──────────────▼────────────────────┐              │         │
│  │     │    db.sqlite3 (Database)          │              │         │
│  │     │  ┌──────────────────────────────┐ │              │         │
│  │     │  │ core_assignment table        │ │              │         │
│  │     │  │ core_studysession table      │ │              │         │
│  │     │  │ core_quicknote table         │ │              │         │
│  │     │  └──────────────────────────────┘ │              │         │
│  │     └───────────────────────────────────┘              │         │
│  └────────────────────────────────────────────────────────┘         │
│                       │ Data returned                                │
│  ┌────────────────────▼───────────────────────────────────┐         │
│  │  5. templates/core/dashboard.html rendered             │         │
│  │     ┌────────────────────────────────────────┐         │         │
│  │     │  {% extends 'base.html' %}             │         │         │
│  │     │  {% block content %}                   │         │         │
│  │     │    <div class="stats-grid">            │         │         │
│  │     │      {% for assignment in assignments %}│        │         │
│  │     │        <div>{{ assignment.title }}</div>│        │         │
│  │     │      {% endfor %}                       │         │         │
│  │     │    </div>                               │         │         │
│  │     │  {% endblock %}                         │         │         │
│  │     └────────────────────────────────────────┘         │         │
│  └────────────────────────────────────────────────────────┘         │
│                       │ HTML generated                               │
└───────────────────────┼──────────────────────────────────────────────┘
                        │ HTTP Response (HTML + CSS + JS)
                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                                 │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  6. Browser receives HTML                                    │   │
│  │     → Loads static/css/style.css (styling)                   │   │
│  │     → Loads static/js/app.js (interactivity)                 │   │
│  │     → Displays beautiful dashboard!                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## 🎯 Key Components

### 1. URLs (Routing)
**Files:** `studyflow/urls.py`, `core/urls.py`
- Maps URLs to view functions
- `/dashboard/` → `dashboard_view()`
- `/assignments/` → `assignments_view()`
- `/study/` → `study_view()`

### 2. Views (Logic)
**File:** `core/views.py`
- Handle HTTP requests
- Query database using models
- Prepare data for templates
- Return HTTP responses

### 3. Models (Database)
**File:** `core/models.py`
- Define database structure
- `Assignment`, `StudySession`, `QuickNote`
- Query methods: `.filter()`, `.get()`, `.all()`

### 4. Templates (Display)
**Folder:** `templates/`
- HTML files with Django template language
- Display data from views
- Inherit from `base.html`

### 5. Static Files (Style & Interaction)
**Folder:** `static/`
- CSS: `static/css/style.css` (Notion-dark theme)
- JS: `static/js/app.js` (timer, treemap, etc.)

## 📊 Example: Adding a New Assignment

```
USER ACTION: Clicks "Add Assignment" button
     │
     ▼
JAVASCRIPT: static/js/app.js captures click
     │ Collects form data: title, date, time
     │ Sends AJAX POST request
     ▼
DJANGO VIEW: core/views.py → add_assignment()
     │ Parses datetime
     │ Creates Assignment object
     │ Saves to database
     ▼
DATABASE: db.sqlite3
     │ INSERT INTO core_assignment...
     │ Returns new assignment ID
     ▼
VIEW RETURNS: JSON response
     │ { "id": 5, "title": "...", "hours_remaining": 24.5 }
     ▼
JAVASCRIPT: Receives response
     │ Calls renderTreemap()
     │ Creates new cube element
     │ Adds to DOM
     ▼
USER SEES: New assignment cube appears in treemap!
```

## 🔐 Authentication Flow

```
UNAUTHENTICATED USER
     │ Visits /dashboard/
     ▼
MIDDLEWARE: Checks if logged in
     │ Not authenticated
     ▼
REDIRECT: → /login/ (LOGIN_URL in settings.py)
     │
     ▼
LOGIN PAGE: templates/core/login.html
     │ User enters credentials
     │ Submits form
     ▼
VIEW: core/views.py → login_view()
     │ Validates credentials
     │ Django authenticate()
     │ Creates session
     ▼
REDIRECT: → /dashboard/
     │ Now authenticated!
     ▼
DASHBOARD: User sees their data
```

## 🗄️ Database Structure

```
db.sqlite3
├── auth_user (Django's user table)
│   ├── id
│   ├── username
│   ├── password (hashed)
│   └── email
│
├── core_assignment
│   ├── id
│   ├── user_id (ForeignKey → auth_user)
│   ├── title
│   ├── subject
│   ├── deadline (DateTimeField)
│   ├── estimated_hours (auto-calculated)
│   ├── status (pending/completed)
│   └── created_at
│
├── core_studysession
│   ├── id
│   ├── user_id (ForeignKey → auth_user)
│   ├── subject
│   ├── duration (minutes)
│   ├── date
│   └── created_at
│
└── core_quicknote
    ├── id
    ├── user_id (ForeignKey → auth_user)
    ├── subject
    ├── content (max 300 chars)
    ├── study_duration
    └── created_at
```

## 🎨 Static Files Loading

```
Browser requests: /dashboard/
     │
     ▼
Django serves: templates/core/dashboard.html
     │ Contains: {% extends 'base.html' %}
     ▼
Loads: templates/base.html
     │ Contains:
     │   <link href="{% static 'css/style.css' %}">
     │   <script src="{% static 'js/app.js' %}">
     ▼
Django resolves {% static %}
     │ STATIC_URL = '/static/' (from settings.py)
     │ Looks in: static/ folder
     ▼
Browser requests:
     │ http://localhost:8000/static/css/style.css
     │ http://localhost:8000/static/js/app.js
     ▼
Django serves files from static/ folder
     │
     ▼
Page fully loaded with styles and interactivity!
```

## 🔄 Request/Response Cycle (Summary)

1. **User Action** → Types URL or clicks button
2. **Browser** → Sends HTTP request to Django server
3. **URLs** → Django matches URL pattern
4. **View** → Function processes request, queries database
5. **Models** → Query database, return data
6. **Template** → Django renders HTML with data
7. **Response** → HTML + CSS + JS sent to browser
8. **Browser** → Displays page to user

## 📂 File Locations Quick Reference

| Component | File Location | Purpose |
|-----------|--------------|---------|
| **URLs** | `studyflow/urls.py`, `core/urls.py` | Route URLs to views |
| **Views** | `core/views.py` | Handle requests, business logic |
| **Models** | `core/models.py` | Database structure |
| **Templates** | `templates/core/*.html` | HTML display |
| **CSS** | `static/css/style.css` | Styling |
| **JavaScript** | `static/js/app.js` | Interactivity |
| **Settings** | `studyflow/settings.py` | Configuration |
| **Database** | `db.sqlite3` | Data storage |

## 🎯 Understanding Django Commands

```bash
# Start server (runs the application)
python manage.py runserver
→ Starts development server at http://localhost:8000/

# Create migrations (prepare database changes)
python manage.py makemigrations
→ Looks at models.py, creates migration files

# Apply migrations (update database)
python manage.py migrate
→ Applies migrations to db.sqlite3

# Create admin user
python manage.py createsuperuser
→ Creates user with admin panel access

# Open Python shell with Django
python manage.py shell
→ Interactive Python with Django models loaded
```

## 💡 Tips for Understanding

1. **Follow the flow** - Start from URL → View → Model → Template
2. **Check the terminal** - Server logs show which view is called
3. **Use print()** - Add `print("Debug:", data)` in views
4. **Django debug toolbar** - Shows SQL queries, context data
5. **Browser dev tools** - F12 to see network requests, JavaScript console

## 📚 Learn More

- [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md) - Complete beginner's guide
- [core/README.md](core/README.md) - Models, views, URLs explained
- [templates/README.md](templates/README.md) - Template system
- [static/README.md](static/README.md) - CSS & JavaScript
- [studyflow/README.md](studyflow/README.md) - Settings explained

---

**Now you understand the flow!** 🎉 Ready to explore the code? Start with [core/views.py](core/views.py)!
