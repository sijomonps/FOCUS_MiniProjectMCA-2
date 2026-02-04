# 📁 FOCUS - Project Organization Guide

> **Clear, logical project structure for easy navigation and maintenance**

---

## 🗂️ Project Structure Overview

```
FOCUS/
│
├── 📱 CORE APPLICATION
│   ├── core/                          # Main Django app (all features)
│   ├── studyflow/                     # Django project configuration
│   ├── templates/                     # HTML templates
│   ├── static/                        # CSS, JS, images
│   └── manage.py                      # Django management script
│
├── 📚 DOCUMENTATION
│   └── docs/                          # All project documentation
│       ├── README.md                  # Documentation index
│       ├── QUICK_START.md             # Getting started guide
│       ├── BEGINNER_GUIDE.md          # Beginner-friendly tutorial
│       ├── HOW_IT_WORKS.md            # Feature explanations
│       ├── PROJECT_WALKTHROUGH.md     # Complete project tour
│       ├── DEPLOYMENT.md              # Deployment instructions
│       ├── TESTING_GUIDE.md           # Testing documentation
│       ├── DESIGN_REFERENCE.md        # Design patterns used
│       ├── ENHANCEMENT_SUMMARY.md     # Feature improvements
│       ├── UI_ENHANCEMENTS.md         # UI/UX improvements
│       ├── MDI_INTEGRATION.md         # MDI icons integration
│       ├── SUBJECTS_UI_IMPROVEMENTS.md
│       ├── TREEMAP_IMPROVEMENTS.md
│       ├── UI_IMPROVEMENTS_SUMMARY.md
│       └── DOCUMENTATION_INDEX.md     # Doc navigation
│
├── 🛠️ UTILITIES
│   └── scripts/                       # Utility scripts
│       ├── README.md                  # Scripts documentation
│       ├── add_sample_data.py         # Add test data
│       └── set_password.py            # Password management
│
├── 📦 PROJECT RESOURCES
│   └── project_resources/             # Project assets & submissions
│       ├── diagrams/                  # ER diagrams, flowcharts
│       ├── screenshots/               # Application screenshots
│       ├── submissions/               # Project submission files
│       └── references/                # Reference documents (PDFs)
│
├── 🗄️ DATABASE & CONFIG
│   ├── db.sqlite3                     # SQLite database
│   ├── requirements.txt               # Python dependencies
│   ├── .gitignore                     # Git ignore rules
│   └── venv/                          # Virtual environment
│
└── 📖 ROOT FILES
    ├── README.md                      # Main project README
    ├── PROJECT_ORGANIZATION.md        # This file
    └── generate_submission.py         # Submission generator

```

---

## 📱 Core Application Structure

### 🎯 **core/** - Main Django App
The single app that handles all features:

```
core/
├── models.py           # Database models (User, Subject, Assignment, Note, StudySession)
├── views.py            # View functions (dashboard, timer, assignments, notes)
├── urls.py             # URL routing
├── forms.py            # Django forms
├── admin.py            # Admin panel configuration
├── apps.py             # App configuration
├── tests.py            # Unit tests
└── migrations/         # Database migrations
```

**What it handles:**
- 📊 Dashboard (analytics, charts, stats)
- ⏱️ Study Timer (Pomodoro sessions)
- 📋 Assignment Tracker (deadline management)
- 📝 Quick Notes (organized by subject)
- 👤 User Management & Authentication
- 👨‍💼 Admin Panel

---

### ⚙️ **studyflow/** - Django Project Config
Project-level settings and configuration:

```
studyflow/
├── settings.py         # Project settings (database, apps, middleware)
├── urls.py             # Project-level URL routing
├── wsgi.py             # WSGI deployment entry point
├── asgi.py             # ASGI deployment entry point
└── __init__.py
```

---

### 🎨 **templates/** - HTML Templates
All HTML files organized by feature:

```
templates/
├── base.html                  # Base template (header, sidebar, footer)
└── core/                      # Feature-specific templates
    ├── dashboard.html         # Dashboard page
    ├── study.html             # Study timer page
    ├── assignments.html       # Assignments page
    ├── notes.html             # Notes page
    ├── login.html             # Login page
    ├── signup.html            # Signup page
    ├── admin_dashboard.html   # Admin dashboard
    ├── admin_users.html       # User management
    ├── admin_user_detail.html # User details
    └── admin_passwords.html   # Password management
```

---

### 🎨 **static/** - Static Assets
CSS, JavaScript, and images:

```
static/
├── css/
│   ├── style.css              # Main stylesheet
│   └── style_backup.css       # Backup
├── js/
│   ├── app.js                 # Main JavaScript
│   └── dashboard.js           # Dashboard-specific JS
├── images/                    # Images and icons
└── README.md
```

