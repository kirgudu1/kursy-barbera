"""
inject_quiz_script.py — Добавляет подключение blog-quiz.js во все блог-статьи.
Вставляет <script src="../js/blog-quiz.js" defer></script> перед </head>.
Пропускает файлы, где скрипт уже подключён.
"""

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(SCRIPT_DIR, 'blog')

SCRIPT_TAG_BLOG = '<script src="../js/blog-quiz.js" defer></script>'
SCRIPT_TAG_ROOT = '<script src="js/blog-quiz.js" defer></script>'
MARKER = 'blog-quiz.js'

SKIP_FILES = {
    'index.html', 'blog-category.html', 'privacy.html',
    'yandex_c82d19addf857c5c.html',
}

def is_blog_article(content):
    return 'data-blog-root' in content

def process_file(filepath, script_tag):
    filename = os.path.basename(filepath)
    if filename in SKIP_FILES:
        return 'SKIP (system)'
    if '.php.html' in filename:
        return 'SKIP (.php.html)'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not is_blog_article(content):
        return 'SKIP (not blog)'
    
    if MARKER in content:
        return 'SKIP (already has quiz)'
    
    # Вставляем перед </head>
    if '</head>' not in content:
        return 'SKIP (no </head>)'
    
    content = content.replace('</head>', script_tag + '\n</head>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return 'OK'

def main():
    stats = {}
    processed = set()
    
    # Blog dir (script path: ../js/)
    for d, tag in [(BLOG_DIR, SCRIPT_TAG_BLOG), (SCRIPT_DIR, SCRIPT_TAG_ROOT)]:
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith('.html'):
                continue
            fp = os.path.join(d, fn)
            if fp in processed:
                continue
            processed.add(fp)
            result = process_file(fp, tag)
            stats[result] = stats.get(result, 0) + 1
            label = '✅' if result == 'OK' else '⏭️'
            print(f'  {label} {os.path.relpath(fp, SCRIPT_DIR):50s} → {result}')
    
    print('\n' + '='*60)
    print('ИТОГО:')
    for k, v in sorted(stats.items()):
        print(f'  {k}: {v}')
    print(f'  ВСЕГО: {sum(stats.values())}')

if __name__ == '__main__':
    main()
