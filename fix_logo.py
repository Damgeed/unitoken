import glob, re

html_files = glob.glob("/Users/openclaw_007/projects/glbtoken/*.html")
patched = 0

for fname in sorted(html_files):
    with open(fname, 'r') as f:
        content = f.read()
    
    # Pattern 1: navbar logo with class="active"
    old_nav_open = '<div class="nav-logo" onclick="window.location=\'index.html\'" class="active">'
    new_nav_open = '<a href="index.html" class="nav-logo active">'
    
    # Pattern 2: footer logo without class="active"
    old_foot_open = '<div class="nav-logo" onclick="window.location=\'index.html\'">'
    new_foot_open = '<a href="index.html" class="nav-logo">'
    
    # Count occurrences
    nav_count = content.count(old_nav_open)
    foot_count = content.count(old_foot_open)
    
    # Replace opening tags
    content = content.replace(old_nav_open, new_nav_open)
    content = content.replace(old_foot_open, new_foot_open)
    
    total_replacements = nav_count + foot_count
    
    # Now replace the closing </div> for each nav-logo with </a>
    # Since nav-logo contains ONLY spans (no nested divs),
    # we replace the first </div> after each opening that's been replaced.
    
    # Simple approach: replace </div> with </a> for the known span pattern
    # The nav-logo always looks like: <a ... class="nav-logo ..."><span ...>GT</span><span ...><span>Glb</span><span>TOKEN</span></span></a>
    # So the closing tag is always: </div> right after </span></span>
    
    # Actually, let me just do exact string replacement
    old_closing = 'logo-token">TOKEN</span></span></div>'
    new_closing = 'logo-token">TOKEN</span></span></a>'
    content = content.replace(old_closing, new_closing)
    
    with open(fname, 'w') as f:
        f.write(content)
    
    if total_replacements > 0:
        patched += 1
        print(f"✅ {fname.split('/')[-1]}: {total_replacements} logo(s) converted to <a> tags")

print(f"\nPatched {patched} files")
