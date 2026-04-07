import io

try:
    with io.open('ltcoe.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Known replacement sequences
    replacements = {
        's,?': '⚠️',
        '? On Track': '✅ On Track',
        '?': '✅',
        '?\"': '—',
        '?"': '—',
        'â€™': "'",
        'â€œ': '"',
        'â€ ': '"',
        'Â': '',
        'âš ï¸': '⚠️',
        'âœ…': '✅',
        'ðŸŽ“': '🎓',
        'ðŸ””': '🔔',
        'ðŸ“‹': '📋',
        'ðŸ‘': '👥',
        'âž•': '➕',
        'ðŸ“Š': '📊',
        'ðŸ“ˆ': '📈',
        'ðŸ‘¤': '👤',
        'ðŸ‘‹': '👋',
        'â Œ': '❌',
        'â ³': '⏳',
        'â¬‡': '⬇',
        'ðŸŽ‰': '🎉',
        'ðŸ—‘ï¸': '🗑️',
        'ðŸ”’': '🔒',
        'ðŸ—„ï¸': '🗄️',
        'âœ•': '✕',
        'âœ“': '✓',
        'âœ—': '✗',
        'ðŸŸ¢': '🟢',
        'ðŸ”´': '🔴',
        'â€”': '—',
        'ðŸ‘¥': '👥',
        'â Œ': '❌',
        'ðŸ”Ž': '🔍',
        'ï¿½': ''
    }
    
    for k, v in replacements.items():
        if k in content:
            content = content.replace(k, v)

    with io.open('ltcoe.html', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print('Corrupted characters replaced successfully!')
except Exception as e:
    print('Error:', e)
