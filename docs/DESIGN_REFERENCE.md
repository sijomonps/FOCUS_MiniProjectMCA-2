# 🎨 Quick Design Reference Card

## 🎨 Color Variables (CSS)

```css
/* Backgrounds */
--bg-primary: #191919
--bg-secondary: #1f1f1f
--bg-tertiary: #2a2a2a
--bg-hover: #292929

/* Borders */
--border-color: #313131
--border-color-light: #3a3a3a

/* Text */
--text-primary: #ffffff
--text-secondary: #9b9b9b
--text-tertiary: #6b6b6b

/* Accents */
--color-blue: #60a5fa
--color-green: #4ade80
--color-orange: #fb923c
--color-red: #f87171
--color-purple: #a78bfa
```

## 📏 Spacing Scale

```css
--spacing-xs: 4px
--spacing-sm: 8px
--spacing-md: 16px
--spacing-lg: 24px
--spacing-xl: 32px
--spacing-2xl: 48px
--spacing-3xl: 64px
```

## 🔲 Border Radius

```css
--border-radius-sm: 4px
--border-radius: 6px
--border-radius-lg: 8px
--border-radius-xl: 12px
```

## 🌫️ Shadows

```css
--shadow-sm: 0 1px 3px rgba(0,0,0,0.3)
--shadow: 0 2px 8px rgba(0,0,0,0.4)
--shadow-lg: 0 4px 16px rgba(0,0,0,0.5)
--shadow-xl: 0 8px 32px rgba(0,0,0,0.6)
```

## ⚡ Transitions

```css
--transition-fast: 150ms ease
--transition-base: 200ms ease
--transition-slow: 300ms ease
```

## 🎯 Common Classes

### Layout
- `.flex` - Display flex
- `.flex-center` - Center items
- `.flex-between` - Space between
- `.grid` - CSS Grid
- `.grid-2/3/4` - Column layouts

### Spacing
- `.mb-1/2/3/4` - Margin bottom
- `.mt-1/2/3/4` - Margin top
- `.gap-1/2/3` - Grid/flex gap

### Text
- `.text-center/left/right` - Alignment
- `.page-title` - Main heading
- `.page-subtitle` - Subheading

### Components
- `.btn` - Base button
- `.btn-primary/secondary/success/danger/ghost` - Variants
- `.btn-sm/lg` - Sizes
- `.card` - Card container
- `.modal` - Modal dialog
- `.badge` - Status badge

## 📱 Breakpoints

```css
/* Mobile */
@media (max-width: 768px)

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px)

/* Desktop */
@media (min-width: 1025px)
```

## 🎬 Animations

```css
/* Fade in page */
.fade-in

/* Pulse effect */
.pulse

/* Hover lift */
.hover-lift

/* Loading skeleton */
.skeleton
```

## 🔧 Utility Functions (JS)

```javascript
// Toast notification
showToast(message, type)

// Debounce function
debounce(func, wait)

// Get cookie
getCookie(name)

// Fetch data
fetchData(url, options)
```

## 🎨 Usage Examples

### Button
```html
<button class="btn btn-primary btn-lg">
    <span>🚀</span>
    <span>Get Started</span>
</button>
```

### Card
```html
<div class="card">
    <div class="card-header">
        <h3 class="card-title">Title</h3>
    </div>
    <div class="card-body">
        Content
    </div>
</div>
```

### Stat Card
```html
<div class="stat-card">
    <span class="stat-icon">📊</span>
    <div class="stat-value">42</div>
    <div class="stat-label">Total</div>
</div>
```

### Badge
```html
<span class="badge badge-green">Success</span>
<span class="badge badge-orange">Warning</span>
<span class="badge badge-red">Error</span>
```

## 🎯 Key Features

✅ **Professional Design**: Notion-inspired dark theme
✅ **Smooth Animations**: 60fps hardware-accelerated
✅ **Responsive**: Mobile, Tablet, Desktop
✅ **Accessible**: WCAG compliant
✅ **Performant**: Optimized CSS/JS
✅ **Consistent**: Design system
✅ **Interactive**: Hover effects & transitions

## 📝 Quick Tips

1. **Use CSS variables** for colors
2. **Follow spacing scale** for consistency
3. **Add hover effects** to interactive elements
4. **Use semantic HTML** for accessibility
5. **Test on multiple devices**
6. **Keep animations smooth** (< 300ms)
7. **Maintain contrast** for readability

---

**Print this for quick reference!** 📄✨
