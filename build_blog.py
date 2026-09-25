#!/usr/bin/env python3
"""Rebuilds the blog: category hubs, articles, blog index, home blog scroller, sitemap."""
import re, html, json, os, glob
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))
D = 'https://tanishurbania.com'
TODAY = '2026-09-25'
PHONE = '+917264011256'
OG = D + '/images/og-image.jpg'
e = html.escape

# ---------------------------------------------------------------- sources
S = {
 'nobroker': ('NoBroker: Charholi Budruk locality overview', 'https://www.nobroker.in/locality-iq/charholi-budruk-pune-liqlt'),
 'edustoke': ('Edustoke: schools in Charholi Budruk', 'https://www.edustoke.com/pune/schools-in-charholi-budruk'),
 'dwello': ('Dwello: hospitals near Charholi Road, Charholi Budruk', 'https://dwello.in/locations/charholi-road-charholi-budruk-pune-overview/hospitals'),
 'bridge': ('The Bridge Chronicle: new Charholi-Lohegaon road (29 Aug 2024)', 'https://www.thebridgechronicle.com/news/new-charholi-lohegaon-road-cuts-travel-time-to-pune-airport-to-minutes'),
 'wiki': ('Wikipedia: Ajeenkya DY Patil University', 'https://en.wikipedia.org/wiki/Ajeenkya_DY_Patil_University'),
 'kk': ('KK Care Hospital, Charholi', 'https://kkcarehospital.com/'),
}
NOTE = ('<div class="source-note"><strong>How to read this list.</strong> Names and distances come from the public sources linked below '
        '(checked September 2026). Distances are measured from the Charholi Budruk locality, not from the Tanish Urbania site, and can change. '
        'Please confirm exact distances, timings and services with our sales team or on the ground before you decide.</div>')

def sources(keys):
    return '<h2>Sources</h2><ul class="src">' + ''.join(f'<li><a href="{S[k][1]}" target="_blank" rel="noopener nofollow">{S[k][0]}</a></li>' for k in keys) + '</ul>'

# ---------------------------------------------------------------- categories
CATS = [
 ('overview', 'Pune & Charholi Overview', 'City and locality overview, landmarks and advantages',
  'Charholi in Pune',
  'Understand Charholi before you buy: where it sits in PCMC, the landmarks around it, and the everyday advantages of living here. These guides cover the city and locality overview for anyone considering a home near Ajinkya D.Y. Patil University.'),
 ('location-connectivity', 'Location & Connectivity', 'Roads, metro, rail and airport access',
  'Location and Connectivity',
  'How well is Charholi connected? These articles explain the main roads, the Charholi-Lohegaon link, the nearest metro and railway stations and the distance to Pune International Airport, with the source for every figure.'),
 ('investment', 'Investment', 'Prices, rents and how to assess value',
  'Property Investment in Charholi',
  'Thinking of Charholi as an investment? Read what listing portals report for prices and rents, and learn the questions to ask about resale and rental demand before you commit.'),
 ('nearby-schools', 'Nearby Schools & Colleges', 'Schools and universities around Charholi',
  'Schools and Colleges near Charholi',
  'A guide to the schools and higher-education institutions around Charholi, including the boards they follow, their approximate distances from Charholi Budruk and how to shortlist them.'),
 ('nearby-hospitals', 'Nearby Hospitals', 'Hospitals and healthcare around Charholi',
  'Hospitals near Charholi',
  'Which hospitals are close to Charholi? This category lists the multispeciality hospitals, maternity centres and rural hospitals reported around Charholi Budruk and Alandi Road.'),
 ('nearby-it-hubs', 'Nearby Employment & IT Hubs', 'Where residents work: industrial areas and IT parks',
  'Employment and IT Hubs near Charholi',
  'Where do Charholi residents work? These articles cover the industrial estates and business areas nearest to Charholi and how to check commute times to Pune’s larger IT clusters.'),
 ('nearby-malls', 'Nearby Malls & Shopping', 'Malls and shopping options within reach',
  'Malls and Shopping near Charholi',
  'From daily shopping to weekend outings: the malls and shopping destinations reported near Charholi, and how to plan a trip to each of them.'),
 ('buying-guides', 'Buying Guides', 'Practical guides for home buyers',
  'Home Buying Guides',
  'Practical guides for buying a flat in Pune: choosing between 2 BHK and 3 BHK, checking an upcoming project, and understanding how good design improves everyday living.'),
]
CAT = {c[0]: c for c in CATS}

