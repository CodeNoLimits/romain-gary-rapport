# Génère soirees/ : liste d'attente + 3 pages soirées × he/fr/en. Rien d'inventé (pas de date, prix, artiste).
import json, os, sys
OUT = sys.argv[1]; S = 'https://romaingarycafebistro.com'; WA = '972546657655'
T = {
 'he': dict(dir='rtl', kick='ערבי מוזיקה ותרבות', wt='ערבי המוזיקה מגיעים בקרוב', ws='הירשמו לרשימת ההמתנה והיו הראשונים לדעת על התאריכים.',
   fn='שם פרטי', ph='טלפון (וואטסאפ)', em='אימייל (לא חובה)', pref='איזה ערב מעניין אתכם?', opts=['ג׳אז חי','ערב רגאיי','ערב פריזאי','כולם'],
   btn='הצטרפות לרשימת ההמתנה', note='בלחיצה ייפתח וואטסאפ עם הודעה מוכנה לשליחה לבית הקפה.', count='היו בין הראשונים.', date='התאריך יפורסם בקרוב',
   join='הצטרפות לרשימת ההמתנה', all='כל ערבי המוזיקה', foot='הלל 35, ירושלים · כשר למהדרין',
   msg='שלום, אני רוצה להצטרף לרשימת ההמתנה לערבי המוזיקה.\nשם: {n}\nטלפון: {p}\nאימייל: {e}\nערב מועדף: {o}',
   ev=[('jazz','ג׳אז <em>חי</em>','בביסטרו הפריזאי של ירושלים'),('reggae','ערב <em>רגאיי</em>','מוזיקה חיה בלב ירושלים'),('paris','ערב <em>פריזאי</em>','מוזיקה צרפתית ומטבח ביסטרו')]),
 'fr': dict(dir='ltr', kick='Soirées musique & culture', wt='Les soirées arrivent bientôt', ws='Inscrivez-vous sur la liste d’attente et soyez les premiers à connaître les dates.',
   fn='Prénom', ph='Téléphone (WhatsApp)', em='E-mail (facultatif)', pref='Quelle soirée vous intéresse ?', opts=['Jazz live','Soirée reggae','Soirée parisienne','Toutes les soirées'],
   btn='Rejoindre la liste', note='L’envoi ouvre WhatsApp avec un message prêt pour le café.', count='Soyez parmi les premiers.', date='Date bientôt révélée',
   join='Rejoindre la liste d’attente', all='Toutes les soirées', foot='35, rue Hillel, Jérusalem · Casher mehadrin',
   msg='Bonjour, je souhaite rejoindre la liste d’attente des soirées.\nPrénom : {n}\nTéléphone : {p}\nE-mail : {e}\nSoirée préférée : {o}',
   ev=[('jazz','Jazz <em>live</em>','Au bistrot parisien de Jérusalem'),('reggae','Soirée <em>reggae</em>','Musique live au cœur de Jérusalem'),('paris','Soirée <em>parisienne</em>','Chanson française et cuisine de bistrot')]),
 'en': dict(dir='ltr', kick='Music & culture evenings', wt='The evenings are coming soon', ws='Join the waiting list and be the first to know the dates.',
   fn='First name', ph='Phone (WhatsApp)', em='Email (optional)', pref='Which evening interests you?', opts=['Live jazz','Reggae night','Parisian evening','All evenings'],
   btn='Join the list', note='Sending opens WhatsApp with a ready message to the café.', count='Be among the first.', date='Date to be revealed soon',
   join='Join the waiting list', all='All evenings', foot='35 Hillel Street, Jerusalem · Kosher mehadrin',
   msg='Hello, I would like to join the waiting list for the evenings.\nName: {n}\nPhone: {p}\nEmail: {e}\nPreferred evening: {o}',
   ev=[('jazz','Live <em>jazz</em>','At the Parisian bistro of Jerusalem'),('reggae','Reggae <em>night</em>','Live music in the heart of Jerusalem'),('paris','Parisian <em>evening</em>','French chanson and bistro cuisine')]),
}
AR = {'he': '←', 'fr': '→', 'en': '→'}
MEDIA = {'jazz': ('bar-1400.webp', 'JAZZ_HE.mp4'), 'reggae': ('hero-1920.webp', 'REGGAE_HE.mp4'), 'paris': ('livres-900.webp', 'SOIREES_FR.mp4')}
CSS = """:root{--ink:#0d0e13;--cream:#f4ede0;--gold:#c9a45c;--gold2:#e7cf98;--muted:#b9ab90}*{box-sizing:border-box;margin:0;padding:0}
html,body{background:var(--ink);color:var(--cream);font:300 18px/1.6 'Frank Ruhl Libre',Georgia,serif}a{color:inherit}
.top{position:fixed;inset:0 0 auto;display:flex;justify-content:space-between;align-items:center;padding:18px 20px;z-index:5;background:linear-gradient(rgba(13,14,19,.85),transparent)}
.brand{font:600 18px 'Cormorant Garamond',serif;letter-spacing:.3em;color:var(--gold2);text-decoration:none;direction:ltr}
.lang a{font:500 14px 'Cormorant Garamond',serif;letter-spacing:.15em;color:var(--muted);text-decoration:none;margin-inline-start:14px}.lang a.on{color:var(--gold2);border-bottom:1px solid var(--gold)}
.hero{position:relative;min-height:100svh;display:flex;align-items:flex-end;overflow:hidden}
.hero video,.hero img.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:sepia(.25) brightness(.62) contrast(1.08)}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(to bottom,rgba(13,14,19,.2) 0%,rgba(13,14,19,.1) 35%,rgba(13,14,19,.88) 78%,var(--ink) 100%)}
.in{position:relative;z-index:2;width:100%;max-width:1100px;margin:0 auto;padding:0 20px 56px}
.kick{display:flex;align-items:center;gap:14px;color:var(--gold2);font-size:16px;letter-spacing:.06em;opacity:0;animation:up .9s .2s forwards}.kick:after{content:"";width:64px;height:1px;background:var(--gold)}
h1{font-weight:500;font-size:clamp(54px,12vw,128px);line-height:.98;margin:14px 0 10px;opacity:0;animation:up 1s .35s forwards}h1 em{font-style:normal;color:var(--gold)}
.sub{font-size:clamp(19px,2.6vw,26px);max-width:34ch;opacity:0;animation:up 1s .5s forwards}
.date{display:inline-block;margin-top:22px;border:1px solid var(--gold);padding:10px 18px;color:var(--gold2);letter-spacing:.04em;opacity:0;animation:up 1s .65s forwards}
.cta{display:inline-flex;align-items:center;gap:12px;margin-top:22px;padding:16px 26px;background:linear-gradient(135deg,#d8b670,#b8914a);color:#14110b;font-weight:500;text-decoration:none;border:0;font-family:inherit;font-size:18px;cursor:pointer;opacity:0;animation:up 1s .8s forwards;transition:transform .3s,box-shadow .3s}
.cta:hover{transform:translateY(-2px);box-shadow:0 12px 34px rgba(201,164,92,.35)}.cta:focus-visible,input:focus-visible,select:focus-visible{outline:2px solid var(--gold2);outline-offset:3px}
@keyframes up{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;opacity:1!important}}
.wrap{max-width:1100px;margin:0 auto;padding:64px 20px}
form{display:grid;gap:16px;max-width:520px;margin-top:28px}label{display:grid;gap:6px;font-size:15px;color:var(--muted)}
input,select{background:rgba(244,237,224,.05);border:1px solid rgba(201,164,92,.45);color:var(--cream);padding:14px;font:inherit;font-size:17px}
select option{color:#111}.note{font-size:14px;color:var(--muted)}.count{margin-top:6px;color:var(--gold2);font-size:20px}
.grid{display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));margin-top:30px}
.card{position:relative;display:block;aspect-ratio:4/5;overflow:hidden;text-decoration:none;border:1px solid rgba(201,164,92,.3)}
.card img{width:100%;height:100%;object-fit:cover;filter:sepia(.25) brightness(.55);transition:transform 1.2s}.card:hover img{transform:scale(1.06)}
.card span{position:absolute;inset:auto 0 0;padding:22px;font-size:34px;font-weight:500;background:linear-gradient(transparent,rgba(13,14,19,.9))}.card span em{font-style:normal;color:var(--gold)}
footer{border-top:1px solid rgba(201,164,92,.3);padding:26px 20px;text-align:center;color:var(--muted);font-size:15px}
"""
def head(l, title, path):
    alt = ''.join(f'<link rel="alternate" hreflang="{k}" href="../{k}/{path}">' for k in T)
    return f'''<!doctype html><html lang="{l}" dir="{T[l]['dir']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{title} · Romain Gary</title>{alt}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Frank+Ruhl+Libre:wght@300;500&display=swap">
<style>{CSS}</style></head><body><header class="top"><a class="brand" href="./">ROMAIN GARY</a><nav class="lang">{''.join(f'<a href="../{k}/{path}" class="{"on" if k==l else ""}">{ {"he":"עב","fr":"FR","en":"EN"}[k]}</a>' for k in T)}</nav></header>'''
def foot(l): return f'<footer>{T[l]["foot"]} · <a href="{S}/{"" if l=="he" else l+"/"}">romaingarycafebistro.com</a></footer></body></html>'
def page_liste(l):
    t = T[l]; o = ''.join(f'<option>{x}</option>' for x in t['opts'])
    cards = ''.join(f'<a class="card" href="{k}.html"><img src="{S}/assets/{MEDIA[k][0]}" alt=""><span>{ti}</span></a>' for k, ti, _ in t['ev'])
    js = "document.getElementById('f').onsubmit=e=>{e.preventDefault();const g=n=>document.getElementById(n).value.trim();const m=%s.replace('{n}',g('n')).replace('{p}',g('p')).replace('{e}',g('e')||'-').replace('{o}',g('o'));location.href='https://wa.me/%s?text='+encodeURIComponent(m)};" % (json.dumps(t['msg']), WA)
    return head(l, t['wt'], 'index.html') + f'''<section class="hero"><img class="bg" src="{S}/assets/hero-1920.webp" alt=""><div class="in">
<div class="kick">{t['kick']}</div><h1>{t['wt']}</h1><p class="sub">{t['ws']}</p><p class="count">{t['count']}</p></div></section>
<section class="wrap" id="liste"><form id="f"><label>{t['fn']}<input id="n" required autocomplete="given-name"></label>
<label>{t['ph']}<input id="p" type="tel" required autocomplete="tel" dir="ltr"></label><label>{t['em']}<input id="e" type="email" autocomplete="email" dir="ltr"></label>
<label>{t['pref']}<select id="o">{o}</select></label><button class="cta" type="submit">{t['btn']} {AR[l]}</button><p class="note">{t['note']}</p></form>
<div class="grid">{cards}</div></section><script>{js}</script>''' + foot(l)
def page_soiree(l, k, ti, sub):
    t = T[l]; img, vid = MEDIA[k]
    return head(l, ti.replace('<em>', '').replace('</em>', ''), f'{k}.html') + f'''<section class="hero"><video autoplay muted loop playsinline poster="{S}/assets/{img}" src="{S}/v/{vid}"></video><div class="in">
<div class="kick">{t['kick']}</div><h1>{ti}</h1><p class="sub">{sub}</p><span class="date">{t['date']}</span><br>
<a class="cta" href="index.html#liste">{t['join']} {AR[l]}</a><p style="margin-top:18px"><a href="index.html" style="color:var(--muted)">{t['all']}</a></p></div></section>''' + foot(l)
for l in T:
    os.makedirs(f'{OUT}/{l}', exist_ok=True)
    open(f'{OUT}/{l}/index.html', 'w').write(page_liste(l))
    for k, ti, sub in T[l]['ev']: open(f'{OUT}/{l}/{k}.html', 'w').write(page_soiree(l, k, ti, sub))
open(f'{OUT}/index.html', 'w').write('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=he/"><a href="he/">he</a>')
print('ok', sum(len(f) for _, _, f in os.walk(OUT)), 'fichiers')
