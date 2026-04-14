import csv
from pathlib import Path
from collections import defaultdict

csv_path = r'D:\GitHub\genesis-to-quantum\html_audit.csv'

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Display summary
print('=' * 120)
print('HTML AUDIT REPORT - SUMMARY')
print('=' * 120)
print(f'Total files: {len(rows)}')

linked = [r for r in rows if r['is_linked'] == 'YES']
orphaned = [r for r in rows if r['is_linked'] == 'NO']

print(f'Linked: {len(linked)} ({100*len(linked)//len(rows)}%)')
print(f'Orphaned: {len(orphaned)} ({100*len(orphaned)//len(rows)}%)')
print()

# By category
by_cat = defaultdict(list)
for r in rows:
    by_cat[r['category']].append(r)

print('By Category:')
for cat in sorted(by_cat.keys()):
    cat_rows = by_cat[cat]
    cat_orphaned = [r for r in cat_rows if r['is_linked'] == 'NO']
    print(f'  {cat}: {len(cat_rows):2} total, {len(cat_orphaned):2} orphaned')

print()
print('=' * 120)
print('ORPHANED FILES (not linked from index/navigation):')
print('=' * 120)
print(f'{"Filename":<55} {"Category":<30} {"Title":<40}')
print('-' * 120)
for r in sorted(orphaned, key=lambda x: x['category']):
    title = r['title'][:35] if r['title'] else '[No title]'
    print(f'{r["filename"]:<55} {r["category"]:<30} {title:<40}')

print()
print('=' * 120)
print('LINKED FILES (accessible from index/navigation):')
print('=' * 120)
print(f'{"Filename":<55} {"Category":<30} {"Title":<40}')
print('-' * 120)
for r in sorted(linked, key=lambda x: x['category']):
    title = r['title'][:35] if r['title'] else '[No title]'
    print(f'{r["filename"]:<55} {r["category"]:<30} {title:<40}')
