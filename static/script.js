const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');
const html = document.documentElement;

// Function to update UI based on theme
const updateThemeUI = (isDark) => {
    if (isDark) {
        html.classList.add('dark');
        themeIcon.innerText = '☀️';
        localStorage.setItem('theme', 'dark');
    } else {
        html.classList.remove('dark');
        themeIcon.innerText = '🌙';
        localStorage.setItem('theme', 'light');
    }
};

// Initialize theme (Default to Dark as requested)
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'light') {
    updateThemeUI(false);
} else {
    updateThemeUI(true);
}

themeToggle.addEventListener('click', () => {
    const isDark = html.classList.contains('dark');
    updateThemeUI(!isDark);
});

// Reset Functionality
const resetBtn = document.getElementById('resetBtn');
const messageInput = document.getElementById('messageInput');

resetBtn.addEventListener('click', () => {
    messageInput.value = '';
    // Redirect to root to clear results
    window.location.href = '/';
});