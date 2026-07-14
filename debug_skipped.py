#!/usr/bin/env python3
"""Debug script to show what texts are being skipped."""
import os, re, html as html_mod

PROJECT_DIR = os.path.expanduser("~/projects/glbtoken")
TRANS_FILE = os.path.join(PROJECT_DIR, "translations.js")

ALL_HTML_FILES = [
    "index.html", "home.html", "about.html", "blog.html", "contact.html",
    "faq.html", "how.html", "models.html", "pricing.html", "privacy.html",
    "terms.html", "refund.html", "blog-article-1.html", "blog-article-2.html",
    "blog-article-3.html", "blog-article-4.html", "blog-article-5.html",
    "blog-article-6.html", "notifications.html", "settings.html",
    "history.html", "billing.html", "apikeys.html", "playground.html",
    "referral.html", "team.html", "topup.html", "presets.html",
    "login.html", "register.html", "dashboard.html",
]

STANDARD_WORDS = {
    "API", "GT", "USD", "AI", "SSE", "CSV", "URL", "HTML", "CSS", "JS",
    "JSON", "SDK", "CLI", "GUI", "HTTP", "HTTPS", "IP", "DNS", "REST",
    "OpenAI", "Anthropic", "Google", "Meta", "DeepSeek", "Mistral",
    "Stripe", "Paystack", "GitHub", "GlbTOKEN", "Glb", "TOKEN",
    "github.com", "glbtoken.com", "Railway", "Cloudflare",
    "GPT-4o", "GPT-4", "Claude 3.5", "Claude 3", "Gemini 2.0",
    "Llama 3.1", "Llama 4", "DeepSeek V3", "Mistral Large",
    "Sonnet", "Maverick", "Opus", "Turbo", "Flash", "GPT",
    "Token", "Tokens", "sk-glt",
    "base_url", "api_key", "Authorization", "Bearer", "max_tokens",
    "temperature", "top_p", "frequency_penalty", "presence_penalty",
    "stream", "role", "content", "model", "messages",
    "EN", "DE", "RU", "JP", "notranslate",
}

with open(TRANS_FILE, "r", encoding="utf-8") as f:
    content = f.read()
trans_keys = set(re.findall(r'TRANS\["([^"]+)"\]', content))
trans_keys.update(re.findall(r"TRANS\['([^']+)'\]", content))

all_texts = set()
for html_file in ALL_HTML_FILES:
    filepath = os.path.join(PROJECT_DIR, html_file)
    if not os.path.exists(filepath):
        continue
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        html_content = f.read()
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<svg[^>]*>.*?</svg>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<pre[^>]*>.*?</pre>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<code[^>]*>.*?</code>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', html_content)
    text = html_mod.unescape(text)
    for line in text.split('\n'):
        line = line.strip()
        if len(line) < 3 or len(line) > 200:
            continue
        if re.match(r'^[\d\s\.,%$₿€£¥₦+\-*/=<>()\[\]{}|&^~@#:;"\'\\\\]+$', line):
            continue
        if re.match(r'^(https?://|/|\.\.|\./|[a-zA-Z]:\\\\|sk-glt)', line):
            continue
        if sum(1 for c in line if c in '{}[]<>()|&^#$@=+/\\"\'') > len(line) * 0.3:
            continue
        all_texts.add(line)

untranslated = []
for text in sorted(all_texts, key=lambda x: (len(x), x)):
    if text in trans_keys:
        continue
    stripped = text.strip()
    if not stripped or len(stripped) < 3:
        continue
    skip = False
    for word in STANDARD_WORDS:
        if stripped.lower() == word.lower():
            skip = True
            break
    if skip:
        continue
    if re.search(r'[{}[\]()=<>]', stripped):
        continue
    if re.match(r'^[\d\s,.$%₿€£¥₦+\-]', stripped):
        continue
    if stripped.startswith('.') or stripped.startswith('#'):
        continue
    if re.search(r'[\u4e00-\u9fff\u0400-\u04ff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]', stripped):
        continue
    similar = False
    for key in trans_keys:
        if text.lower() == key.lower():
            similar = True
            break
    if similar:
        continue
    untranslated.append(text)

# Show some skipped texts grouped by type
print(f"Total untranslated: {len(untranslated)}")
print("\n=== Sample of skipped texts ===")
for t in untranslated[:50]:
    print(f"  [{len(t):3d}] {repr(t)}")
if len(untranslated) > 30:
    print(f"  ... and {len(untranslated)-30} more")
