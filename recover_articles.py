"""
recover_articles.py — Восстанавливает содержимое повреждённых блог-статей
из продакшен-сайта на kursy-barbera.vercel.app.

Для каждого файла в /blog/ проверяет, есть ли маркер "section_p" (признак
нормального контента). Если нет — скачивает оригинал с Vercel.
"""
import os
import urllib.request
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(SCRIPT_DIR, 'blog')
DOMAIN = 'https://kursy-barbera.vercel.app'

SKIP = {
    'index.html', 'blog-category.html', 'privacy.html',
    'yandex_c82d19addf857c5c.html',
}

def is_damaged(filepath):
    """Файл повреждён, если нет ни одного section_p или section_block."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Проверяем наличие контентных маркеров
    return ('section_p' not in content and 'section_block' not in content 
            and '<!-- end blok -->' not in content)

def download(url):
    """Скачать страницу по URL."""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8')
    except Exception as e:
        return None

def main():
    recovered = 0
    skipped = 0
    failed = 0
    
    # Собираем список повреждённых файлов
    for fn in sorted(os.listdir(BLOG_DIR)):
        if not fn.endswith('.html') or '.php.html' in fn or fn in SKIP:
            continue
        
        fp = os.path.join(BLOG_DIR, fn)
        
        if not is_damaged(fp):
            skipped += 1
            continue
        
        # Скачиваем оригинал
        url = f'{DOMAIN}/blog/{fn}'
        print(f'  🔄 {fn} — скачиваю с {url}...')
        
        content = download(url)
        if content is None or len(content) < 1000:
            print(f'  ❌ {fn} — НЕ УДАЛОСЬ СКАЧАТЬ')
            failed += 1
            continue
        
        # Сохраняем в blog/
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Также сохраняем копию в корень
        root_fp = os.path.join(SCRIPT_DIR, fn)
        if os.path.exists(root_fp):
            with open(root_fp, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  ✅ {fn} — восстановлен (blog/ + root)')
        else:
            print(f'  ✅ {fn} — восстановлен (blog/ only)')
        
        recovered += 1
        time.sleep(0.3)  # не DDoSить Vercel
    
    print(f'\n{"="*60}')
    print(f'  Восстановлено: {recovered}')
    print(f'  Не повреждено: {skipped}')
    print(f'  Ошибки: {failed}')

if __name__ == '__main__':
    main()
