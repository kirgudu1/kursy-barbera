/* blog-quiz.js
 * Квиз «Подходит ли вам профессия барбера?» для блог-страниц.
 * Автоматически встраивается перед сайдбаром (<aside>).
 * Партнёрские ссылки — span[data-nav] (невидимы для поисковиков).
 */
(() => {
  'use strict';

  // Только для блоговых страниц
  if (!document.querySelector('[data-blog-root]')) return;

  // Не вставлять дважды
  if (document.getElementById('blog-quiz')) return;

  // ===== НАСТРОЙКИ =====
  const AFF_URL = 'https://go.2038.pro/3b6bc242f51d5261?erid=LdtCKaoMZ&m=2'
    + '&dl=https%3A%2F%2Fecolespb.ru%2Fbarber-school'
    + '&sub1=https%3A%2F%2Fecolespb.ru%2Fbarber-school'
    + '&sub2=kursy-barbera.vercel.app'
    + '&sub3=blog-quiz';

  // ===== ВОПРОСЫ =====
  const STEPS = [
    {
      key: 'attract',
      title: 'Что вас привлекает в барберинге?',
      opts: [
        { v: 'hands',    label: '✋ Работа руками и результат сразу' },
        { v: 'people',   label: '🗣️ Общение с людьми' },
        { v: 'freedom',  label: '🕐 Свобода графика, работа на себя' },
        { v: 'income',   label: '💰 Модная профессия с хорошим доходом' }
      ]
    },
    {
      key: 'social',
      title: 'Как вы относитесь к общению с незнакомыми людьми?',
      opts: [
        { v: 'easy',     label: '😊 Легко нахожу общий язык' },
        { v: 'neutral',  label: '😐 Нормально, но предпочитаю работать молча' },
        { v: 'hard',     label: '😟 Скорее некомфортно' }
      ]
    },
    {
      key: 'experience',
      title: 'Какой у вас опыт?',
      opts: [
        { v: 'friends',  label: '✂️ Стригу друзей / себя' },
        { v: 'trained',  label: '🎓 Учился на парикмахера' },
        { v: 'zero',     label: '🌱 Полный ноль, но интересно' },
        { v: 'working',  label: '💼 Уже работаю, хочу прокачаться' }
      ]
    },
    {
      key: 'time',
      title: 'Готовы ли вы учиться 2–4 недели?',
      opts: [
        { v: 'yes',      label: '👍 Да, готов вложить время' },
        { v: 'part',     label: '⚖️ Нужно совмещать с работой' },
        { v: 'fast',     label: '⚡ Хочу быструю программу' }
      ]
    },
    {
      key: 'priority',
      title: 'Что для вас важнее на старте?',
      opts: [
        { v: 'practice', label: '🎯 Практика на моделях' },
        { v: 'diploma',  label: '📜 Диплом / сертификат' },
        { v: 'job',      label: '🤝 Помощь с трудоустройством' }
      ]
    }
  ];

  const TOTAL = STEPS.length;

  // ===== РЕЗУЛЬТАТЫ =====
  const RESULTS = {
    perfect: {
      emoji: '🔥',
      title: 'У вас отличные задатки!',
      text: '87% мастеров с похожими ответами уже работают через 3 месяца после обучения. Рекомендуем начать с курса.'
    },
    good: {
      emoji: '👍',
      title: 'Профессия барбера вам подходит!',
      text: 'Ваши ответы показывают хорошую предрасположенность к профессии. Интенсивный курс — отличный способ начать.'
    },
    explore: {
      emoji: '🤔',
      title: 'Стоит попробовать!',
      text: 'Барберинг может стать для вас отличной профессией, но важно выбрать правильный формат обучения. Посмотрите программы.'
    }
  };

  function getResult(answers) {
    let score = 0;
    if (['hands','people','freedom'].includes(answers.attract)) score += 2;
    if (answers.attract === 'income') score += 1;
    if (answers.social === 'easy') score += 2;
    if (answers.social === 'neutral') score += 1;
    if (['friends','trained','working'].includes(answers.experience)) score += 2;
    if (answers.experience === 'zero') score += 1;
    if (['yes','part'].includes(answers.time)) score += 1;
    if (answers.priority === 'practice') score += 1;
    if (score >= 7) return RESULTS.perfect;
    if (score >= 4) return RESULTS.good;
    return RESULTS.explore;
  }

  // ===== CSS =====
  const CSS = `
#blog-quiz{
  --bq-bg:#fbf7f2;--bq-card:#fff;--bq-text:#2b2b2b;--bq-muted:#6f6f6f;
  --bq-accent:#c97e45;--bq-accent2:#b56e3b;--bq-shadow:0 10px 30px rgba(32,22,7,.08);
  margin:32px 0 24px;
}
#blog-quiz *{box-sizing:border-box}
#blog-quiz .bq-box{
  color:var(--bq-text);font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
  background:var(--bq-card);border-radius:18px;box-shadow:var(--bq-shadow);
  padding:clamp(16px,2.2vw,22px);
}
#blog-quiz .bq-head{display:flex;align-items:center;justify-content:space-between;gap:14px;margin-bottom:12px}
#blog-quiz .bq-head-left{display:flex;align-items:center;gap:14px}
#blog-quiz .bq-badge{width:46px;height:46px;border:2px dashed #efdcc9;border-radius:14px;display:grid;place-items:center;font-size:22px;background:#fff;flex-shrink:0}
#blog-quiz .bq-title{margin:0;font-size:clamp(17px,2.2vw,24px);font-weight:800;line-height:1.25}
#blog-quiz .bq-subtitle{margin:4px 0 0;color:var(--bq-muted);font-size:.92rem}
#blog-quiz .bq-steps{color:var(--bq-muted);white-space:nowrap;font-weight:600}
#blog-quiz .bq-progress{height:8px;background:#f0e6db;border-radius:999px;overflow:hidden;margin:6px 0 16px}
#blog-quiz .bq-progress__bar{height:100%;width:0;background:linear-gradient(90deg,var(--bq-accent),#e2aa78);transition:width .35s ease;border-radius:999px}
#blog-quiz .bq-question{font-size:clamp(16px,1.9vw,20px);line-height:1.45;margin:0 0 12px;font-weight:600}
#blog-quiz .bq-fields{display:grid;gap:8px}
#blog-quiz .bq-opt{
  display:flex;align-items:center;gap:12px;padding:12px 14px;
  border:1px solid #efe3d6;border-radius:12px;background:#fbf7f2;
  cursor:pointer;transition:all .15s ease;font-size:.97rem;
}
#blog-quiz .bq-opt:hover{background:#fff;box-shadow:var(--bq-shadow);transform:translateY(-1px)}
#blog-quiz .bq-opt input{accent-color:var(--bq-accent);width:18px;height:18px;flex-shrink:0;cursor:pointer}
#blog-quiz .bq-opt.selected{background:#fff;border-color:var(--bq-accent);box-shadow:0 0 0 1px var(--bq-accent)}
#blog-quiz .bq-actions{display:flex;gap:12px;justify-content:center;margin-top:14px;flex-wrap:wrap}
#blog-quiz .bq-btn{border:0;border-radius:14px;padding:12px 18px;font-weight:700;cursor:pointer;transition:.2s;font-size:.95rem}
#blog-quiz .bq-btn:disabled{opacity:.45;cursor:not-allowed}
#blog-quiz .bq-btn--accent{background:var(--bq-accent);color:#fff}
#blog-quiz .bq-btn--accent:hover:not(:disabled){background:var(--bq-accent2)}
#blog-quiz .bq-btn--ghost{background:transparent;border:1px dashed #e0cdb9;color:#6a594a}
#blog-quiz .bq-btn--next{background:#d9cbbc;color:#4d3b2c}
#blog-quiz .bq-btn--next:hover:not(:disabled){background:#c9b9a8}
#blog-quiz .bq-result{margin-top:8px;background:#fff;border-radius:14px;padding:20px;border:1px dashed #efdcc9;text-align:center}
#blog-quiz .bq-result-emoji{font-size:42px;margin-bottom:8px}
#blog-quiz .bq-result-title{margin:0 0 6px;font-size:clamp(18px,2.2vw,24px);font-weight:800}
#blog-quiz .bq-result-text{margin:0 0 16px;color:var(--bq-muted);line-height:1.5}
#blog-quiz .bq-result-cta{
  display:inline-block;background:var(--bq-accent);color:#fff;font-weight:700;
  padding:14px 28px;border-radius:12px;cursor:pointer;font-size:1.05rem;
  transition:all .2s;user-select:none;border:none;
}
#blog-quiz .bq-result-cta:hover{background:var(--bq-accent2);transform:translateY(-1px)}
#blog-quiz .bq-result-actions{display:flex;justify-content:center;margin-top:12px}
@media(max-width:600px){
  #blog-quiz .bq-head{flex-direction:column;align-items:flex-start;gap:8px}
  #blog-quiz .bq-steps{align-self:flex-end}
}
`;

  // ===== HTML =====
  const HTML = `
<div class="bq-box" role="application" aria-label="Квиз — подходит ли вам профессия барбера">
  <header class="bq-head">
    <div class="bq-head-left">
      <div class="bq-badge" aria-hidden="true">💈</div>
      <div>
        <h3 class="bq-title">Подходит ли вам профессия барбера?</h3>
        <p class="bq-subtitle">Ответьте на 5 вопросов — узнайте свои шансы в профессии</p>
      </div>
    </div>
    <div class="bq-steps"><span class="bq-step">0</span>/<span class="bq-total">${TOTAL}</span></div>
  </header>
  <div class="bq-progress" aria-hidden="true"><div class="bq-progress__bar"></div></div>
  <div class="bq-card">
    <div class="bq-question">Нажмите «Начать», чтобы пройти быстрый тест.</div>
    <div class="bq-fields"></div>
    <div class="bq-actions">
      <button class="bq-btn bq-btn--accent bq-start">Начать тест</button>
      <button class="bq-btn bq-btn--ghost bq-prev" disabled>Назад</button>
      <button class="bq-btn bq-btn--next bq-next" disabled>Далее</button>
    </div>
  </div>
  <div class="bq-result" hidden>
    <div class="bq-result-emoji"></div>
    <h3 class="bq-result-title"></h3>
    <p class="bq-result-text"></p>
    <span class="bq-result-cta js-nav" data-nav="${AFF_URL}">Проверить цены на курсы →</span>
    <div class="bq-result-actions">
      <button class="bq-btn bq-btn--ghost bq-restart">Пройти ещё раз</button>
    </div>
  </div>
</div>
`;

  // ===== INJECT =====
  const style = document.createElement('style');
  style.textContent = CSS;
  document.head.appendChild(style);

  const container = document.createElement('div');
  container.id = 'blog-quiz';
  container.innerHTML = HTML;

  // Вставляем после 2-го блока контента (~3-4 абзаца от начала)
  const content = document.querySelector('[data-blog-root] #article-body');
  if (!content) return;

  // Ищем комментарии <!-- end blok --> в DOM
  const walker = document.createTreeWalker(content, NodeFilter.SHOW_COMMENT);
  const endBloks = [];
  while (walker.nextNode()) {
    if (walker.currentNode.textContent.trim() === 'end blok') {
      endBloks.push(walker.currentNode);
    }
  }

  // Вставляем после 2-го end blok (или в конец, если блоков мало)
  const insertAfter = endBloks.length >= 2 ? endBloks[1] : null;
  if (insertAfter && insertAfter.nextSibling) {
    content.insertBefore(container, insertAfter.nextSibling);
  } else if (insertAfter) {
    content.appendChild(container);
  } else {
    content.appendChild(container);
  }

  // ===== ЛОГИКА =====
  const root = container;
  const stepCur  = root.querySelector('.bq-step');
  const progress = root.querySelector('.bq-progress__bar');
  const qEl      = root.querySelector('.bq-question');
  const fields   = root.querySelector('.bq-fields');
  const startBtn = root.querySelector('.bq-start');
  const prevBtn  = root.querySelector('.bq-prev');
  const nextBtn  = root.querySelector('.bq-next');
  const resultEl = root.querySelector('.bq-result');
  const restartBtn = root.querySelector('.bq-restart');

  let idx = -1;
  const answers = {};

  function render(i) {
    const s = STEPS[i];
    if (!s) return;
    stepCur.textContent = i + 1;
    progress.style.width = (i / TOTAL * 100) + '%';
    qEl.textContent = s.title;

    fields.innerHTML = '';
    s.opts.forEach((opt, k) => {
      const label = document.createElement('label');
      label.className = 'bq-opt';
      const input = document.createElement('input');
      input.type = 'radio';
      input.name = s.key;
      input.value = opt.v;
      if (answers[s.key] === opt.v) input.checked = true;

      input.addEventListener('change', () => {
        // Visual selection
        fields.querySelectorAll('.bq-opt').forEach(o => o.classList.remove('selected'));
        label.classList.add('selected');
        nextBtn.disabled = false;
      });

      const span = document.createElement('span');
      span.textContent = opt.label;
      label.appendChild(input);
      label.appendChild(span);
      fields.appendChild(label);

      if (input.checked) label.classList.add('selected');
    });

    startBtn.style.display = 'none';
    prevBtn.style.display = '';
    nextBtn.style.display = '';
    prevBtn.disabled = (i === 0);
    nextBtn.disabled = !answers[s.key];
  }

  function save() {
    const s = STEPS[idx];
    if (!s) return false;
    const checked = fields.querySelector('input[type="radio"]:checked');
    if (!checked) return false;
    answers[s.key] = checked.value;
    return true;
  }

  function finish() {
    progress.style.width = '100%';
    root.querySelector('.bq-card').hidden = true;
    resultEl.hidden = false;

    const r = getResult(answers);
    resultEl.querySelector('.bq-result-emoji').textContent = r.emoji;
    resultEl.querySelector('.bq-result-title').textContent = r.title;
    resultEl.querySelector('.bq-result-text').textContent = r.text;

    // Scroll to result
    resultEl.scrollIntoView({ behavior: 'smooth', block: 'center' });

    // Metrika goal
    try { if (typeof ym === 'function') ym(104699306, 'reachGoal', 'blog_quiz_finish', answers); } catch(e){}
  }

  function reset() {
    idx = -1;
    Object.keys(answers).forEach(k => delete answers[k]);
    root.querySelector('.bq-card').hidden = false;
    resultEl.hidden = true;
    qEl.textContent = 'Нажмите «Начать», чтобы пройти быстрый тест.';
    fields.innerHTML = '';
    startBtn.style.display = '';
    prevBtn.style.display = 'none';
    nextBtn.style.display = 'none';
    stepCur.textContent = '0';
    progress.style.width = '0';
  }

  // Events
  startBtn.addEventListener('click', () => {
    idx = 0;
    render(0);
    try { if (typeof ym === 'function') ym(104699306, 'reachGoal', 'blog_quiz_start'); } catch(e){}
  });

  nextBtn.addEventListener('click', () => {
    if (!save()) return;
    idx++;
    if (idx >= TOTAL) {
      finish();
    } else {
      render(idx);
    }
  });

  prevBtn.addEventListener('click', () => {
    if (idx > 0) {
      idx--;
      render(idx);
    }
  });

  restartBtn.addEventListener('click', reset);

  // Init
  prevBtn.style.display = 'none';
  nextBtn.style.display = 'none';

})();