CATX = {
 'overview': dict(more=['Charholi lies in the Pimpri-Chinchwad (PCMC) part of Pune, close to Ajeenkya D.Y. Patil University in Lohegaon. The area is served by D.Y. Patil University Road, Kaljewadi Road and the Pune-Alandi Road, and it is close to Alandi, Moshi and Bhosari.',
                    'Use this category to understand the locality before you look at individual projects. Each guide names its sources so you can check the facts for yourself.'],
    faq=[('Where is Charholi?', 'Charholi is in the Pimpri-Chinchwad (PCMC) area of Pune, near Ajeenkya D.Y. Patil University in Lohegaon.'),
         ('Which main roads serve Charholi?', 'D.Y. Patil University Road, Kaljewadi Road and the Pune-Alandi Road, according to a locality portal.'),
         ('Which project is planned here?', 'Tanish Urbania by Tanish Group: 2 BHK and 3 BHK Elite Homes near Ajeenkya D.Y. Patil University.')]),
 'location-connectivity': dict(more=['Connectivity covers more than distance. It includes the roads you use every day, the nearest metro and railway stations, and how quickly you can reach the airport. Public sources report a metro station about 12 km from Charholi Budruk and a new road link that a 2024 news report says shortens the trip to the airport.',
                    'Because infrastructure timelines change, every article here dates its sources and asks you to confirm the current status.'],
    faq=[('What is the nearest metro station?', 'Bhosari Metro Station on the Purple Line, about 12.3 km from Charholi Budruk according to NoBroker.'),
         ('How far is Pune Airport?', 'About 11 km by one portal. A news report from 29 August 2024 says it is six to seven kilometres via the Charholi-Lohegaon road. Check the current route before you rely on either number.'),
         ('Which railway stations are nearest?', 'Kasarwadi Railway Station (about 13 km) and Pune Railway Station (about 18 km), as reported by NoBroker.')]),
 'investment': dict(more=['Property investment depends on price, rent, resale demand and the quality of the project. Listing portals show a wide range of asking prices for Charholi Budruk because they mix older and newer buildings, so always compare like with like.',
                    'These guides share the reported numbers, the assumptions behind them and a checklist for evaluating a specific project. They are general information, not financial advice.'],
    faq=[('What is the price range in Charholi Budruk?', 'A locality portal reports asking prices of about Rs. 2,000 to Rs. 4,250 per sq ft across listings. New projects can differ from this range.'),
         ('What rents are reported?', 'About Rs. 8,000 a month for a 1 BHK, Rs. 18,000 for a 2 BHK and Rs. 25,000 for a 3 BHK, as listed by NoBroker.'),
         ('Are returns guaranteed?', 'No. Property values and rents can rise or fall. Check the RERA registration, the developer record and the total cost before you invest.')]),
 'nearby-schools': dict(more=['Families usually shortlist schools by board, fees and the daily commute. Around Charholi Budruk, public sources list schools following the State Board, CBSE and ICSE, including Crystal Modern School, Radcliffe School Pune, D Y Patil International School and SPG International School and Junior College.',
                    'For higher education, Ajeenkya D.Y. Patil University in Lohegaon is the nearest university named, founded in 2015 as part of the D.Y. Patil group.'],
    faq=[('Which boards are available near Charholi?', 'The listed schools include State Board, CBSE and ICSE options, according to Edustoke.'),
         ('Which school is closest?', 'Edustoke lists Crystal Modern School at about 1.6 km from Charholi Budruk. Distances are from the locality, not from Tanish Urbania.'),
         ('Is there a university nearby?', 'Yes. Ajeenkya D.Y. Patil University is located in Lohegaon, Pune, and was founded in 2015.')]),
 'nearby-hospitals': dict(more=['Hospitals near Charholi Budruk range from maternity and rural hospitals to multispeciality centres. Public sources list Siddhivinayak Maternity Hospital and Infertility Center near Charholi Road, Shri Sai Hospital and Rural Hospital in Alandi, and several others.',
                    'None of the sources give distances or bed counts, so this category focuses on what is listed and how to check facilities yourself.'],
    faq=[('Is there a maternity hospital near Charholi?', 'Siddhivinayak Maternity Hospital and Infertility Center is listed near Charholi Road, Charholi Budruk.'),
         ('Are there multispeciality hospitals?', 'KK Care Hospital describes itself as a multispeciality hospital in Charholi, and NoBroker lists Orchid Speciality Hospital, Medicover Hospitals and Shree Multispeciality Hospital for the locality.'),
         ('How far are the hospitals?', 'The sources do not state distances. Check the route and travel time on a maps app.')]),
 'nearby-it-hubs': dict(more=['Charholi’s nearest listed employment areas are industrial: Tingre Industrial Estate (about 7.3 km), Borate Park (about 9.3 km) and the MIDC Bhosari Industrial Area (about 9.5 km), according to NoBroker.',
                    'We could not verify distances to Pune’s larger IT parks, so we do not quote any. These guides show how to test your own commute instead.'],
    faq=[('What is the nearest employment hub?', 'Tingre Industrial Estate in Bhosari, about 7.3 km from Charholi Budruk according to NoBroker.'),
         ('Are IT parks nearby?', 'The source lists industrial and business areas rather than IT parks. Check commute times to your own office using a maps app.'),
         ('Is there a metro for commuting?', 'The nearest listed station is Bhosari Metro Station on the Purple Line, about 12.3 km away.')]),
 'nearby-malls': dict(more=['Charholi’s daily shopping is local, while larger malls are for weekends. NoBroker lists Phoenix Marketcity Pune, Aeromall and Spine City Mall for the Charholi Budruk area.',
                    'The source does not give distances, so this category explains how to plan trips and check travel times yourself.'],
    faq=[('Which malls are listed near Charholi?', 'Phoenix Marketcity Pune, Aeromall and Spine City Mall, according to NoBroker.'),
         ('How far are the malls?', 'The source lists names without distances. Check the current travel time on a maps app.'),
         ('What about daily shopping?', 'Local shops and markets serve everyday needs. Ask the sales team what retail is planned near the project.')]),
 'buying-guides': dict(more=['Buying a flat is a large decision. These guides cover how to pick a configuration, what to verify before you book in an upcoming project, and how design choices such as wing placement and balconies affect daily comfort.',
                    'Tanish Urbania offers 2 BHK homes of about 720 to 770 sq ft and 3 BHK homes of about 920 to 980 sq ft.'],
    faq=[('What sizes are available at Tanish Urbania?', '2 BHK of approximately 720 to 770 sq ft and 3 BHK of approximately 920 to 980 sq ft.'),
         ('When is the launch?', 'The launch is expected within about a month. Register your interest to be contacted first.'),
         ('What should I check before booking?', 'RERA registration, approved plans, the payment schedule, the possession date and the total cost.')]),
}

