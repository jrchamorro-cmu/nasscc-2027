#!/usr/bin/env python3
"""Builds the NASSCC 2027 site into ./docs from the content below.
Run: python3 build.py. Edit content here, never in docs/. No dependencies.

Photos: speaker portraits go in img/speakers/<slug>.jpg and organizer portraits in
img/organizers/<slug>.jpg (slug = last field of the entry below). A missing photo renders as
a plain grey box, so the page never breaks.
"""
import pathlib, shutil, html, datetime

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs"
IMG = ROOT / "img"
DOMAIN = "nasscc.com"

NAV = [("index.html", "Home"), ("about.html", "About"), ("program.html", "Program"),
       ("speakers.html", "Speakers"), ("abstracts.html", "Abstracts"),
       ("registration.html", "Registration"), ("pittsburgh.html", "Travel"),
       ("history.html", "History"), ("sponsors.html", "Sponsors"), ("contact.html", "Contact")]

THEMES = {
    "QM":   "New Frontiers in Quantum Materials",
    "NCS":  "Novel Properties of Noncentrosymmetric Materials",
    "Xtal": "Advances in Crystal Growth and Reaction Mechanisms",
    "NRG":  "Next-Generation Energy Conversion and Storage Materials",
    "ML":   "Machine Learning, Autonomous Synthesis, and Data-Driven Approaches for Materials Discovery and Optimization",
}

# Confirmed invited speakers. Source: Jen Aitken's sheet "NASSC Invited speaker list for google
# docs", column Accept Y/N, read 2026-09-23, plus the acceptance emails. Only firm acceptances
# are listed; tentative replies (Chan, Nazar) and silent invitees (Powderly) stay off until they
# confirm. Titles and departments are as entered in the sheet except where a speaker's own email
# signature says otherwise (Zaikina: Associate Professor, signature 2026-09-14). Each speaker is
# being asked to confirm their listing and send a photo.
# Fields: name, title, department (or empty), institution, theme code, website (or empty), slug.
SPEAKERS = [
    ("Gang Cao", "Professor", "Department of Physics", "University of Colorado Boulder", "QM",
     "https://www.colorado.edu/lab/cao/", "cao-gang"),
    ("Amitava Choudhury", "Associate Professor", "Department of Chemistry", "Missouri University of Science and Technology", "NRG",
     "https://sites.mst.edu/amitava/", "choudhury-amitava"),
    ("Andrew (AJ) Craig", "R&amp;D Crystal Growth Engineer", "", "Northrop Grumman", "Xtal",
     "", "craig-andrew"),
    ("James M. Hodges", "Assistant Professor", "Department of Chemistry", "Penn State University", "NRG",
     "https://www.hodgeschemistry.com/", "hodges-james"),
    ("Abishek K. Iyer", "Assistant Professor", "Department of Chemistry", "University of Manitoba", "NCS",
     "https://www.iyerlab.ca/home", "iyer-abishek"),
    ("Milena Jovanovic", "Assistant Professor", "Department of Chemistry", "North Carolina State University", "ML",
     "https://jovanovicgroup.wordpress.ncsu.edu", "jovanovic-milena"),
    ("Jason F. Khoury", "Assistant Professor", "School of Molecular Sciences", "Arizona State University", "QM",
     "https://search.asu.edu/profile/4849908", "khoury-jason"),
    ("Vladislav Klepov", "Assistant Professor", "Department of Chemistry", "University of Georgia", "QM",
     "https://klepovlab.org/research.html", "klepov-vladislav"),
    ("Kirill A. Kovnir", "Professor", "Department of Chemistry", "Iowa State University", "NRG",
     "https://group.chem.iastate.edu/Kovnir/index.html", "kovnir-kirill"),
    ("Xiaotong Li", "Assistant Professor", "Department of Chemistry", "North Carolina State University", "NRG",
     "https://www.lisolidstatelab.com/home", "li-xiaotong"),
    ("Paul A. Maggard", "Professor", "Department of Chemistry and Biochemistry", "Baylor University", "NRG",
     "https://sites.baylor.edu/paul_maggard/research-areas/", "maggard-paul"),
    ("Anton O. Oliynyk", "Assistant Professor", "Department of Chemistry", "Hunter College, City University of New York", "ML",
     "https://oliynyklab.github.io/", "oliynyk-anton"),
    ("Gordon G. C. Peterson", "Assistant Professor", "Department of Chemistry", "Haverford College", "ML",
     "https://sites.google.com/haverford.edu/petersonlab/home", "peterson-gordon"),
    ("Efrain E. Rodriguez", "Professor", "Department of Chemistry and Biochemistry", "University of Maryland", "NCS",
     "https://www.rodriguezgroupumd.com/", "rodriguez-efrain"),
    ("James Salvador", "Technical Fellow", "", "General Motors", "NRG",
     "", "salvador-james"),
    ("Ashley Schmidt", "Single Crystal XRD Applications Scientist", "", "Bruker AXS", "Xtal",
     "", "schmidt-ashley"),
    ("Taylor D. Sparks", "Professor", "Department of Materials Science and Engineering", "University of Utah", "ML",
     "", "sparks-taylor"),
    ("Daniel B. Straus", "Assistant Professor", "School of Science and Engineering", "Tulane University", "NCS",
     "https://straus.tulane.edu/", "straus-daniel"),
    ("Xianghan Xu", "Assistant Professor", "School of Physics and Astronomy", "University of Minnesota", "QM",
     "https://sites.google.com/umn.edu/xu-lab/", "xu-xianghan"),
    ("Jiaqiang Yan", "Senior Staff Scientist", "", "Oak Ridge National Laboratory", "Xtal",
     "https://www.ornl.gov/staff-profile/jiaqiang-yan", "yan-jiaqiang"),
    ("Julia V. Zaikina", "Associate Professor", "Department of Chemistry", "Iowa State University", "Xtal",
     "https://group.chem.iastate.edu/Zaikina/index.html", "zaikina-julia"),
    ("Xiuquan Zhou", "Assistant Professor", "Department of Chemistry", "Georgetown University", "Xtal",
     "https://xiuquanzhou.github.io/", "zhou-xiuquan"),
]

