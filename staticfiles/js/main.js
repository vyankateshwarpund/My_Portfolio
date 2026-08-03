// Production Main JavaScript Controller
document.addEventListener('DOMContentLoaded', () => {
    initPreloader();
    initTheme();
    initTypewriter();
    initParticles();
    initCustomCursor();
    initBackToTop();
    initCountUp();
    initContactForm();
    initProjectLike();
});

// Preloader Screen Handler
function initPreloader() {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;
    setTimeout(() => {
        preloader.style.opacity = '0';
        preloader.style.visibility = 'hidden';
    }, 700);
}

// Theme Switcher (Dark/Light Mode)
function initTheme() {
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const savedTheme = localStorage.getItem('vp_theme') || 'dark';

    if (savedTheme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        if (themeToggleBtn) themeToggleBtn.innerHTML = '<i class="bi bi-moon-stars-fill"></i>';
    } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        if (themeToggleBtn) themeToggleBtn.innerHTML = '<i class="bi bi-sun-fill"></i>';
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            let newTheme = 'dark';
            if (currentTheme === 'dark') {
                newTheme = 'light';
                themeToggleBtn.innerHTML = '<i class="bi bi-moon-stars-fill"></i>';
            } else {
                themeToggleBtn.innerHTML = '<i class="bi bi-sun-fill"></i>';
            }
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('vp_theme', newTheme);
        });
    }
}

// Typewriter Effect
function initTypewriter() {
    const element = document.getElementById('typewriter-text');
    if (!element) return;

    const roles = [
        "Junior Software Engineer",
        "Python Developer",
        "Django Backend Developer",
        "Python Full Stack Developer"
    ];
    let roleIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    function type() {
        const currentRole = roles[roleIndex];
        if (isDeleting) {
            element.textContent = currentRole.substring(0, charIndex - 1);
            charIndex--;
        } else {
            element.textContent = currentRole.substring(0, charIndex + 1);
            charIndex++;
        }

        let speed = isDeleting ? 40 : 80;

        if (!isDeleting && charIndex === currentRole.length) {
            speed = 2000;
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            roleIndex = (roleIndex + 1) % roles.length;
            speed = 400;
        }

        setTimeout(type, speed);
    }
    type();
}

// Particles Canvas Background
function initParticles() {
    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    const particles = [];
    const particleCount = Math.min(Math.floor(width / 22), 55);

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
            radius: Math.random() * 2 + 1
        });
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);

        const isLight = document.documentElement.getAttribute('data-theme') === 'light';
        ctx.fillStyle = isLight ? 'rgba(79, 70, 229, 0.35)' : 'rgba(168, 85, 247, 0.4)';
        ctx.strokeStyle = isLight ? 'rgba(79, 70, 229, 0.08)' : 'rgba(99, 102, 241, 0.12)';

        for (let i = 0; i < particles.length; i++) {
            p = particles[i];
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0 || p.x > width) p.vx *= -1;
            if (p.y < 0 || p.y > height) p.vy *= -1;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fill();

            for (let j = i + 1; j < particles.length; j++) {
                p2 = particles[j];
                const dx = p.x - p2.x;
                const dy = p.y - p2.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < 130) {
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animate);
    }
    animate();
}

// Custom Cursor Tracker
function initCustomCursor() {
    const cursor = document.querySelector('.custom-cursor');
    const cursorDot = document.querySelector('.custom-cursor-dot');
    if (!cursor || !cursorDot) return;

    window.addEventListener('mousemove', (e) => {
        cursor.style.left = `${e.clientX}px`;
        cursor.style.top = `${e.clientY}px`;
        cursorDot.style.left = `${e.clientX}px`;
        cursorDot.style.top = `${e.clientY}px`;
    });
}

// Back to top button
function initBackToTop() {
    const btn = document.getElementById('back-to-top');
    if (!btn) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 400) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// Count-Up Scroll Animation