# ---------------------------------------------------------------- existing articles (extracted)
EXISTING = json.load(open('blog_data/existing.json'))
def extract(slug):
    x = EXISTING[slug]
    return dict(title=x['title'], desc=x['desc'], h1='', body=x['body'])

POSTS = []
def add(slug, cat, img, read, excerpt, h1=None, title=None, desc=None, body=None):
    POSTS.append(dict(slug=slug, cat=cat, img=img, read=read, excerpt=excerpt, h1=h1, title=title, desc=desc, body=body))

# --- new articles (facts limited to what the linked sources state) -------
add('charholi-locality-overview', 'overview', 'aerial-1.jpg', '4 min read',
    'Where Charholi sits in PCMC, what is around it and how the area is changing.',
    h1='Charholi, Pune: a locality overview for home buyers',
    title='Charholi Pune Locality Overview | Tanish Urbania',
    desc='A locality overview of Charholi in PCMC, Pune: where it is, the landmarks around it, main roads and what to check before buying a home here.',
    body=f'''<p>Charholi is a locality in the Pimpri-Chinchwad (PCMC) part of Pune. Two villages carry the name, Charholi Budruk and Charholi Khurd, and the area sits between the Pune-Nashik and Pune-Nagar highways. Tanish Urbania is planned in Charholi near Ajeenkya D.Y. Patil University.</p>
{NOTE}
<h2>Landmarks around Charholi</h2>
<ul>
<li><strong>Ajeenkya D.Y. Patil University.</strong> A private university founded in 2015, part of the D.Y. Patil group and located in Lohegaon, Pune.</li>
<li><strong>D.Y. Patil International School.</strong> An ICSE school listed at Charoli Bk, about 3.4 km from Charholi Budruk.</li>
<li><strong>Pune International Airport.</strong> Reported about 11 km away by one portal. A newer road link is said to shorten the trip (see our connectivity guide).</li>
<li><strong>Major roads.</strong> D.Y. Patil University Road, Kaljewadi Road and the Pune-Alandi Road.</li>
</ul>
<h2>What the area offers</h2>
<p>Schools, hospitals and shopping centres are spread across Charholi and the neighbouring areas of Alandi, Moshi and Bhosari. Our dedicated guides list them one by one, with the sources.</p>
<h2>What to check yourself</h2>
<p>Visit at different times of day, test the commute you would make daily, and ask for the current status of any infrastructure you are counting on.</p>
{sources(['nobroker','wiki','edustoke'])}''')

add('advantages-of-living-in-charholi', 'overview', 'elevation-2.jpg', '3 min read',
    'Seven everyday advantages to weigh when considering a home in Charholi.',
    h1='Advantages of living in Charholi, Pune',
    title='Advantages of Living in Charholi, Pune | Tanish Urbania',
    desc='Seven practical advantages of living in Charholi, PCMC: education nearby, road links, healthcare, shopping, jobs and housing choices. With sources.',
    body=f'''<p>Every neighbourhood has trade-offs. These are the advantages that the public sources point to for Charholi, and what each one means for daily life.</p>
{NOTE}
<h2>1. Education close by</h2><p>Ajeenkya D.Y. Patil University, D.Y. Patil International School and several other schools are within a few kilometres of Charholi Budruk.</p>
<h2>2. Road links in several directions</h2><p>The Pune-Alandi Road, D.Y. Patil University Road and Kaljewadi Road serve the area, and the Charholi-Lohegaon road links the Pune-Nashik and Pune-Nagar highways.</p>
<h2>3. Healthcare within reach</h2><p>Multispeciality, maternity and rural hospitals are reported around Charholi Budruk and Alandi Road.</p>
<h2>4. Shopping and leisure</h2><p>Malls such as Phoenix Marketcity Pune, Aeromall and Spine City Mall are listed for the area.</p>
<h2>5. Employment nearby</h2><p>Industrial areas around Bhosari are the closest employment hubs listed, about 7 to 10 km away.</p>
<h2>6. Choice of homes</h2><p>Listing portals show a wide spread of prices per square foot, so buyers can compare several projects and budgets.</p>
<h2>7. A growing area</h2><p>New roads and projects are changing the area. Growth also means construction and traffic, so visit before you decide.</p>
{sources(['nobroker','edustoke','dwello','bridge'])}''')