# Opening (keynote) talks on Sunday evening. Amy Prieto confirmed 2026-09-21 on Jen Aitken's
# thread. Linda Nazar has a tentative yes (2026-09-11) and is added when she confirms.
OPENING = [
    ("Amy L. Prieto", "Professor", "Department of Chemistry", "Colorado State University", None,
     "https://prietolab.colostate.edu/index.html", "prieto-amy"),
]

ORGANIZERS = [
    ("Jennifer A. Aitken", "Professor and conference chair", "Department of Chemistry and Biochemistry",
     "Duquesne University", None, "", "aitken-jennifer"),
    ("Xin Gui", "Assistant Professor", "Department of Chemistry", "University of Pittsburgh", None, "", "gui-xin"),
    ("Juan R. Chamorro", "Assistant Professor", "Department of Materials Science and Engineering",
     "Carnegie Mellon University", None, "", "chamorro-juan"),
]

# Every meeting in the series with a documented host. Organizers are listed only where a
# conference page, program, or award names them. Sources: Service/NASSCC-2027/Past-Conferences/.
HISTORY = [
    ("2027", "Duquesne University", "Pittsburgh, Pennsylvania", "July 25 to 28", "Jennifer Aitken, Xin Gui, Juan Chamorro"),
    ("2025", "Iowa State University", "Ames, Iowa", "July 28 to 31", "Julia Zaikina, Kirill Kovnir"),
    ("2023", "University of Calgary", "Calgary, Alberta", "August 2 to 4", "Michelle Dolgos, Simon Trudel, Venkataraman Thangadurai"),
    ("2021", "University of Southern California (online)", "", "July 28 to 30", "Brent Melot"),
    ("2019", "Colorado School of Mines", "Golden, Colorado", "July 31 to August 2", ""),
    ("2017", "University of California, Santa Barbara", "Santa Barbara, California", "August 16 to 19", "Ram Seshadri and the UCSB Materials Research Laboratory"),
    ("2015", "Florida State University", "Tallahassee, Florida", "May 22 to 24", "Michael Shatruk, Susan Latturner, Thomas Albrecht-Schmitt, Theo Siegrist"),
    ("2013", "Oregon State University", "Corvallis, Oregon", "June 23 to 26", "Mas Subramanian, Douglas Keszler"),
    ("2011", "McMaster University", "Hamilton, Ontario", "June", ""),
    ("2009", "The Ohio State University", "Columbus, Ohio", "June", "Patrick Woodward"),
    ("2007", "Texas A&amp;M University", "College Station, Texas", "May 17 to 19", "Timothy Hughbanks"),
    ("2005", "University of Notre Dame", "Notre Dame, Indiana", "May 26 to 28", "Slavi Sevov"),
]
LINEAGE = [
    ("2003", "Michigan State University", "East Lansing, Michigan", "May 29 to 31", "Mercouri Kanatzidis, S. D. Mahanti"),
    ("2001", "Colorado State University", "Fort Collins, Colorado", "June 20 to 24", "Peter Dorhout"),
    ("1991", "University of Kansas", "Lawrence, Kansas", "June 9 to 12", "Paul Gilles"),
]

