// Toggle language dropdown on click
const langSelector = document.getElementById('languageSelector');
const langDropdown = document.getElementById('languageDropdown');

langSelector.addEventListener('click', e => {
    e.stopPropagation();
    langDropdown.classList.toggle('active');
});

// Close dropdown if click outside
window.addEventListener('click', () => {
    langDropdown.classList.remove('active');
});

// Change language text on selection
langDropdown.querySelectorAll('div').forEach(option => {
    option.addEventListener('click', () => {
    const selected = option.textContent;
    document.querySelector('.selected-language').textContent = selected;
    langDropdown.classList.remove('active');
    });
});

// Optional: Smooth scroll or small JS animation setup can go here later
  const cards = document.querySelectorAll('.service-card');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animation = 'fadeUp 0.8s ease forwards';
      }
    });
  }, { threshold: 0.1 });

  cards.forEach(card => observer.observe(card));

  // ✨ Fade-in on scroll
  const steps = document.querySelectorAll('.timeline-step');
  const revealSteps = () => {
    const triggerBottom = window.innerHeight * 0.85;
    steps.forEach(step => {
      const stepTop = step.getBoundingClientRect().top;
      if (stepTop < triggerBottom) step.classList.add('active');
    });
  };
  window.addEventListener('scroll', revealSteps);
  revealSteps();