add('connectivity-from-charholi', 'location-connectivity', 'elevation-1.jpg', '4 min read',
    'Roads, metro, rail and airport: what public sources say about reaching and leaving Charholi.',
    h1='Connectivity from Charholi: roads, metro, rail and airport',
    title='Charholi Connectivity: Roads, Metro, Airport | Tanish Urbania',
    desc='How well is Charholi, Pune connected? Main roads, the Charholi-Lohegaon link to the airport, nearest metro and railway stations, with sources.',
    body=f'''<p>Connectivity is the first thing most buyers check. Here is what public sources report for Charholi Budruk.</p>
{NOTE}
<h2>Nearest metro, rail and airport</h2>
<ul>
<li><strong>Metro:</strong> Bhosari Metro Station (Purple Line), about 12.3 km.</li>
<li><strong>Railway:</strong> Kasarwadi Railway Station about 13 km; Pune Railway Station about 18 km.</li>
<li><strong>Airport:</strong> Pune International Airport, about 11 km by one portal.</li>
<li><strong>Bus stops:</strong> Tajne Mala Phata and Sankalp Garden.</li>
</ul>
<h2>The Charholi-Lohegaon road</h2>
<p>A news report from 29 August 2024 describes a 90-metre-wide road connecting the Pune-Nagar and Pune-Nashik highways, with about 90% complete at that time. The report says the airport is six to seven kilometres from Charholi via this road, compared with a 20 to 22 km detour through Dighi and Vishrantwadi that took more than an hour in traffic. The two sources measure the airport distance differently, so check the current route yourself.</p>
<h2>Main roads</h2>
<p>D.Y. Patil University Road, Kaljewadi Road and the Pune-Alandi Road.</p>
<h2>Before you rely on any of this</h2>
<p>Infrastructure timelines change. Ask for the current status of any road, metro extension or bus service that matters to your daily commute.</p>
{sources(['nobroker','bridge'])}''')

add('investing-in-charholi', 'investment', 'aerial-2.jpg', '4 min read',
    'What listing portals report for prices and rents in Charholi, and how to judge value.',
    h1='Investing in Charholi: prices, rents and what to check',
    title='Property Investment in Charholi, Pune | Tanish Urbania',
    desc='Reported price and rent ranges in Charholi Budruk, Pune, plus a checklist for judging resale and rental potential before you invest.',
    body=f'''<p>Charholi sits in a part of PCMC where roads, education and employment are all developing. This guide shares the price data that listing portals report and the checks that matter for an investor.</p>
{NOTE}
<h2>Reported price and rent ranges</h2>
<ul>
<li><strong>Buying:</strong> about Rs. 2,000 to Rs. 4,250 per sq ft across listings in Charholi Budruk.</li>
<li><strong>Renting (monthly):</strong> about Rs. 8,000 for a 1 BHK, Rs. 18,000 for a 2 BHK and Rs. 25,000 for a 3 BHK.</li>
</ul>
<p>These are asking prices from a listing portal, not registered sale values, and the range is wide because it mixes old and new projects. Compare like with like.</p>
<h2>Why demand may hold</h2>
<p>Education institutions, road links and nearby industrial areas can support both owner-occupier and rental demand. That is a reason to research, not a guarantee of returns.</p>
<h2>Investor checklist</h2>
<ul>
<li>Confirm the RERA registration and approved plans.</li>
<li>Compare the price per sq ft on carpet area, not super built-up area.</li>
<li>Ask about the developer's delivery record.</li>
<li>Estimate rent and vacancy honestly against your EMI.</li>
<li>Get the total cost: taxes, registration, maintenance deposit.</li>
</ul>
<p>Property values can fall as well as rise. This is general information, not financial advice.</p>
{sources(['nobroker'])}''')

add('schools-and-colleges-near-charholi', 'nearby-schools', 'courtyard.jpg', '4 min read',
    'Schools and universities reported around Charholi, with boards and approximate distances.',
    h1='Schools and colleges near Charholi, Pune',
    title='Schools & Colleges near Charholi, Pune | Tanish Urbania',
    desc='Schools and universities near Charholi Budruk, Pune: boards (CBSE, ICSE, State), approximate distances and Ajeenkya D.Y. Patil University, with sources.',
    body=f'''<p>For families, the school run decides a lot. These institutions are reported near Charholi Budruk.</p>
{NOTE}
<h2>Schools with reported distances</h2>
<ul>
<li><strong>Crystal Modern School</strong>: State Board, Pimpri Chinchwad, about 1.6 km.</li>
<li><strong>Radcliffe School Pune</strong>: CBSE, Sanjay Park, about 2.7 km.</li>
<li><strong>D Y Patil International School</strong>: ICSE, Charoli Bk, about 3.4 km.</li>
<li><strong>SPG International School and Junior College</strong>: CBSE, Bhosari, about 4.0 km.</li>
</ul>
<h2>Other institutions listed for the area</h2>
<p>Gayatri International School, Podar International School Pimpri and Kaveri International School are listed by another portal, along with the MIT Alandi Campus and Dr. D. Y. Patil Vidyapeeth, Pimpri. That portal gives no distances for them.</p>
<h2>Higher education</h2>
<p>Ajeenkya D.Y. Patil University, founded in 2015 and part of the D.Y. Patil group, is located in Lohegaon and is the nearest university named in this area.</p>
<h2>How to shortlist</h2>
<ul>
<li>Check the board, fee structure and admission dates directly with each school.</li>
<li>Drive the route at school hours.</li>
<li>Ask about school bus coverage for your address.</li>
</ul>
{sources(['edustoke','nobroker','wiki'])}''')

