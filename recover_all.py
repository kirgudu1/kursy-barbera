"""
recover_all.py — Восстанавливаем ВСЕ блог-статьи с продакшена kursy-barbera.vercel.app.
Скачиваем и из /blog/ и из корня (дубликаты).
Затем повторно применяем safe SEO-фиксы (canonical, og:url).
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

def download(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode('utf-8')
    except Exception as e:
        print(f'    ⚠️ Ошибка: {e}')
        return None

def main():
    ok = 0
    fail = 0
    
    # 1. Восстанавливаем /blog/ файлы
    print('='*60)
    print('📂 Восстанавливаем /blog/ файлы')
    print('='*60)
    
    for fn in sorted(os.listdir(BLOG_DIR)):
        if not fn.endswith('.html') or '.php.html' in fn or fn in SKIP:
            continue
        
        url = f'{DOMAIN}/blog/{fn}'
        print(f'  🔄 blog/{fn}')
        
        content = download(url)
        if content and len(content) > 1000:
            fp = os.path.join(BLOG_DIR, fn)
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(content)
            ok += 1
        else:
            fail += 1
        
        time.sleep(0.2)
    
    # 2. Восстанавливаем дубликаты в корне  
    print('\n' + '='*60)
    print('📂 Восстанавливаем дубликаты в корне')
    print('='*60)
    
    for fn in sorted(os.listdir(SCRIPT_DIR)):
        if not fn.endswith('.html') or '.php.html' in fn or fn in SKIP:
            continue
        
        fp = os.path.join(SCRIPT_DIR, fn)
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Только блоговые статьи (с data-blog-root)
        if 'data-blog-root' not in content:
            continue
        
        url = f'{DOMAIN}/{fn}'
        print(f'  🔄 {fn}')
        
        new_content = download(url)
        if new_content and len(new_content) > 1000:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            ok += 1
        else:
            fail += 1
        
        time.sleep(0.2)
    
    print(f'\n{"="*60}')
    print(f'  ✅ Восстановлено: {ok}')
    print(f'  ❌ Ошибки: {fail}')
    print('='*60)

if __name__ == '__main__':
    main()
