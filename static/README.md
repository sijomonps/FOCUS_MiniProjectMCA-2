# Static Files Folder

This folder contains CSS, JavaScript, images, and other static assets.

## 📁 Structure

```
static/
├── css/
│   └── style.css      # Main stylesheet (Notion-dark theme)
└── js/
    └── app.js         # JavaScript functionality
```

## 🎨 CSS (style.css)

### What's Inside:
- **CSS Variables** - Color scheme, spacing, fonts
- **Layout Styles** - Sidebar, cards, grids
- **Component Styles** - Buttons, forms, modals
- **Animations** - Smooth transitions, hover effects
- **Responsive Design** - Mobile and desktop layouts

### Key CSS Variables:
```css
:root {
    --spacing: 8px;              /* Base spacing unit */
    --bg-primary: #191919;       /* Main background */
    --bg-secondary: #232323;     /* Cards background */
    --text-primary: #e6e6e6;     /* Main text color */
    --color-green: #4caf50;      /* Success/progress */
    --color-orange: #ff9800;     /* Warnings */
    --color-red: #f44336;        /* Urgent/errors */
}
```

## 📜 JavaScript (app.js)

### Features:
- Study timer logic (start, pause, stop)
- Assignment treemap rendering
- Form submissions (AJAX)
- Animations and transitions
- Quick note modal

### Key Functions:
- `calculateHoursRemaining()` - Calculate time until deadline
- `formatHoursRemaining()` - Format as "12h" or "3d 5h"
- `renderTreemap()` - Display assignments as sized cubes
- Timer controls and session tracking

## 🔧 Customization

### Change Colors:
Edit CSS variables in `css/style.css`

### Add New Styles:
1. Open `css/style.css`
2. Add your CSS at the bottom
3. Refresh browser (Ctrl+F5 to clear cache)

### Modify JavaScript:
1. Open `js/app.js`
2. Add/modify functions
3. Test in browser console first

## 📦 External Libraries

- **Material Design Icons** v7.4.47 (CDN) - Icon library
- **Chart.js** (CDN) - Weekly analytics charts

No npm or build process required - pure vanilla CSS & JS!
