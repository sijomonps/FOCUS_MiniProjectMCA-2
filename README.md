# 🎯 FOCUS – Simple Study Dashboard

FOCUS is a small web app that helps students see their study life in one clean place: time spent, subjects, assignments, and streaks.

It is built as an MCA Semester 2 mini project using **Python + Django**.

---

## 🧠 Problem It Solves

Many students:

- Study for hours but **don’t know how much they really did**
- **Forget assignments** until the last minute
- Have notes **spread across books, photos, and random apps**
- Find it hard to **stay consistent** day after day

FOCUS was made to handle these simple but real problems.

---

## ✅ What FOCUS Gives You

- **Dashboard** – see today’s study time, streak, weekly/monthly graph, and subject breakdown
- **Study Timer** – start a focused session with a subject; time is saved automatically
- **Assignments** – add tasks with deadlines and see urgency visually
- **Quick Notes** – keep short notes grouped by subject
- **Leaderboard & Streaks** – small motivation boost by seeing top learners and your own streak

Everything is designed to be minimal, calm, and easy to understand even on first use.

---

## 🎓 Who Is This For?

- School / college students who want a **simple study tracker**
- Beginners who are **new to productivity tools**
- Anyone who wants to **see their progress instead of guessing**

You don’t need any technical knowledge to use the website.

---

## 🚀 Run the Project (Local Setup)

1. Open a terminal in the project folder.
2. Create and activate a virtual environment:

        ```bash
        python -m venv venv
        venv\Scripts\activate   # on Windows
        ```

3. Install dependencies and set up the database:

        ```bash
        pip install -r requirements.txt
        python manage.py migrate
        ```

4. Start the server and open the site:

        ```bash
        python manage.py runserver
        ```

        Then visit: http://127.0.0.1:8000

---

## 🔍 Learn More (Optional)

If you want more details about how everything works:

- Beginner overview: [docs/BEGINNER_GUIDE.md](docs/BEGINNER_GUIDE.md)
- Quick setup guide: [docs/QUICK_START.md](docs/QUICK_START.md)
- Full project tour: [docs/PROJECT_WALKTHROUGH.md](docs/PROJECT_WALKTHROUGH.md)

This README stays short on purpose so even a beginner can read it in one go and understand **what the project is, why it exists, and how to run it**.
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
