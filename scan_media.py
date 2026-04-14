import os
from pathlib import Path
from collections import defaultdict

REPO_PATH = r'D:\GitHub\genesis-to-quantum'

# Media file extensions to scan for
MEDIA_EXTENSIONS = {
    # Images
    '.jpg': 'Image',
    '.jpeg': 'Image',
    '.png': 'Image',
    '.gif': 'Image',
    '.svg': 'Image',
    '.webp': 'Image',
    '.bmp': 'Image',
    '.ico': 'Image',
    '.tiff': 'Image',
    
    # Video
    '.mp4': 'Video',
    '.avi': 'Video',
    '.mov': 'Video',
    '.mkv': 'Video',
    '.webm': 'Video',
    '.flv': 'Video',
    '.m4v': 'Video',
    
    # Audio
    '.mp3': 'Audio',
    '.wav': 'Audio',
    '.flac': 'Audio',
    '.aac': 'Audio',
    '.ogg': 'Audio',
    '.wma': 'Audio',
    '.m4a': 'Audio',
    
    # Documents (often large)
    '.pdf': 'Document',
    '.docx': 'Document',
    '.xlsx': 'Document',
    '.pptx': 'Document',
    
    # Archives
    '.zip': 'Archive',
    '.rar': 'Archive',
    '.7z': 'Archive',
    '.tar': 'Archive',
    '.gz': 'Archive',
}

# Scan for media files
media_files = []
for file_path in Path(REPO_PATH).rglob('*'):
    if file_path.is_file():
        ext = file_path.suffix.lower()
        if ext in MEDIA_EXTENSIONS:
            size_mb = file_path.stat().st_size / (1024 * 1024)
            rel_path = file_path.relative_to(REPO_PATH)
            media_type = MEDIA_EXTENSIONS[ext]
            media_files.append({
                'path': str(rel_path),
                'filename': file_path.name,
                'type': media_type,
                'size_mb': round(size_mb, 2),
                'ext': ext
            })

# Organize by type
by_type = defaultdict(list)
by_dir = defaultdict(list)

for mf in media_files:
    by_type[mf['type']].append(mf)
    dir_name = Path(mf['path']).parent
    by_dir[str(dir_name)].append(mf)

# Print report
print('=' * 100)
print('MEDIA FILES AUDIT')
print('=' * 100)
print(f'Total media files found: {len(media_files)}')
print()

# Summary by type
print('By Type:')
total_size = 0
for mtype in sorted(by_type.keys()):
    files = by_type[mtype]
    type_size = sum(f['size_mb'] for f in files)
    total_size += type_size
    print(f'  {mtype:10} {len(files):3} files, {type_size:8.2f} MB')

print(f'\nTotal Size: {total_size:.2f} MB')
print()

# List all media files
print('=' * 100)
print('DETAILED MEDIA FILE LIST')
print('=' * 100)
print(f'{"Path":<60} {"Type":<10} {"Size (MB)":<12}')
print('-' * 100)

for mf in sorted(media_files, key=lambda x: (x['type'], x['path'])):
    size_str = f"{mf['size_mb']:.2f}"
    print(f'{mf["path"]:<60} {mf["type"]:<10} {size_str:<12}')

# Check which media files are referenced in HTML
print()
print('=' * 100)
print('MEDIA USAGE IN HTML FILES')
print('=' * 100)

html_files = list(Path(REPO_PATH).rglob('*.html'))
used_media = set()
unused_media = []

for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        for mf in media_files:
            filename = mf['filename']
            if filename in content or mf['path'].replace('\\', '/') in content:
                used_media.add(mf['path'])
    except:
        pass

# Find unused media
for mf in media_files:
    if mf['path'] not in used_media:
        unused_media.append(mf)

print(f'Media files referenced in HTML: {len(used_media)}')
print(f'Media files NOT referenced (orphaned): {len(unused_media)}')
print()

if unused_media:
    print('ORPHANED MEDIA FILES (not referenced in any HTML):')
    print('-' * 100)
    print(f'{"Path":<60} {"Type":<10} {"Size (MB)":<12}')
    print('-' * 100)
    orphaned_size = 0
    for mf in sorted(unused_media, key=lambda x: (x['type'], x['path'])):
        size_str = f"{mf['size_mb']:.2f}"
        print(f'{mf["path"]:<60} {mf["type"]:<10} {size_str:<12}')
        orphaned_size += mf['size_mb']
    print(f'\nTotal orphaned media size: {orphaned_size:.2f} MB')
