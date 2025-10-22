/* /js/aff-wrap.ecolespb.js
 * Авто-обёртка всех внешних ссылок на *.ecolespb.ru → в трекинговый формат.
 * Достаточно положить файл и подключить 1 раз — дальше всё работает само (включая динамически добавленные ссылки).
 */

(function(){
  'use strict';

  // === НАСТРОЙКИ ===
  const WRAP_BASE   = 'https://go.2038.pro/3b6bc242f51d5261';
  const ERID        = 'LdtCKaoMZ';
  const M_PARAM     = '2';
  const SUB2_STATIC = 'kursy-barbera.vercel.app'; // можно заменить на location.hostname, если нужно подставлять домен автоматически

  // домены для обёртки (кастомизируй при необходимости)
  const MATCH_HOST_PART = '.ecolespb.ru';

  // атрибут-маркер, чтобы не оборачивать повторно
  const MARK_ATTR = 'data-aff-ecolespb';

  // === УТИЛИТЫ ===
  const enc = encodeURIComponent;

  function isWrapped(url){
    if (!url) return false;
    return url.startsWith(WRAP_BASE);
  }

  function needsWrap(url){
    if (!url) return false;
    try {
      const u = new URL(url, location.href);
      // только http(s)
      if (!/^https?:$/i.test(u.protocol)) return false;
      // уже наш редиректор
      if (isWrapped(u.href)) return false;
      // подходит по домену
      return u.hostname.endsWith(MATCH_HOST_PART);
    } catch(e){
      return false;
    }
  }

  function buildWrappedHref(originalHref){
    // Пример:
    // https://go.2038.pro/3b6bc242f51d5261?erid=LdtCKaoMZ&m=2&dl=ORIG&sub1=ORIG&sub2=kursy-barbera.vercel.app
    const params = [
      'erid=' + enc(ERID),
      'm='    + enc(M_PARAM),
      'dl='   + enc(originalHref),
      'sub1=' + enc(originalHref),
      'sub2=' + enc(SUB2_STATIC)
    ];
    return WRAP_BASE + '?' + params.join('&');
  }

  function wrapAnchor(a){
    if (!a || a.hasAttribute(MARK_ATTR)) return;

    const href = a.getAttribute('href');
    if (!href || !needsWrap(href)) return;

    const wrapped = buildWrappedHref(new URL(href, location.href).href);
    a.setAttribute('href', wrapped);
    a.setAttribute(MARK_ATTR, '1');

    // Рекомендуемые атрибуты для платных/партнёрских ссылок
    const rel = (a.getAttribute('rel') || '').split(/\s+/).filter(Boolean);
    ['nofollow','noopener','noreferrer','sponsored'].forEach(flag=>{
      if (!rel.includes(flag)) rel.push(flag);
    });
    a.setAttribute('rel', rel.join(' '));
  }

  function scan(root){
    const anchors = (root || document).querySelectorAll('a[href]');
    anchors.forEach(wrapAnchor);
  }

  // === ИНИЦИАЛИЗАЦИЯ ===
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ()=>scan(document));
  } else {
    scan(document);
  }

  // Обработка динамически появляющихся ссылок (SPA, AJAX, виджеты и т.п.)
  const mo = new MutationObserver(muts=>{
    muts.forEach(m=>{
      m.addedNodes && m.addedNodes.forEach(node=>{
        if (node.nodeType !== 1) return;
        if (node.tagName === 'A') {
          wrapAnchor(node);
        } else {
          scan(node);
        }
      });
    });
  });
  mo.observe(document.documentElement, { childList: true, subtree: true });

})();