add('hospitals-near-charholi', 'nearby-hospitals', 'elevation-2.jpg', '3 min read',
    'Hospitals and maternity centres reported around Charholi Budruk and Alandi Road.',
    h1='Hospitals near Charholi, Pune',
    title='Hospitals near Charholi, Pune | Tanish Urbania',
    desc='Hospitals near Charholi Budruk and Alandi Road, Pune: multispeciality, maternity and rural hospitals listed by public sources, with tips for emergencies.',
    body=f'''<p>Good healthcare nearby is a basic need. These hospitals are reported around Charholi Budruk and Alandi Road.</p>
{NOTE}
<h2>Hospitals listed for the area</h2>
<ul>
<li><strong>Siddhivinayak Maternity Hospital and Infertility Center</strong>: near Charholi Road, Charholi Budruk.</li>
<li><strong>Shri Sai Hospital</strong>: Pune-Alandi Road, Dehu Phata, Alandi.</li>
<li><strong>Rural Hospital, Alandi</strong>: Alandi.</li>
<li><strong>KK Care Hospital</strong>: describes itself as a multispeciality hospital in Charholi.</li>
<li><strong>Rahane Hospital, Orchid Speciality Hospital, Medicover Hospitals and Shree Multispeciality Hospital</strong>: listed for the locality by another portal.</li>
</ul>
<p>The sources do not give distances or bed counts, so please check services, specialities and emergency facilities with each hospital.</p>
<h2>Planning for emergencies</h2>
<ul>
<li>Save the number of the nearest 24-hour emergency department.</li>
<li>Check which hospitals accept your health insurance.</li>
<li>Test the route at peak hours.</li>
</ul>
{sources(['dwello','nobroker','kk'])}''')

add('jobs-and-it-hubs-near-charholi', 'nearby-it-hubs', 'aerial-2.jpg', '3 min read',
    'The industrial and business areas nearest Charholi, and how to check IT park commutes.',
    h1='Jobs and IT hubs near Charholi, Pune',
    title='Jobs & IT Hubs near Charholi, Pune | Tanish Urbania',
    desc='Employment hubs near Charholi Budruk, Pune: Bhosari industrial areas and Borate Park with distances, plus how to check commutes to larger IT parks.',
    body=f'''<p>Where you work decides how you live. These are the employment hubs that a public source lists nearest to Charholi Budruk.</p>
{NOTE}
<h2>Nearest employment hubs</h2>
<ul>
<li><strong>Tingre Industrial Estate, Bhosari:</strong> about 7.3 km.</li>
<li><strong>Borate Park:</strong> about 9.3 km.</li>
<li><strong>MIDC Bhosari Industrial Area:</strong> about 9.5 km.</li>
</ul>
<h2>What about IT parks?</h2>
<p>The source lists industrial and business areas rather than IT parks, and we could not verify distances to Pune's larger IT clusters, so we have not listed any. If your office is in an IT park such as Hinjewadi or Kharadi, check the current drive time at your usual commute hours using a maps app before you choose.</p>
<h2>How to test your commute</h2>
<ul>
<li>Check the route at your real start and end times, on a weekday.</li>
<li>Look at the metro option: the nearest listed station is Bhosari, about 12.3 km away.</li>
<li>Ask colleagues who live nearby.</li>
</ul>
{sources(['nobroker'])}''')

add('malls-and-shopping-near-charholi', 'nearby-malls', 'courtyard.jpg', '3 min read',
    'The malls and shopping centres reported for Charholi, and how to plan trips to them.',
    h1='Malls and shopping near Charholi, Pune',
    title='Malls & Shopping near Charholi, Pune | Tanish Urbania',
    desc='Malls near Charholi, Pune: Phoenix Marketcity Pune, Aeromall and Spine City Mall listed for the area, with tips for planning shopping trips.',
    body=f'''<p>Everyday shopping is usually local, while malls are for weekends. These malls are listed for the Charholi Budruk area.</p>
{NOTE}
<h2>Malls listed for the area</h2>
<ul>
<li><strong>Phoenix Marketcity Pune</strong></li>
<li><strong>Aeromall</strong></li>
<li><strong>Spine City Mall</strong></li>
</ul>
<p>The source lists the names without distances, so we have not quoted any. Check the current travel time on a maps app.</p>
<h2>Planning a trip</h2>
<ul>
<li>Choose weekday evenings or early weekend mornings to avoid traffic.</li>
<li>Check opening hours and parking before you leave.</li>
<li>For groceries and daily needs, look for stores within walking distance of the project once it is built.</li>
</ul>
{sources(['nobroker'])}''')

H1FIX = {
 'why-charholi-pcmc': 'Why Charholi is on every Pune home buyer\u2019s radar',
 '2-bhk-vs-3-bhk': '2 BHK or 3 BHK: how to choose the right home',
 'buying-a-pre-launch-home-checklist': 'A checklist for buying a home before the launch',
 'light-and-ventilation-in-apartment-design': 'How planning for light and air improves daily life',
}
# --- existing articles ----------------------------------------------------
for slug, cat, img, read, excerpt in [
    ('why-charholi-pcmc', 'overview', 'aerial-2.jpg', '3 min read', 'A look at what makes Charholi, near Ajinkya D.Y. Patil University, a practical address in PCMC.'),
    ('2-bhk-vs-3-bhk', 'buying-guides', 'elevation-2.jpg', '3 min read', 'Space, budget and how your family may grow: a simple way to compare the two configurations.'),
    ('buying-a-pre-launch-home-checklist', 'buying-guides', 'elevation-1.jpg', '4 min read', 'Six things to verify before you book a home in an upcoming project.'),
    ('light-and-ventilation-in-apartment-design', 'buying-guides', 'courtyard.jpg', '3 min read', 'Why wing placement, balconies and open areas matter as much as the floor plan.')]:
    x = extract(slug)
    x['h1'] = H1FIX.get(slug, x['h1'])
    add(slug, cat, img, read, excerpt, h1=x['h1'], title=x['title'], desc=x['desc'], body=x['body'])

