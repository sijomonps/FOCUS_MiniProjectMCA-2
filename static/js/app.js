// ================================
// Enhanced UI Interactions
// ================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all enhanced features
    initSmoothScrolling();
    initTooltips();
    initAnimations();
    initKeyboardShortcuts();
    initThemeEnhancements();
    initGlobalTimer();
});

// Smooth scrolling for anchor links
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Initialize tooltips
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const tooltipText = e.target.getAttribute('data-tooltip');
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = tooltipText;
    tooltip.style.cssText = `
        position: absolute;
        background: var(--bg-tertiary);
        color: var(--text-primary);
        padding: 6px 12px;
        border-radius: var(--border-radius);
        font-size: 0.85rem;
        z-index: 9999;
        pointer-events: none;
        white-space: nowrap;
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--border-color);
    `;
    document.body.appendChild(tooltip);
    
    const rect = e.target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
    
    e.target._tooltip = tooltip;
}

function hideTooltip(e) {
    if (e.target._tooltip) {
        e.target._tooltip.remove();
        e.target._tooltip = null;
    }
}

// Intersection Observer for animations
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.card, .stat-card').forEach(el => {
        observer.observe(el);
    });
}

// Keyboard shortcuts
function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K for quick search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            // You can add search functionality here
            console.log('Quick search triggered');
        }
        
        // ESC to close modals
        if (e.key === 'Escape') {
            const modal = document.querySelector('.modal-overlay.active');
            if (modal) {
                modal.classList.remove('active');
            }
        }
    });
}

// Theme enhancements
function initThemeEnhancements() {
    // Add loading state management
    window.addEventListener('load', () => {
        document.body.classList.add('loaded');
    });
    
    // Auto-dismiss messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateX(20px)';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
}

// Utility function for AJAX requests
async function fetchData(url, options = {}) {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
                ...options.headers
            }
        });
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        right: 24px;
        background: var(--bg-secondary);
        color: var(--text-primary);
        padding: 16px 24px;
        border-radius: var(--border-radius-lg);
        box-shadow: var(--shadow-xl);
        border: 1px solid var(--border-color);
        z-index: 9999;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Add CSS for toast animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    .animate-in {
        animation: fadeInUp 0.5s ease forwards;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);


// ================================
// Global Timer Logic
// ================================
function initGlobalTimer() {
    const timerContainer = document.getElementById('globalTimerContainer');
    const timerDisplay = document.getElementById('globalTimerDisplay');
    const timerLabel = document.querySelector('.global-timer-label');
    const timerDot = document.querySelector('.global-timer-dot');

    if (!timerContainer || !timerDisplay) return;

    // Update function that runs frequently
    function updateGlobalTimerDisplay() {
        const savedState = localStorage.getItem('focusTimerState');
        
        // Don't show on study page - it has its own big timer
        const isStudyPage = window.location.pathname.includes('/study');
        if (isStudyPage) {
            timerContainer.classList.add('hidden');
            return;
        }

        if (!savedState) {
            timerContainer.classList.add('hidden');
            return;
        }

        try {
            const state = JSON.parse(savedState);
            
            if (state.isRunning && state.timerEndTime) {
                const now = Date.now();
                const remaining = Math.max(0, Math.floor((state.timerEndTime - now) / 1000));
                
                if (remaining > 0) {
                    // Timer is running - show it
                    timerContainer.classList.remove('hidden');
                    
                    // Format time
                    const m = Math.floor(remaining / 60);
                    const s = remaining % 60;
                    timerDisplay.textContent = `${m}:${s < 10 ? '0' : ''}${s}`;
                    
                    // Update label with subject if available
                    if (timerLabel && state.subject) {
                        timerLabel.textContent = `Studying: ${state.subject}`;
                    } else if (timerLabel) {
                        timerLabel.textContent = 'Session Active';
                    }
                    
                    // Ensure dot is pulsing red
                    if (timerDot) {
                        timerDot.style.background = 'var(--color-red)';
                        timerDot.style.boxShadow = '0 0 8px var(--color-red)';
                    }
                } else {
                    // Timer ended
                    timerContainer.classList.add('hidden');
                }
            } else if (!state.isRunning && state.remainingTime && state.remainingTime < state.selectedDuration) {
                // Timer is paused with remaining time
                timerContainer.classList.remove('hidden');
                
                const m = Math.floor(state.remainingTime / 60);
                const s = state.remainingTime % 60;
                timerDisplay.textContent = `${m}:${s < 10 ? '0' : ''}${s}`;
                
                if (timerLabel) {
                    timerLabel.textContent = 'Paused';
                }
                
                // Show yellow dot for paused
                if (timerDot) {
                    timerDot.style.background = 'var(--color-yellow)';
                    timerDot.style.boxShadow = '0 0 8px var(--color-yellow)';
                    timerDot.style.animation = 'none';
                }
            } else {
                timerContainer.classList.add('hidden');
            }
        } catch (e) {
            timerContainer.classList.add('hidden');
        }
    }

    // Run immediately
    updateGlobalTimerDisplay();
    
    // Update every 200ms for smooth countdown
    setInterval(updateGlobalTimerDisplay, 200);
    
    // Also update when tab becomes visible
    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) {
            updateGlobalTimerDisplay();
        }
    });
}
