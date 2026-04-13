#!/usr/bin/env python3
"""Phase 10B: Fix invalid height="Auto" attributes across all HTML files.

height="Auto" is not valid HTML — height attributes must be numeric.
This causes Lighthouse Best Practices warnings and potential CLS issues.
Removes the invalid attribute entirely (CSS handles auto height).
"""

import glob

files = sorted(glob.glob('*.html'))
count = 0
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    if 'height="Auto"' in html:
        html = html.replace(' height="Auto"', '')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1
        print(f'  OK {filepath}')

print(f'\nFixed {count} files')