NEWSLUG = {
 'charholi-locality-overview': 'locality-overview',
 'why-charholi-pcmc': 'why-buy-in-charholi',
 'connectivity-from-charholi': 'roads-metro-rail-airport',
 'investing-in-charholi': 'property-prices-and-rents',
 'schools-and-colleges-near-charholi': 'schools-and-colleges',
 'hospitals-near-charholi': 'hospitals-and-healthcare',
 'jobs-and-it-hubs-near-charholi': 'jobs-and-employment-hubs',
 'malls-and-shopping-near-charholi': 'malls-and-shopping',
 'buying-a-pre-launch-home-checklist': 'pre-launch-home-buying-checklist',
}
for p in POSTS:
    p['slug'] = NEWSLUG.get(p['slug'], p['slug'])
def aurl(p): return f"/blog/{p['cat']}/{p['slug']}/"
BYSLUG = {p['slug']: p for p in POSTS}
# card titles for lists
for p in POSTS:
    p['card'] = p['h1']

# ---------------------------------------------------------------- templates
def ldjson(o):
    return '  <script type="application/ld+json">\n' + json.dumps(o, indent=2, ensure_ascii=False) + '\n  </script>\n'

def head(url, title, desc, pre, typ='website', extra='', ld=''):
    return f'''<!DOCTYPE html>
<html lang="en-IN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="author" content="Tanish Group">
  <meta name="theme-color" content="#14263d">
  <meta name="geo.region" content="IN-MH">
  <meta name="geo.placename" content="Charholi, Pune">
  <link rel="alternate" hreflang="en-IN" href="{url}">
  <link rel="alternate" hreflang="x-default" href="{url}">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta property="og:site_name" content="Tanish Urbania">
  <meta property="og:locale" content="en_IN">
  <meta property="og:type" content="{typ}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{OG}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{e(title)}">
{extra}  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(title)}">
  <meta name="twitter:description" content="{e(desc)}">
  <meta name="twitter:image" content="{OG}">
{ld}  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <a href="/" class="brand" aria-label="Tanish Urbania"><span class="brand-mark">Tanish</span><span class="brand-sub">Urbania</span></a>
      <button class="nav-toggle" id="navToggle" aria-label="Menu" aria-expanded="false" aria-controls="mainNav"><span></span><span></span><span></span></button>
      <nav class="main-nav" id="mainNav">
        <a href="/#overview">Overview</a>
        <a href="/#homes">Homes</a>
        <a href="/#gallery">Gallery</a>
        <a href="/#location">Location</a>
        <a href="/#faq">FAQ</a>
        <a href="/blog/">Blog</a>
        <a class="btn btn-small" href="/#contact">Enquire Now</a>
      </nav>
    </div>
  </header>
'''

def foot(pre):
    return f'''
  <footer class="site-footer">
    <div class="container">
      <p class="footer-brand">Tanish Group &mdash; <em>Going That Extra Mile</em></p>
      <p class="disclaimer">Tanish Urbania is an upcoming project. Details, specifications, areas and images are indicative and subject to change. Articles are general information compiled from public sources, not financial or legal advice; distances are approximate. Please confirm RERA registration details with the sales team before booking.</p>
      <p class="copy">&copy; <span id="year">2026</span> Tanish Group. All rights reserved.</p>
    </div>
  </footer>
  <script src="/config.js"></script>
  <script src="/index.js"></script>
  <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
'''

def wh(img, pre):
    w, h = Image.open('images/' + img).size
    return f'width="{w}" height="{h}" src="{pre}images/{img}"'

def card(p, pre, tocat):
    """pre = path prefix to site root; links: blog articles live in blog/."""
    href = aurl(p)
    return f'''<a class="post-card" href="{href}">
            <img {wh(p['img'], '' if pre == '' else '/')} alt="{e(p['card'])}" loading="lazy">
            <div class="post-meta"><span class="tag">{e(CAT[p['cat']][1])}</span><span>{p['read']}</span></div>
            <h3>{e(p['card'])}</h3>
            <p>{e(p['excerpt'])}</p>
            <span class="read-more">Read article &rarr;</span>
          </a>'''

def chips(pre, active=None):
    out = f'<a class="chip{" active" if active is None else ""}" href="/blog/">All</a>'
    for slug, name, *_ in CATS:
        out += f'<a class="chip{" active" if active == slug else ""}" href="/blog/{slug}/">{e(name)}</a>'
    return f'<nav class="chips" aria-label="Blog categories">{out}</nav>'

