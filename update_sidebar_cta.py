"""
update_sidebar_cta.py — Обновляет блок «Подбор курсов» в сайдбаре блог-статей:
1. Заменяет <a href="..//#cities"> на <span data-nav="..."> с партнёрской ссылкой
2. Добавляет margin-bottom к карточке
"""

import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(SCRIPT_DIR, 'blog')

AFF_URL = ('https://go.2038.pro/3b6bc242f51d5261?erid=LdtCKaoMZ&m=2'
           '&dl=https%3A%2F%2Fecolespb.ru%2Fbarber-school'
           '&sub1=https%3A%2F%2Fecolespb.ru%2Fbarber-school'
           '&sub2=kursy-barbera.vercel.app'
           '&sub3=sidebar-cta')

# Старая ссылка (может быть ..//#cities или ../#cities или /#cities)
OLD_LINK_RE = re.compile(
    r'<a\s+class="btn btn-primary"\s+href="[^"]*#cities">\s*Выберите ваш город\s*</a>',
    re.IGNORECASE
)

NEW_LINK = (
    f'<span class="btn btn-primary js-nav" data-nav="{AFF_URL}" '
    f'style="cursor:pointer; user-select:none;">Посмотреть цены</span>'
)

SKIP_FILES = {
    'index.html', 'blog-category.html', 'privacy.html',
    'yandex_c82d19addf857c5c.html',
}

def is_blog_article(content):
    return 'data-blog-root' in content

def process_file(filepath):
    filename = os.path.basename(filepath)
    if filename in SKIP_FILES or '.php.html' in filename:
        return 'SKIP'

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if not is_blog_article(content):
        return 'SKIP (not blog)'

    if 'sidebar-cta' in content:
        return 'SKIP (already done)'

    if not OLD_LINK_RE.search(content):
        return 'SKIP (no old link)'

    # Заменяем ссылку
    content = OLD_LINK_RE.sub(NEW_LINK, content)

    # Добавляем margin-bottom к карточке «Подбор курсов»
    # Ищем: <!-- Подбор курсов -->\n<div class="card">
    content = content.replace(
        '<!-- Подбор курсов -->\n<div class="card">',
        '<!-- Подбор курсов -->\n<div class="card" style="margin-bottom:18px;">'
    )
    # Вариант с \r\n
    content = content.replace(
        '<!-- Подбор курсов -->\r\n<div class="card">',
        '<!-- Подбор курсов -->\r\n<div class="card" style="margin-bottom:18px;">'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return 'OK'


def main():
    stats = {}
    processed = set()

    for d in [BLOG_DIR, SCRIPT_DIR]:
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith('.html'):
                continue
            fp = os.path.join(d, fn)
            if fp in processed:
                continue
            processed.add(fp)
            result = process_file(fp)
            stats[result] = stats.get(result, 0) + 1
            label = '✅' if result == 'OK' else '⏭️'
            print(f'  {label} {os.path.relpath(fp, SCRIPT_DIR):50s} → {result}')

    print('\n' + '='*60)
    for k, v in sorted(stats.items()):
        print(f'  {k}: {v}')
    print(f'  ВСЕГО: {sum(stats.values())}')

if __name__ == '__main__':
    main()
