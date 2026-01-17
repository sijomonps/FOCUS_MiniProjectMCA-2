# 🚀 FOCUS - Quick Start Guide

Welcome to **FOCUS**! This guide will get you up and running in just a few minutes.

---

## ⚡ Quick Setup (5 Minutes)

### Prerequisites
- Python 3.8 or higher installed
- Basic command line knowledge

### Step 1: Navigate to Project Directory
```bash
cd "c:\Users\sijom\OneDrive\Desktop\Marian\Sem2\Mini Project"
```

### Step 2: Verify Django Installation
Django is already installed. The server should already be running!

If it's not running, start it with:
```bash
python manage.py runserver
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:8000/**

---

## 🎓 First Time User Guide

### Create Your Account

1. **Click "Sign up"** on the login page
2. **Choose a username** (e.g., "student1")
3. **Create a password** (must be at least 8 characters)
4. **Confirm password**
5. **Click "Create Account"**

You'll be automatically logged in and redirected to your dashboard!

---

## 📚 Using FOCUS

### 1. **Start Your First Study Session**

**Go to: Study Timer** (sidebar)

1. Enter what you're studying (e.g., "Mathematics")
2. Click **Start** button
3. Study! The timer will count up automatically
4. Optional: Click **Focus Mode** for distraction-free view
5. When done, click **Stop**
6. Add a quick note about what you learned (optional)
7. Your session is automatically saved!

**Tips:**
- Use Focus Mode during deep study sessions
- Keep notes brief (300 characters max)
- Subject names autocomplete from past sessions

---

### 2. **Add Your First Assignment**

**Go to: Assignments** (sidebar)

1. Click **+ Add Assignment** button
2. Fill in the details:
   - **Title**: e.g., "Math Quiz 1"
   - **Subject**: e.g., "Mathematics"
   - **Deadline**: Pick a date
   - **Estimated Hours**: How long you think it'll take
3. Click **Add Assignment**
4. Watch it appear as a colored cube!

**Understanding the Colors:**
- 🟢 **Green**: You have plenty of time
- 🟠 **Orange**: Getting closer (< 7 days)
- 🔴 **Red**: Urgent! (< 3 days or overdue)

**To Complete an Assignment:**
- Simply click on its cube
- Confirm completion
- It fades away smoothly!

---

### 3. **View Your Notes**

**Go to: Notes** (sidebar)

- See all your study session reflections
- Filter by **Subject** or **Date**
- Review what you've learned over time

---

### 4. **Check Your Dashboard**

**Go to: Dashboard** (sidebar)

Your dashboard shows:
- ⏱️ **Today's Study Time**: Total minutes studied today
- 🔥 **Study Streak**: Consecutive days of studying
- 📝 **Pending Tasks**: Number of incomplete assignments
- 📊 **Weekly Chart**: Visual representation of your study pattern
- 📋 **Upcoming Assignments**: Preview of deadlines

---

## 🎯 Study Workflow Recommendation

1. **Morning**: Check dashboard → Review assignments
2. **Start Study**: Use timer → Take notes after each session
3. **Evening**: Review dashboard → Plan tomorrow

---

## 💡 Pro Tips

### Study Timer
- Start small: Even 15 minutes counts!
- Use Focus Mode to eliminate distractions
- Write notes immediately while fresh in your mind
- Track different subjects separately

### Assignments
- Add assignments as soon as you get them
- Be realistic with estimated hours
- Check the treemap daily for visual urgency
- Celebrate completions (they fade away nicely!)

### Streaks
- Study even 10 minutes to keep your streak
- Don't stress if you break it - just start again!
- Consistency matters more than duration

### Dashboard
- Make it your homepage
- Check it first thing when studying
- Use the weekly chart to spot patterns
- Aim for steady improvement, not perfection

---

## 🎨 Interface Guide

### Sidebar Navigation
Always visible on the left side (desktop):
- 📊 **Dashboard**: Overview and analytics
- ⏱️ **Study Timer**: Track study sessions
- 📝 **Assignments**: Deadline visualization
- 📔 **Notes**: Study reflections

On mobile: Sidebar auto-hides

### Color Meanings
- **Blue**: Interactive elements, actions
- **Green**: Success, low urgency, progress
- **Orange**: Medium urgency, warnings
- **Red**: High urgency, important deadlines

---

## 🔐 Account Management

### Logging Out
Click the **Logout** button at the bottom of the sidebar

### Logging Back In
- Username: Your chosen username
- Password: Your password
- Click **Login**

### Forgot Password?
Contact admin to reset (this is a local development version)

---

## 🐛 Troubleshooting

### "Server not running" error
```bash
python manage.py runserver
```
Then refresh your browser

### "CSRF token missing" error
- Refresh the page
- Clear browser cache
- Try in incognito mode

### Assignment won't add
- Make sure deadline is in YYYY-MM-DD format
- Check all fields are filled
- Look for error messages

### Timer won't start
- Enter a subject first
- Refresh the page and try again

---

## 📱 Mobile Use

FOCUS works on mobile devices:
- Tap the menu icon to open sidebar
- All features are touch-friendly
- Landscape mode recommended for charts

---

## 🎓 Sample Study Session

Let's do a complete workflow:

**1. Check Dashboard**
- See you studied 30 minutes yesterday
- Current streak: 3 days
- 2 assignments pending

**2. Add Assignment**
- Title: "History Essay"
- Subject: "History"
- Deadline: Next Friday
- Hours: 5
- **Added!** Shows as orange cube (7 days away)

**3. Start Study Session**
- Subject: "History"
- Click Start
- Study for 45 minutes
- Click Stop
- Note: "Researched topic, found 3 good sources"
- **Saved!**

**4. Check Dashboard Again**
- Today's time: 45 minutes
- Streak: 4 days (continued!)
- Weekly chart shows new bar

**5. Done!**
- Feel accomplished ✅
- Come back tomorrow to continue streak

---

## 🌟 Feature Highlights

### What Makes FOCUS Special?

1. **Habit Building**
   - Streaks without pressure
   - Visual progress tracking
   - Positive reinforcement

2. **Visual Deadlines**
   - Treemap makes urgency clear at a glance
   - No missed deadlines
   - Satisfying completion animations

3. **Integrated Notes**
   - Tied to study sessions
   - Prompts reflection
   - Easy to review later

4. **Calm Design**
   - Dark theme reduces eye strain
   - Minimal distractions
   - Notion-inspired aesthetics

---

## 📊 Understanding Your Data

### Study Time
- Measured in minutes
- Aggregated by day/week
- Subject breakdowns available in notes

### Streaks
- Count consecutive days with any study
- Reset if you skip a full day
- Start fresh anytime!

### Assignments
- Urgency auto-calculated
- Visual size = estimated effort
- Completion rate visible in history

---

## 🎉 Your First Week Goals

**Day 1**: Set up account, explore interface
**Day 2**: Complete first study session with notes
**Day 3**: Add 3-5 assignments to treemap
**Day 4**: Try Focus Mode, maintain streak
**Day 5**: Review notes, check weekly chart
**Day 6**: Complete an assignment, continue streak
**Day 7**: Celebrate your first week! 🎊

---

## 🆘 Need Help?

### Documentation
- **README.md**: Full project documentation
- **PROJECT_WALKTHROUGH.md**: Technical details

### Admin Access
For testing/demo purposes:
- URL: http://localhost:8000/admin/
- Username: `admin`
- Password: `admin123`

---

## ✨ Final Tips

1. **Be Consistent**: Study every day, even if brief
2. **Be Honest**: Accurate time tracking helps you improve
3. **Reflect**: Write meaningful notes
4. **Visualize**: Use the treemap to stay organized
5. **Enjoy**: Studying should feel calm, not stressful

---

**Ready to start building better study habits?**

**Click here to begin:** [http://localhost:8000/](http://localhost:8000/)

---

*Happy Studying! 📚✨*