function initCountUp() {
    const counters = document.querySelectorAll('.counter-value');
    if (counters.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const finalVal = parseInt(target.getAttribute('data-target') || '0', 10);
                let startVal = 0;
                const duration = 1500;
                const startTime = performance.now();

                function updateCount(currentTime) {
                    const elapsed = currentTime - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    const currentVal = Math.floor(progress * finalVal);
                    target.textContent = currentVal + (target.getAttribute('data-suffix') || '');

                    if (progress < 1) {
                        requestAnimationFrame(updateCount);
                    } else {
                        target.textContent = finalVal + (target.getAttribute('data-suffix') || '');
                    }
                }
                requestAnimationFrame(updateCount);
                observer.unobserve(target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

// Contact Form AJAX Handler — Full UX with validation, loading state & feedback
function initContactForm() {
    const form = document.getElementById('contact-form');
    if (!form) return;

    const alertBox = document.getElementById('contact-alert');
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnHTML = submitBtn ? submitBtn.innerHTML : 'Send Message';

    // Real-time validation on blur
    form.querySelectorAll('input, textarea').forEach(field => {
        field.addEventListener('blur', () => validateField(field));
        field.addEventListener('input', () => {
            if (field.classList.contains('is-invalid')) validateField(field);
        });
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Validate all fields before submitting
        let isValid = true;
        form.querySelectorAll('input[required], textarea[required]').forEach(field => {
            if (!validateField(field)) isValid = false;
        });
        if (!isValid) {
            showAlert('error', '⚠️ Please fill in all required fields correctly.');
            return;
        }

        // Show loading state
        setLoading(true);
        hideAlert();

        const formData = new FormData(form);
        formData.append('is_ajax', 'true');

        const csrfTokenEl = form.querySelector('[name=csrfmiddlewaretoken]');
        const csrfToken = csrfTokenEl ? csrfTokenEl.value : '';

        const headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json'
        };
        if (csrfToken) {
            headers['X-CSRFToken'] = csrfToken;
        }

        try {
            const res = await fetch('/contact/?ajax=1', {
                method: 'POST',
                body: formData,
                headers: headers
            });

            let data;
            try {
                data = await res.json();
            } catch (jsonErr) {
                if (res.ok) {
                    data = { status: 'success', message: 'Thank you! Your message has been sent successfully.' };
                } else {
                    data = { status: 'error', message: `Server error (Status ${res.status}). Please try again.` };
                }
            }

            if (data.status === 'success') {
                showAlert('success', '✅ ' + (data.message || 'Thank you! Your message has been sent successfully.'));
                form.reset();
                clearAllValidation();
            } else {
                if (data.errors) {
                    Object.entries(data.errors).forEach(([field, errs]) => {
                        const input = form.querySelector(`[name="${field}"]`);
                        if (input) markInvalid(input, Array.isArray(errs) ? errs[0] : errs);
                    });
                }
                showAlert('error', '❌ ' + (data.message || 'Something went wrong. Please try again.'));
            }
        } catch (err) {
            console.error('Contact form JS error:', err);
            showAlert('error', '⚠️ Network error. Please try again or email pundvyankateshwar@gmail.com directly.');
        } finally {
            setLoading(false);
        }
    });

    // --- Helpers ---

    function validateField(field) {
        const value = field.value.trim();
        if (!value) {
            markInvalid(field, `${getFieldLabel(field)} is required.`);
            return false;
        }
        if (field.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
            markInvalid(field, 'Please enter a valid email address.');
            return false;
        }
        markValid(field);
        return true;
    }

    function getFieldLabel(field) {
        const label = form.querySelector(`label[for="${field.id}"]`);
        if (label) return label.textContent.replace('*', '').trim();
        const name = field.getAttribute('name') || '';
        return name.charAt(0).toUpperCase() + name.slice(1);
    }

    function markInvalid(field, message) {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
        let feedback = field.nextElementSibling;
        if (!feedback || !feedback.classList.contains('invalid-feedback')) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            field.parentNode.insertBefore(feedback, field.nextSibling);
        }
        feedback.textContent = message;
    }

    function markValid(field) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        const feedback = field.nextElementSibling;
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.textContent = '';
        }
    }

    function clearAllValidation() {
        form.querySelectorAll('.is-valid, .is-invalid').forEach(el => {
            el.classList.remove('is-valid', 'is-invalid');
        });
        form.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
    }

    function setLoading(loading) {
        if (!submitBtn) return;
        submitBtn.disabled = loading;
        submitBtn.innerHTML = loading
            ? '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Sending...'
            : originalBtnHTML;
    }

    function showAlert(type, message) {
        if (!alertBox) return;
        alertBox.className = `alert alert-${type === 'success' ? 'success' : 'danger'} mb-4`;
        alertBox.textContent = message;
        alertBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function hideAlert() {
        if (!alertBox) return;
        alertBox.className = 'd-none mb-4';
        alertBox.textContent = '';
    }
}

// Project Like AJAX Handler
function initProjectLike() {
    document.querySelectorAll('.btn-like-project').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const projectId = this.getAttribute('data-project-id');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : '';

            fetch(`/projects/${projectId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    const countSpan = this.querySelector('.likes-count');
                    if (countSpan) countSpan.textContent = data.likes_count;
                    this.classList.add('text-danger');
                }
            });
        });
    });
}
