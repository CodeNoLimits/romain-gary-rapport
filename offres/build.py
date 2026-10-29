# Pages « offres » pour Uzi (Café Bistro Romain Gary). python3 build.py → index.html + terrain/ boker/ iskit/ happy-hour/
# Textes HE/FR/EN ici ; aucun prix inventé (« המחיר בתפריט »). Hébreu vérifié par dn-hebreu-verif sur chaque page générée.
from pathlib import Path
from urllib.parse import quote
import re
ICI = Path(__file__).parent
WA = 'https://wa.me/972546657655?text='
MENU = 'https://romaingarycafebistro.com/menu/menu-romain-gary.pdf'
SOIREES = 'https://codenolimits.github.io/romain-gary-rapport/soirees/'

def t(he, fr, en, tag='span'):
    he = re.sub(r'(\d\d:\d\d–\d\d:\d\d|\d\d:\d\d|\d+(?:\.\d+)?%|\d+(?:\.\d+)?–\d+(?:\.\d+)?)', r'<bdi dir="ltr">\1</bdi>', he)  # horaires lisibles en RTL
    return f'<{tag} class="he">{he}</{tag}><{tag} class="fr">{fr}</{tag}><{tag} class="en">{en}</{tag}>'

def wa(he, fr, en, label):
    """Bouton WhatsApp : un lien par langue, message pré-rempli dans la langue lue."""
    return ''.join(f'<a class="cta {l}" href="{WA}{quote(m)}">{lab}</a>' for l, m, lab in zip(('he', 'fr', 'en'), (he, fr, en), label))

HOURS = t('א׳–ה׳ 08:00–23:30 · ו׳ 08:00–13:00 · מוצ״ש: שעה אחרי צאת שבת',
          'dim.–jeu. 08:00–23:30 · ven. 08:00–13:00 · samedi soir : 1 h après la fin du Chabbat',
          'Sun–Thu 08:00–23:30 · Fri 08:00–13:00 · Sat night: one hour after Shabbat ends')
KOSHER = t('כשר למהדרין · חלבי · בהשגחת הרבנות', 'Casher mehadrin · laitier · sous la supervision du rabbinat',
           'Kosher mehadrin · dairy · under rabbinical supervision')
PAGES = [('boker', t('בוקר', 'Matin', 'Morning'), t('מ-08:00', 'dès 08:00', 'from 08:00')),
         ('iskit', t('עסקית', 'Midi', 'Business lunch'), t('12:00–14:00', '12:00–14:00', '12:00–14:00')),
         ('happy-hour', t('הפי האוור', 'Happy hour', 'Happy hour'), t('17:00–18:00', '17:00–18:00', '17:00–18:00'))]

def page(title, body, depth, sticky=''):
    up = '../' * depth
    return f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Frank+Ruhl+Libre:wght@300;500&family=Heebo:wght@300;400;600&display=swap">
<link rel="stylesheet" href="{up}style.css"></head>
<body class="l-he{' has-sticky' if sticky else ''}">
<div class="top"><a class="brand" href="{up or "./"}">ROMAIN GARY</a><span class="lang"><button data-l="he" class="on">עב</button><button data-l="fr">FR</button><button data-l="en">EN</button></span></div>
{body}
<footer><div class="mk">◆</div>
<p>{t('קפה ביסטרו רומן גארי · הלל 35, ירושלים', 'Café Bistro Romain Gary · 35 rue Hillel, Jérusalem', 'Café Bistro Romain Gary · 35 Hillel St, Jerusalem')}</p>
<p>{HOURS}</p><p>{KOSHER}</p>
<p class="ltr"><a href="tel:+972546657655">054-665-7655</a> · <a href="https://romaingarycafebistro.com">romaingarycafebistro.com</a> · <a href="https://www.instagram.com/romain.gary.cafe.bistro/">@romain.gary.cafe.bistro</a></p>
</footer>{sticky}
<script src="{up}lang.js"></script></body></html>
'''

def hero(img, k, h1, lead, depth):
    return f'<header class="hero"><img src="{"../" * depth}assets/{img}" alt=""><div class="in"><div class="k">{k}</div><h1>{h1}</h1><p class="lead">{lead}</p></div></header>'

def others(cur):
    cards = ''.join(f'<a class="mini" href="../{s}/"><b>{n}</b><span>{h}</span></a>' for s, n, h in PAGES if s != cur)
    cards += f'<a class="mini" href="{SOIREES}"><b>{t("ערבי המוזיקה", "Soirées musicales", "Music nights")}</b><span>{t("רשימת המתנה", "liste d’attente", "waitlist")}</span></a>'
    return f'<section><div class="k">{t("עוד ברומן גארי", "Aussi chez Romain Gary", "Also at Romain Gary")}</div><div class="minis">{cards}</div></section>'

def offre(slug, img, k, h1, lead, h2, items, price, code, note, msg, label, extra=''):
    li = ''.join(f'<li>{x}</li>' for x in items)
    cta = wa(*msg, label)
    body = hero(img, k, h1, lead, 1) + f'''