def bc(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

# ---------------------------------------------------------------- write articles
import shutil
for f in glob.glob('blog/*.html'):
    if not f.endswith('index.html'): os.remove(f)
shutil.rmtree('blog/category', ignore_errors=True)
for d_ in glob.glob('blog/*/'):
    if os.path.basename(d_.rstrip('/')) not in {c[0] for c in CATS} and os.path.basename(d_.rstrip('/')) != 'category':
        pass
for p in POSTS:
    url = D + aurl(p)
    cat = CAT[p['cat']]
    ld = ldjson({"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "headline": p['h1'], "description": p['desc'], "image": D + '/images/' + p['img'],
         "datePublished": TODAY, "dateModified": TODAY, "mainEntityOfPage": url, "inLanguage": "en-IN",
         "articleSection": cat[1],
         "author": {"@type": "Organization", "name": "Tanish Group", "url": D + "/"},
         "publisher": {"@type": "Organization", "name": "Tanish Group", "logo": {"@type": "ImageObject", "url": D + "/android-chrome-512x512.png"}}},
        bc([("Home", D + "/"), ("Blog", D + "/blog/"), (cat[1], f"{D}/blog/{cat[0]}/"), (p['h1'], url)])]})
    extra = f'  <meta property="article:published_time" content="{TODAY}">\n  <meta property="article:section" content="{e(cat[1])}">\n  <meta property="article:author" content="Tanish Group">\n'
    same = [q for q in POSTS if q['cat'] == p['cat'] and q is not p]
    rest = [q for q in POSTS if q['cat'] != p['cat'] and q is not p]
    related = (same + rest)[:2]
    rel = '\n          '.join(card(q, '../', True) for q in related)
    page = head(url, p['title'], p['desc'], '../', 'article', extra, ld) + f'''
  <main class="blog-main">
    <article class="article">
      <div class="container narrow">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/blog/">Blog</a> / <a href="/blog/{cat[0]}/">{e(cat[1])}</a></nav>
        <div class="post-meta"><a class="tag" href="/blog/{cat[0]}/">{e(cat[1])}</a><span>{p['read']}</span></div>
        <h1>{e(p['h1'])}</h1>
        <p class="byline">By <a href="/">Tanish Group</a> &middot; Published <time datetime="{TODAY}">25 September 2026</time> &middot; Updated <time datetime="{TODAY}">25 September 2026</time></p>
        <img class="article-img" fetchpriority="high" {wh(p['img'], '/')} alt="{e(p['h1'])}">
        <div class="article-body">{p['body']}</div>
        <div class="cta-box">
          <h3>Interested in Tanish Urbania?</h3>
          <p>2 BHK and 3 BHK Elite Homes in Charholi, PCMC. Register to get pricing and floor plans.</p>
          <a class="btn btn-primary" href="/#contact">Enquire Now</a>
        </div>
      </div>
      <div class="container related">
        <h2>Keep reading</h2>
        <div class="post-grid two">
          {rel}
        </div>
      </div>
    </article>
  </main>''' + foot('../')
    os.makedirs(f'blog/{p["cat"]}/{p["slug"]}', exist_ok=True)
    open(f'blog/{p["cat"]}/{p["slug"]}/index.html', 'w').write(page)

# ---------------------------------------------------------------- category pages
for slug, name, short, h1, intro in CATS:
    posts = [p for p in POSTS if p['cat'] == slug]
    url = f'{D}/blog/{slug}/'
    title = f'{h1} | Tanish Urbania Blog'
    ld = ldjson({"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": h1, "url": url, "description": intro, "inLanguage": "en-IN",
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": D + aurl(p), "name": p['h1']} for i, p in enumerate(posts)]}},
        bc([("Home", D + "/"), ("Blog", D + "/blog/"), (name, url)]),
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in CATX[slug]['faq']]}]})
    cards = '\n          '.join(card(p, '../../', True) for p in posts)
    page = head(url, title, intro[:158].rsplit(' ', 1)[0] + ('.' if not intro[:158].endswith('.') else ''), '../../', 'website', '', ld) + f'''
  <main class="blog-main">
    <section class="blog-hero"><div class="container">
      <nav class="crumbs light" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/blog/">Blog</a> / <span>{e(name)}</span></nav>
      <p class="section-label">Category</p>
      <h1>{e(h1)}</h1>
      <p class="lead">{e(intro)}</p>
    </div></section>
    <section class="section"><div class="container">
      {chips('../../', slug)}
      <div class="cat-intro">{''.join('<p>'+e(x)+'</p>' for x in CATX[slug]['more'])}</div>
      <h2 class="h-sm">Articles in this category</h2>
      <div class="post-grid">
          {cards}
      </div>
      <h2 class="h-sm faq-h">Quick answers</h2>
      <div class="faq-list cat-faq">{''.join('<details class="faq"><summary>'+e(q)+'</summary><p>'+e(a)+'</p></details>' for q,a in CATX[slug]['faq'])}</div>
      <div class="cta-box wide">
        <h3>See Tanish Urbania for yourself</h3>
        <p>2 &amp; 3 BHK Elite Homes at Charholi, PCMC, near Ajinkya D.Y. Patil University. Launching soon.</p>
        <a class="btn btn-primary" href="/#contact">Get Price &amp; Floor Plans</a>
      </div>
    </div></section>
  </main>''' + foot('../../')
    os.makedirs(f'blog/{slug}', exist_ok=True)
    open(f'blog/{slug}/index.html', 'w').write(page)

# ---------------------------------------------------------------- blog index
url = D + '/blog/'
t = 'Blog: Guides for Buying a Home in Charholi, Pune'
d = 'Guides for home buyers in Charholi, PCMC: locality overview, connectivity, investment, nearby schools, hospitals, IT hubs and malls, plus buying guides.'
ld = ldjson({"@context": "https://schema.org", "@graph": [
    {"@type": "CollectionPage", "name": t, "url": url, "description": d, "inLanguage": "en-IN",
     "mainEntity": {"@type": "ItemList", "itemListElement": [
         {"@type": "ListItem", "position": i + 1, "url": D + aurl(p), "name": p['h1']} for i, p in enumerate(POSTS)]}},
    bc([("Home", D + "/"), ("Blog", url)])]})