CSS = r"""
body{margin:0;background:#fff;color:#222;font:16px/1.55 "Helvetica Neue",Helvetica,Arial,sans-serif}
*{box-sizing:border-box}
a{color:#1a4a8a}
a:hover{color:#0b2f5e}
img{max-width:100%;display:block}
.wrap{max-width:1200px;margin:0 auto;padding:0 24px}
h1,h2,h3{font-family:Georgia,"Iowan Old Style",Palatino,"Times New Roman",serif;font-weight:700;line-height:1.25}
h2{color:#1b2a4e;padding-bottom:4px;border-bottom:2px solid #d4a017;display:inline-block}
h3{color:#1b2a4e}
.topband{height:8px;background:#1b2a4e;border-bottom:3px solid #d4a017}
.masthead{padding:22px 0 0;border-bottom:1px solid #c8c8c8}
.masthead .row{display:flex;align-items:center;gap:22px}
.masthead .row>a{flex:none}
.masthead .titleblock{flex:1 1 auto;min-width:0}
.masthead .host img{width:215px;height:auto;margin-bottom:10px}
@media (max-width:900px){.masthead .host img{width:170px}}
@media (max-width:720px){.masthead .row{flex-wrap:wrap}.masthead .host{order:3;margin-left:0}.masthead .host img{width:150px}}
.masthead .mark{width:112px;height:112px;flex:none;margin-bottom:10px}
@media (max-width:600px){.masthead .mark{width:72px;height:72px}}
.masthead h1{font-size:clamp(24px,3.4vw,34px);margin:0 0 2px}
.masthead .sub{margin:0 0 12px}
.masthead h1 a{color:#1b2a4e;text-decoration:none}
.masthead .sub{margin:0 0 12px;font-size:17px;color:#444}
nav{font-size:16.5px;padding:10px 0 0;display:flex;justify-content:space-between;flex-wrap:wrap;gap:0 14px}
nav a{color:#1a4a8a;text-decoration:none;padding-bottom:9px;border-bottom:3px solid transparent;white-space:nowrap}
nav a.active{font-weight:700;color:#1b2a4e;border-bottom-color:#d4a017}
nav a:hover{color:#1b2a4e}
@media (max-width:720px){nav{justify-content:flex-start;gap:0 18px}nav a{padding-bottom:6px}}
main{padding:26px 0 50px;min-height:50vh}
h2{font-size:27px;margin:28px 0 10px}
h2:first-child{margin-top:0}
h3{font-size:20px;margin:22px 0 6px}
p{margin:0 0 12px;text-align:justify;hyphens:auto}
ul,ol{margin:0 0 12px;padding-left:26px}
li{margin:0 0 4px}
.small{font-size:14px;color:#555}
.sect{margin-top:30px}
.lead{}
.tba{color:#666;font-style:italic}
figure{margin:0 0 22px}
figure img{width:100%;height:auto}
figcaption{font-size:13px;color:#555;padding-top:6px}
.banner img{aspect-ratio:2/1.1;object-fit:cover;object-position:50% 0}
.cols{display:grid;grid-template-columns:1.15fr 1fr;gap:48px;align-items:start}
.cols h2{margin-top:0}
@media (max-width:720px){.cols{grid-template-columns:1fr;gap:12px}}
table{border-collapse:collapse;width:100%;margin:6px 0 16px;font-size:15.5px}
th,td{text-align:left;padding:7px 12px 7px 0;border-bottom:1px solid #ccc;vertical-align:top}
th{font-weight:700;border-bottom:2px solid #d4a017}
table.facts td:first-child{font-weight:700;width:120px;white-space:nowrap}
table.facts td{padding-top:9px;padding-bottom:9px;white-space:nowrap}
@media (max-width:720px){table.facts td{white-space:normal}}
.tscroll{overflow-x:auto}
/* people */
.pgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:26px 24px;margin:6px 0 10px}
@media (max-width:1000px){.pgrid{grid-template-columns:repeat(4,1fr)}}
@media (max-width:820px){.pgrid{grid-template-columns:repeat(3,1fr)}}
@media (max-width:600px){.pgrid{grid-template-columns:repeat(2,1fr);gap:20px 14px}}
.pcard{margin:0}
.portrait{width:100%;aspect-ratio:1/1;object-fit:cover;background:#e9e9e9}
.portrait.empty{background:#eee}
.pcard figcaption{padding-top:7px;font-size:14px;color:#444;line-height:1.4}
.pcard .nm{font-size:16px;font-weight:700;color:#222;display:block;margin-bottom:2px}
.pcard .site{display:inline-block;margin-top:3px;font-size:13.5px}
.orgs{display:grid;grid-template-columns:repeat(3,1fr);gap:26px 24px;max-width:720px}
@media (max-width:600px){.orgs{grid-template-columns:1fr 1fr;gap:20px 14px}}
.namelist{columns:2;column-gap:40px;padding-left:22px;font-size:15.5px;max-width:none}
.namelist.one{columns:1}
.namelist li{break-inside:avoid;max-width:none}
@media (max-width:600px){.namelist{columns:1}}
footer{border-top:4px solid #1b2a4e;padding:16px 0 40px;font-size:14px;color:#555}
footer p{margin:0 0 4px;max-width:none;text-align:left}
footer p.credit{margin-top:8px;font-size:13px;color:#777}
.slist{list-style:none;padding:0;margin:0 0 18px}
.slist li{padding:7px 0;border-bottom:1px solid #e2e2e2;margin:0}
.slist b{color:#1b2a4e}
.slist span{color:#555}
.tba,table p{text-align:left}
@media (max-width:600px){p{text-align:left;hyphens:manual}}
.themes-wrap{margin:14px 0 6px}
.orgrow{display:grid;grid-template-columns:repeat(3,1fr);gap:24px 60px;margin:6px 0 10px}
.org{display:flex;gap:18px;align-items:flex-start;font-size:14.5px;line-height:1.45;color:#444}
.org .portrait{width:120px;flex:none;aspect-ratio:4/5;object-fit:cover}
.org b{color:#1b2a4e;font-size:16px}
@media (max-width:900px){.orgrow{grid-template-columns:1fr}}
.themes-fig{width:100%;height:auto;display:block}
"""


MARK = """<svg class="mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="4" fill="#d4a017"/><path d="M6 32 C 12 24, 16 20, 20 20 C 24 20, 28 16, 34 8" fill="none" stroke="#111" stroke-width="3.2" stroke-linecap="round"/><path d="M6 8 C 12 16, 16 20, 20 20 C 24 20, 28 24, 34 32" fill="none" stroke="#111" stroke-width="3.2" stroke-linecap="round"/><circle cx="20" cy="20" r="3.2" fill="#111"/></svg>"""

FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">' + MARK.split(">",1)[1]
TBA = '<span class="tba">To be announced</span>'


def portrait(folder, slug, name):
    if (IMG / folder / f"{slug}.jpg").exists():
        return f'<img class="portrait" src="img/{folder}/{slug}.jpg" alt="{html.escape(name)}">'
    return '<div class="portrait empty" aria-hidden="true"></div>'


