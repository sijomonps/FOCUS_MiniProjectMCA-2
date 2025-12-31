# StudyFlow

**A calm, habit-building learning platform for students**

> 🎓 **New to the project?** Start with [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md) for a friendly introduction!  
> 📚 **Looking for specific docs?** Check [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) for a complete guide to all documentation.

StudyFlow is a modern web application designed to help students manage their study time, track assignments, and build consistent learning habits. Built with Django and vanilla JavaScript, it features a beautiful Notion-inspired dark theme with Material Design Icons.

---

## ✨ Features

### 1. **Study Time Tracker**
- Large digital timer (HH:MM:SS format)
- Subject selection with autocomplete
- Start, Pause, and Stop controls
- Focus Mode: Distraction-free full-screen timer
- Automatic quick note prompt after each session
- Weekly analytics with Chart.js visualization
- Daily study streak tracking

### 2. **Smart Assignment Management (Treemap)**
- **Intelligent treemap visualization** - assignments sized by urgency
- **Automatic time calculation** - just enter name, date, and time
- **Smart sizing**: Less time = smaller cube (140px-300px range)
- **Visual time badges** - remaining hours displayed in corner (e.g., "12h", "3d 5h")
- Color-coded urgency system:
  - Green: More time remaining
  - Orange: Medium urgency (7 days or less)
  - Red: High urgency (3 days or less) with pulse animation
- Click to mark as completed
- Smooth fade-out animations
- Recently completed assignments list

### 3. **Personal Study Streaks**
- Tracks consecutive days of study
- Displays current streak with fire icon
- Resets only after missing a full day
- No competition, just personal growth

### 4. **Quick Notes (Session Notes)**
- Automatic modal popup after stopping timer
- Subject auto-filled from study session
- 300-character limit for concise reflections
- Filter notes by subject or date
- Chronological display with metadata

### 5. **Dashboard Overview**
- Personalized greeting (Good morning/afternoon/evening)
- Today's total study time
- Current study streak
- Pending assignments count
- Weekly study bar chart
- Quick action cards
- Assignment previews

---

## 📁 Project Structure

```
studyflow/
├── core/              # Main Django app (models, views, URLs)
├── studyflow/         # Project settings and configuration
├── templates/         # HTML templates (base + core pages)
├── static/            # CSS, JavaScript, and assets
├── docs/              # All documentation files
├── scripts/           # Utility scripts
├── manage.py          # Django management command
├── requirements.txt   # Python dependencies
└── db.sqlite3         # SQLite database
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed structure.

---

## 🎨 Design System

**Notion-Inspired Dark Theme**

### Color Palette
```css
Primary Background: #191919
Card Background: #232323
Borders: #2e2e2e
Text Primary: #e6e6e6
Text Secondary: #9a9a9a

Accent Colors:
- Green: #4caf50 (progress)
- Orange: #ff9800 (warnings)
- Red: #f44336 (urgent)
- Blue: #2196f3 (actions)
```

### Design Principles
- Clean layout with 8px spacing system
- Rounded corners (10-14px)
- Soft shadows with low opacity
- Smooth hover transitions
- **Material Design Icons** v7.4.47
- Minimal, distraction-free interface
- Purposeful transitions only

---

## 🛠️ Technology Stack

### Backend
- **Django 6.0**
- **SQLite** database
- Django authentication system
- Django ORM for database operations

### Frontend
- **HTML5** for structure
- **Vanilla CSS** with CSS Variables
- **Vanilla JavaScript** (ES6+)
- **Material Design Icons** v7.4.47
- **Chart.js** for weekly analytics
- Responsive design (mobile + desktop)

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+ installed
- pip package manager

### Quick Start

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

6. **Access Application**
   ```
   Open browser to: http://127.0.0.1:8000/
   ```

For more details, see [docs/QUICK_START.md](docs/QUICK_START.md)

---

## 👤 Default Credentials

For testing purposes, a superuser has been created:

- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@studyflow.com`

You can use these credentials to:
1. Access the Django admin panel at http://localhost:8000/admin/
2. Create sample data for testing
3. Test the application features

---

## 📄 Pages & Navigation

### Public Pages
- **Login** (`/`)
- **Sign Up** (`/signup/`)

### Authenticated Pages
- **Dashboard** (`/dashboard/`) - Overview with stats and quick actions
- **Study Timer** (`/study/`) - Pomodoro-style study tracker
- **Assignments** (`/assignments/`) - Treemap visualization of deadlines
- **Notes** (`/notes/`) - Study session notes with filters

---

## 🗄️ Database Models

### 1. StudySession
```python
- user (ForeignKey)
- subject (CharField)
- duration (IntegerField)  # in minutes
- date (DateField)
- created_at (DateTimeField)
```

**Class Methods:**
- `get_today_total(user)` - Total study time for today
- `get_weekly_data(user)` - Last 7 days of study data
- `get_study_streak(user)` - Calculate consecutive study days

### 2. Assignment
```python
- user (ForeignKey)
- title (CharField)
- subject (CharField, nullable)
- deadline (DateTimeField)
- estimated_hours (FloatField, auto-calculated)
- status (CharField)  # pending/completed
- urgency (CharField, auto-calculated)  # low/medium/high
- created_at (DateTimeField)
- completed_at (DateTimeField, nullable)
```

