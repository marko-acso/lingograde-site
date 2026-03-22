#!/usr/bin/env python3
"""
Patch review.html to add:
1. Email field (optional)
2. Avatar picker (3 silhouettes: female, male, neutral)
3. Consent checkbox (required)
4. Update JS to collect and send new fields
"""
import sys, os

path = sys.argv[1] if len(sys.argv) > 1 else 'review.html'
html = open(path, 'r', encoding='utf-8').read()

# ── 1. Add email field after Name/Country row ──
old_lang = '<div class="input-row"><div><label>Language Assessed</label>'
new_lang = (
    '<div class="input-row"><div><label>Email (optional)</label>'
    '<input type="email" id="reviewEmail" placeholder="So we can follow up if needed"></div></div>\n'
    '<div class="input-row"><div><label>Language Assessed</label>'
)
html = html.replace(old_lang, new_lang, 1)

# ── 2. Add avatar picker after Language row ──
old_textarea = '<div style="text-align:left;margin-top:12px;"><label style="font-size:0.8rem;font-weight:600;color:var(--ink-soft);display:block;margin-bottom:4px;">Anything else? (optional)</label>'
new_textarea = (
    '<div style="text-align:left;margin-top:16px;">'
    '<label style="font-size:0.8rem;font-weight:600;color:var(--ink-soft);display:block;margin-bottom:8px;">Choose your avatar</label>'
    '<div style="display:flex;gap:16px;justify-content:flex-start;" id="avatarPicker">'
    '<div class="avatar-opt" onclick="pickAvatar(this,\'female\')" style="width:56px;height:56px;border-radius:50%;border:2px solid #E0E0E0;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:28px;transition:all 0.2s;" title="Female">👩</div>'
    '<div class="avatar-opt" onclick="pickAvatar(this,\'male\')" style="width:56px;height:56px;border-radius:50%;border:2px solid #E0E0E0;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:28px;transition:all 0.2s;" title="Male">👨</div>'
    '<div class="avatar-opt" onclick="pickAvatar(this,\'neutral\')" style="width:56px;height:56px;border-radius:50%;border:2px solid #E0E0E0;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:28px;transition:all 0.2s;" title="Neutral">🧑</div>'
    '</div></div>\n'
    '<div style="text-align:left;margin-top:12px;"><label style="font-size:0.8rem;font-weight:600;color:var(--ink-soft);display:block;margin-bottom:4px;">Anything else? (optional)</label>'
)
html = html.replace(old_textarea, new_textarea, 1)

# ── 3. Add consent checkbox before Submit button ──
old_submit = '<button class="btn-next" id="btnSubmit" onclick="submitReview()">Submit My Review</button>'
new_submit = (
    '<div style="text-align:left;margin-top:16px;">'
    '<label style="display:flex;align-items:flex-start;gap:8px;cursor:pointer;font-size:0.85rem;color:var(--ink-soft);line-height:1.5;">'
    '<input type="checkbox" id="reviewConsent" style="margin-top:3px;min-width:18px;min-height:18px;accent-color:var(--accent);">'
    '<span>I agree that LingoGrade may publish this review on its website. '
    '<a href="/privacy.html" target="_blank" style="color:var(--accent);text-decoration:underline;">Privacy Policy</a></span>'
    '</label></div>\n'
    '<button class="btn-next" id="btnSubmit" onclick="submitReview()">Submit My Review</button>'
)
html = html.replace(old_submit, new_submit, 1)

# ── 4. Update JS: add avatar, email to data object ──
old_data = "var data={rating:0,valuable:'',recommend:'',name:'',country:'',language:'',feedback:''};"
new_data = "var data={rating:0,valuable:'',recommend:'',name:'',country:'',language:'',feedback:'',email:'',avatar:'',consent:false};"
html = html.replace(old_data, new_data, 1)

# ── 5. Add pickAvatar function after goTo function ──
old_submit_fn = 'function submitReview(){'
new_submit_fn = (
    "function pickAvatar(el,type){document.querySelectorAll('.avatar-opt').forEach(function(a){"
    "a.style.borderColor='#E0E0E0';a.style.background='transparent';a.style.transform='scale(1)';});"
    "el.style.borderColor='var(--accent)';el.style.background='rgba(37,99,171,0.08)';el.style.transform='scale(1.1)';"
    "data.avatar=type;}\n"
    "function submitReview(){"
)
html = html.replace(old_submit_fn, new_submit_fn, 1)

# ── 6. Update submitReview to collect email, consent, validate consent ──
old_collect = "data.feedback=document.getElementById('reviewFeedback').value.trim();"
new_collect = (
    "data.feedback=document.getElementById('reviewFeedback').value.trim();"
    "data.email=document.getElementById('reviewEmail').value.trim();"
    "data.consent=document.getElementById('reviewConsent').checked;"
    "if(!data.consent){alert('Please agree to the review publishing consent.');return;}"
)
html = html.replace(old_collect, new_collect, 1)

# ── 7. Update fetch body to include email, avatar, consent ──
old_body = "feedback:data.feedback}"
new_body = "feedback:data.feedback,email:data.email,avatar:data.avatar,consent:data.consent}"
html = html.replace(old_body, new_body, 1)

open(path, 'w', encoding='utf-8').write(html)
print('✅ review.html patched successfully!')
print('   Added: email field, avatar picker, consent checkbox')
print('   Updated: JS data object, submitReview function, fetch body')