def person(entry, folder):
    name, title, dept, inst, theme, site, slug = entry
    lines = [f'<span class="nm">{name}</span>', title]
    if dept:
        lines.append(dept)
    lines.append(inst)
    cap = "<br>".join(lines)
    return f'<figure class="pcard">{portrait(folder, slug, name)}<figcaption>{cap}</figcaption></figure>'


def people_grid(entries, folder, cls="pgrid"):
    return f'<div class="{cls}">' + "".join(person(e, folder) for e in entries) + "</div>"


def page(file, title, body):
    credit = '<p class="credit">Photograph: downtown Pittsburgh from the Duquesne Incline, by Dllu, Wikimedia Commons, <a href="https://creativecommons.org/licenses/by-sa/4.0">CC BY-SA 4.0</a>.</p>' if file == "index.html" else ""
    nav = "\n".join(f'<a href="{f}"{" class=\"active\"" if f == file else ""}>{t}</a>' for f, t in NAV)
    year = datetime.date.today().year
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | NASSCC 2027</title>
<meta name="description" content="North American Solid State Chemistry Conference 2027, Duquesne University, Pittsburgh, July 25 to 28, 2027.">
<link rel="canonical" href="https://{DOMAIN}/{'' if file == 'index.html' else file}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="NASSCC 2027">
<meta property="og:title" content="{title} | NASSCC 2027">
<meta property="og:description" content="North American Solid State Chemistry Conference, Duquesne University, Pittsburgh, July 25 to 28, 2027.">
<meta property="og:image" content="https://{DOMAIN}/img/site/logo.png">
<link rel="icon" href="img/site/favicon.png" type="image/png">
<link rel="stylesheet" href="style.css">
<!-- Google tag (gtag.js), GA4 property NASSCC 2027 (nasscc.com), stream G-YR8GGGNSF3 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-YR8GGGNSF3"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-YR8GGGNSF3');
</script>
</head>
<body>
<div class="topband"></div>
<div class="masthead"><div class="wrap">
<div class="row"><a href="index.html"><img class="mark" src="img/site/logo.png" alt="NASSCC 2027"></a><div class="titleblock">
<h1><a href="index.html">North American Solid State Chemistry Conference 2027</a></h1>
<p class="sub">Duquesne University, Pittsburgh, Pennsylvania. Sunday, July 25 to Wednesday, July 28, 2027.</p>
</div><a class="host" href="https://www.duq.edu/"><img src="img/site/duquesne.svg" alt="Duquesne University"></a></div>
<nav>
{nav}
</nav>
</div></div>
<main><div class="wrap">
{body}
</div></main>
<footer><div class="wrap">
<p>NASSCC 2027 is hosted by Duquesne University and organized by faculty of Duquesne University, the University of Pittsburgh, and Carnegie Mellon University.</p>
<p>Registration and housing are handled by Duquesne University Conference and Event Services. Questions: <a href="contact.html">Contact</a>.</p>
{credit}
<p>&copy; {year} NASSCC 2027 Organizing Committee.</p>
</div></footer>
</body>
</html>
"""


PAGES = {}

# SHOW_PHOTOS = True switches the page back to the portrait grid once headshots are on disk.
SHOW_PHOTOS = False

def speaker_line(e):
    name, title, dept, inst, theme, site, slug = e
    parts = [title] + ([dept] if dept else []) + [inst]
    return f"<li><b>{name}</b>, <span>{', '.join(parts)}</span></li>"

def theme_lists():
    out = []
    for code, name in THEMES.items():
        group = [x for x in SPEAKERS if x[4] == code]
        if group:
            out.append(f'<h3>{name}</h3><ul class="slist">{"".join(speaker_line(e) for e in group)}</ul>')
    return "".join(out)


speaker_names = ", ".join(f"{n} ({i})" for n, t, d, i, k, w, s in SPEAKERS)

# ---------------------------------------------------------------- Home
PAGES["index.html"] = ("Home", f"""
<p>NASSCC is the biennial meeting of the North American solid state chemistry community, held in the years between the Gordon Research Conference on Solid State Chemistry.</p>
<p>The conference covers the synthesis, crystal growth, structure, bonding, and properties of extended inorganic and hybrid solids. It runs as a single session so that everyone can attend every talk, and it gives students, postdoctoral researchers, and early-career faculty a place on the program alongside established researchers. Contributed talks are chosen from submitted abstracts with priority for postdocs and senior graduate students, and every accepted abstract receives a poster slot.</p>
<p>The 2027 meeting is hosted by Duquesne University and organized jointly by faculty of Duquesne, the University of Pittsburgh, and Carnegie Mellon University. It is the first NASSCC in Pittsburgh.</p>

<figure class="banner"><img src="img/site/pittsburgh.jpg" alt="Downtown Pittsburgh from the Duquesne Incline, with the Monongahela and Allegheny rivers meeting at the Point"></figure>

