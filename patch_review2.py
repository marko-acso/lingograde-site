#!/usr/bin/env python3
"""
Patch review.html:
1. Change country text input to dropdown with common countries
2. Add Trustpilot button to the thank-you page
"""
import sys

path = sys.argv[1] if len(sys.argv) > 1 else 'review.html'
html = open(path, 'r', encoding='utf-8').read()

# ── 1. Replace country text input with dropdown ──
old_country = '<label>Country</label><input type="text" id="reviewCountry" placeholder="e.g. Italy">'
new_country = (
    '<label>Country</label>'
    '<select id="reviewCountry">'
    '<option value="">Select...</option>'
    '<option>Albania</option>'
    '<option>Argentina</option>'
    '<option>Australia</option>'
    '<option>Austria</option>'
    '<option>Belarus</option>'
    '<option>Belgium</option>'
    '<option>Bosnia and Herzegovina</option>'
    '<option>Brazil</option>'
    '<option>Bulgaria</option>'
    '<option>Canada</option>'
    '<option>Chile</option>'
    '<option>China</option>'
    '<option>Colombia</option>'
    '<option>Croatia</option>'
    '<option>Czech Republic</option>'
    '<option>Denmark</option>'
    '<option>Egypt</option>'
    '<option>Estonia</option>'
    '<option>Finland</option>'
    '<option>France</option>'
    '<option>Germany</option>'
    '<option>Greece</option>'
    '<option>Hungary</option>'
    '<option>India</option>'
    '<option>Indonesia</option>'
    '<option>Iran</option>'
    '<option>Iraq</option>'
    '<option>Ireland</option>'
    '<option>Israel</option>'
    '<option>Italy</option>'
    '<option>Japan</option>'
    '<option>Kosovo</option>'
    '<option>Latvia</option>'
    '<option>Lebanon</option>'
    '<option>Lithuania</option>'
    '<option>Luxembourg</option>'
    '<option>Mexico</option>'
    '<option>Moldova</option>'
    '<option>Montenegro</option>'
    '<option>Morocco</option>'
    '<option>Netherlands</option>'
    '<option>Nigeria</option>'
    '<option>North Macedonia</option>'
    '<option>Norway</option>'
    '<option>Pakistan</option>'
    '<option>Peru</option>'
    '<option>Philippines</option>'
    '<option>Poland</option>'
    '<option>Portugal</option>'
    '<option>Romania</option>'
    '<option>Russia</option>'
    '<option>Saudi Arabia</option>'
    '<option>Serbia</option>'
    '<option>Slovakia</option>'
    '<option>Slovenia</option>'
    '<option>South Africa</option>'
    '<option>South Korea</option>'
    '<option>Spain</option>'
    '<option>Sweden</option>'
    '<option>Switzerland</option>'
    '<option>Syria</option>'
    '<option>Tunisia</option>'
    '<option>Turkey</option>'
    '<option>Ukraine</option>'
    '<option>United Arab Emirates</option>'
    '<option>United Kingdom</option>'
    '<option>United States</option>'
    '<option>Venezuela</option>'
    '<option>Vietnam</option>'
    '<option>Other</option>'
    '</select>'
)
html = html.replace(old_country, new_country, 1)

# ── 2. Add Trustpilot button to thank-you page ──
# REPLACE the Trustpilot URL below with your actual Trustpilot profile URL
TRUSTPILOT_URL = 'https://www.trustpilot.com/review/lingograde.com'

old_thankyou = "<p style=\"margin-top:24px;\"><a href=\"/\" style=\"color:var(--accent);font-weight:600;text-decoration:none;\">Back to LingoGrade</a></p>"
new_thankyou = (
    '<div style="margin-top:32px;padding:24px;background:#f0faf0;border-radius:12px;border:1px solid #d4edda;text-align:center;">'
    '<p style="margin:0 0 8px;font-size:1rem;font-weight:600;color:#1C1C1C;">Loved your experience?</p>'
    '<p style="margin:0 0 16px;font-size:0.9rem;color:var(--ink-soft);">Help others find us — it takes 30 seconds.</p>'
    f'<a href="{TRUSTPILOT_URL}" target="_blank" rel="noopener" '
    'style="display:inline-flex;align-items:center;gap:8px;padding:12px 24px;background:#00b67a;color:white;'
    'border-radius:8px;text-decoration:none;font-weight:600;font-size:0.95rem;transition:background 0.2s;" '
    'onmouseover="this.style.background=\'#009a68\'" onmouseout="this.style.background=\'#00b67a\'">'
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>'
    'Review us on Trustpilot'
    '</a></div>\n'
    '<p style="margin-top:24px;"><a href="/" style="color:var(--accent);font-weight:600;text-decoration:none;">Back to LingoGrade</a></p>'
)
html = html.replace(old_thankyou, new_thankyou, 1)

open(path, 'w', encoding='utf-8').write(html)
print('✅ review.html patched successfully!')
print('   Changed: country to dropdown (70+ countries)')
print('   Added: Trustpilot button on thank-you page')
print(f'   Trustpilot URL: {TRUSTPILOT_URL}')
print('   ⚠️  If your Trustpilot URL is different, edit the script and re-run')
