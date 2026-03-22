"""
inject_cta_safe.py — Безопасная вставка CTA-блоков в блог-статьи.
ТОЛЬКО ВСТАВЛЯЕТ, НИЧЕГО НЕ УДАЛЯЕТ.

Вставляет:
- CTA mid: после ~50% комментариев <!-- end blok --> (середина статьи)
- CTA end: перед закрывающим </div> блока article-body (конец статьи)
"""
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(SCRIPT_DIR, 'blog')

CTA_MID = """<!-- CTA: проверьте цены (mid-article) -->
<div class="blog-cta" style="margin:28px 0; padding:18px 22px; background:linear-gradient(135deg, #fff8ee, #fff4e0); border:1px solid #f0d9b5; border-left:4px solid #c98e5b; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
  <p style="margin:0 0 10px; font-weight:600; font-size:1.05rem; color:#333;">💈 Проверьте цены на курсы барбера в вашем городе</p>
  <p style="margin:0 0 12px; color:#555; font-size:.95rem;">Мы собрали курсы в 50+ городах — сравните программы, стоимость и отзывы выпускников.</p>
  <span class="js-nav" data-nav="https://go.2038.pro/3b6bc242f51d5261?erid=LdtCKaoMZ&m=2&dl=https%3A%2F%2Fecolespb.ru%2Fbarber-school&sub1=https%3A%2F%2Fecolespb.ru%2Fbarber-school&sub2=kursy-barbera.vercel.app&sub3=blog-cta-mid" style="display:inline-block; background:#c98e5b; color:#fff; font-weight:600; padding:10px 20px; border-radius:8px; cursor:pointer; transition:background .2s; user-select:none;">Посмотреть цены →</span>
</div>
<!-- /CTA -->"""

CTA_END = """<!-- CTA: проверьте цены (end-article) -->
<div class="blog-cta" style="margin:32px 0 16px; padding:22px 24px; background:linear-gradient(135deg, #fff8ee, #fff4e0); border:1px solid #f0d9b5; border-left:4px solid #c98e5b; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
  <p style="margin:0 0 8px; font-weight:700; font-size:1.1rem; color:#333;">✂️ Готовы начать карьеру барбера?</p>
  <p style="margin:0 0 14px; color:#555; font-size:.95rem;">Проверьте цены на курсы барбера в вашем городе — школы в 50+ городах России, практика на моделях, диплом.</p>
  <span class="js-nav" data-nav="https://go.2038.pro/3b6bc242f51d5261?erid=LdtCKaoMZ&m=2&dl=https%3A%2F%2Fecolespb.ru%2Fbarber-school&sub1=https%3A%2F%2Fecolespb.ru%2Fbarber-school&sub2=kursy-barbera.vercel.app&sub3=blog-cta-end" style="display:inline-block; background:#c98e5b; color:#fff; font-weight:600; padding:12px 24px; border-radius:8px; cursor:pointer; font-size:1.05rem; transition:background .2s; user-select:none;">Проверить цены в моём городе →</span>
</div>
<!-- /CTA -->"""

SKIP = {
    'index.html', 'blog-category.html', 'privacy.html',
    'yandex_c82d19addf857c5c.html',
}


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'data-blog-root' not in content:
        return 'SKIP (no data-blog-root)'
    
    if 'blog-cta-mid' in content:
        return 'SKIP (already has CTAs)'
    
    # Находим все позиции <!-- end blok --> ВНУТРИ article-body
    # article-body начинается с id="article-body"
    ab_start = content.find('id="article-body"')
    if ab_start == -1:
        return 'SKIP (no article-body)'
    
    # Считаем end blok маркеры после article-body
    positions = []
    pos = ab_start
    while True:
        idx = content.find('<!-- end blok -->', pos)
        if idx == -1:
            break
        positions.append(idx)
        pos = idx + 17  # len('<!-- end blok -->')
    
    if len(positions) < 3:
        return 'SKIP (too few blocks)'
    
    # CTA mid: после маркера на ~40-50% (чтобы было ближе к середине)
    mid_idx = len(positions) // 2
    mid_pos = positions[mid_idx] + 17  # после <!-- end blok -->
    
    # CTA end: перед последним <!-- end blok --> (он закрывает весь article)
    # Но на самом деле вставляем перед </div> (Сайдбар) — т.е. перед закрытием article-body
    # Найдём позицию сайдбара
    sidebar_pos = content.find('<!-- Сайдбар -->', ab_start)
    if sidebar_pos == -1:
        # Попробуем найти закрывающий </div> после последнего end blok
        end_pos = positions[-1] + 17
    else:
        # Вставляем перед <!-- Сайдбар -->
        # Но нужно до закрытия <div id="article-body">
        # Ищем </div> перед сайдбаром
        end_pos = content.rfind('\n', ab_start, sidebar_pos)
        if end_pos == -1:
            end_pos = sidebar_pos
    
    # Вставляем в обратном порядке (сначала end, потом mid), чтобы позиции не сдвигались
    # CTA end: перед сайдбаром (перед закрытием контентной зоны)
    if sidebar_pos != -1:
        # Вставляем CTA end перед </div>\n<!-- Сайдбар -->
        close_div_before_sidebar = content.rfind('</div>', ab_start, sidebar_pos)
        if close_div_before_sidebar != -1:
            content = content[:close_div_before_sidebar] + '\n' + CTA_END + '\n' + content[close_div_before_sidebar:]
        else:
            content = content[:sidebar_pos] + CTA_END + '\n' + content[sidebar_pos:]
    
    # CTA mid: после середины контента (позиция уже верна, т.к. вставка end была ПОСЛЕ mid_pos)
    # Но если end_pos < mid_pos, нужен пересчёт. Проще: mid_pos всегда < sidebar, значит ОК.
    content_new = content[:mid_pos] + '\n' + CTA_MID + '\n' + content[mid_pos:]
    
    # Финальная проверка: файл не стал короче
    orig_len = len(open(filepath, 'r', encoding='utf-8').read())
    if len(content_new) < orig_len:
        return 'ERROR (file got shorter!)'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content_new)
    
    return 'OK'


def main():
    stats = {}
    processed = set()
    
    for d in [BLOG_DIR, SCRIPT_DIR]:
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith('.html') or '.php.html' in fn or fn in SKIP:
                continue
            fp = os.path.join(d, fn)
            if fp in processed:
                continue
            processed.add(fp)
            
            result = process_file(fp)
            stats[result] = stats.get(result, 0) + 1
            label = '✅' if result == 'OK' else '⏭️'
            print(f'  {label} {os.path.relpath(fp, SCRIPT_DIR):50s} → {result}')
    
    print(f'\n{"="*60}')
    for k, v in sorted(stats.items()):
        print(f'  {k}: {v}')
    print(f'  ВСЕГО: {sum(stats.values())}')

if __name__ == '__main__':
    main()
