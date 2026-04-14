import os
import re
from pathlib import Path
import csv
from collections import defaultdict

REPO_PATH = r'D:\GitHub\genesis-to-quantum'
OUTPUT_CSV = r'D:\GitHub\genesis-to-quantum\html_audit.csv'

CATEGORIES = {
    'Genesis to Quantum': r'^gtq-\d+',
    'Consciousness': r'^consciousness-',
    'Moral Decline of America': r'^moral-decline-',
    'Salvation': r'^(salvation-|salvation_)',
    'Family Briefing': r'^blue-',
    'Standalone': None
}

def extract_title(html_path):
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return '[No title found]'
    except Exception as e:
        return f'[Error: {str(e)}]'

def categorize_file(filename):
    base_name = Path(filename).stem
    for category, pattern in CATEGORIES.items():
        if pattern and re.match(pattern, base_name):
            return category
    return 'Standalone'

def find_links_in_file(html_path, target_filename):
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        patterns = [
            rf'href=["\']([^"\']*{re.escape(target_filename)}["\'])',
            rf'href=["\']([^"\']*{re.escape(Path(target_filename).stem)}["\'])',
        ]
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    except:
        return False

def get_all_html_files(repo_path):
    return sorted([f for f in Path(repo_path).rglob('*.html')])

def get_index_pages(html_files):
    index_pages = []
    for f in html_files:
        name = f.name.lower()
        if 'index' in name:
            index_pages.append(f)
    return index_pages

if __name__ == '__main__':
    all_files = get_all_html_files(REPO_PATH)
    print(f'Found {len(all_files)} HTML files')

    index_pages = get_index_pages(all_files)
    print(f'Found {len(index_pages)} index pages')

    audit_data = []
    for i, html_file in enumerate(all_files):
        rel_path = html_file.relative_to(REPO_PATH)
        filename = html_file.name
        title = extract_title(html_file)
        category = categorize_file(filename)
        
        is_linked = False
        linked_from = []
        
        for idx_page in index_pages:
            if idx_page != html_file and find_links_in_file(idx_page, filename):
                is_linked = True
                linked_from.append(str(idx_page.relative_to(REPO_PATH)))
        
        audit_data.append({
            'filename': str(rel_path),
            'title': title,
            'category': category,
            'is_linked': 'YES' if is_linked else 'NO',
            'linked_from': ', '.join(linked_from) if linked_from else 'N/A'
        })
        
        if (i + 1) % 10 == 0:
            print(f'Processed {i + 1}/{len(all_files)}')

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'title', 'category', 'is_linked', 'linked_from'])
        writer.writeheader()
        writer.writerows(audit_data)

    total = len(audit_data)
    linked = sum(1 for d in audit_data if d['is_linked'] == 'YES')
    unlinked = total - linked

    print(f'\nTotal: {total}, Linked: {linked}, Orphaned: {unlinked}')
    print(f'Saved to {OUTPUT_CSV}')
