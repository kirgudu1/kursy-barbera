"""
inject_cta.py — Массовая вставка CTA-блоков в блог-статьи kursy-barbera.

Что делает:
 1. Обходит все .html файлы в /blog/ и в корне (статейные файлы)
 2. Пропускает городские, системные и уже обработанные файлы
 3. Вставляет CTA «Проверьте цены» в середину статьи (после ~50% блоков)
 4. Вставляет финальный CTA в конец статьи (перед сайдбаром)
 5. Убирает закомментированный блок «Полезные ссылки» если есть

Ссылки: <span data-nav="..."> — невидимы для поисковика.
Трекинг: sub3=blog-cta-mid | sub3=blog-cta-end
"""

import os
import re

# === НАСТРОЙКИ ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(SCRIPT_DIR, 'blog')

# Партнёрская ссылка (полная, готовая)
AFF_BASE = 'https://go.2038.pro/3b6bc242f51d5261'
ERID = 'LdtCKaoMZ'
M = '2'
DL = 'https%3A%2F%2Fecolespb.ru%2Fbarber-school'
SUB1 = 'https%3A%2F%2Fecolespb.ru%2Fbarber-school'
SUB2 = 'kursy-barbera.vercel.app'

def aff_url(sub3):
    return f'{AFF_BASE}?erid={ERID}&m={M}&dl={DL}&sub1={SUB1}&sub2={SUB2}&sub3={sub3}'

# CTA HTML-блоки
CTA_MID = f'''<!-- CTA: проверьте цены (mid-article) -->
<div class="blog-cta" style="margin:28px 0; padding:18px 22px; background:linear-gradient(135deg, #fff8ee, #fff4e0); border:1px solid #f0d9b5; border-left:4px solid #c98e5b; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
  <p style="margin:0 0 10px; font-weight:600; font-size:1.05rem; color:#333;">💈 Проверьте цены на курсы барбера в вашем городе</p>
  <p style="margin:0 0 12px; color:#555; font-size:.95rem;">Мы собрали курсы в 50+ городах — сравните программы, стоимость и отзывы выпускников.</p>
  <span class="js-nav" data-nav="{aff_url('blog-cta-mid')}" style="display:inline-block; background:#c98e5b; color:#fff; font-weight:600; padding:10px 20px; border-radius:8px; cursor:pointer; transition:background .2s; user-select:none;">Посмотреть цены →</span>
</div>
<!-- /CTA -->'''

CTA_END = f'''<!-- CTA: проверьте цены (end-article) -->
<div class="blog-cta" style="margin:32px 0 16px; padding:22px 24px; background:linear-gradient(135deg, #fff8ee, #fff4e0); border:1px solid #f0d9b5; border-left:4px solid #c98e5b; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
  <p style="margin:0 0 8px; font-weight:700; font-size:1.1rem; color:#333;">✂️ Готовы начать карьеру барбера?</p>
  <p style="margin:0 0 14px; color:#555; font-size:.95rem;">Проверьте цены на курсы барбера в вашем городе — школы в 50+ городах России, практика на моделях, диплом.</p>
  <span class="js-nav" data-nav="{aff_url('blog-cta-end')}" style="display:inline-block; background:#c98e5b; color:#fff; font-weight:600; padding:12px 24px; border-radius:8px; cursor:pointer; font-size:1.05rem; transition:background .2s; user-select:none;">Проверить цены в моём городе →</span>
</div>
<!-- /CTA -->'''

# Файлы, которые НЕ трогаем
SKIP_FILES = {
    'index.html', 'blog-category.html', 'privacy.html',
    'yandex_c82d19addf857c5c.html',
}

# Городские файлы определяем по наличию "course-card" и отсутствию "data-blog-root"
def is_blog_article(content):
    """Определяем, является ли файл блог-статьёй (а не городской страницей)."""
    return 'data-blog-root' in content

def already_has_cta(content):
    """Проверяем, есть ли уже CTA."""
    return 'blog-cta' in content

def remove_commented_links(content):
    """Убираем закомментированный блок 'Полезные ссылки'."""
    # Паттерн для блока <!-- start blok --> + закомментированный section_links
    pattern = r'<!-- start blok -->\s*\n<!-- <url>.*?</url> -->\s*\n<!-- Внутренние ссылки.*?</section>-->\s*\n'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    return content

