(() => {
  const toast = document.querySelector('.toast');
  let toastTimer;
  function showToast(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('show'), 2800);
  }

  const menuToggle = document.querySelector('.menu-toggle');
  const menu = document.querySelector('.main-nav');
  if (menuToggle && menu) {
    menuToggle.addEventListener('click', () => {
      const isOpen = menu.classList.toggle('open');
      menuToggle.setAttribute('aria-expanded', String(isOpen));
    });
    menu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
      menu.classList.remove('open');
      menuToggle.setAttribute('aria-expanded', 'false');
    }));
  }

  document.querySelectorAll('.save-match, .save-result').forEach(button => button.addEventListener('click', () => {
    const saved = button.getAttribute('aria-pressed') !== 'true';
    button.setAttribute('aria-pressed', String(saved));
    if (button.classList.contains('save-result')) button.textContent = saved ? '♥ Saved' : '♡ Save';
    else button.textContent = saved ? '♥' : '♡';
    button.setAttribute('aria-label', saved ? 'Remove from shortlist' : 'Save to shortlist');
    showToast(saved ? 'Saved to your shortlist.' : 'Removed from your shortlist.');
  }));

  document.querySelectorAll('.intro-button').forEach(button => button.addEventListener('click', () => {
    showToast('Introduction requests are a prototype interaction. No message was sent.');
  }));

  document.querySelectorAll('.filter-chip[data-filter]').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('.filter-chip[data-filter]').forEach(chip => chip.classList.remove('selected'));
    button.classList.add('selected');
    document.querySelectorAll('.filter-chip[data-filter]').forEach(chip => chip.setAttribute('aria-pressed', String(chip === button)));
    const filter = button.dataset.filter;
    let visibleCount = 0;
    document.querySelectorAll('.result-list .result-card').forEach(card => {
      const sectorMatch = /climate|energy/i.test(card.dataset.sector || '');
      const stageMatch = /seed/i.test(card.dataset.stage || '');
      const chequeMin = Number(card.dataset.chequeMin || 0);
      const chequeMax = Number(card.dataset.chequeMax || Infinity);
      const chequeMatch = chequeMin <= 200 && chequeMax >= 50;
      const visible = filter === 'all' || (filter === 'climate' && sectorMatch) || (filter === 'seed' && stageMatch) || (filter === 'cheque' && chequeMatch);
      card.hidden = !visible;
      if (visible) visibleCount += 1;
    });
    const count = document.querySelector('.filter-count');
    if (count) count.textContent = `${visibleCount} ${visibleCount === 1 ? 'profile' : 'profiles'} shown`;
  }));

  const stepSections = [...document.querySelectorAll('.onboarding-step')];
  if (stepSections.length) {
    let currentStep = 1;
    const progress = document.querySelector('.progress-track span');
    const progressCopy = document.querySelector('.progress-copy');
    const paintStep = () => {
      stepSections.forEach(section => section.classList.toggle('active', Number(section.dataset.step) === currentStep));
      if (progress) progress.style.width = `${currentStep * 25}%`;
      if (progressCopy) progressCopy.textContent = `Step ${currentStep} of 4`;
      if (currentStep === 4) {
        const value = selector => document.querySelector(selector)?.value.trim() || 'Not provided';
        const review = {
          company: value('#company'),
          'sector-stage': `${value('#sector')} · ${value('#stage')}`,
          raise: value('#raise'),
          region: value('#region'),
          description: value('#description'),
        };
        Object.entries(review).forEach(([key, text]) => {
          const field = document.querySelector(`[data-review="${key}"]`);
          if (field) field.value = text;
        });
      }
    };
    document.querySelectorAll('.step-next').forEach(button => button.addEventListener('click', () => {
      const activeInputs = [...document.querySelectorAll(`.onboarding-step[data-step="${currentStep}"] input:not([readonly]), .onboarding-step[data-step="${currentStep}"] select, .onboarding-step[data-step="${currentStep}"] textarea`)].filter(input => input.required);
      const invalid = activeInputs.find(input => !input.checkValidity());
      if (invalid) { invalid.reportValidity(); return; }
      if (currentStep < 4) { currentStep += 1; paintStep(); }
    }));
    document.querySelectorAll('.step-back').forEach(button => button.addEventListener('click', () => {
      if (currentStep > 1) { currentStep -= 1; paintStep(); }
    }));
    document.querySelectorAll('.choice-button').forEach(button => button.addEventListener('click', () => button.classList.toggle('selected')));
    const finish = document.querySelector('.finish-setup');
    if (finish) finish.addEventListener('click', () => { window.location.href = 'workspace.html'; });
  }
})();
