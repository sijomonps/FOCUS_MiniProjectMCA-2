# 📁 FOCUS Project Structure

## 🗂️ Visual Overview

```
studyflow/                              📦 Root Project Folder
│
├── 📖 BEGINNER_GUIDE.md               ★ START HERE if you're new!
├── 📖 README.md                        Main project documentation
├── 📖 PROJECT_STRUCTURE.md             This file - structure guide
│
├── 🎯 manage.py                        Django command center
├── 📋 requirements.txt                 Python dependencies list
├── 🗄️ db.sqlite3                       Database (stores all your data)
│
├── 🚀 core/                            Main Django App
│   ├── 📖 README.md                    ← Core app guide (read this!)
│   ├── 📊 models.py                    Database models (tables)
│   ├── 🎮 views.py                     Page logic and API endpoints
│   ├── 🔗 urls.py                      URL routing for this app
│   ├── ⚙️ admin.py                     Admin panel configuration
│   ├── 📝 apps.py                      App configuration
│   ├── 🧪 tests.py                     Unit tests (for testing)
│   ├── 📦 migrations/                  Database change history
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── 0002_alter_assignment...py
│   └── 🗑️ __pycache__/                 Compiled Python (auto-generated)
│
├── ⚙️ studyflow/                       Project Configuration
│   ├── 📖 README.md                    ← Settings guide (read this!)
│   ├── 🔧 settings.py                  Main configuration file
│   ├── 🔗 urls.py                      Root URL routing
│   ├── 🌐 wsgi.py                      Web server interface
│   ├── 🌐 asgi.py                      Async server interface
│   ├── __init__.py
│   └── 🗑️ __pycache__/                 Compiled Python (auto-generated)
│
├── 🎨 templates/                       HTML Templates
│   ├── 📖 README.md                    ← Templates guide (read this!)
│   ├── 🏠 base.html                    Base layout (sidebar, nav)
│   └── core/                           Page templates
│       ├── 📊 dashboard.html           Dashboard with stats
│       ├── 🗂️ assignments.html         Treemap visualization
│       ├── ⏱️ study.html                Study timer page
│       ├── 📝 notes.html                Notes management
│       ├── 🔐 login.html                Login page
│       └── ✍️ signup.html               Registration page
│
├── 💅 static/                          CSS, JavaScript, Assets
│   ├── 📖 README.md                    ← Assets guide (read this!)
│   ├── css/
│   │   └── 🎨 style.css                Notion-dark theme styles
│   └── js/
│       └── ⚡ app.js                    Interactive features
│
├── 📚 docs/                            Documentation Folder
│   ├── 📖 README.md                    ← Docs index (read this!)
│   ├── 🚀 QUICK_START.md               Setup instructions
│   ├── 🗺️ PROJECT_WALKTHROUGH.md       Detailed project tour
│   ├── 🎨 DESIGN_REFERENCE.md          Design system guide
│   ├── ✅ TESTING_GUIDE.md             Testing instructions
│   ├── 💎 UI_ENHANCEMENTS.md           UI improvement history
│   └── 📋 ENHANCEMENT_SUMMARY.md       Feature changelog
│
└── 🔧 scripts/                         Utility Scripts
    ├── 📖 README.md                    ← Scripts guide (read this!)
    └── 🔑 set_password.py              Password reset tool
```

## 📍 Navigation Guide

### 🎯 Quick Start (First Time Here?)
1. Read [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md) ← **Start here!**
2. Read [README.md](README.md)
3. Follow [docs/QUICK_START.md](docs/QUICK_START.md)
4. Run `python manage.py runserver`

### 📚 Understanding Each Part
Every major folder has its own README.md file:

| Folder | README Location | What You'll Learn |
|--------|----------------|-------------------|
| **Core App** | [core/README.md](core/README.md) | Models, views, URLs, how the app works |
| **Templates** | [templates/README.md](templates/README.md) | HTML structure, template inheritance |
| **Static Files** | [static/README.md](static/README.md) | CSS styling, JavaScript functions |
| **Configuration** | [studyflow/README.md](studyflow/README.md) | Settings, URLs, deployment |
| **Documentation** | [docs/README.md](docs/README.md) | All guides and references |
| **Scripts** | [scripts/README.md](scripts/README.md) | Utility scripts and tools |

### 🗂️ File Types Explained

| Symbol | Meaning | Can I Edit? |
|--------|---------|------------|
| 📖 | Documentation | ✅ Yes, improve docs! |
| 🎯 | Main entry point | ⚠️ Rarely need to |
| 🚀 | Your code | ✅ Yes, this is where you work |
| 🎨 | Styling | ✅ Yes, customize freely |
| ⚡ | JavaScript | ✅ Yes, add features |
| 🗄️ | Database | ❌ No, managed by Django |
| 🗑️ | Auto-generated | ❌ No, don't touch |
| 📦 | Migration files | ❌ Auto-generated by Django |

---

## 🎓 Learning Resources

### Documentation Files (All Include README)
- **[BEGINNER_GUIDE.md](BEGINNER_GUIDE.md)** ⭐ Complete beginner's walkthrough
- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** 📚 Master index of all docs
- **[HOW_IT_WORKS.md](HOW_IT_WORKS.md)** 🔄 Visual flow diagrams
- **[README.md](README.md)** 📖 Project overview

### Folder Documentation
Every major folder has its own `README.md`:
- [core/README.md](core/README.md) - App structure
- [templates/README.md](templates/README.md) - HTML templates
- [static/README.md](static/README.md) - CSS & JavaScript
- [studyflow/README.md](studyflow/README.md) - Configuration
- [docs/README.md](docs/README.md) - Documentation index
- [scripts/README.md](scripts/README.md) - Utility scripts

---

## 🚀 Key Features

### Assignment Management (Treemap View)
- Visual treemap layout with dynamic sizing
- Automatic time calculation from deadline
- Smart cube sizing: `140px + √(hours_remaining) * 8`
- Time badges in corner (e.g., "12h", "3d 5h")
- Color-coded priority (auto-calculated)

### Notes System
- Quick session notes (max 300 chars)
- Subject auto-fill from study session
- Filter by subject or date
- Chronological display

### Study Session Tracker
- Digital timer with start/pause/stop
- Focus mode (full-screen)
- Automatic quick note prompt
- Weekly analytics chart
- Streak tracking

---

## 🛠️ Tech Stack

- **Backend**: Django 6.0
- **Database**: SQLite3
- **Frontend**: HTML, CSS (CSS Variables), Vanilla JavaScript
- **Icons**: Material Design Icons v7.4.47
- **Charts**: Chart.js (CDN)

---

## 🎨 Design System

- **Colors**: #191919 (background), #232323 (cards), #2e2e2e (borders)
- **Spacing**: 8px base unit system
- **Typography**: System fonts with fallbacks
- **Theme**: Notion-dark inspired minimal design
- **Icons**: Material Design Icons (mdi-* classes)

---

## 📌 Quick Commands

```bash
# Start server
python manage.py runserver

# Create/apply migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Reset password
python scripts/set_password.py
```

---

## 🎯 Next Steps

1. **New?** Start with [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md)
2. **Setup?** Follow [docs/QUICK_START.md](docs/QUICK_START.md)
3. **Understand?** Read [HOW_IT_WORKS.md](HOW_IT_WORKS.md)
4. **Customize?** Check [docs/DESIGN_REFERENCE.md](docs/DESIGN_REFERENCE.md)
5. **Lost?** See [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