<div class="cols">
<div>
<h2>Invited speakers</h2>
<p>Confirmed to date. Invitations are still out, and the <a href="speakers.html">speakers page</a> is updated as replies arrive.</p>
<ul class="namelist one">
{"".join(f"<li>{n}, {i}</li>" for n, t, d, i, k, w, s in SPEAKERS)}
</ul>
<p>Opening talk: {", ".join(f"{n} ({i})" for n, t, d, i, k, w, s in OPENING)}.</p>
</div>
<div>
<table class="facts">
<tr><td>Dates</td><td>July 25 to 28, 2027</td></tr>
<tr><td>Venue</td><td>Duquesne University, Pittsburgh</td></tr>
<tr><td>Program</td><td>Workshops and opening talks, Sunday<br>Talks, Monday to Wednesday<br>Posters, Monday and Tuesday evenings<br>Conference dinner, Wednesday</td></tr>
<tr><td>Organizers</td><td>Jennifer Aitken, Duquesne University<br>Xin Gui, University of Pittsburgh<br>Juan Chamorro, Carnegie Mellon University</td></tr>
<tr><td>Abstracts</td><td>{TBA}</td></tr>
<tr><td>Registration</td><td>{TBA}</td></tr>
</table>
</div>
</div>
""")

# ---------------------------------------------------------------- About
def org_row():
    out = ['<div class="orgrow">']
    for name, title, dept, inst, theme, site, slug in ORGANIZERS:
        out.append(f'<div class="org">{portrait("organizers", slug, name)}<div><b>{name}</b><br>{title}<br>{dept}<br>{inst}</div></div>')
    out.append('</div>')
    return "".join(out)

THEME_LINES = [
    ["New Frontiers in", "Quantum Materials"],
    ["Novel Properties of", "Noncentrosymmetric", "Materials"],
    ["Advances in Crystal", "Growth and Reaction", "Mechanisms"],
    ["Next-Generation Energy", "Conversion and", "Storage Materials"],
    ["Machine Learning,", "Autonomous Synthesis,", "and Data-Driven", "Approaches for Materials", "Discovery and", "Optimization"],
]

# Soft fills in the site's navy and gold family, one per theme, with a darker edge of the same hue.
THEME_COLORS = [
    ("#e6ebf4", "#1b2a4e"),   # pale navy
    ("#f7eed6", "#a67c1a"),   # pale gold
    ("#e9e6f2", "#4b4a7a"),   # pale violet, from the crystals in the logo
    ("#e4eff0", "#2f6b73"),   # pale teal
    ("#f4e7e4", "#8c3a34"),   # pale brick, from the incline car
]

def themes_figure():
    W, n, gap = 1000, 5, 18
    bw = (W - gap * (n - 1)) / n
    bh = 150
    out = [f'<svg class="themes-fig" viewBox="0 0 {W} {bh + 4}" role="img" aria-label="The five session themes of NASSCC 2027">']
    out.append('<style>.tf-t{font:14.5px "Helvetica Neue",Helvetica,Arial,sans-serif;fill:#222}.tf-n{font:bold 13px "Helvetica Neue",Helvetica,Arial,sans-serif}</style>')
    for i, lines in enumerate(THEME_LINES):
        x = i * (bw + gap) + 1
        cx = x + bw / 2
        fill, edge = THEME_COLORS[i]
        out.append(f'<rect x="{x}" y="2" width="{bw-2}" height="{bh}" fill="{fill}" stroke="{edge}" stroke-width="1.5"/>')
        out.append(f'<text class="tf-n" x="{x+10}" y="20" fill="{edge}">{i+1}</text>')
        y0 = 2 + bh / 2 - (len(lines) - 1) * 9.5 + 5
        for j, ln in enumerate(lines):
            out.append(f'<text class="tf-t" x="{cx}" y="{y0 + j*19}" text-anchor="middle">{ln}</text>')
    out.append('</svg>')
    return "".join(out)

PAGES["about.html"] = ("About", f"""
<h2>About NASSCC</h2>
<p class="lead">The North American Solid State Chemistry Conference is a biennial meeting for the solid state chemistry community of the United States, Canada, and Mexico. It alternates with the Gordon Research Conference on Solid State Chemistry, so the community meets every summer.</p>
<p>The conference covers solid state chemistry broadly: synthesis, crystal growth, structure determination, bonding, and the physical properties of inorganic and hybrid extended solids. It keeps the informal, single-session style of a Gordon conference while giving students, postdoctoral researchers, and early-career faculty a place on the program. Attendance has grown to about two hundred, and students usually make up more than half of it.</p>

<div class="sect">
<h2>Session themes</h2>
<p>Talks are grouped under five themes. Abstracts are submitted to one of them.</p>
<figure class="themes-wrap">{themes_figure()}</figure>
</div>

<div class="sect">
<h2>The 2027 meeting</h2>
<p>NASSCC 2027 is hosted by Duquesne University and organized jointly by faculty of Duquesne, the University of Pittsburgh, and Carnegie Mellon University. It runs from Sunday July 25 through Wednesday July 28, 2027, on the Duquesne campus on the Bluff above downtown Pittsburgh.</p>
<ul>
<li>Sunday: hands-on workshops, an industry careers panel, an opening reception, and the opening talks.</li>
<li>Monday through Wednesday: invited talks of 30 minutes and contributed talks of 15 to 20 minutes, in a single session organized by five themes.</li>
<li>Poster sessions on Monday and Tuesday evenings, and a closing dinner with poster awards on Wednesday.</li>
</ul>
<p>Invited speakers are chosen to balance established and early-career researchers, with at least three per theme. Contributed talks go to the strongest postdoc and senior graduate student abstracts. See the <a href="program.html">program</a> and the <a href="speakers.html">speakers</a>.</p>
</div>

<div class="sect">
<h2>Organizing committee</h2>
{org_row()}
</div>

