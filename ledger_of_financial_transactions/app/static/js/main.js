/**
 * Main JavaScript for Financial Ledger Application
 * Handles common functionality across all pages
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-dismiss flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Toggle password visibility
    document.querySelectorAll('.toggle-password').forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const input = document.getElementById(targetId);
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('bi-eye');
                icon.classList.add('bi-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('bi-eye-slash');
                icon.classList.add('bi-eye');
            }
        });
    });

    // Format currency inputs
    document.querySelectorAll('.currency-input').forEach(input => {
        input.addEventListener('input', function(e) {
            // Remove any non-digit characters except decimal point
            let value = this.value.replace(/[^\d.]/g, '');
            
            // Ensure only one decimal point
            const decimalSplit = value.split('.');
            if (decimalSplit.length > 2) {
                value = decimalSplit[0] + '.' + decimalSplit.slice(1).join('');
            }
            
            // Format with 2 decimal places
            if (decimalSplit.length === 2) {
                value = decimalSplit[0] + '.' + decimalSplit[1].slice(0, 2);
            }
            
            this.value = value;
        });
    });

    // Handle form submissions with confirmation
    document.querySelectorAll('form[data-confirm]').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm(this.getAttribute('data-confirm'))) {
                e.preventDefault();
                return false;
            }
            return true;
        });
    });

    // Auto-submit forms when select changes
    document.querySelectorAll('select[data-auto-submit]').forEach(select => {
        select.addEventListener('change', function() {
            this.form.submit();
        });
    });

    // Initialize datepickers
    if (typeof flatpickr !== 'undefined') {
        document.querySelectorAll('.datepicker').forEach(input => {
            flatpickr(input, {
                dateFormat: 'Y-m-d',
                allowInput: true
            });
        });
    }

    // Handle sidebar toggle for mobile
    const sidebarToggler = document.getElementById('sidebarToggler');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggler && sidebar) {
        sidebarToggler.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768 && sidebar && !sidebar.contains(e.target) && !e.target.matches('#sidebarToggler, #sidebarToggler *')) {
            sidebar.classList.remove('show');
        }
    });

    // Handle file input styling
    document.querySelectorAll('.custom-file-input').forEach(input => {
        input.addEventListener('change', function() {
            const fileName = this.files[0]?.name || 'Choose file';
            const label = this.nextElementSibling;
            label.textContent = fileName;
        });
    });

    // Handle tab persistence
    const tabLinks = document.querySelectorAll('a[data-bs-toggle="tab"]');
    tabLinks.forEach(tab => {
        tab.addEventListener('click', function() {
            const tabId = this.getAttribute('href');
            localStorage.setItem('lastTab', tabId);
        });
    });

    // Restore last active tab
    const lastTab = localStorage.getItem('lastTab');
    if (lastTab) {
        const tab = new bootstrap.Tab(document.querySelector(`a[href="${lastTab}"]`));
        tab.show();
    }

    // Handle print buttons
    document.querySelectorAll('.print-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });

    // Initialize charts if Chart.js is available
    if (typeof Chart !== 'undefined') {
        initializeCharts();
    }
});

/**
 * Initialize dashboard charts
 */
function initializeCharts() {
    // Monthly Expenses Chart
    const expensesCtx = document.getElementById('monthlyExpensesChart');
    if (expensesCtx) {
        new Chart(expensesCtx, {
            type: 'line',
            data: {
                labels: JSON.parse(expensesCtx.dataset.labels || '[]'),
                datasets: [{
                    label: 'Expenses',
                    data: JSON.parse(expensesCtx.dataset.values || '[]'),
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            drawBorder: false
                        },
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    // Categories Pie Chart
    const categoriesCtx = document.getElementById('categoriesChart');
    if (categoriesCtx) {
        const backgroundColors = [
            '#4361ee', '#3f37c9', '#4895ef', '#4cc9f0', '#f72585',
            '#b5179e', '#7209b7', '#560bad', '#480ca8', '#3a0ca3'
        ];

        new Chart(categoriesCtx, {
            type: 'doughnut',
            data: {
                labels: JSON.parse(categoriesCtx.dataset.labels || '[]'),
                datasets: [{
                    data: JSON.parse(categoriesCtx.dataset.values || '[]'),
                    backgroundColor: backgroundColors,
                    borderWidth: 0,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: $${value.toLocaleString()} (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '60%'
            }
        });
    }
}

/**
 * Format date as time ago
 * @param {Date} date - The date to format
 * @returns {string} Formatted time ago string
 */
function timeAgo(date) {
    if (!date) return '';
    
    const seconds = Math.floor((new Date() - new Date(date)) / 1000);
    
    const intervals = {
        year: 31536000,
        month: 2592000,
        week: 604800,
        day: 86400,
        hour: 3600,
        minute: 60,
        second: 1
    };
    
    for (const [unit, secondsInUnit] of Object.entries(intervals)) {
        const interval = Math.floor(seconds / secondsInUnit);
        if (interval >= 1) {
            return interval === 1 ? `1 ${unit} ago` : `${interval} ${unit}s ago`;
        }
    }
    
    return 'just now';
}

// Add timeAgo to window for global access
window.timeAgo = timeAgo;

// Add a global error handler
window.addEventListener('error', function(e) {
    console.error('An error occurred:', e.error || e.message || e);
    
    // Show a user-friendly error message
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show position-fixed bottom-0 end-0 m-3';
    alertDiv.style.zIndex = '9999';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        <strong>Error:</strong> An unexpected error occurred. Please try again.
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
});

// Add a global AJAX error handler
$(document).ajaxError(function(event, jqXHR, ajaxSettings, thrownError) {
    console.error('AJAX Error:', thrownError || jqXHR.statusText);
    
    // Show error message to user
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show position-fixed bottom-0 end-0 m-3';
    alertDiv.style.zIndex = '9999';
    alertDiv.role = 'alert';
    
    let errorMessage = 'An error occurred while processing your request.';
    
    try {
        const response = JSON.parse(jqXHR.responseText);
        if (response.message) {
            errorMessage = response.message;
        }
    } catch (e) {
        console.error('Error parsing error response:', e);
    }
    
    alertDiv.innerHTML = `
        <strong>Error:</strong> ${errorMessage}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
});