---

## 📚 Documentation Structure

### **docs/** - All Documentation
Organized by purpose:

| File | Purpose |
|------|---------|
| `QUICK_START.md` | Setup & run in 5 minutes |
| `BEGINNER_GUIDE.md` | Step-by-step tutorial for beginners |
| `HOW_IT_WORKS.md` | How each feature works |
| `PROJECT_WALKTHROUGH.md` | Complete code walkthrough |
| `DEPLOYMENT.md` | Deploy to production |
| `TESTING_GUIDE.md` | Testing instructions |
| `DESIGN_REFERENCE.md` | Design patterns & architecture |
| `ENHANCEMENT_SUMMARY.md` | Feature improvements log |
| `UI_ENHANCEMENTS.md` | UI/UX improvements |

---

## 🛠️ Utilities & Scripts

### **scripts/** - Helper Scripts

```
scripts/
├── add_sample_data.py      # Populate database with test data
├── set_password.py         # Change user passwords
└── README.md               # Scripts documentation
```

**Usage:**
```bash
python scripts/add_sample_data.py
python scripts/set_password.py
```

---

## 📦 Project Resources

### **project_resources/** - Assets & Submissions

```
project_resources/
├── diagrams/              # ER diagrams, flowcharts
│   └── ER diagram.webp
├── screenshots/           # Application screenshots
│   └── login image.webp
├── submissions/           # Project submissions
│   ├── StudyFlow_Project_Submission.docx
│   └── sijomonps_25pmc154.docx
└── references/            # Reference documents
    ├── Review1_instructions-1.pdf
    └── SRS_anjana_25pmc115.pdf
```

---

## 🔍 Quick Navigation Guide

### Want to...

| Task | Go to |
|------|-------|
| **Understand the project** | `README.md` |
| **Get started quickly** | `docs/QUICK_START.md` |
| **Learn as a beginner** | `docs/BEGINNER_GUIDE.md` |
| **Understand features** | `docs/HOW_IT_WORKS.md` |
| **Explore the code** | `docs/PROJECT_WALKTHROUGH.md` |
| **Deploy the app** | `docs/DEPLOYMENT.md` |
| **Add test data** | `scripts/add_sample_data.py` |
| **View ER diagram** | `project_resources/diagrams/` |
| **See screenshots** | `project_resources/screenshots/` |
| **Modify styles** | `static/css/style.css` |
| **Edit templates** | `templates/core/` |
| **Change database models** | `core/models.py` |
| **Add/modify features** | `core/views.py` |
| **Configure settings** | `studyflow/settings.py` |

---

## 🎯 Why This Structure?

### ✅ Benefits:

1. **Clear Separation of Concerns**
   - Code in `core/` and `studyflow/`
   - Docs in `docs/`
   - Resources in `project_resources/`
   - Scripts in `scripts/`

2. **Easy Navigation**
   - Everything is in its logical place
   - No loose files cluttering the root

3. **Beginner-Friendly**
   - Clear folder names
   - Comprehensive documentation
   - Easy to find what you need

4. **Maintainable**
   - Easy to add new features
   - Easy to update documentation
   - Easy to onboard new developers

5. **Professional**
   - Follows Django best practices
   - Industry-standard organization
   - Portfolio-ready structure

---

## 🚀 Development Workflow

### 1. **Starting Development**
```bash
# Navigate to project
cd "Mini Project"

# Activate virtual environment
venv\Scripts\activate

# Run development server
python manage.py runserver
```

### 2. **Adding a New Feature**
```
1. Add model to core/models.py (if needed)
2. Create/update view in core/views.py
3. Add URL route in core/urls.py
4. Create template in templates/core/
5. Add styles in static/css/style.css
6. Add JS logic in static/js/app.js
7. Document in docs/
```

### 3. **Making Changes**
```
Code Changes     → core/, templates/, static/
Database Changes → python manage.py makemigrations
                   python manage.py migrate
Documentation    → docs/
Resources        → project_resources/
```

---

## 📝 Notes

- **Single App Design**: All features are in `core/` because they're tightly related
- **Flat Documentation**: All docs in one `docs/` folder for easy access
- **No Nested Complexity**: Simple, straightforward structure
- **Version Control**: `.gitignore` configured to exclude `venv/`, `db.sqlite3`, etc.

---

## 🤝 Contributing

When adding files:
- **Code** → `core/`, `templates/`, or `static/`
- **Documentation** → `docs/`
- **Scripts** → `scripts/`
- **Resources** → `project_resources/` (in appropriate subfolder)

---

**Happy Coding! 🎯**
