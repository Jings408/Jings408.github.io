(() => {
  const root = document.documentElement;

  // Theme
  const stored = localStorage.getItem('sl-theme');
  const preferred = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  root.dataset.theme = stored || preferred;
  const themeBtn = document.getElementById('theme-toggle');
  const syncThemeIcon = () => {
    if (themeBtn) themeBtn.textContent = root.dataset.theme === 'dark' ? '☀' : '◐';
  };
  syncThemeIcon();
  themeBtn?.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('sl-theme', root.dataset.theme);
    syncThemeIcon();
  });

  // Mobile sidebar
  const sidebar = document.getElementById('sidebar');
  const menuBtn = document.getElementById('menu-toggle');
  menuBtn?.addEventListener('click', () => sidebar?.classList.toggle('open'));
  sidebar?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => sidebar.classList.remove('open')));

  // Copy buttons
  document.querySelectorAll('.code').forEach(block => {
    const btn = document.createElement('button');
    btn.className = 'copy';
    btn.type = 'button';
    btn.textContent = '复制';
    btn.addEventListener('click', async () => {
      const pre = block.querySelector('pre');
      if (!pre) return;
      try {
        await navigator.clipboard.writeText(pre.innerText);
        btn.textContent = '已复制';
      } catch {
        btn.textContent = '复制失败';
      }
      setTimeout(() => { btn.textContent = '复制'; }, 1400);
    });
    block.appendChild(btn);
  });

  // Open details when navigating to a recipe anchor
  const openHash = () => {
    const id = location.hash.slice(1);
    if (!id) return;
    const target = document.getElementById(id);
    if (target && target.tagName === 'DETAILS') target.open = true;
  };
  window.addEventListener('hashchange', openHash);
  openHash();

  // Progress bar
  const progress = document.getElementById('progress');
  const onScroll = () => {
    const h = document.documentElement;
    const max = h.scrollHeight - h.clientHeight;
    const pct = max > 0 ? (h.scrollTop / max) * 100 : 0;
    if (progress) progress.style.width = pct + '%';
  };
  document.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Active sidebar link
  const links = [...document.querySelectorAll('.sidebar a[href^="#"]')];
  const map = new Map(links.map(a => [a.getAttribute('href').slice(1), a]));
  const sections = [...document.querySelectorAll('main section[id], main details[id], main h3[id]')];
  if ('IntersectionObserver' in window && sections.length) {
    const obs = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        links.forEach(a => a.classList.remove('active'));
        const a = map.get(entry.target.id);
        if (a) {
          a.classList.add('active');
          a.scrollIntoView({ block: 'nearest' });
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px', threshold: [0, 0.1] });
    sections.forEach(s => obs.observe(s));
  }
})();
