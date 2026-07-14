#!/usr/bin/env python3
"""Add additional meaningful translations for the remaining untranslated texts."""
import os, re

TRANS_FILE = os.path.expanduser("~/projects/glbtoken/translations.js")

# Additional UI texts found in skipped list that should be translated
ADDITIONAL_TRANS = {
    "All": {"zh-CN": "全部", "ru": "Все", "ja": "すべて", "de": "Alle"},
    "Pro": {"zh-CN": "专业版", "ru": "Про", "ja": "プロ", "de": "Pro"},
    "Launch": {"zh-CN": "发布", "ru": "Запуск", "ja": "リリース", "de": "Einführung"},
    "Endpoint": {"zh-CN": "端点", "ru": "Точка доступа", "ja": "エンドポイント", "de": "Endpunkt"},
    "AI Models": {"zh-CN": "AI 模型", "ru": "Модели ИИ", "ja": "AIモデル", "de": "KI-Modelle"},
    "Excellent": {"zh-CN": "优秀", "ru": "Отлично", "ja": "優秀", "de": "Hervorragend"},
    "Very Good": {"zh-CN": "非常好", "ru": "Очень хорошо", "ja": "とても良い", "de": "Sehr gut"},
    "Good": {"zh-CN": "良好", "ru": "Хорошо", "ja": "良い", "de": "Gut"},
    "Capability": {"zh-CN": "能力", "ru": "Возможности", "ja": "機能", "de": "Fähigkeit"},
    "↓ Price": {"zh-CN": "↓ 价格", "ru": "↓ Цена", "ja": "↓ 価格", "de": "↓ Preis"},
    "🤖 Model": {"zh-CN": "🤖 模型", "ru": "🤖 Модель", "ja": "🤖 モデル", "de": "🤖 Modell"},
    "✅ Success": {"zh-CN": "✅ 成功", "ru": "✅ Успешно", "ja": "✅ 成功", "de": "✅ Erfolg"},
    "❌ Failed": {"zh-CN": "❌ 失败", "ru": "❌ Ошибка", "ja": "❌ 失敗", "de": "❌ Fehlgeschlagen"},
    "~0 tokens": {"zh-CN": "~0 代币", "ru": "~0 токенов", "ja": "~0 トークン", "de": "~0 Tokens"},
    "Glb  TOKEN": {"zh-CN": "Glb  TOKEN", "ru": "Glb  TOKEN", "ja": "Glb  TOKEN", "de": "Glb  TOKEN"},
}

with open(TRANS_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Check which ones are already in TRANS
existing_keys = set(re.findall(r'TRANS\["([^"]+)"\]', content))
existing_keys.update(re.findall(r"TRANS\['([^']+)'\]", content))

new_entries = []
for text, trans in ADDITIONAL_TRANS.items():
    if text in existing_keys:
        print(f"  Already exists: {repr(text)}")
        continue
    escaped_text = text.replace('\\', '\\\\').replace('"', '\\"')
    zh = trans["zh-CN"].replace('\\', '\\\\').replace('"', '\\"')
    ru = trans["ru"].replace('\\', '\\\\').replace('"', '\\"')
    ja = trans["ja"].replace('\\', '\\\\').replace('"', '\\"')
    de = trans["de"].replace('\\', '\\\\').replace('"', '\\"')
    entry = f'TRANS["{escaped_text}"] = {{en: "{escaped_text}", "zh-CN": "{zh}", ru: "{ru}", ja: "{ja}", de: "{de}"}};'
    new_entries.append(entry)
    print(f"  NEW: {repr(text)} → {zh}")

if new_entries:
    # Insert before the last IIFE
    insert_pos = content.rfind("(function() {")
    if insert_pos == -1:
        insert_pos = len(content)
    
    new_section = "\n\n// ── Additional short UI labels ──\n" + "\n".join(new_entries)
    updated = content[:insert_pos] + new_section + content[insert_pos:]
    
    with open(TRANS_FILE, "w", encoding="utf-8") as f:
        f.write(updated)
    
    print(f"\n✅ Added {len(new_entries)} more translations")
else:
    print("\n⚠️ Nothing new to add")