**Instance Methods:**
- `hours_remaining()` - Calculate hours until deadline (float)
- `save()` - Auto-calculate urgency and estimated_hours

### 3. QuickNote
```python
- user (ForeignKey)
- subject (CharField)
- content (TextField)  # max 300 chars
- study_duration (IntegerField)  # in minutes
- created_at (DateTimeField)
```

---

## 🚀 Key Features Implementation

### Smart Treemap Visualization
- Dynamic sizing algorithm: `140px + √(hours_remaining) * 8` (max 300px)
- Automatic time calculation from deadline
- Time badges positioned in top-right corner (e.g., "12h", "3d 5h")
- Color coding based on urgency (auto-calculated)
- Smooth animations on completion
- Responsive flex layout

### AJAX Integration
- No page reloads for:
  - Saving study sessions
  - Adding assignments
  - Completing assignments
  - Saving quick notes
- CSRF token protection enabled
- Real-time treemap updates

---

## 📱 Responsive Design

- Sidebar collapses on mobile
- Grid layouts adapt to screen size
- Touch-friendly controls
- Treemap flexbox adapts to viewport
- Optimized for both desktop and mobile

---
---

## 🔒 Security Features

- Django CSRF protection
- Authentication required for all main pages
- Password validation with Django's built-in validators
- Secure session management
- SQL injection protection (Django ORM)

---

## 🎯 Usage Guide

### Starting a Study Session
1. Navigate to **Study Timer** page
2. Enter subject name (autocomplete available)
3. Click **Start** to begin timer
4. Optional: Click **Focus Mode** for distraction-free view
5. Click **Stop** when done
6. Add a quick note in the popup modal

### Managing Assignments
1. Navigate to **Assignments** page
2. Click **+ Add Assignment**
3. Fill in: **Title**, **Date**, and **Time** (that's it!)
4. System automatically calculates remaining hours
5. View assignments as sized cubes in treemap layout
6. Smaller cubes = less time remaining (more urgent)
7. Click on any cube to mark as completed

### Viewing Notes
1. Navigate to **Notes** page
2. Use filters to find specific notes by subject or date
3. View all your study session reflections

### Tracking Progress
1. Dashboard shows:
   - Today's study time
   - Current streak
   - Weekly chart
   - Upcoming assignments

---

## 📊 Analytics

### Weekly Chart
- Bar chart showing last 7 days
- Study time in minutes per day
- Helps identify study patterns
- Built with Chart.js

### Study Streak
- Counts consecutive days
- Motivates daily study habit
- Resets if you skip a day
- No pressure, just encouragement

---

## 🎨 Customization

### Changing Colors
Edit [static/css/style.css](static/css/style.css) and modify CSS variables:
```css
:root {
    --spacing: 8px;
    --bg-primary: #191919;
    --bg-secondary: #232323;
    --color-green: #4caf50;
    /* etc... */
}
```

### Icon Customization
The project uses Material Design Icons v7.4.47. Browse available icons at:
https://pictogrammers.com/library/mdi/

---

## 🐛 Troubleshooting

### Issue: Static files not loading
```bash
python manage.py collectstatic
```

### Issue: Database errors after model changes
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Migration conflicts
```bash
python manage.py migrate --run-syncdb
```

### Issue: Can't log in / Reset password
Use the password reset utility:
```bash
python scripts/set_password.py
```

Or via Django shell:
```python
python manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='your_username')
user.set_password('new_password')
user.save()
```

---

## 📚 Documentation

- [Quick Start Guide](docs/QUICK_START.md)
- [Project Walkthrough](docs/PROJECT_WALKTHROUGH.md)
- [Testing Guide](docs/TESTING_GUIDE.md)
- [Design Reference](docs/DESIGN_REFERENCE.md)
- [UI Enhancements](docs/UI_ENHANCEMENTS.md)
- [Enhancement Summary](docs/ENHANCEMENT_SUMMARY.md)

---

## 🔮 Future Enhancements

- [ ] Export study data as CSV/PDF
- [ ] Assignment reminder notifications
- [ ] Study session tags and categories
- [ ] Advanced analytics dashboard
- [ ] Calendar integration
- [ ] Mobile app (React Native)
- [ ] Collaborative study groups

---

## 🤝 Contributing

This is a student project. Feel free to:
- Report bugs
- Suggest features
- Improve documentation
- Submit pull requests

---

## 📄 License

This project is created for educational purposes.

---

## 👨‍💻 Developer

Built as a Mini Project for Semester 2

**Project Name**: StudyFlow  
**Purpose**: Personalized Learning Platform  
**Tech Stack**: Django 6.0, SQLite, Vanilla JS, Material Design Icons

---

## 🌟 Why StudyFlow?

**Philosophy**: Calm, habit-building, student-friendly

StudyFlow focuses on:
- Simplicity over complexity
- Progress over perfection  
- Habits over cramming
- Visual clarity over feature bloat

Built with ❤️ for students who want a peaceful, distraction-free study companion.

---

## 📞 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Material Design Icons](https://pictogrammers.com/library/mdi/)
- [Chart.js Documentation](https://www.chartjs.org/)
- Chart.js documentation: https://www.chartjs.org/docs/

---

**Happy Studying! 📚✨**
