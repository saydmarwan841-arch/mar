/**
 * Quiz App - Main JavaScript
 * Handles interactions, animations, and user experience enhancements
 */

// DOM Ready
document.addEventListener('DOMContentLoaded', function () {
    // Initialize tooltips and interactions
    initializeQuiz();
});

/**
 * Initialize quiz interactions
 */
function initializeQuiz() {
    // Set focus on first interactive element
    const firstRadio = document.querySelector('input[type="radio"]');
    if (firstRadio) {
        firstRadio.focus();
    }

    // Add event listeners to options
    addOptionListeners();

    // Initialize animations
    initializeAnimations();
}

/**
 * Add event listeners to quiz options
 */
function addOptionListeners() {
    const options = document.querySelectorAll('.option-label');

    options.forEach(option => {
        option.addEventListener('click', function () {
            // Remove animation from all options
            options.forEach(o => o.classList.remove('option-selected'));
            // Add animation to clicked option
            this.classList.add('option-selected');
        });

        // Keyboard navigation
        const input = option.querySelector('input[type="radio"]');
        if (input) {
            input.addEventListener('change', function () {
                // Smooth transition
                option.classList.add('option-selected');
            });
        }
    });
}

/**
 * Initialize page animations
 */
function initializeAnimations() {
    // Animate progress bar
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        const width = progressBar.style.width;
        progressBar.style.width = '0';
        setTimeout(() => {
            progressBar.style.width = width;
        }, 100);
    }

    // Stagger animate options
    const optionLabels = document.querySelectorAll('.option-label');
    optionLabels.forEach((option, index) => {
        option.style.animation = `slideUpIn 0.5s ease-out ${index * 0.1}s backwards`;
    });
}

/**
 * Handle form submission with animation
 */
function handleQuizSubmit() {
    const form = document.querySelector('.answer-form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        const selectedOption = document.querySelector('input[type="radio"]:checked');

        if (!selectedOption) {
            e.preventDefault();
            showNotification('الرجاء اختيار إجابة', 'error');
            return;
        }

        // Add loading animation
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.style.opacity = '0.7';
        }

        // Fade out effect
        const questionCard = document.querySelector('.question-card');
        if (questionCard) {
            questionCard.style.transition = 'opacity 0.3s ease';
            questionCard.style.opacity = '0.5';
        }
    });
}

/**
 * Show notification message
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background: ${type === 'error' ? '#F5A6A6' : '#FFB6D9'};
        color: white;
        border-radius: 10px;
        font-weight: 600;
        z-index: 1000;
        animation: slideDown 0.3s ease-out;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideUp 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * Keyboard shortcuts
 */
document.addEventListener('keydown', function (e) {
    // Number keys to select options
    if (e.key >= '1' && e.key <= '4') {
        const optionIndex = parseInt(e.key) - 1;
        const radios = document.querySelectorAll('input[type="radio"]');
        if (radios[optionIndex]) {
            radios[optionIndex].checked = true;
            radios[optionIndex].dispatchEvent(new Event('change', { bubbles: true }));
        }
    }

    // Enter to submit
    if (e.key === 'Enter') {
        const form = document.querySelector('.answer-form');
        if (form) {
            form.dispatchEvent(new Event('submit'));
        }
    }
});

/**
 * Add smooth scroll behavior
 */
window.addEventListener('scroll', function () {
    const elements = document.querySelectorAll('.glass-card, .option-label');
    elements.forEach(el => {
        const rect = el.getBoundingClientRect();
        const isVisible = rect.top < window.innerHeight && rect.bottom > 0;

        if (isVisible) {
            el.style.opacity = '1';
        }
    });
});

/**
 * Performance optimization - Lazy load animations
 */
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'slideUpIn 0.6s ease-out';
            observer.unobserve(entry.target);
        }
    });
});

document.querySelectorAll('.glass-card').forEach(card => {
    observer.observe(card);
});

/**
 * Add ripple effect on button click
 */
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function (e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            background: radial-gradient(circle, rgba(255,255,255,0.5), transparent);
            border-radius: 50%;
            left: ${x}px;
            top: ${y}px;
            pointer-events: none;
            animation: ripple 0.6s ease-out;
        `;

        this.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    });
});

/**
 * CSS Animations injected via JavaScript for dynamic elements
 */
const style = document.createElement('style');
style.textContent = `
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideUp {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-20px);
        }
    }

    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }

    .option-selected {
        animation: pulse 0.3s ease-out !important;
    }

    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.02);
        }
        100% {
            transform: scale(1);
        }
    }
`;
document.head.appendChild(style);

// Call form handler
handleQuizSubmit();