<div class="sect">
<h2>Student volunteers</h2>
<p>{TBA}</p>
</div>
""")

# ---------------------------------------------------------------- Program
PAGES["program.html"] = ("Program", f"""
<h2>Program</h2>
<p class="lead">An opening Sunday of workshops, an industry panel, a reception, and the opening talks, then three full days of invited and contributed talks with posters on two evenings and a closing dinner. The detailed schedule is posted once the invited program is complete.</p>

<div class="sect">
<h3>Sunday, July 25</h3>
<table>
<tr><th>Time</th><th>Session</th></tr>
<tr><td>Afternoon</td><td>Workshop on neutron scattering and high-pressure methods, planned with Oak Ridge National Laboratory</td></tr>
<tr><td>Late afternoon</td><td>Industry panel: careers and collaboration in solid state chemistry</td></tr>
<tr><td>Evening</td><td>Opening reception and opening talks</td></tr>
</table>

<h3>Monday, July 26 to Wednesday, July 28</h3>
<p>Each day carries invited talks of 30 minutes and contributed talks of 15 to 20 minutes, grouped by the five session themes. Poster sessions run Monday and Tuesday evenings. The conference dinner and poster awards close the meeting on Wednesday evening.</p>
<table>
<tr><th>Day</th><th>Daytime</th><th>Evening</th></tr>
<tr><td>Monday, July 26</td><td>Talks</td><td>Poster session I</td></tr>
<tr><td>Tuesday, July 27</td><td>Talks</td><td>Poster session II</td></tr>
<tr><td>Wednesday, July 28</td><td>Talks</td><td>Conference dinner and poster awards</td></tr>
</table>
</div>

<div class="sect">
<h2>Contributed talks and posters</h2>
<p>Contributed talks are selected from submitted abstracts, with priority for postdoctoral researchers and senior graduate students. All other accepted abstracts are presented as posters. See <a href="abstracts.html">Abstracts</a> for the submission process.</p>
</div>
""")

# ---------------------------------------------------------------- Speakers
def theme_blocks():
    out = []
    for code, name in THEMES.items():
        group = [s for s in SPEAKERS if s[4] == code]
        if group:
            out.append(f'<div class="sect"><h3 style="margin-top:0">{name}</h3>{people_grid(group, "speakers")}</div>')
    return "".join(out)

if SHOW_PHOTOS:
    PAGES["speakers.html"] = ("Speakers", f"""
<h2>Invited speakers</h2>
<p>Confirmed invited speakers, listed by session theme. Invitations are still out, and this page is updated as replies arrive.</p>
<div class="sect">
<h3 style="margin-top:0">Opening talks, Sunday evening</h3>
{people_grid(OPENING, "speakers")}
</div>
{theme_blocks()}
<div class="sect">
<h2>Workshops and panel</h2>
<p>{TBA}</p>
</div>
""")
else:
    PAGES["speakers.html"] = ("Speakers", f"""
<h2>Invited speakers</h2>
<p>Confirmed invited speakers, listed by session theme. Invitations are still out, and this page is updated as replies arrive.</p>
<h3>Opening talks, Sunday evening</h3>
<ul class="slist">{"".join(speaker_line(e) for e in OPENING)}</ul>
{theme_lists()}
<h2>Workshops and panel</h2>
<p>{TBA}</p>
""")

# ---------------------------------------------------------------- Abstracts
PAGES["abstracts.html"] = ("Abstracts", f"""
<h2>Abstract submission</h2>
<p class="lead">Abstracts are invited for contributed talks and posters across the five session themes.</p>
<table>
<tr><th>Milestone</th><th>Date</th></tr>
<tr><td>Submission opens</td><td>{TBA}</td></tr>
<tr><td>Submission deadline</td><td>{TBA}</td></tr>
<tr><td>Notification of acceptance</td><td>{TBA}</td></tr>
</table>
<h3>Guidelines</h3>
<p>Submission instructions, the abstract template, and the length limit will be posted when submission opens. Presenters indicate a preference for a contributed talk or a poster at submission; the organizers select contributed talks from the pool with priority for postdoctoral researchers and senior graduate students.</p>
<h3>Attendance</h3>
<p>Attendance is capped by the venue. If registrations reach the cap, abstracts received after that point are placed on a waiting list in order of submission.</p>
""")

# ---------------------------------------------------------------- Registration
PAGES["registration.html"] = ("Registration", f"""
<h2>Registration and housing</h2>
<p class="lead">Registration, on-campus housing, and payment are handled through Duquesne University Conference and Event Services. Links will appear here when registration opens.</p>
<h3>Registration</h3>
<table>
<tr><th>Category</th><th>Early</th><th>Regular</th></tr>
<tr><td>Faculty, national laboratory, industry</td><td>{TBA}</td><td>{TBA}</td></tr>
<tr><td>Student and postdoc</td><td>{TBA}</td><td>{TBA}</td></tr>
<tr><td>Accompanying person</td><td>{TBA}</td><td>{TBA}</td></tr>
</table>
<p>Registration includes the reception, lunches, coffee breaks, poster sessions, and the conference dinner.</p>
<h3>Housing</h3>
<p>On-campus housing at Duquesne will be offered at a per-night rate for the nights of July 24 through July 28. Hotel options near campus are listed under <a href="pittsburgh.html">Travel</a>.</p>
""")

# ---------------------------------------------------------------- Travel and Pittsburgh
# Local recommendations, requested by Xin Gui. Long-standing landmarks and neighborhoods only;
# the organizers' personal picks go in the last block when they send them. Nothing here has been
# re-verified for 2027 hours, prices, or closures.
PAGES["pittsburgh.html"] = ("Travel and Pittsburgh", f"""
<h2>Travel and Pittsburgh</h2>
<p class="lead">Duquesne University sits on the Bluff above the Monongahela River, a ten-minute walk from downtown Pittsburgh and its Cultural District.</p>

