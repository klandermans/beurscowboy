/**
 * Beurs Cowboy - Main JavaScript
 * Handles theme toggle, search, mobile menu, and filtering
 */

// ============================================
// Theme Management
// ============================================
class ThemeManager {
    constructor() {
        this.toggle = document.getElementById('themeToggle');
        this.currentTheme = localStorage.getItem('theme') || this.getSystemTheme();
        this.init();
    }

    getSystemTheme() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }

    init() {
        this.applyTheme(this.currentTheme);
        if (this.toggle) {
            this.toggle.addEventListener('click', () => this.toggleTheme());
        }
        
        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                this.currentTheme = e.matches ? 'dark' : 'light';
                this.applyTheme(this.currentTheme);
            }
        });
    }

    toggleTheme() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(this.currentTheme);
        localStorage.setItem('theme', this.currentTheme);
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
    }
}

// ============================================
// Mobile Menu Management
// ============================================
class MobileMenuManager {
    constructor() {
        this.toggle = document.getElementById('mobileMenuToggle');
        this.nav = document.getElementById('mainNav');
        this.init();
    }

    init() {
        if (this.toggle && this.nav) {
            this.toggle.addEventListener('click', () => this.toggleMenu());
            
            // Close menu when clicking nav links
            this.nav.querySelectorAll('a').forEach(link => {
                link.addEventListener('click', () => this.closeMenu());
            });
            
            // Close menu when clicking outside
            document.addEventListener('click', (e) => {
                if (!this.toggle.contains(e.target) && !this.nav.contains(e.target)) {
                    this.closeMenu();
                }
            });
        }
    }

    toggleMenu() {
        this.toggle.classList.toggle('active');
        this.nav.classList.toggle('active');
        document.body.style.overflow = this.nav.classList.contains('active') ? 'hidden' : '';
    }

    closeMenu() {
        this.toggle.classList.remove('active');
        this.nav.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// ============================================
// Search Management
// ============================================
class SearchManager {
    constructor() {
        this.searchToggle = document.getElementById('searchToggle');
        this.searchBar = document.getElementById('searchBar');
        this.searchInput = document.getElementById('searchInput');
        this.searchClose = document.getElementById('searchClose');
        this.searchData = window.searchData?.results || {};
        this.init();
    }

    init() {
        if (this.searchToggle) {
            this.searchToggle.addEventListener('click', () => this.toggleSearch());
        }
        if (this.searchClose) {
            this.searchClose.addEventListener('click', () => this.closeSearch());
        }
        if (this.searchInput) {
            this.searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value));
            this.searchInput.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') this.closeSearch();
            });
        }
        // Close on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') this.closeSearch();
        });
    }

    toggleSearch() {
        const isActive = this.searchBar.classList.toggle('active');
        if (isActive) {
            this.searchInput.focus();
        }
    }

    closeSearch() {
        this.searchBar.classList.remove('active');
        this.searchInput.value = '';
        this.resetFilters();
    }

    handleSearch(query) {
        if (!query.trim()) {
            this.resetFilters();
            return;
        }

        const lowercaseQuery = query.toLowerCase();
        const rows = document.querySelectorAll('.stock-row');

        rows.forEach(row => {
            const ticker = row.dataset.ticker?.toLowerCase() || '';
            const sector = row.dataset.sector?.toLowerCase() || '';
            const signal = row.dataset.signal?.toLowerCase() || '';
            
            const matches = ticker.includes(lowercaseQuery) ||
                           sector.includes(lowercaseQuery) ||
                           signal.includes(lowercaseQuery);
            
            row.style.display = matches ? '' : 'none';
        });
    }

    resetFilters() {
        const rows = document.querySelectorAll('.stock-row');
        rows.forEach(row => {
            row.style.display = '';
        });
    }
}

// ============================================
// Filter Management
// ============================================
class FilterManager {
    constructor() {
        this.filterButtons = document.querySelectorAll('.filter-btn');
        this.init();
    }