<section><div class="k">01</div><h2>{h2}</h2><ul class="list">{li}</ul>
<div class="price"><span>{price}</span><a href="{MENU}">{t('לתפריט המלא ←', 'Voir le menu →', 'See the menu →')}</a></div>{extra}</section>
<section><div class="k">02</div><h2>{t('שולחים הודעה ובאים', 'Un message, et on vous attend', 'Send a message, we’ll be ready')}</h2>
<div class="code"><small>{t('הקוד שלכם', 'Votre code', 'Your code')}</small><b>{code}</b><p>{note}</p></div>{cta}
<p class="hours">{HOURS}</p></section>
{others(slug)}'''
    sticky = f'<div class="sticky">{cta}</div>'
    (ICI / slug).mkdir(exist_ok=True)
    (ICI / slug / 'index.html').write_text(page(f'Romain Gary · {slug}', body, 1, sticky), encoding='utf-8')

CODE_NOTE = lambda c: t(f'אומרים את הקוד {c} בקופה או שולחים אותו בוואטסאפ.', f'Dites le code {c} à la caisse ou envoyez-le sur WhatsApp.',
                        f'Say the code {c} at the counter or send it on WhatsApp.')
PRIX = t('המחירים לפי התפריט', 'Prix au menu', 'Price on the menu')
LABEL = ('לשמור מקום בוואטסאפ', 'Réserver sur WhatsApp', 'Book on WhatsApp')

offre('boker', 'salon-900.webp', t('בוקר · מ-08:00', 'Matin · dès 08:00', 'Morning · from 08:00'),
      t('הבוקר מתחיל<br><em>בפריז.</em>', 'Le matin commence<br><em>à Paris.</em>', 'Mornings begin<br><em>in Paris.</em>'),
      t('קפה, מאפים צרפתיים וארוחת בוקר בביסטרו פריזאי בלב ירושלים, ברחוב הלל 35.',
        'Café, viennoiseries et petit-déjeuner dans un bistro parisien au cœur de Jérusalem, 35 rue Hillel.',
        'Coffee, French pastries and breakfast in a Parisian bistro in the heart of Jerusalem, 35 Hillel St.'),
      t('הטבת הבוקר', 'L’offre du matin', 'The morning offer'),
      [t('ארוחת בוקר צרפתית, קפה ומאפים מהפטיסרי שלנו', 'Petit-déjeuner à la française, café et viennoiseries de la pâtisserie', 'French breakfast, coffee and pastries from our pâtisserie'),
       t('פינה שקטה לפגישה, לעבודה על הלפטופ או לקריאה בין מדפי הספרים', 'Un coin calme pour un rendez-vous, travailler ou lire entre les rayons de livres', 'A quiet corner to meet, work or read among the bookshelves'),
       t('מציגים את הקוד BOKER ומקבלים את ההטבה', 'Montrez le code BOKER et profitez de l’offre du matin', 'Show the code BOKER and get the morning offer')],
      PRIX, 'BOKER', CODE_NOTE('BOKER'),
      ('שלום! ראיתי את הטבת הבוקר של רומן גארי. קוד: BOKER', 'Bonjour ! J’ai vu l’offre du matin de Romain Gary. Code : BOKER', 'Hello! I saw Romain Gary’s morning offer. Code: BOKER'), LABEL)

offre('iskit', 'salle-800.webp', t('עסקית · א׳–ה׳ 12:00–14:00', 'Midi · dim.–jeu. 12:00–14:00', 'Lunch · Sun–Thu 12:00–14:00'),
      t('הפסקת הצהריים,<br><em>בסגנון ביסטרו.</em>', 'La pause de midi,<br><em>version bistro.</em>', 'Your lunch break,<br><em>bistro style.</em>'),
      t('תפריט עסקית לעובדי האזור, בימים א׳–ה׳ בין 12:00 ל-14:00. אוכלים טוב וחוזרים למשרד בזמן.',
        'Un menu du midi pour ceux qui travaillent dans le quartier, du dimanche au jeudi de 12:00 à 14:00. On mange bien et on rentre au bureau à l’heure.',
        'A business lunch menu for people working nearby, Sunday to Thursday, 12:00–14:00. Eat well and be back at the office on time.'),
      t('העסקית של רומן גארי', 'Le menu du midi', 'The business lunch'),
      [t('תפריט עסקית מיוחד לעובדי המשרדים והעסקים במרכז העיר', 'Un menu spécial pour les bureaux et commerces du centre-ville', 'A special menu for offices and shops in the city centre'),
       t('מחיר עסקית משתלם', 'Un prix de midi avantageux, pensé pour le quartier', 'A lunch price made for the neighbourhood'),
       t('מגיעים לבד, עם הצוות או לפגישת עבודה', 'Seul, en équipe ou pour un déjeuner d’affaires', 'Come alone, with your team, or for a business meeting'),
       t('קבוצה מהמשרד? כותבים לנו כמה אתם, ואנחנו שומרים לכם שולחן', 'Un groupe du bureau ? Dites-nous combien vous êtes, on garde la table', 'Coming as a group? Tell us how many and we’ll hold a table')],
      PRIX, 'ISKIT', CODE_NOTE('ISKIT'),
      ('שלום! אשמח להזמין מקום לעסקית. קוד: ISKIT. מספר אנשים: ', 'Bonjour ! Je voudrais réserver pour le menu du midi. Code : ISKIT. Nombre de personnes : ',
       'Hello! I’d like to book the business lunch. Code: ISKIT. Number of people: '), LABEL)

offre('happy-hour', 'bar-800.webp', t('הפי האוור · א׳–ה׳ 17:00–18:00', 'Happy hour · dim.–jeu. 17:00–18:00', 'Happy hour · Sun–Thu 17:00–18:00'),
      t('השעה של<br><em>אחרי העבודה.</em>', 'L’heure<br><em>d’après le travail.</em>', 'The hour<br><em>after work.</em>'),
      t('בימים א׳–ה׳ בין 17:00 ל-18:00, בבר של הביסטרו ברחוב הלל 35.', 'Du dimanche au jeudi de 17:00 à 18:00, au bar du bistro, 35 rue Hillel.',
        'Sunday to Thursday, 17:00–18:00, at the bistro bar, 35 Hillel St.'),
      t('ההטבה', 'L’offre', 'The offer'),
      [t('כוס יין שנייה במתנה או 10% הנחה על שאר המשקאות', 'Le 2<sup>e</sup> verre de vin offert ou 10 % sur les autres boissons', 'Second glass of wine on the house, or 10% off other drinks'),
       t('גם קפה, משקאות קלים ומאפים', 'Aussi café, boissons sans alcool et pâtisseries', 'Coffee, soft drinks and pastries too')],
      PRIX, 'HAPPY', CODE_NOTE('HAPPY'),
      ('שלום! אשמח לבוא להפי האוור. קוד: HAPPY', 'Bonjour ! Je viens pour le happy hour. Code : HAPPY', 'Hello! I’m coming for happy hour. Code: HAPPY'),
      ('לשלוח הודעה בוואטסאפ', 'Écrire sur WhatsApp', 'Message us on WhatsApp'),
      extra=f'<p class="legal">{t("ההטבה מגיל 18 בלבד. צריכה מופרזת של אלכוהול מסכנת חיים.", "Offre réservée aux plus de 18 ans. L’abus d’alcool est dangereux pour la santé.", "Over 18 only. Please drink responsibly.")}</p>')

# --- Stratégie face-à-face (page pour Uzi) ---
def terrain():
    where = [t('חנויות ועסקים ברחובות הלל, בן יהודה וקינג ג׳ורג׳ ובשדרות ממילא', 'Commerces des rues Hillel, Ben Yehuda, King George et de l’avenue Mamilla', 'Shops on Hillel, Ben Yehuda and King George streets and Mamilla Avenue'),
             t('משרדים: עורכי דין, רואי חשבון, מרפאות, חברות', 'Bureaux : avocats, comptables, cabinets médicaux, entreprises', 'Offices: lawyers, accountants, clinics, companies'),
             t('בתי המלון באזור: דלפק הקבלה והקונסיירז׳', 'Hôtels du quartier : réception et concierge', 'Nearby hotels: front desk and concierge'),
             t('שיחות טלפון לקונסוליות, לשגרירויות ולמשרדים', 'Appels aux ambassades, consulats et bureaux', 'Phone calls to embassies, consulates and offices')]
    say = [(f'../boker/', t('ארוחת בוקר מ-08:00', 'Petit-déjeuner dès 08:00', 'Breakfast from 08:00'), 'BOKER'),
           (f'../iskit/', t('עסקית 12:00–14:00', 'Menu du midi 12:00–14:00', 'Business lunch 12:00–14:00'), 'ISKIT'),
           (f'../happy-hour/', t('הפי האוור 17:00–18:00', 'Happy hour 17:00–18:00', 'Happy hour 17:00–18:00'), 'HAPPY'),
           (SOIREES, t('ערב רגאיי ורשימת ההמתנה לערבי המוזיקה', 'Soirée reggae et liste d’attente des soirées musicales', 'Reggae night and the music nights waitlist'), '')]
    say_html = ''.join(f'<li><a href="{u}">{n}</a>{f" <span class=c>{c}</span>" if c else ""}</li>' for u, n, c in say)
    rows = [('A', t('3 שעות בשבוע', '3 h / semaine', '3 h / week'), '12', '70–120', '105–300', '3–15'),
            ('B', t('5 שעות בשבוע', '5 h / semaine', '5 h / week'), '20', '120–200', '180–500', '5–25')]
    tr = ''.join(f'<tr><td>{f}</td><td class="n">{h}</td><td class="n">{v}</td><td class="n">{p}</td><td class="n">{c}</td></tr>' for _, f, h, v, p, c in rows)
    body = hero('facade-900.webp', t('הצעה · עבודת שטח', 'Proposition · terrain', 'Proposal · on the ground'),
                t('פנים מול פנים,<br><em>עסק אחרי עסק.</em>', 'Face à face,<br><em>commerce après commerce.</em>', 'Face to face,<br><em>door after door.</em>'),
                t('הפרסום ברשתות מביא אנשים שעוד לא מכירים את המקום. עבודת השטח מביאה את השכנים: מי שעובד, גר או מתארח במרחק של כמה דקות הליכה מרחוב הלל.',
                  'La publicité en ligne amène des gens qui ne connaissent pas encore le lieu. Le terrain amène les voisins : ceux qui travaillent, vivent ou séjournent à quelques minutes à pied de la rue Hillel.',
                  'Online ads bring people who don’t know the place yet. Fieldwork brings the neighbours: people who work, live or stay a few minutes’ walk from Hillel Street.'), 1)
    body += f'''