catcards = ''.join(f'''<a class="cat-card" href="/blog/{s}/"><h3>{e(n)}</h3><p>{e(sh)}</p><span class="count">{sum(1 for p in POSTS if p['cat']==s)} article{'' if sum(1 for p in POSTS if p['cat']==s)==1 else 's'}</span></a>''' for s, n, sh, *_ in CATS)
cards = '\n          '.join(card(p, '../', True) for p in POSTS)
page = head(url, t, d, '../', 'website', '', ld) + f'''
  <main class="blog-main">
    <section class="blog-hero"><div class="container">
      <p class="section-label">Blog</p>
      <h1>Guides and insights</h1>
      <p class="lead">Practical reading for anyone considering a home in Charholi, PCMC.</p>
    </div></section>
    <section class="section"><div class="container">
      <h2 class="h-sm">Browse by topic</h2>
      <div class="cat-grid">{catcards}</div>
    </div></section>
    <section class="section section-tint"><div class="container">
      <h2 class="h-sm">All articles</h2>
      {chips('../', None)}
      <div class="post-grid">
          {cards}
      </div>
    </div></section>
  </main>''' + foot('../')
open('blog/index.html', 'w').write(page)

# ---------------------------------------------------------------- home scroller
h = open('index.html').read()
m = re.search(r'(<div class="post-scroll"[^>]*>).*?(\n      </div>\n      <p class="center more">)', h, re.S)
home_posts = POSTS[:8]
cards = ''.join('\n          ' + card(p, '', False) for p in home_posts)
h = h[:m.start()] + m.group(1) + cards + m.group(2) + h[m.end():]
open('index.html', 'w').write(h)


# ---------------------------------------------------------------- home: neighbourhood links (internal linking)
h = open('index.html').read()
block = """<div class="hub-links">
            <p class="hub-title">Explore the neighbourhood</p>
            <ul>
              <li><a href="blog/location-connectivity/">Connectivity: roads, metro &amp; airport</a></li>
              <li><a href="blog/nearby-schools/">Nearby schools &amp; colleges</a></li>
              <li><a href="blog/nearby-hospitals/">Nearby hospitals</a></li>
              <li><a href="blog/nearby-it-hubs/">Employment &amp; IT hubs</a></li>
              <li><a href="blog/nearby-malls/">Nearby malls &amp; shopping</a></li>
              <li><a href="blog/investment/">Investment in Charholi</a></li>
              <li><a href="blog/overview/">Charholi locality overview</a></li>
            </ul>
          </div>"""
h = h.replace('blog/index.html', 'blog/')
h = re.sub(r'\s*<div class="hub-links">.*?</ul>\s*</div>', '', h, flags=re.S)
h = h.replace('View the area on Google Maps &rarr;</a></p>', 'View the area on Google Maps &rarr;</a></p>\n          ' + block, 1)
open('index.html', 'w').write(h)

# ---------------------------------------------------------------- WebP versions + <picture> (idempotent)
import glob
for jf in glob.glob('images/*.jpg'):
    wf = jf[:-4] + '.webp'
    if not os.path.exists(wf) or os.path.getmtime(wf) < os.path.getmtime(jf):
        Image.open(jf).convert('RGB').save(wf, 'WEBP', quality=80, method=6)
def picturize(path):
    s = open(path).read()
    if 'og-image' in path: return
    def rep(m):
        tag = m.group(0)
        src = re.search(r'src="((?:\.\./)*/?)images/([^"]+)\.jpg"', tag)
        if not src or 'og-image' in tag: return tag
        return f'<picture><source type="image/webp" srcset="{src.group(1)}images/{src.group(2)}.webp">{tag}</picture>'
    # skip imgs already inside <picture>
    s = re.sub(r'(?<!<picture>)(?<!\.webp">)<img [^>]*>', lambda m: rep(m) if 'src="' in m.group(0) else m.group(0), s)
    s = re.sub(r'<picture><source type="image/webp" srcset="([^"]+)"><picture><source type="image/webp" srcset="[^"]+">', r'<picture><source type="image/webp" srcset="\1">', s)
    # preload hero as webp
    s = s.replace('<link rel="preload" as="image" href="images/aerial-1.jpg" fetchpriority="high">', '<link rel="preload" as="image" href="images/aerial-1.webp" type="image/webp" fetchpriority="high">')
    open(path, 'w').write(s)
for pth in ['index.html', 'blog/index.html'] + glob.glob('blog/*/index.html') + glob.glob('blog/*/*/index.html'):
    picturize(pth)

# ---------------------------------------------------------------- sitemap
urls = [('/', '1.0', 'weekly'), ('/blog/', '0.8', 'weekly')] + \
       [(f'/blog/{c[0]}/', '0.7', 'weekly') for c in CATS] + \
       [(aurl(p), '0.6', 'monthly') for p in POSTS]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
for u, pr, cf in urls:
    sm += f'  <url>\n    <loc>{D}{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n'
    if u == '/':
        for im in ['aerial-1', 'elevation-2', 'courtyard']:
            sm += f'    <image:image><image:loc>{D}/images/{im}.jpg</image:loc></image:image>\n'
    sm += '  </url>\n'
sm += '</urlset>\n'
open('sitemap.xml', 'w').write(sm)
print(len(POSTS), 'articles,', len(CATS), 'categories,', len(urls), 'sitemap urls')
