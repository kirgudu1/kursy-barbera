"""
fix_seo.py — Исправляет SEO-проблемы на kursy-barbera:
1. Двойная точка в og:url (..html → .html) на городских страницах
2. Пустой og:url на главной
3. Создание robots.txt
4. Генерация sitemap.xml
5. Добавление canonical тегов на все страницы
"""

import os
import re
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOMAIN = 'https://kursy-barbera.vercel.app'
BLOG_DIR = os.path.join(SCRIPT_DIR, 'blog')

# ================================================
# 1. ИСПРАВЛЯЕМ og:url С ДВОЙНОЙ ТОЧКОЙ
# ================================================
def fix_og_urls():
    print('='*60)
    print('1. Исправляем og:url с двойной точкой')
    print('='*60)
    fixed = 0
    for fn in sorted(os.listdir(SCRIPT_DIR)):
        if not fn.endswith('.html'):
            continue
        fp = os.path.join(SCRIPT_DIR, fn)
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ищем ..html в og:url
        new_content = re.sub(
            r'(og:url"\s+content="[^"]*?)\.\.html',
            r'\1.html',
            content
        )
        
        if new_content != content:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed += 1
            print(f'  ✅ {fn}')
    
    print(f'  Исправлено: {fixed} файлов\n')
    return fixed


# ================================================
# 2. ИСПРАВЛЯЕМ ПУСТОЙ og:url НА ГЛАВНОЙ
# ================================================
def fix_index_og():
    print('='*60)
    print('2. Исправляем пустой og:url на главной')
    print('='*60)
    fp = os.path.join(SCRIPT_DIR, 'index.html')
    if not os.path.exists(fp):
        print('  ⏭️ index.html не найден\n')
        return
    
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace(
        'og:url" content=""',
        f'og:url" content="{DOMAIN}/"'
    )
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  ✅ index.html → og:url="{DOMAIN}/"\n')


# ================================================
# 3. СОЗДАЁМ robots.txt
# ================================================
def create_robots():
    print('='*60)
    print('3. Создаём robots.txt')
    print('='*60)
    fp = os.path.join(SCRIPT_DIR, 'robots.txt')
    robots = f"""User-agent: *
Allow: /
Disallow: /js/
Disallow: /IMUGA/

Sitemap: {DOMAIN}/sitemap.xml
"""
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(robots)
    print(f'  ✅ robots.txt создан\n')


# ================================================
# 4. ГЕНЕРИРУЕМ sitemap.xml
# ================================================
def create_sitemap():
    print('='*60)
    print('4. Генерируем sitemap.xml')
    print('='*60)
    
    SKIP = {
        'yandex_c82d19addf857c5c.html', 'privacy.html',
        'blog-category.html',
    }
    
    urls = []
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Главная
    urls.append((f'{DOMAIN}/', '1.0', 'weekly'))
    
    # Городские страницы (только из корня, не из blog/)
    for fn in sorted(os.listdir(SCRIPT_DIR)):
        if not fn.endswith('.html') or fn in SKIP:
            continue
        if '.php.html' in fn:
            continue
        fp = os.path.join(SCRIPT_DIR, fn)
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Городские страницы (без data-blog-root)
        if 'data-blog-root' not in content:
            if fn != 'index.html':
                urls.append((f'{DOMAIN}/{fn}', '0.8', 'monthly'))
    
    # Блог-категория
    urls.append((f'{DOMAIN}/blog-category.html', '0.6', 'weekly'))
    
    # Блог-статьи (только из /blog/)
    for fn in sorted(os.listdir(BLOG_DIR)):
        if not fn.endswith('.html') or '.php.html' in fn:
            continue
        urls.append((f'{DOMAIN}/blog/{fn}', '0.5', 'monthly'))
    
    # XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url, priority, freq in urls:
        xml += f'  <url>\n'
        xml += f'    <loc>{url}</loc>\n'
        xml += f'    <lastmod>{today}</lastmod>\n'
        xml += f'    <changefreq>{freq}</changefreq>\n'
        xml += f'    <priority>{priority}</priority>\n'
        xml += f'  </url>\n'
    xml += '</urlset>\n'
    
    fp = os.path.join(SCRIPT_DIR, 'sitemap.xml')
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(xml)
    
    print(f'  ✅ sitemap.xml создан ({len(urls)} URL)\n')


# ================================================
# 5. ДОБАВЛЯЕМ CANONICAL ТЕГИ
# ================================================
def add_canonicals():
    print('='*60)
    print('5. Добавляем canonical теги')
    print('='*60)
    
    SKIP = {'yandex_c82d19addf857c5c.html'}
    added = 0
    
    # Все HTML в корне
    for fn in sorted(os.listdir(SCRIPT_DIR)):
        if not fn.endswith('.html') or fn in SKIP or '.php.html' in fn:
            continue
        fp = os.path.join(SCRIPT_DIR, fn)
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'rel="canonical"' in content:
            continue
        
        # Определяем canonical URL
        if 'data-blog-root' in content:
            # Статья-дубль в корне → canonical на /blog/ версию
            canonical = f'{DOMAIN}/blog/{fn}'
        elif fn == 'index.html':
            canonical = f'{DOMAIN}/'
        else:
            canonical = f'{DOMAIN}/{fn}'
        
        tag = f'  <link rel="canonical" href="{canonical}">'
        
        # Вставляем после последнего <meta> в <head>, перед </head> или <style>
        # Ищем позицию для вставки — перед первым <style> или </head>
        insert_before = '</head>'
        for marker in ['<style>', '<link rel="stylesheet"', '</head>']:
            if marker in content:
                insert_before = marker
                break
        
        content = content.replace(insert_before, tag + '\n' + insert_before, 1)
        
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        added += 1
        print(f'  ✅ {fn:50s} → {canonical}')
    
    # Все HTML в /blog/
    for fn in sorted(os.listdir(BLOG_DIR)):
        if not fn.endswith('.html') or '.php.html' in fn:
            continue
        fp = os.path.join(BLOG_DIR, fn)
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'rel="canonical"' in content:
            continue
        
        canonical = f'{DOMAIN}/blog/{fn}'
        tag = f'  <link rel="canonical" href="{canonical}">'
        
        insert_before = '</head>'
        for marker in ['<style>', '<link rel="stylesheet"', '</head>']:
            if marker in content:
                insert_before = marker
                break
        
        content = content.replace(insert_before, tag + '\n' + insert_before, 1)
        
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        added += 1
        print(f'  ✅ blog/{fn:46s} → {canonical}')
    
    print(f'\n  Добавлено canonical: {added} страниц\n')


# ================================================
# MAIN
# ================================================
if __name__ == '__main__':
    fix_og_urls()
    fix_index_og()
    create_robots()
    create_sitemap()
    add_canonicals()
    print('='*60)
    print('✅ ВСЕ SEO-ФИКСЫ ПРИМЕНЕНЫ!')
    print('='*60)
