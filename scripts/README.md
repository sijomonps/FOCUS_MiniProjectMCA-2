# Utility Scripts

This folder contains helper scripts for common tasks.

## 📜 Available Scripts

### `set_password.py`
Reset user password without accessing Django admin.

**Usage:**
```bash
python scripts/set_password.py
```

**What it does:**
1. Prompts for username
2. Prompts for new password
3. Updates password in database
4. Confirms success

**Use cases:**
- Forgot admin password
- Need to reset user password
- Testing with different users

## 💡 Creating New Scripts

When adding utility scripts, follow this pattern:

```python
#!/usr/bin/env python
"""
Script Name: describe_purpose.py
Description: What this script does
Usage: python scripts/script_name.py
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyflow.settings')
django.setup()

# Import models after Django setup
from django.contrib.auth import get_user_model
from core.models import Assignment, StudySession, QuickNote

# Your script logic here
def main():
    pass

if __name__ == '__main__':
    main()
```

## 🔧 Common Script Ideas

- **create_sample_data.py** - Generate test assignments and sessions
- **export_data.py** - Export user data as CSV
- **cleanup_old_sessions.py** - Remove sessions older than X days
- **backup_database.py** - Create database backup
- **calculate_stats.py** - Generate study statistics report

All scripts should:
- Include a docstring explaining purpose
- Setup Django environment first
- Have helpful error messages
- Be idempotent (safe to run multiple times)
