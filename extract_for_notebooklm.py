"""
Extract clean text from all GTQ HTML articles for NotebookLM upload.
Strips HTML/CSS/JS, keeps title + narrative prose.
Output: D:\GitHub\genesis-to-quantum\notebooklm_text\
"""
import os, re, html
from pathlib import Path

BASE = Path(r"D:\GitHub\genesis-to-quantum")
OUT  = BASE / "notebooklm_text"
OUT.mkdir(exist_ok=True)

# Files to skip (not articles)
SKIP = {
    "index.html", "cover.html", "paper-template.html",
    "moral-decline-SAMPLE.html", "deploy.bat",
    "README_STATUS.md",
}

# Folders to skip entirely
SKIP_DIRS = {".git", ".wrangler", "source_markdown", "__pycache__"}

def strip_html(raw_html):
    """Remove all HTML tags, scripts, styles, and decode entities."""
    # Remove script and style blocks
    text = re.sub(r'<script[^>]*>.*?</script>', '', raw_html, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', raw_html, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<noscript[^>]*>.*?</noscript>', '', raw_html, flags=re.DOTALL|re.IGNORECASE)
    # Remove HTML comments
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    # Remove SVG blocks
    text = re.sub(r'<svg[^>]*>.*?</svg>', '', text, flags=re.DOTALL|re.IGNORECASE)
    # Replace br/hr/p/div/h tags with newlines
    text = re.sub(r'<(?:br|hr|/p|/div|/h[1-6]|/li|/tr)[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<(?:p|div|h[1-6]|li|tr)[^>]*>', '\n', text, flags=re.IGNORECASE)
    # Remove all remaining tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = html.unescape(text)
    # Clean up whitespace
    lines = []
    for line in text.split('\n'):
        stripped = line.strip()
        if stripped:
            lines.append(stripped)
    # Collapse multiple blank lines
    result = '\n\n'.join(lines)
    # Remove any remaining excessive whitespace
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.strip()

def get_title(raw_html):
    """Extract title from <title> tag."""
    m = re.search(r'<title[^>]*>(.*?)</title>', raw_html, re.DOTALL|re.IGNORECASE)
    if m:
        return html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
    return "Untitled"

def process_file(filepath):
    """Process a single HTML file and return clean text."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            raw = f.read()
    except Exception as e:
        print(f"  ERROR reading {filepath}: {e}")
        return None
    title = get_title(raw)
    body = strip_html(raw)
    if len(body) < 100:
        print(f"  SKIP (too short): {filepath.name} ({len(body)} chars)")
        return None
    return f"# {title}\n\n{body}"

# Collect all HTML files
html_files = []
for root, dirs, files in os.walk(BASE):
    # Skip excluded directories
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for fname in sorted(files):
        if not fname.endswith('.html'):
            continue
        if fname in SKIP:
            continue
        html_files.append(Path(root) / fname)

print(f"Found {len(html_files)} HTML files to process")
print(f"Output directory: {OUT}\n")

count = 0
for fpath in html_files:
    rel = fpath.relative_to(BASE)
    # Create output filename: flatten path with underscores
    out_name = str(rel).replace('\\', '_').replace('/', '_')
    out_name = out_name.replace('.html', '.txt')
    print(f"Processing: {rel}")
    text = process_file(fpath)
    if text:
        out_path = OUT / out_name
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(text)
        word_count = len(text.split())
        print(f"  -> {out_name} ({word_count:,} words)")
        count += 1

print(f"\nDone! Extracted {count} articles to {OUT}")
print(f"Total files ready for NotebookLM upload.")
