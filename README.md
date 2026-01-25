# 🎯 FOCUS - Your Personal Study Companion

<div align="center">

![FOCUS Logo](https://img.shields.io/badge/FOCUS-Study%20Smarter-6699BB?style=for-the-badge&logo=target&logoColor=white)

**A Smart Study Management Application**

*MCA Semester 2 Mini Project*  
*Marian College Kuttikanam*

---

[![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-Web%20Framework-green?style=flat-square&logo=django)](https://djangoproject.com)
[![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)]()

</div>

---

## 📖 What is FOCUS?

**FOCUS** is a web-based study management application designed to help students organize their academic life. Think of it as your digital study buddy that helps you:

- ⏱️ **Track your study time** - Know exactly how much you're studying
- 📋 **Manage assignments** - Never miss a deadline again
- 📝 **Organize notes** - Keep all your quick notes in one place
- 📊 **Visualize progress** - See your study patterns and improve

---

## 🤔 The Problem

> *"I studied for hours but don't know where my time went..."*
> 
> *"I forgot about that assignment due tomorrow!"*
> 
> *"My notes are scattered everywhere - in books, phones, and random papers..."*

**Sound familiar?** 

As students, we often struggle with:

| Problem | Impact |
|---------|--------|
| 😵 **No time awareness** | Study for hours without knowing if it's effective |
| 📅 **Missed deadlines** | Forget assignments until the last minute |
| 📑 **Disorganized notes** | Waste time searching for information |
| 📉 **No progress tracking** | Can't identify weak areas or improvements |
| 🎯 **Lack of focus** | Get distracted easily without structure |

---

## 💡 The Solution

**FOCUS** provides a simple, beautiful, and effective solution:

### 🎯 One App, Everything You Need

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   📊 DASHBOARD          ⏱️ STUDY TIMER                 │
│   See your progress     Track focus sessions           │
│   at a glance           with subjects                  │
│                                                         │
│   📋 ASSIGNMENTS        📝 QUICK NOTES                 │
│   Visual deadline       Organized by                   │
│   management            subject folders                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

### 1. 📊 Smart Dashboard
Your personal command center showing:
- Today's study time (live updating!)
- Weekly/Monthly progress charts
- Subject-wise breakdown (pie chart)
- Upcoming assignment deadlines with calendar
- Study streak counter 🔥

### 2. ⏱️ Focus Timer
A beautiful Pomodoro-style timer:
- Pre-set durations (15, 25, 45, 60 minutes)
- Custom time option (up to 180 minutes)
- Subject selection for tracking
- Session completion notifications with sound 🔔
- **Live timer in sidebar** (visible on all pages!)
- Paused sessions are preserved

### 3. 📋 Assignment Tracker
Never miss a deadline with:
- Visual treemap showing all assignments
- Color-coded urgency:
  - 🟢 Green = Plenty of time
  - 🟡 Yellow = Getting close
  - 🔴 Red = Due soon! (with pulse animation)
- Time remaining display (hours/days)
- Mark as complete ✅
- View completed assignments history

### 4. 📝 Quick Notes
Organize your thoughts:
- Create subject folders 📁
- Pin important notes (up to 4 per subject) 📌
- Quick capture of ideas
- Edit and delete notes easily
- Responsive grid layout

### 5. 👨‍💼 Admin Panel (For Administrators)
Complete user management:
- View all registered users
- Monitor platform statistics
- Enable/disable user accounts
- View individual user details
- Delete users when needed

---

## 🎨 Beautiful Dark Theme

FOCUS features a modern, eye-friendly dark theme perfect for late-night study sessions:

- 🌙 **Easy on the eyes** - Reduced eye strain
- 🎯 **Minimal distractions** - Clean interface
- ✨ **Modern design** - Notion-inspired aesthetics
- 📱 **Fully responsive** - Works on mobile, tablet, and desktop!

---

## 🚀 How It Works

### For Students:

```
1️⃣ Sign Up / Login
        ↓
2️⃣ Start a focus timer session with your subject
        ↓
3️⃣ Add your assignments with deadlines
        ↓
4️⃣ Create quick notes as you study
        ↓
5️⃣ Check dashboard to see your progress!
        ↓
6️⃣ Build your study streak 🔥
```

### Simple Example:

| Action | What Happens |
|--------|--------------|
| Start 25-min timer for "Mathematics" | Timer counts down, shows in sidebar on all pages |
| Timer completes | 25 minutes added to your Math study time + sound notification |
| Check Dashboard | See Math progress in pie chart, weekly graph updates |
| Add assignment "Math Homework - Due Friday" | Appears in treemap with countdown timer |
| Write a quick note about formulas | Saved in your Math folder, can pin it for quick access |

---

## 🖥️ Screen Overview

### Dashboard
```
┌──────────────────────────────────────────────────┐
│  Good evening, Student! 👋                       │
│                                                  │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐           │
│  │ 2h   │ │ 5🔥  │ │ 3    │ │ 12h  │           │
│  │Today │ │Streak│ │Tasks │ │Month │           │
│  └──────┘ └──────┘ └──────┘ └──────┘           │
│                                                  │
│  📊 Weekly Progress        🥧 Subject Breakdown  │
│  Mon ████████              Math: 40%            │
│  Tue ████░░░░              Science: 35%         │
│  Wed ██████████            English: 25%         │
│                                                  │
│  📅 Calendar    📋 Upcoming Assignments          │
│                                                  │
└──────────────────────────────────────────────────┘
```

### Focus Timer
```
┌──────────────────────────────────────────────────┐
│                                                  │
│              🎯 Focus Session                    │
│                                                  │
│                 24:59                            │
│              ───────────                         │
│                                                  │
│    [15m] [25m] [45m] [60m] [Custom]             │
│                                                  │
│         Subject: [Mathematics ▼]                 │
│                                                  │
│              [ ⏸️ Pause ]                        │
│                                                  │
│         Today's Study: 1h 25m 🟢                 │
│                                                  │
└──────────────────────────────────────────────────┘
```

### Assignment Treemap
```
┌──────────────────────────────────────────────────┐
│                                                  │
│  ┌────────────┐ ┌──────────────────┐            │
│  │ 🔴 Math HW │ │ 🟢 Project Report │            │
│  │   2 days   │ │     14 days      │            │
│  └────────────┘ │                  │            │
│  ┌────────────┐ └──────────────────┘            │
│  │ 🟡 Essay   │ ┌──────────┐                    │
│  │   5 days   │ │ 🟢 Quiz  │                    │
│  └────────────┘ │  10 days │                    │
│                 └──────────┘                    │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| 🐍 Backend | Python + Django | Server-side logic & database |
| 🎨 Frontend | HTML, CSS, JavaScript | User interface |
| 💾 Database | SQLite | Data storage |
| 📊 Charts | Chart.js | Visual graphs |
| 🎯 Icons | Material Design Icons | Beautiful icons |
| 🌙 Theme | Custom CSS | Dark theme styling |

---

## 📦 Installation Guide

### What You Need
- Python 3.8 or higher installed on your computer
- A web browser (Chrome, Firefox, Edge, etc.)

### Step-by-Step Setup

```bash
# Step 1: Open terminal/command prompt and navigate to project folder
cd "Mini Project"

# Step 2: Create a virtual environment (keeps things organized)
python -m venv venv

# Step 3: Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Step 4: Install required packages
pip install -r requirements.txt

# Step 5: Set up the database
python manage.py migrate

# Step 6: Create an admin account
python manage.py createsuperuser
# (Follow the prompts to set username and password)

# Step 7: Start the application
python manage.py runserver

# Step 8: Open your browser and visit:
# http://127.0.0.1:8000
```

### 🎉 That's it! You're ready to use FOCUS!

---

## 👤 How to Use

### For New Users

1. **Create Your Account**
   - Click "Sign Up" on the login page
   - Choose a username and password
   - Click "Create Account"

2. **Start Studying**
   - Go to "Study Timer" from the sidebar
   - Select your subject from the dropdown
   - Choose how long you want to study (25 min is a good start!)
   - Click "Start" and focus!

3. **Track Assignments**
   - Go to "Assignments" from the sidebar
   - Click "Add Assignment"
   - Fill in: Title, Subject, Due Date & Time
   - Watch it appear in your visual treemap!

4. **Take Notes**
   - Go to "Quick Notes" from the sidebar
   - Create a folder for your subject
   - Click "+" to add notes
   - Pin important notes for quick access (📌)

5. **Check Your Progress**
   - Visit "Dashboard" anytime
   - See today's study time
   - View weekly/monthly charts
   - Track your study streak!

---

## 🔐 For Administrators

If you're an admin, you'll see additional options:

- **Admin Panel** - Overview of all platform statistics
- **Manage Users** - View, disable, or delete user accounts

Admin accounts see a different sidebar without student features.

---

## 🎯 Why the Name "FOCUS"?

```
F - Focus Timer for distraction-free study
O - Organize assignments and notes
C - Chart your progress visually  
U - Understand your study patterns
S - Succeed in your academics!
```

---

## 📊 What Makes FOCUS Special?

| Feature | Benefit |
|---------|---------|
| 🔴 Live Timer | See timer running even when on other pages |
| 📊 Visual Treemap | Assignments sized by urgency - big = more time |
| 📌 Pin Notes | Quick access to important information |
| 🌙 Dark Theme | Study comfortably at any time |
| 📱 Responsive | Use on phone, tablet, or computer |
| 🔥 Streaks | Stay motivated with daily goals |

---

## 🎓 About This Project

### Project Information
- **Project Name:** FOCUS - Study Management Application
- **Course:** Master of Computer Applications (MCA)
- **Semester:** 2
- **Institution:** Marian College Kuttikanam
- **Project Type:** Mini Project

### Learning Outcomes
Through this project, I learned:
- ✅ Web development with Django framework
- ✅ Database design and management
- ✅ Frontend development (HTML, CSS, JavaScript)
- ✅ User authentication and authorization
- ✅ Responsive design principles
- ✅ Real-time features with JavaScript
- ✅ Data visualization with charts

---

## 🚀 Future Improvements

Ideas for future versions:
- 📱 Dedicated mobile app
- 🔔 Push notifications for deadlines
- 👥 Study groups and collaboration
- 🏆 Achievements and badges system
- 📊 Downloadable study reports
- ☁️ Cloud sync across devices
- 🎵 Background study music/sounds

---

## 📁 Project Structure

```
FOCUS/
├── 📱 CORE APPLICATION
│   ├── core/                          # Main Django app (all features)
│   ├── studyflow/                     # Django project configuration
│   ├── templates/                     # HTML templates
│   ├── static/                        # CSS, JS, images
│   └── manage.py                      # Django management script
│
├── 📚 DOCUMENTATION
│   └── docs/                          # All project documentation
│       ├── QUICK_START.md             # Getting started guide
│       ├── BEGINNER_GUIDE.md          # Beginner-friendly tutorial
│       ├── HOW_IT_WORKS.md            # Feature explanations
│       ├── PROJECT_WALKTHROUGH.md     # Complete project tour
│       └── DEPLOYMENT.md              # Deployment instructions
│
├── 🛠️ UTILITIES
│   └── scripts/                       # Utility scripts
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
└── 📖 ROOT FILES
    ├── README.md                      # Main project README (this file!)
    ├── PROJECT_ORGANIZATION.md        # Detailed structure guide
    ├── requirements.txt               # Python dependencies
    └── db.sqlite3                     # SQLite database
```

**📘 For detailed structure explanation, see [PROJECT_ORGANIZATION.md](PROJECT_ORGANIZATION.md)**

---

## ❓ Troubleshooting

### Common Issues

**"Page not found" error**
- Make sure the server is running (`python manage.py runserver`)
- Check the URL: should be `http://127.0.0.1:8000`

**"Module not found" error**
- Activate your virtual environment first
- Run `pip install -r requirements.txt`

**Database errors**
- Run `python manage.py migrate`

**Forgot admin password**
- Create a new superuser: `python manage.py createsuperuser`

---

## 📝 License

This project was created for educational purposes as part of the MCA curriculum at Marian College Kuttikanam.

---

<div align="center">

## 💖 Thank You!

Thank you for checking out FOCUS! 

This project represents my learning journey in web development during MCA Semester 2.

---

**Made with ❤️ for Students, by a Student**

*Marian College Kuttikanam*  
*MCA - Semester 2 | 2026*

---

### 📚 *"The secret of getting ahead is getting started."*

**Happy Studying! 🎯**

</div>