    init() {
        this.filterButtons.forEach(btn => {
            btn.addEventListener('click', () => this.handleFilter(btn));
        });
    }

    handleFilter(button) {
        // Update active state
        this.filterButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        const filter = button.dataset.filter;
        const rows = document.querySelectorAll('.stock-row');

        rows.forEach(row => {
            const signal = row.dataset.signal || '';
            
            if (filter === 'all') {
                row.style.display = '';
            } else if (filter === 'buy' && (signal === 'buy' || signal === 'buy-strong')) {
                row.style.display = '';
            } else if (filter === 'sell' && (signal === 'sell' || signal === 'sell-strong')) {
                row.style.display = '';
            } else if (filter === 'neutral' && signal === 'neutral') {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
}

// ============================================
// Table Sorting
// ============================================
class TableSortManager {
    constructor() {
        this.headers = document.querySelectorAll('.market-table th');
        this.init();
    }

    init() {
        this.headers.forEach((header, index) => {
            const sortable = header.dataset.sortable !== 'false';
            if (sortable) {
                header.style.cursor = 'pointer';
                header.setAttribute('role', 'button');
                header.setAttribute('tabindex', '0');
                header.addEventListener('click', () => this.sortTable(index));
                header.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        this.sortTable(index);
                    }
                });
            }
        });
    }

    sortTable(columnIndex) {
        const table = document.querySelector('.market-table');
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        // Determine sort direction
        const isAscending = !table.dataset.sortAsc || table.dataset.sortAsc === 'false';
        table.dataset.sortAsc = isAscending;

        // Update header indicators
        this.headers.forEach((h, i) => {
            h.textContent = h.textContent.replace(' ▲', '').replace(' ▼', '');
            if (i === columnIndex) {
                h.textContent += isAscending ? ' ▲' : ' ▼';
            }
        });

        // Sort rows
        rows.sort((a, b) => {
            const aValue = this.getCellText(a, columnIndex);
            const bValue = this.getCellText(b, columnIndex);
            
            // Try numeric sort first
            const aNum = parseFloat(aValue.replace(/[€,$,%]/g, '').replace(/,/g, ''));
            const bNum = parseFloat(bValue.replace(/[€,$,%]/g, '').replace(/,/g, ''));
            
            if (!isNaN(aNum) && !isNaN(bNum)) {
                return isAscending ? aNum - bNum : bNum - aNum;
            }
            
            // Fall back to string sort
            return isAscending 
                ? aValue.localeCompare(bValue)
                : bValue.localeCompare(aValue);
        });

        // Re-append sorted rows
        rows.forEach(row => tbody.appendChild(row));
    }

    getCellText(row, index) {
        return row.cells[index]?.textContent.trim() || '';
    }
}

// ============================================
// Smooth Scroll for Anchor Links
// ============================================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    });
}

// ============================================
// Touch-friendly Enhancements
// ============================================
function initTouchEnhancements() {
    // Add touch-friendly hover states
    const isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    if (isTouch) {
        document.documentElement.classList.add('touch');
    }
}

// ============================================
// Performance: Debounce Helper
// ============================================
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

// ============================================
// Initialize Everything
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    new ThemeManager();
    new MobileMenuManager();
    new SearchManager();
    new FilterManager();
    new TableSortManager();
    initSmoothScroll();
    initTouchEnhancements();

    console.log('🤠 Beurs Cowboy initialized');
});

// ============================================
// Utility Functions
// ============================================
function formatNumber(num) {
    return new Intl.NumberFormat('nl-NL').format(num);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('nl-NL', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

function formatPercent(percent) {
    return new Intl.NumberFormat('nl-NL', {
        style: 'percent',
        minimumFractionDigits: 2
    }).format(percent / 100);
}

// Export for use in other scripts
window.BeursCowboy = {
    formatNumber,
    formatCurrency,
    formatPercent,
    debounce
};