def inject_ctas(content):
    """Вставляем два CTA в контент статьи."""
    
    # Находим все позиции <!-- end blok -->
    marker = '<!-- end blok -->'
    positions = []
    start = 0
    while True:
        idx = content.find(marker, start)
        if idx == -1:
            break
        positions.append(idx + len(marker))
        start = idx + len(marker)
    
    if len(positions) < 2:
        return content, False  # слишком мало блоков, пропускаем
    
    # Вставляем mid-CTA: после ~50% блоков (минимум после 2-го)
    mid_idx = max(1, len(positions) // 2)  # индекс блока (0-based)
    if mid_idx >= len(positions):
        mid_idx = len(positions) - 1
    
    mid_pos = positions[mid_idx]
    
    # Вставляем end-CTA: перед закрывающим </div> контента
    # Ищем последний <!-- end blok --> и вставляем после него
    end_pos = positions[-1]
    
    # Убираем закомментированные ссылки если есть
    content = remove_commented_links(content)
    
    # Пересчитываем позиции после удаления комментариев
    positions = []
    start = 0
    while True:
        idx = content.find(marker, start)
        if idx == -1:
            break
        positions.append(idx + len(marker))
        start = idx + len(marker)
    
    if len(positions) < 2:
        return content, False
    
    mid_idx = max(1, len(positions) // 2)
    if mid_idx >= len(positions):
        mid_idx = len(positions) - 1
    
    # Вставляем сначала end (чтобы не сбить позицию mid)
    end_pos = positions[-1]
    content = content[:end_pos] + '\n' + CTA_END + '\n' + content[end_pos:]
    
    # Пересчитываем mid_pos (end добавился после mid, так что mid_pos не изменился)
    mid_pos = positions[mid_idx]
    
    # Но если mid_idx == последний, то нужно вставить ДО end CTA
    if mid_idx >= len(positions) - 1:
        # mid и end совпадают — ставим mid после предпоследнего
        if len(positions) >= 2:
            mid_pos = positions[-2]
        else:
            mid_pos = positions[0]
    
    content = content[:mid_pos] + '\n' + CTA_MID + '\n' + content[mid_pos:]
    
    return content, True


def process_file(filepath):
    """Обрабатываем один файл."""
    filename = os.path.basename(filepath)
    
    # Пропуск системных файлов
    if filename in SKIP_FILES:
        return 'SKIP (system)'
    
    # Пропуск .php.html дублей
    if '.php.html' in filename:
        return 'SKIP (.php.html)'
    
    # Чтение
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Не блог-статья?
    if not is_blog_article(content):
        return 'SKIP (not blog)'
    
    # Уже есть CTA?
    if already_has_cta(content):
        return 'SKIP (already has CTA)'
    
    # Вставка
    new_content, ok = inject_ctas(content)
    if not ok:
        return 'SKIP (too few blocks)'
    
    # Запись
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return 'OK'


def main():
    stats = {'OK': 0, 'SKIP (system)': 0, 'SKIP (.php.html)': 0,
             'SKIP (not blog)': 0, 'SKIP (already has CTA)': 0, 'SKIP (too few blocks)': 0}
    
    dirs = [BLOG_DIR, SCRIPT_DIR]
    processed_files = set()
    
    for d in dirs:
        if not os.path.isdir(d):
            continue
        for filename in sorted(os.listdir(d)):
            if not filename.endswith('.html'):
                continue
            filepath = os.path.join(d, filename)
            if filepath in processed_files:
                continue
            processed_files.add(filepath)
            
            result = process_file(filepath)
            stats[result] = stats.get(result, 0) + 1
            
            label = '✅' if result == 'OK' else '⏭️'
            print(f'  {label} {os.path.relpath(filepath, SCRIPT_DIR):50s} → {result}')
    
    print('\n' + '='*60)
    print('ИТОГО:')
    for k, v in sorted(stats.items()):
        print(f'  {k}: {v}')
    print(f'  ВСЕГО файлов: {sum(stats.values())}')


if __name__ == '__main__':
    main()
