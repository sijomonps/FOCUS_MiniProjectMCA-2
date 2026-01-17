# Core App

This is the main Django application that contains all the business logic for FOCUS.

## 📁 Files Overview

### Main Files
- **`models.py`** - Database models (Assignment, StudySession, QuickNote)
- **`views.py`** - View functions that handle HTTP requests and responses
- **`urls.py`** - URL routing for this app
- **`admin.py`** - Django admin panel configuration
- **`apps.py`** - App configuration

### Folders
- **`migrations/`** - Database schema change history (auto-generated)
- **`__pycache__/`** - Python compiled files (auto-generated, can ignore)

## 🔄 How It Works

1. **User visits a URL** → Django checks `urls.py`
2. **URL matches a pattern** → Calls the corresponding function in `views.py`
3. **View function runs** → Queries database using `models.py`
4. **Returns response** → Renders HTML template with data

## 🗄️ Database Models

### StudySession
Tracks study time for each subject with duration and date.

### Assignment  
Manages deadlines with automatic time calculation and treemap visualization.

### QuickNote
Stores quick reflections after study sessions.

## 🎯 Key Features in This App

- Study timer with session tracking
- Smart assignment treemap with auto-calculation
- Quick notes system
- Dashboard analytics
- User authentication
