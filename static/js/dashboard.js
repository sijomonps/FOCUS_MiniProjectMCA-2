// Dashboard JavaScript - FOCUS Study Platform
// This file contains all dashboard initialization logic

console.log('Dashboard script loaded from external file');

// --- Helper: Safe JSON Parse ---
function safeParse(jsonStr, fallback) {
    try {
        if (!jsonStr) return fallback;
        const parsed = JSON.parse(jsonStr);
        return parsed === null ? fallback : parsed;
    } catch (e) {
        console.error('Data parsing error:', e);
        return fallback;
    }
}

// Initialize Dashboard - This will be called from the inline template with data
function initDashboard(config) {
    console.log('initDashboard called');

    // Extract data from config passed from template
    const weeklyLabels = config.weeklyLabels || [];
    const weeklyData = config.weeklyData || [];
    const monthlyLabels = config.monthlyLabels || [];
    const monthlyData = config.monthlyData || [];
    const subjectLabels = config.subjectLabels || [];
    const subjectData = config.subjectData || [];
    const calendarAssignments = config.calendarAssignments || [];
    const hasSubjectBreakdown = config.hasSubjectBreakdown || false;

    // --- Chart.js Check ---
    const chartJsAvailable = typeof Chart !== 'undefined';
    if (!chartJsAvailable) {
        console.error('Chart.js is not loaded. Charts will not be displayed.');
        const chartContainers = document.querySelectorAll('canvas');
        chartContainers.forEach(c => {
            c.style.display = 'none';
            const msg = document.createElement('div');
            msg.textContent = 'Chart library failed to load.';
            msg.className = 'text-tertiary';
            msg.style.padding = '20px';
            msg.style.textAlign = 'center';
            c.parentNode.insertBefore(msg, c.nextSibling);
        });
    } else {
        console.log('Chart.js is ready.');
    }

    // --- Activity Chart Logic ---
    let activityChart = null;

    function initActivityChart(type) {
        if (!chartJsAvailable) return;

        const chartElement = document.getElementById('activityChart');
        if (!chartElement) return;

        const ctx = chartElement.getContext('2d');
        const gradient = ctx.createLinearGradient(0, 0, 0, 200);
        gradient.addColorStop(0, 'rgba(79, 70, 229, 0.4)');
        gradient.addColorStop(1, 'rgba(79, 70, 229, 0.0)');

        if (activityChart) activityChart.destroy();

        const labels = type === 'weekly' ? weeklyLabels : monthlyLabels;
        const data = type === 'weekly' ? weeklyData : monthlyData;

        // Ensure data is array
        const safeLabels = Array.isArray(labels) ? labels : [];
        const safeData = Array.isArray(data) ? data : [];

        activityChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: safeLabels,
                datasets: [{
                    label: 'Minutes',
                    data: safeData,
                    backgroundColor: gradient,
                    borderColor: '#4f46e5',
                    borderWidth: 2,
                    pointBackgroundColor: '#4f46e5',
                    pointRadius: type === 'weekly' ? 4 : 2,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: 'rgba(255, 255, 255, 0.7)' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: {
                            maxTicksLimit: type === 'weekly' ? 7 : 10,
                            autoSkip: true,
                            color: 'rgba(255, 255, 255, 0.7)'
                        }
                    }
                }
            }
        });
    }

    // Expose toggle function globally
    window.toggleChart = function (type) {
        const btnWeekly = document.getElementById('btnWeekly');
        const btnMonthly = document.getElementById('btnMonthly');
        const title = document.getElementById('chartTitle');

        if (type === 'weekly') {
            btnWeekly.classList.add('active');
            btnMonthly.classList.remove('active');
            title.innerHTML = '<i class="mdi mdi-chart-line" style="margin-right: 8px;"></i> Weekly Activity';
        } else {
            btnWeekly.classList.remove('active');
            btnMonthly.classList.add('active');
            title.innerHTML = '<i class="mdi mdi-calendar-month" style="margin-right: 8px;"></i> Monthly Activity';
        }
        initActivityChart(type);
    };

    // Initialize defaults
    initActivityChart('weekly');

    // --- Pie Chart Logic ---
    if (hasSubjectBreakdown && chartJsAvailable) {
        const pieCtx = document.getElementById('subjectPieChart');
        if (pieCtx) {
            const pieColors = [
                '#6366f1', '#8b5cf6', '#ec4899', '#f43f5e', '#f97316',
                '#eab308', '#22c55e', '#14b8a6', '#06b6d4', '#3b82f6'
            ];

            // CSS for legend dots
            pieColors.forEach((color, i) => {
                const style = document.createElement('style');
                style.innerHTML = `.pie-color-${i} { background: ${color} !important; }`;
                document.head.appendChild(style);
            });

            const safeSubLabels = Array.isArray(subjectLabels) ? subjectLabels : [];
            const safeSubData = Array.isArray(subjectData) ? subjectData : [];

            new Chart(pieCtx, {
                type: 'doughnut',
                data: {
                    labels: safeSubLabels,
                    datasets: [{
                        data: safeSubData,
                        backgroundColor: pieColors.slice(0, safeSubData.length),
                        borderWidth: 0,
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    cutout: '60%',
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    const mins = context.raw;
                                    const hours = Math.floor(mins / 60);
                                    const m = mins % 60;
                                    return hours > 0 ? `${hours}h ${m}m` : `${m}m`;
                                }
                            }
                        }
                    }
                }
            });
        }
    }

    // --- Calendar Logic ---
    let currentDate = new Date();
    let selectedDate = new Date();

    function renderCalendar() {
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();
        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

        const monthEl = document.getElementById('calendarMonthYear');
        if (monthEl) monthEl.textContent = `${monthNames[month]} ${year}`;

        const grid = document.getElementById('calendarGrid');
        if (!grid) return;
        grid.innerHTML = '';

        const firstDay = new Date(year, month, 1).getDay();
        const adjustedFirstDay = firstDay === 0 ? 6 : firstDay - 1;
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        // Empty slots
        for (let i = 0; i < adjustedFirstDay; i++) {
            const div = document.createElement('div');
            div.className = 'calendar-day empty';
            grid.appendChild(div);
        }

        const today = new Date();
        // Safe array for iteration
        const safeAssignments = Array.isArray(calendarAssignments) ? calendarAssignments : [];

        for (let i = 1; i <= daysInMonth; i++) {
            const div = document.createElement('div');
            div.className = 'calendar-day';
            div.textContent = i;

            // Event check
            const hasEvent = safeAssignments.some(t => {
                if (!t.deadline) return false; // Guard against missing deadline
                const d = new Date(t.deadline);
                return d.getFullYear() === year && d.getMonth() === month && d.getDate() === i;
            });
            if (hasEvent) div.classList.add('has-event');

            if (year === today.getFullYear() && month === today.getMonth() && i === today.getDate()) div.classList.add('current-day');
            if (year === selectedDate.getFullYear() && month === selectedDate.getMonth() && i === selectedDate.getDate()) div.classList.add('active');

            div.onclick = () => {
                selectedDate = new Date(year, month, i);
                renderCalendar();
                renderSchedule();
            };

            grid.appendChild(div);
        }
    }

    window.changeMonth = function (delta) {
        currentDate.setMonth(currentDate.getMonth() + delta);
        renderCalendar();
    };

    function renderSchedule() {
        const selectedDateList = document.getElementById('selectedDateList');
        const upcomingList = document.getElementById('upcomingList');
        const selectedDateCount = document.getElementById('selectedDateCount');
        const upcomingCount = document.getElementById('upcomingCount');
        const selectedDateLabel = document.getElementById('selectedDateLabel');

        if (!selectedDateList || !upcomingList) return;

        selectedDateList.innerHTML = '';
        upcomingList.innerHTML = '';

        // Format label
        const now = new Date();
        const todayDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        const selDate = new Date(selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate());

        if (selectedDateLabel) {
            if (selDate.getTime() === todayDate.getTime()) {
                selectedDateLabel.textContent = 'Today';
            } else {
                const options = { month: 'short', day: 'numeric' };
                selectedDateLabel.textContent = selectedDate.toLocaleDateString('en-US', options);
            }
        }

        // Safe array
        const safeAssignments = Array.isArray(calendarAssignments) ? calendarAssignments : [];
        const selectedDateTasks = [];
        const upcomingTasks = [];

        safeAssignments.forEach(task => {
            if (!task.deadline) return;
            const deadline = new Date(task.deadline);
            const deadlineDate = new Date(deadline.getFullYear(), deadline.getMonth(), deadline.getDate());

            if (deadlineDate.getTime() === selDate.getTime()) {
                selectedDateTasks.push(task);
            } else {
                upcomingTasks.push(task);
            }
        });

        selectedDateTasks.sort((a, b) => new Date(a.deadline) - new Date(b.deadline));
        upcomingTasks.sort((a, b) => new Date(a.deadline) - new Date(b.deadline));

        if (selectedDateCount) selectedDateCount.textContent = selectedDateTasks.length > 0 ? `${selectedDateTasks.length}` : '';
        if (upcomingCount) upcomingCount.textContent = upcomingTasks.length > 0 ? `${upcomingTasks.length}` : '';

        // Render logic helper
        const renderList = (tasks, container, emptyMsg) => {
            if (tasks.length === 0) {
                container.innerHTML = `<div class="text-tertiary" style="text-align: center; padding: 20px; font-size: 0.85rem;">${emptyMsg}</div>`;
            } else {
                tasks.forEach(task => renderTaskItem(task, container));
            }
        };

        renderList(selectedDateTasks, selectedDateList, '<i class="mdi mdi-calendar-blank-outline" style="opacity: 0.5;"></i> No tasks for this date');
        renderList(upcomingTasks, upcomingList, 'No other pending tasks');
    }

    function renderTaskItem(task, container) {
        const item = document.createElement('div');
        item.className = 'schedule-item';

        const deadline = new Date(task.deadline || new Date());
        const now = new Date();
        const msLeft = deadline - now;
        const hoursLeft = msLeft / (1000 * 60 * 60);
        const daysLeft = hoursLeft / 24;

        let ringColor = '#4f46e5';
        if (hoursLeft <= 0) ringColor = '#dc2626';
        else if (hoursLeft <= 6) ringColor = '#ef4444';
        else if (hoursLeft <= 24) ringColor = '#f59e0b';
        else if (hoursLeft <= 72) ringColor = '#4f46e5';
        else ringColor = '#10b981';

        const maxHours = 168;
        let percent = Math.max(0, Math.min(100, (hoursLeft / maxHours) * 100));
        if (hoursLeft <= 0) percent = 0;
        const circumference = 100;
        const offset = circumference - (percent / 100 * circumference);

        let timeText = '';
        if (hoursLeft <= 0) {
            const ho = Math.abs(hoursLeft);
            timeText = ho < 24 ? `${Math.floor(ho)}h overdue` : `${Math.floor(ho / 24)}d overdue`;
        } else if (hoursLeft < 1) {
            timeText = `${Math.floor(hoursLeft * 60)}m`;
        } else {
            timeText = hoursLeft < 24 ? `${Math.floor(hoursLeft)}h` : `${Math.floor(daysLeft)}d`;
        }

        // Safe urgency access
        const urgency = task.urgency || 'low';

        item.innerHTML = `
            <div class="ring-container">
                 <svg class="ring-svg">
                    <circle class="ring-circle-bg" cx="18" cy="18" r="16"></circle>
                    <circle class="ring-circle-progress" cx="18" cy="18" r="16" stroke="${ringColor}" stroke-dashoffset="${offset}"></circle>
                </svg>
                <div class="ring-dot" style="background: ${ringColor}; transform: translate(-50%, -50%) rotate(${percent * 3.6}deg) translate(16px) rotate(-${percent * 3.6}deg);"></div>
            </div>
            <div class="schedule-info">
                <div class="schedule-title">${task.subject}: ${task.title}</div>
                <div class="schedule-meta" style="color: ${ringColor}">
                     ${timeText} remaining
                </div>
            </div>
        `;
        container.appendChild(item);
    }

    // Leaderboard Toggle
    let lbMode = 'streaks';
    window.toggleLeaderboard = function () {
        const title = document.getElementById('lbTitle');
        const streakBoard = document.getElementById('streakBoard');
        const timeBoard = document.getElementById('timeBoard');

        if (lbMode === 'streaks') {
            lbMode = 'time';
            title.innerHTML = '<i class="mdi mdi-clock-outline"></i> Monthly Top Time';
            streakBoard.style.display = 'none';
            timeBoard.style.display = 'flex';
        } else {
            lbMode = 'streaks';
            title.innerHTML = '<i class="mdi mdi-fire"></i> Top Streaks';
            streakBoard.style.display = 'flex';
            timeBoard.style.display = 'none';
        }
    };

    // Initialize Calendar
    renderCalendar();
    renderSchedule();

    console.log('Dashboard initialization complete');
}

// Make initDashboard available globally
window.initDashboard = initDashboard;