<div class="sect">
<h3 style="margin-top:0">Getting here</h3>
<table>
<tr><th>By</th><th>Details</th></tr>
<tr><td>Air</td><td>Pittsburgh International Airport (PIT) is about 20 miles west of campus, 30 to 40 minutes by car or rideshare. The 28X Airport Flyer bus runs from the terminal to downtown and Oakland.</td></tr>
<tr><td>Train</td><td>Amtrak serves Pittsburgh Union Station downtown, on the Pennsylvanian (New York, Philadelphia, Harrisburg) and Capitol Limited (Washington, Chicago) routes.</td></tr>
<tr><td>Car</td><td>Campus is at 600 Forbes Avenue, Pittsburgh, PA 15282, just off the Boulevard of the Allies and I-376. Parking information will be posted with the final program.</td></tr>
</table>
<h3>Venue</h3>
<p>Session rooms, the poster hall, and on-campus housing are all on the Duquesne campus. Building details will be posted with the final program.</p>
<h3>Hotels</h3>
<p>{TBA}</p>
</div>

<div class="sect">
<h2>Exploring Pittsburgh</h2>
<p>Pittsburgh is a compact city of rivers, bridges, hillside neighborhoods, and museums, and most of what follows is within a short walk, bus ride, or rideshare of campus. Late July is warm, with long evenings. The city's visitor site is <a href="https://www.visitpittsburgh.com/">visitpittsburgh.com</a>.</p>
<div class="cols">
<div>
<h3>Rivers and views</h3>
<ul>
<li><a href="https://www.duquesneincline.org/">Duquesne Incline</a> and Monongahela Incline: cable cars up Mount Washington for the classic view of the Point and the skyline, best at sunset.</li>
<li><a href="https://www.pa.gov/agencies/dcnr/recreation/where-to-go/state-parks/find-a-park/point-state-park">Point State Park</a>, where the Allegheny and Monongahela meet to form the Ohio.</li>
<li><a href="https://friendsoftheriverfront.org/">Three Rivers Heritage Trail</a>: riverside walking and cycling along the North Shore and South Side.</li>
<li>Kayak rentals on the North Shore and bike share stations across the city.</li>
</ul>
<h3>Museums</h3>
<ul>
<li><a href="https://www.warhol.org/">The Andy Warhol Museum</a>, on the North Shore.</li>
<li>Carnegie Museums of <a href="https://carnegiemnh.org/">Natural History</a> and Art in Oakland, with the dinosaur halls and the Hall of Minerals and Gems.</li>
<li><a href="https://mattress.org/">Mattress Factory</a>: installation art in the Mexican War Streets.</li>
<li><a href="https://www.phipps.conservatory.org/">Phipps Conservatory</a>: Victorian glasshouse and gardens at the edge of Schenley Park.</li>
<li><a href="https://www.heinzhistorycenter.org/">Heinz History Center</a>, <a href="https://www.thefrickpittsburgh.org/">The Frick Pittsburgh</a>, <a href="https://www.aviary.org/">National Aviary</a>, <a href="https://carnegiesciencecenter.org/">Carnegie Science Center</a>.</li>
</ul>
<h3>Neighborhoods</h3>
<ul>
<li>Strip District: produce markets, Italian groceries, coffee roasters, and <a href="https://wholey.com/">Wholey's</a> fish market, walking distance from campus.</li>
<li>Oakland: the university district, with the Cathedral of Learning and its <a href="https://www.nationalityrooms.pitt.edu/">Nationality Rooms</a>, Schenley Plaza, and the Carnegie Mellon campus.</li>
<li>Lawrenceville: restaurants, bars, and shops along Butler Street.</li>
<li>South Side and Mount Washington: East Carson Street below, Grandview Avenue overlooks above.</li>
<li>Squirrel Hill, Shadyside, and Bloomfield (Pittsburgh's Little Italy): residential streets with good dinner options.</li>
</ul>
</div>
<div>
<h3>Food and evenings</h3>
<ul>
<li><a href="https://primantibros.com/">Primanti Brothers</a>: the Pittsburgh sandwich, with the fries and slaw inside. The original is in the Strip District.</li>
<li>Pierogies: <a href="https://pierogiesplus.com/">Pierogies Plus</a> in McKees Rocks, made in an old gas station; <a href="https://www.sdpolishdeli.com/">S&amp;D Polish Deli</a> in the Strip; and <a href="https://aptekapgh.com/">Apteka</a> in Bloomfield for a modern Eastern European take.</li>
<li><a href="https://www.hofbrauhauspittsburgh.com/">Hofbräuhaus Pittsburgh</a> on the South Side, a beer hall with a riverside biergarten, and <a href="https://www.pennbrew.com/">Penn Brewery</a> on the North Side, the city's oldest brewery, in the old Eberhardt and Ober brewery in Deutschtown.</li>
<li><a href="https://churchbrew.com/">Church Brew Works</a> in Lawrenceville: a brewery and restaurant in a former Catholic church, brew tanks on the altar.</li>
<li><a href="https://www.grandconcourserestaurant.com/">Grand Concourse</a> at Station Square: seafood in the restored Pittsburgh and Lake Erie Railroad station, across the river from campus.</li>
<li><a href="https://pamelasdiner.com/">Pamela's Diner</a> for crepe-style hotcakes at breakfast, and <a href="https://klavons.com/">Klavon's</a>, a 1920s ice cream parlor in the Strip.</li>
<li>Downtown Cultural District: theaters and galleries a short walk from campus (<a href="https://www.trustarts.org/">Pittsburgh Cultural Trust</a>), with <a href="https://www.marketsquarepgh.com/">Market Square</a> in the middle.</li>
<li><a href="https://www.mlb.com/pirates/ballpark">PNC Park</a>: the Pirates' riverside ballpark. Check the schedule for home games during the conference week.</li>
<li><a href="https://www.kennywood.com/">Kennywood</a>: a century-old amusement park with wooden roller coasters, a short drive east.</li>
</ul>
</div>
</div>
</div>
""")

# ---------------------------------------------------------------- History
def history_table(rows):
    body = "".join(f"<tr><td>{y}</td><td>{h}</td><td>{c}</td><td>{d}</td><td>{o}</td></tr>" for y, h, c, d, o in rows)
    return f'<div class="tscroll"><table><tr><th>Year</th><th>Host</th><th>City</th><th>Dates</th><th>Organizers</th></tr>{body}</table></div>'

PAGES["history.html"] = ("History", f"""
<h2>History of the meeting</h2>
<p class="lead">NASSCC has met every two years since 2005, moving between universities across the continent. Its roots go back further, to a Midwestern high-temperature chemistry conference that added "solid state chemistry" to its name in 1991.</p>
<p>The meeting began as the Midwest High Temperature and Solid State Chemistry Conference, a regional gathering of high-temperature and solid state chemists. The 2005 meeting at Notre Dame dropped "High Temperature" from the name, and the 2007 meeting at Texas A&amp;M was the first to call itself North American. Since then the conference has alternated with the Gordon Research Conference on Solid State Chemistry, so that the community meets every summer, and has grown from roughly one hundred participants to more than two hundred.</p>
<p>The format has stayed constant: three days of single-session talks mixing invited and contributed speakers, two evening poster sessions, and a conference dinner with poster prizes. Pre-conference workshops on diffraction, machine learning, and outreach have been part of the meeting since 2015. The 2027 meeting in Pittsburgh is the twelfth under the North American name and the first in Pennsylvania.</p>

<div class="sect">
<h3 style="margin-top:0">North American Solid State Chemistry Conference</h3>
{history_table(HISTORY)}
<h3>Before 2005: the Midwest High Temperature and Solid State Chemistry Conference</h3>
<p>The documented predecessors. Meetings in the 1990s between these are being compiled.</p>
{history_table(LINEAGE)}
<p class="small">Several early meetings left no web record, and organizers for some years are missing above. If you organized, spoke at, or attended one of them and can fill a gap, the organizers would be glad to hear from you through the <a href="contact.html">Contact</a> page.</p>
</div>
""")

# ---------------------------------------------------------------- Sponsors
PAGES["sponsors.html"] = ("Sponsors", f"""
<h2>Sponsors</h2>
<p class="lead">NASSCC keeps registration affordable for students and postdocs through the support of its sponsors.</p>
<h3>2027 sponsors</h3>
<p>{TBA}</p>
<h3>Sponsoring NASSCC 2027</h3>
<p>Sponsors support student travel and registration, poster awards, the conference dinner, lunches, and coffee breaks, and are recognized on this site, in the program book, and at the meeting. Organizations interested in sponsoring NASSCC 2027 should write to the organizers through the <a href="contact.html">Contact</a> page.</p>
""")

# ---------------------------------------------------------------- Contact
PAGES["contact.html"] = ("Contact", f"""
<h2>Contact</h2>
<p>Questions about the scientific program, abstracts, or sponsorship go to the organizing committee. Questions about registration and housing go to Duquesne University Conference and Event Services once registration opens.</p>
<table>
<tr><th>Name</th><th>Affiliation</th><th>Email</th></tr>
<tr><td>Jennifer A. Aitken, conference chair</td><td>Duquesne University</td><td><a href="mailto:aitkenj@duq.edu">aitkenj@duq.edu</a></td></tr>
<tr><td>Xin Gui</td><td>University of Pittsburgh</td><td><a href="mailto:xig75@pitt.edu">xig75@pitt.edu</a></td></tr>
<tr><td>Juan R. Chamorro</td><td>Carnegie Mellon University</td><td><a href="mailto:jchamorr@andrew.cmu.edu">jchamorr@andrew.cmu.edu</a></td></tr>
</table>
<p>Please send questions or corrections about this website to Juan Chamorro at <a href="mailto:jchamorr@andrew.cmu.edu">jchamorr@andrew.cmu.edu</a>.</p>
""")

# ---------------------------------------------------------------- build
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
(OUT / "style.css").write_text(CSS.strip() + "\n")
(OUT / "CNAME").write_text(DOMAIN + "\n")
(OUT / ".nojekyll").write_text("")
if IMG.exists():
    shutil.copytree(IMG, OUT / "img", ignore=shutil.ignore_patterns(".DS_Store"))
for f, (t, b) in PAGES.items():
    (OUT / f).write_text(page(f, t, b))
print("built", len(PAGES), "pages into", OUT)
