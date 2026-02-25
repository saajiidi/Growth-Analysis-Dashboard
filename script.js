// Theme Toggle Logic with Persistence
const toggleBtn = document.getElementById('theme-toggle');
const body = document.body;

// Initialize theme from localStorage
const savedTheme = localStorage.getItem('theme') || 'light';
body.setAttribute('data-theme', savedTheme);
updateToggleUI(savedTheme);

toggleBtn.addEventListener('click', () => {
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateToggleUI(newTheme);
});

function updateToggleUI(theme) {
    const span = toggleBtn.querySelector('span');
    span.textContent = theme === 'dark' ? '🌙' : '☀️';

    // Optional: Update Plotly charts theme colors here if theme changes
    // This would require replotting with new layout colors
}

// Global Chart Resizing
window.addEventListener('resize', () => {
    const plots = document.querySelectorAll('.js-plotly-plot');
    plots.forEach(plot => Plotly.Plots.resize(plot));
});
