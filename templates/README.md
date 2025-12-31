# Templates Folder

This folder contains all HTML templates that define how pages look.

## 📁 Structure

```
templates/
├── base.html          # Base template (navigation, header, footer)
└── core/              # Core app templates
    ├── dashboard.html     # Main dashboard with stats
    ├── assignments.html   # Treemap visualization
    ├── study.html         # Study timer page
    ├── notes.html         # Notes management
    ├── login.html         # User login
    └── signup.html        # User registration
```

## 🎨 How Templates Work

### Template Inheritance
All pages extend `base.html` which provides:
- Common navigation sidebar
- Header with user info
- Material Design Icons
- CSS and JS imports
- Consistent layout

### Example:
```html
{% extends 'base.html' %}

{% block title %}Dashboard{% endblock %}

{% block content %}
    <!-- Your page content here -->
{% endblock %}
```

## 🔗 Template Tags

- `{% extends 'base.html' %}` - Inherit from base template
- `{% block content %}` - Define content section
- `{{ variable }}` - Display variable value
- `{% for item in list %}` - Loop through items
- `{% if condition %}` - Conditional rendering

## 📝 Editing Tips

1. **Change navigation** → Edit `base.html`
2. **Modify dashboard** → Edit `core/dashboard.html`
3. **Update treemap** → Edit `core/assignments.html`
4. **Customize styles** → Edit `static/css/style.css`

All templates use the Notion-dark theme with Material Design Icons.
