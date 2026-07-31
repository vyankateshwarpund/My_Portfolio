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

// Contact Form AJAX Handler
function initContactForm() {
    const form = document.getElementById('contact-form');
    if (!form) return;

    const alertBox = document.getElementById('contact-alert');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(form);

        fetch('/contact/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(res => res.json())
        .then(data => {
            if (alertBox) {
                alertBox.classList.remove('d-none', 'alert-danger', 'alert-success');
                if (data.status === 'success') {
                    alertBox.classList.add('alert', 'alert-success');
                    alertBox.textContent = data.message;
                    form.reset();
                } else {
                    alertBox.classList.add('alert', 'alert-danger');
                    alertBox.textContent = data.message || 'An error occurred. Please try again.';
                }
            }
        })
        .catch(err => {
            if (alertBox) {
                alertBox.classList.remove('d-none');
                alertBox.classList.add('alert', 'alert-danger');
                alertBox.textContent = 'Connection error. Please try again.';
            }
        });
    });
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