<section><div class="k">01</div><h2>{t('איפה', 'Où', 'Where')}</h2><ul class="list">{''.join(f'<li>{x}</li>' for x in where)}</ul>
<p class="note">{t('עם פליירים וכרטיסי ביקור מעודכנים. את רשימת המקומות נכין יחד בכל שבוע.', 'Avec flyers et cartes de visite à jour. La liste des lieux se prépare ensemble chaque semaine.', 'With updated flyers and business cards. We prepare the list of places together every week.')}</p></section>
<section><div class="k">02</div><h2>{t('המסר', 'Le message', 'The message')}</h2><p>{t('שלוש הצעות פשוטות, דף לכל אחת, וקוד שמאפשר לספור כמה אנשים הגיעו:', 'Trois offres simples, une page pour chacune, et un code pour compter qui vient :', 'Three simple offers, one page each, and a code to count who comes:')}</p>
<ul class="list links">{say_html}</ul></section>
<section><div class="k">03</div><h2>{t('שתי חבילות', 'Deux formules', 'Two packages')}</h2>
<div class="packs"><div class="pack"><small>A</small><b>{t('3 שעות בשבוע', '3 h par semaine', '3 h per week')}</b><span>{t('12 שעות בחודש', '12 h par mois', '12 h per month')}</span><strong>{t('‏1,800 ₪ לחודש', '1 800 ₪ / mois', '₪1,800 / month')}</strong></div>
<div class="pack"><small>B</small><b>{t('5 שעות בשבוע', '5 h par semaine', '5 h per week')}</b><span>{t('20 שעות בחודש', '20 h par mois', '20 h per month')}</span><strong>{t('‏3,000 ₪ לחודש', '3 000 ₪ / mois', '₪3,000 / month')}</strong></div></div>
<p class="note">{t('התשלום: חצי ב-1/11 וחצי ב-15/11.', 'Paiement : moitié le 01/11, moitié le 15/11.', 'Payment: half on 1 Nov, half on 15 Nov.')}</p>
<p>{t('המחיר כולל גם: ייעוץ, כתיבת התכנים ופיתוח הפלטפורמה (אתר, רשימת המתנה, דפי ערבי המוזיקה). ניהול הקמפיינים בפייסבוק ובאינסטגרם (‏3,000 ₪ לחודש) ותקציב המודעות ב-Meta אינם כלולים ומשולמים בנפרד.',
     'Inclus en plus : conseil, rédaction des messages et développement de la plateforme (site, liste d’attente, pages des soirées). La gestion des campagnes Facebook et Instagram (3 000 ₪ / mois) et le budget publicitaire Meta ne sont pas inclus et se paient à part.',
     'Also included: advice, writing the messages and building the platform (website, waitlist, music night pages). Managing the Facebook and Instagram campaigns (₪3,000 / month) and the Meta ad budget are not included and are paid separately.')}</p></section>
