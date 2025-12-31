# How to Deploy StudyFlow for Free

The simplest and most reliable way to deploy a Django project with a database (SQLite) for free is **PythonAnywhere**.

I have already pre-configured your project with the necessary settings (`whitenoise` for static files, `ALLOWED_HOSTS`).

## Option 1: PythonAnywhere (Recommended)
This option is free forever and keeps your dadabase safe (unlike Render's free tier which might wipe SQLite files).

### Step 1: Open Terminal on PythonAnywhere
1. Go to [PythonAnywhere.com](https://www.pythonanywhere.com/) and create a "Beginner" (free) account.
2. Go to the **Consoles** tab and click **Bash**.

### Step 2: Clone your GitHub Repo
In the console, run:
```bash
# Clone your repository (replace URL with YOUR github link)
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Go into the folder
cd YOUR_REPO_NAME
```

### Step 3: Install Dependencies
In the Bash Console, run:
```bash
# Create a virtual environment
mkvirtualenv --python=/usr/bin/python3.10 my-env

# Install your project requirements
pip install -r requirements.txt
```

### Step 4: Configure the Web App
1. Go to the **Web** tab on PythonAnywhere.
2. Click **Add a new web app**.
3. Select **Manual configuration** (not Django, trust me, this avoids default file overwrites).
4. Select **Python 3.10** (ensure it matches the virtualenv version).
5. Once created, scroll down to **Virtualenv**:
   - Enter the path: `/home/yourusername/.virtualenvs/my-env` (check the path in your console if unsure).

### Step 5: Configure WSGI
1. In the **Code** section of the Web tab, click the link to edit the **WSGI configuration file**.
2. Delete everything and paste this (replace `yourusername` and paths if different):
   ```python
   import os
   import sys

   # path to your project folder (change 'YOUR_REPO_NAME' to the actual folder name)
   path = '/home/yourusername/YOUR_REPO_NAME'
   if path not in sys.path:
       sys.path.append(path)

   os.environ['DJANGO_SETTINGS_MODULE'] = 'studyflow.settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
3. Save the file.

### Step 6: Finalize
1. Go back to the **Web** tab.
2. Click the big green **Reload** button.
3. Click the link to your site (e.g., `yourusername.pythonanywhere.com`).

---

## Option 2: Render.com (Modern, but tricky with Database)
Render is great but their free tier does **not** keep your SQLite database. If your app restarts, you lose your data. To use Render properly, you need an external database (like Neon, free Postgres) which adds complexity.

If you still want to try Render:
1. Create a GitHub repository and push your code there.
2. Sign up on Render with GitHub.
3. Create a **New Web Service**.
4. Connect your repo.
5. Render will detect Python. 
6. Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
7. Start Command: `gunicorn studyflow.wsgi:application`
8. **Add Environment Variable**: `PYTHON_VERSION` = `3.11.0` (or similar).

*Note: I added `whitenoise` to your project, so static files will work on both platforms.*