<section><div class="k">04</div><h2>{t('הערכה זהירה, לא הבטחה', 'Estimation prudente, pas une promesse', 'A cautious estimate, not a promise')}</h2>
<div class="scroll"><table class="tbl"><tr><th>{t('חבילה', 'Formule', 'Package')}</th><th>{t('שעות בחודש', 'Heures / mois', 'Hours / month')}</th><th>{t('מקומות שאבקר בהם', 'Lieux visités', 'Places visited')}</th><th>{t('אנשים שאפגוש', 'Personnes touchées', 'People reached')}</th><th>{t('לקוחות חדשים', 'Nouveaux clients', 'New customers')}</th></tr>{tr}</table></div>
<p class="note">{t('ההנחות: 6 עד 10 מקומות בשעה; בממוצע 1.5 עד 2.5 אנשים בכל מקום; 3% עד 5% מהם הופכים ללקוחות במהלך החודש. נמדוד מהיציאה הראשונה ונעדכן את המספרים לפי מה שקורה בפועל.',
     'Hypothèses : 6 à 10 lieux par heure ; en moyenne 1,5 à 2,5 personnes par lieu ; 3 % à 5 % deviennent clients dans le mois. On mesure dès la première sortie et on corrige les chiffres selon le réel.',
     'Assumptions: 6–10 places per hour; on average 1.5–2.5 people per place; 3–5% become customers within the month. We measure from the first outing and adjust the numbers to what really happens.')}</p></section>
<section><div class="k">05</div><h2>{t('מעקב שבועי', 'Suivi chaque semaine', 'Weekly tracking')}</h2><ul class="steps">
<li>{t('בתחילת כל שבוע: רשימת מקומות שנכין יחד.', 'Avant la semaine : la liste des lieux, préparée ensemble.', 'Before the week: the list of places, prepared together.')}</li>
<li>{t('אחרי כל יציאה: דוח קצר – איפה הייתי, כמה אנשים פגשתי ואילו פרטי קשר אספתי.', 'Après chaque sortie : un compte rendu court. Où, combien de personnes, quels contacts.', 'After each outing: a short report. Where, how many people, which contacts.')}</li>
<li>{t('בנוסף לקוד של כל הצעה, הקוד FLYER יופיע על הפלייר: מי שמגיע אומר אותו בקופה או כותב אותו בוואטסאפ, וכך סופרים כמה אנשים באו בזכות עבודת השטח.', 'En plus du code de chaque offre, le code FLYER figure sur le flyer : on le dit à la caisse ou on l’écrit sur WhatsApp, et on compte ainsi les venues dues au terrain.', 'On top of each offer’s code, the code FLYER is on the flyer: customers say it at the counter or write it on WhatsApp, so we count who came thanks to fieldwork.')}</li>
<li>{t('בסוף החודש: סיכום המספרים והחלטה משותפת – להמשיך, להרחיב או לשנות.', 'En fin de mois : bilan face aux chiffres, et décision ensemble : continuer, augmenter ou changer.', 'End of month: review against the numbers, and we decide together to continue, grow or change.')}</li></ul></section>
{others("terrain")}'''
    (ICI / 'terrain').mkdir(exist_ok=True)
    (ICI / 'terrain' / 'index.html').write_text(page('Romain Gary · עבודת שטח', body, 1), encoding='utf-8')

def index():
    cards = [('terrain/', 'facade-900.webp', t('עבודת שטח', 'Terrain', 'Fieldwork'), t('ההצעה: 3 או 5 שעות בשבוע', 'La proposition : 3 ou 5 h par semaine', 'The proposal: 3 or 5 h a week')),
             ('boker/', 'salon-900.webp', t('בוקר', 'Matin', 'Morning'), t('ארוחת בוקר מ-08:00 · קוד BOKER', 'Petit-déjeuner dès 08:00 · code BOKER', 'Breakfast from 08:00 · code BOKER')),
             ('iskit/', 'salle-800.webp', t('עסקית', 'Midi', 'Business lunch'), t('א׳–ה׳ 12:00–14:00 · קוד ISKIT', 'dim.–jeu. 12:00–14:00 · code ISKIT', 'Sun–Thu 12:00–14:00 · code ISKIT')),
             ('happy-hour/', 'bar-800.webp', t('הפי האוור', 'Happy hour', 'Happy hour'), t('א׳–ה׳ 17:00–18:00 · קוד HAPPY', 'dim.–jeu. 17:00–18:00 · code HAPPY', 'Sun–Thu 17:00–18:00 · code HAPPY')),
             (SOIREES, 'hero-1280.webp', t('ערבי המוזיקה', 'Soirées musicales', 'Music nights'), t('ערב רגאיי ורשימת המתנה', 'Soirée reggae et liste d’attente', 'Reggae night and waitlist'))]
    c = ''.join(f'<a class="card" href="{u}"><img src="assets/{i}" alt="" loading="lazy"><div><b>{n}</b><span>{d}</span></div></a>' for u, i, n, d in cards)
    body = hero('hero-1280.webp', t('רומן גארי · ההצעות', 'Romain Gary · les offres', 'Romain Gary · the offers'),
                t('כל ההצעות,<br><em>במקום אחד.</em>', 'Toutes les offres,<br><em>au même endroit.</em>', 'Every offer,<br><em>in one place.</em>'),
                t('דף נפרד לכל הצעה, לשלוח ללקוחות ולשתף. כל דף זמין בעברית, בצרפתית ובאנגלית.', 'Une page par offre, à envoyer aux clients et à partager. Chaque page en hébreu, français et anglais.',
                  'One page per offer, to send to customers and share. Every page in Hebrew, French and English.'), 0)
    body += f'<section><div class="cards">{c}</div></section>'
    (ICI / 'index.html').write_text(page('Romain Gary · ההצעות', body, 0), encoding='utf-8')

terrain(); index()
for s in ('index.html', 'terrain/index.html', 'boker/index.html', 'iskit/index.html', 'happy-hour/index.html'):
    assert (ICI / s).stat().st_size > 2000, s
print('ok')
