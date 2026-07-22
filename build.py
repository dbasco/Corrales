#!/usr/bin/env python3
"""
Generador estático — Los Corrales de Rota.

Regla dura (arquitectura): una página = un idioma = una URL, HTML autocontenido.
Salida en dist/. El bloque de estilo Monumento (templates/base.css) se inlinea
verbatim en cada página; solo cambia el copy entre idiomas.

Uso:  python3 build.py
Contenido:  content/<lang>/<page_id>.json   +   content/ui.<lang>.json
Config:     site.config.json
"""
import json, os, shutil, html, pathlib, re

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / "dist"
CFG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
CSS = (ROOT / "templates" / "base.css").read_text(encoding="utf-8")

SITE = CFG["site"]
LANGS = CFG["languages"]
PAGES = CFG["pages"]
TRACK = CFG["tracking"]
ORIGIN = SITE["canonical_origin"].rstrip("/")
LANG_BY_CODE = {l["code"]: l for l in LANGS}
PAGE_BY_ID = {p["id"]: p for p in PAGES}

# ---------- logo (isotipo Monumento, SVG inline) ----------
LOGO_LIGHT = ('<svg width="{w}" height="{h}" viewBox="0 0 120 120" aria-hidden="true">'
  '<path d="M25 82 A38 30 0 0 1 95 82 Z" fill="#35494E"/>'
  '<path d="M17 82 A45 37 0 0 1 103 82" fill="none" stroke="#23201C" stroke-width="10.5" stroke-linecap="round" stroke-dasharray="7.5 3.2"/>'
  '<line x1="11" y1="82" x2="109" y2="82" stroke="#23201C" stroke-width="3.6" stroke-linecap="round"/></svg>')
LOGO_DARK = ('<svg width="{w}" height="{h}" viewBox="0 0 120 120" aria-hidden="true">'
  '<path d="M25 82 A38 30 0 0 1 95 82 Z" fill="#7FA0A6"/>'
  '<path d="M17 82 A45 37 0 0 1 103 82" fill="none" stroke="#F4F1E9" stroke-width="10.5" stroke-linecap="round" stroke-dasharray="7.5 3.2"/>'
  '<line x1="11" y1="82" x2="109" y2="82" stroke="#F4F1E9" stroke-width="3.6" stroke-linecap="round"/></svg>')

PLAY_SVG = ('<svg viewBox="0 0 74 74" aria-hidden="true"><circle cx="37" cy="37" r="37" fill="#F4F1E9" opacity=".92"/>'
  '<path d="M30 24 L52 37 L30 50 Z" fill="#35494E"/></svg>')

GTM_HEAD = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','__GTM_ID__');</script>
<!-- End Google Tag Manager -->"""
GTM_BODY = """<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=__GTM_ID__" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

LANG_REDIRECT = """<script>
/* Autoselección de idioma en la primera visita del hub (raíz ES). Preferencia recordada. */
(function(){try{
  if(location.pathname!=='/' && location.pathname!=='/index.html') return;
  var saved=localStorage.getItem('lcr_lang');
  var map={en:'/en/',de:'/de/',fr:'/fr/'};
  var target=null;
  if(saved && map[saved]) target=map[saved];
  else{var n=(navigator.language||'').slice(0,2).toLowerCase(); if(map[n]) target=map[n];}
  if(target && !sessionStorage.getItem('lcr_redir')){sessionStorage.setItem('lcr_redir','1');location.replace(target);}
}catch(e){}})();
</script>"""

NAV_JS = """<script>
(function(){var t=document.querySelector('.nav-toggle'),l=document.getElementById('navlinks');
if(t&&l){t.addEventListener('click',function(){l.classList.toggle('open');var e=l.classList.contains('open');t.setAttribute('aria-expanded',e);});}
document.querySelectorAll('.video[data-yt]').forEach(function(v){v.addEventListener('click',function(){
var id=v.getAttribute('data-yt');var f=document.createElement('iframe');f.width='100%';f.height='100%';f.allow='accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture';f.allowFullscreen=true;f.title=v.getAttribute('data-title')||'Vídeo';
f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0';f.style.border='0';f.style.position='absolute';f.style.inset='0';v.innerHTML='';v.appendChild(f);});});
var d=document.getElementById('lang');if(d){document.addEventListener('click',function(e){if(!d.contains(e.target))d.removeAttribute('open');});}
})();
</script>"""

def esc(s): return html.escape(str(s), quote=True)

_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
def linkify(s):
    # convierte [texto](url) en un <a>; s ya viene escapado con esc()
    return _LINK_RE.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)

def page_url(page, lang_code, absolute=False):
    lang = LANG_BY_CODE[lang_code]
    slug = page["slugs"][lang_code]
    prefix = lang["path_prefix"]
    if page["type"] == "hub":
        path = (prefix + "/") if prefix else "/"
    else:
        path = f"{prefix}/{slug}/"
    return (ORIGIN + path) if absolute else path

def alternates(page):
    alts = []
    for l in LANGS:
        alts.append((l["hreflang"], page_url(page, l["code"], absolute=True)))
    xd = LANG_BY_CODE[[l["code"] for l in LANGS if l.get("x_default")][0]]
    alts.append(("x-default", page_url(page, xd["code"], absolute=True)))
    return alts

def load_content(page_id, lang_code):
    f = ROOT / "content" / lang_code / f"{page_id}.json"
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    return None

def load_ui(lang_code):
    f = ROOT / "content" / f"ui.{lang_code}.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}

def rel(from_lang):  # asset root is absolute from origin -> use root-absolute paths
    return ""

# ---------- render helpers ----------
def render_nav(page, lang_code, ui):
    home = page_url(PAGE_BY_ID["home"], lang_code)
    def L(pid):
        p = PAGE_BY_ID[pid]; return page_url(p, lang_code)
    links = ui.get("nav", {})
    items = [
        (L("visita"), links.get("visita","Visita")),
        (L("aves"), links.get("aves","Aves")),
        (home + "#joyas", links.get("joyas","Joyas de Rota")),
        (home + "#contacto", links.get("contacto","Contacto")),
    ]
    lis = "".join(f'<a href="{esc(u)}">{esc(t)}</a>' for u,t in items)
    # selector de idioma
    opts=[]
    for l in LANGS:
        u = page_url(page, l["code"])
        cur = ' aria-current="true"' if l["code"]==lang_code else ''
        opts.append(f'<a href="{esc(u)}" hreflang="{l["hreflang"]}"{cur}>{esc(l["label"])}</a>')
    lang_menu = ('<details class="lang" id="lang"><summary>'+esc(LANG_BY_CODE[lang_code]["label"])+
                 ' ▾</summary><div class="lang-menu">'+"".join(opts)+'</div></details>')
    reserve = ui.get("reserve_cta","Reservar")
    return (f'<nav class="navbar" aria-label="Principal">'
            f'<a class="brand" href="{esc(home)}">{LOGO_LIGHT.format(w=30,h=30)}<span>Los Corrales de Rota</span></a>'
            f'<button class="nav-toggle" aria-expanded="false" aria-controls="navlinks" aria-label="Menú"><span></span><span></span><span></span></button>'
            f'<div class="links" id="navlinks">{lis}{lang_menu}'
            f'<a class="btn btn-primary" href="{esc(page_url(PAGE_BY_ID["visita"],lang_code))}">{esc(reserve)}</a>'
            f'</div></nav>')

def render_footer(lang_code, ui):
    f = ui.get("footer", {})
    legal = " · ".join(
        f'<a href="{esc(page_url(PAGE_BY_ID[pid],lang_code))}">{esc(t)}</a>'
        for pid,t in [("aviso-legal",f.get("legal","Aviso legal")),("privacidad",f.get("privacy","Privacidad"))]
    )
    return (f'<footer><div class="wrap">'
            f'<div class="fbrand">LOS CORRALES DE ROTA</div>'
            f'<p><b>{esc(f.get("pledge","El 100 % de lo recaudado va a la conservación del monumento."))}</b></p>'
            f'<p>{esc(SITE["org_legal_name"])} · {esc(SITE["place"])}<br>'
            f'<a href="mailto:{SITE["email"]}">{SITE["email"]}</a></p>'
            f'<p style="margin-top:14px">{legal}</p>'
            f'</div></footer>')

def block_prose(b):
    out=[f'<div class="prose">']
    if b.get("kicker"): out.append(f'<span class="kicker">{esc(b["kicker"])}</span>')
    if b.get("h2"): out.append(f'<h2>{esc(b["h2"])}</h2>')
    if b.get("lead"): out.append(f'<p class="lead">{linkify(esc(b["lead"]))}</p>')
    for p in b.get("paras",[]): out.append(f'<p>{linkify(esc(p))}</p>')
    out.append('</div>')
    anchor = f' id="{esc(b["anchor"])}"' if b.get("anchor") else ''
    return f'<div class="wrap"{anchor}>'+"".join(out)+'</div>'

def block_stats(b):
    cells="".join(f'<div><div class="n">{esc(s["n"])}</div><div class="l">{esc(s["l"])}</div></div>' for s in b["items"])
    return f'<div class="wrap"><div class="stats">{cells}</div></div>'

def block_jewels(b, lang_code):
    cards=[]
    for jid in CFG["joyas_order"]:
        jp = PAGE_BY_ID[jid]
        meta = b.get("cards",{}).get(jid,{})
        tag = meta.get("tag", jid)
        title = meta.get("title", jid)
        desc = meta.get("desc","")
        grad = meta.get("grad","grad-pizarra").replace("grad-","")
        img = meta.get("img")
        style = f'background-image:linear-gradient(120deg,rgba(20,30,33,.15),rgba(20,30,33,.35)),url({esc(img)})' if img else ''
        cls = "" if img else {"pizarra":"linear-gradient(135deg,#4a666c,#35494E)","stone":"linear-gradient(135deg,#9A8F7C,#7a715f)","oxido":"linear-gradient(135deg,#A85A32,#8a4526)"}.get(grad,"linear-gradient(135deg,#4a666c,#35494E)")
        ph_style = f'style="{style}"' if img else f'style="background:{cls}"'
        cards.append(
            f'<a class="jewel" href="{esc(page_url(jp,lang_code))}">'
            f'<div class="ph" {ph_style}><span class="tag">{esc(tag)}</span></div>'
            f'<div class="body"><h3>{esc(title)}</h3><p>{esc(desc)}</p>'
            f'<div class="more">{esc(b.get("more","Ver más →"))}</div></div></a>')
    head=''
    if b.get("h2"):
        head=(f'<div class="sec-head"><span class="kicker">{esc(b.get("kicker",""))}</span>'
              f'<h2>{esc(b["h2"])}</h2><p>{esc(b.get("intro",""))}</p></div>')
    return f'<div class="wrap" id="joyas">{head}<div class="grid g3">{"".join(cards)}</div></div>'

def block_video(b):
    thumb = b.get("thumb") or f'https://i.ytimg.com/vi/{b["yt"]}/hqdefault.jpg'
    return (f'<div class="wrap"><div class="video" data-yt="{esc(b["yt"])}" data-title="{esc(b.get("title",""))}" role="button" tabindex="0" aria-label="{esc(b.get("title","Reproducir vídeo"))}">'
            f'<img src="{esc(thumb)}" alt="{esc(b.get("alt",b.get("title","")))}" loading="lazy" width="1280" height="720">'
            f'<div class="play">{PLAY_SVG}</div>'
            f'<div class="vlabel">{esc(b.get("title",""))}</div></div></div>')

def block_faq(b):
    items="".join(f'<details><summary>{esc(q["q"])}</summary><p>{esc(q["a"])}</p></details>' for q in b["items"])
    head=(f'<div class="sec-head"><span class="kicker">{esc(b.get("kicker","FAQ"))}</span><h2>{esc(b.get("h2","Preguntas frecuentes"))}</h2></div>')
    return f'<div class="wrap">{head}<div class="faq">{items}</div></div>'

def block_support(b):
    bizum=(f'<div class="tile"><span class="kicker">Bizum</span><h3 style="margin:8px 0">{esc(b.get("bizum_title","Dona por Bizum"))}</h3>'
           f'<p class="muted">{esc(b.get("bizum_text",""))}</p>'
           f'<p><span class="pill-note">{esc(b.get("bizum_code_note","Código ONG pendiente"))}</span></p></div>')
    card=(f'<div class="tile"><span class="kicker">{esc(b.get("card_kicker","Tarjeta"))}</span><h3 style="margin:8px 0">{esc(b.get("card_title","Tarjeta"))}</h3>'
          f'<p class="muted">{esc(b.get("card_text",""))}</p>'
          f'<p><span class="pill-note">{esc(b.get("card_note","Pasarela pendiente"))}</span></p></div>')
    head=(f'<div class="sec-head"><span class="kicker">{esc(b.get("kicker","Apoyar"))}</span><h2>{esc(b.get("h2","Apoya el monumento"))}</h2><p>{esc(b.get("intro",""))}</p></div>')
    return f'<div class="wrap" id="apoyar">{head}<div class="support">{bizum}{card}</div></div>'

def block_contact(b):
    return (f'<div class="wrap" id="contacto"><div class="sec-head"><span class="kicker">{esc(b.get("kicker","Contacto"))}</span>'
            f'<h2>{esc(b.get("h2","Contacto"))}</h2><p>{esc(b.get("intro",""))}</p></div>'
            f'<div class="grid g2"><div class="prose"><p><b>Email</b><br><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></p>'
            f'<p><b>{esc(b.get("place_label","Dónde"))}</b><br>{esc(SITE["place"])}</p>'
            f'{("<p><b>WhatsApp</b><br>"+esc(b.get("whatsapp",""))+"</p>") if b.get("whatsapp") else ""}</div>'
            f'<form class="prose" onsubmit="return false" aria-label="{esc(b.get("h2","Contacto"))}">'
            f'<div class="field"><label>{esc(b.get("f_name","Nombre"))}</label><input type="text" name="name"></div>'
            f'<div class="field"><label>{esc(b.get("f_email","Email"))}</label><input type="email" name="email"></div>'
            f'<div class="field"><label>{esc(b.get("f_msg","Mensaje"))}</label><textarea name="msg"></textarea></div>'
            f'<button class="btn btn-primary" type="submit">{esc(b.get("f_send","Enviar"))}</button>'
            f'<p class="muted" style="font-size:.8rem;margin-top:10px">{esc(b.get("form_note",""))}</p>'
            f'</form></div></div>')

def block_figure(b):
    cap = f'<figcaption>{esc(b["caption"])}</figcaption>' if b.get("caption") else ''
    return (f'<div class="wrap"><figure class="figure">'
            f'<img src="{esc(b["img"])}" alt="{esc(b.get("alt",""))}" loading="lazy" width="{b.get("w",1600)}" height="{b.get("h",900)}">'
            f'{cap}</figure></div>')

def block_band(b):
    cap=''
    if b.get("caption") or b.get("kicker"):
        k=f'<span class="kicker">{esc(b.get("kicker",""))}</span>' if b.get("kicker") else ''
        p=f'<p>{esc(b.get("caption",""))}</p>' if b.get("caption") else ''
        cap=f'<div class="band-cap">{k}{p}</div>'
    return (f'<div class="band"><img class="bg" src="{esc(b["img"])}" alt="{esc(b.get("alt",""))}" '
            f'loading="lazy" width="{b.get("w",1920)}" height="{b.get("h",800)}">'
            f'<div class="band-veil"></div>{cap}</div>')

def block_gallery(b):
    head=''
    if b.get("h2"):
        head=(f'<div class="sec-head"><span class="kicker">{esc(b.get("kicker",""))}</span>'
              f'<h2>{esc(b["h2"])}</h2><p>{esc(b.get("intro",""))}</p></div>')
    items=''
    for it in b.get("items",[]):
        cap=f'<figcaption>{esc(it["caption"])}</figcaption>' if it.get("caption") else ''
        items+=(f'<figure><img src="{esc(it["img"])}" alt="{esc(it.get("alt",""))}" '
                f'loading="lazy" width="800" height="600">{cap}</figure>')
    cols=b.get("cols",3)
    return f'<div class="wrap">{head}<div class="grid g{cols} gallery">{items}</div></div>'

def render_block(b, lang_code):
    t=b["type"]
    if t=="prose": return block_prose(b)
    if t=="stats": return block_stats(b)
    if t=="jewels": return block_jewels(b, lang_code)
    if t=="video": return block_video(b)
    if t=="faq": return block_faq(b)
    if t=="support": return block_support(b)
    if t=="contact": return block_contact(b)
    if t=="figure": return block_figure(b)
    if t=="band": return block_band(b)
    if t=="gallery": return block_gallery(b)
    return ""

# ---------- hero ----------
def render_hero(page, c, lang_code, ui):
    h = c.get("hero", {})
    crumbs = ""
    if page["type"] != "hub":
        home = page_url(PAGE_BY_ID["home"], lang_code)
        crumbs = (f'<div class="wrap"><nav class="crumbs" aria-label="breadcrumb">'
                  f'<a href="{esc(home)}">{esc(ui.get("nav",{}).get("home","Inicio"))}</a> / {esc(h.get("h1",""))}</nav></div>')
    reserve = ui.get("reserve_cta","Reservar")
    ctas = []
    cta1_href = h.get("cta1_href") or page_url(PAGE_BY_ID["visita"],lang_code)
    ctas.append(f'<a class="btn btn-accent" href="{esc(cta1_href)}">{esc(h.get("cta1",reserve))}</a>')
    if h.get("cta2"):
        ctas.append(f'<a class="btn btn-secondary" href="{esc(h.get("cta2_href","#joyas"))}">{esc(h["cta2"])}</a>')
    inner = (f'<div class="content"><span class="kicker">{esc(h.get("kicker",""))}</span>'
             f'<h1>{esc(h.get("h1",""))}</h1><p>{esc(h.get("sub",""))}</p>'
             f'<div class="cta-row">{"".join(ctas)}</div></div>')
    img = h.get("img")
    if img:
        bg = f'<img class="bg" src="{esc(img)}" alt="{esc(h.get("img_alt",""))}" width="1920" height="1080" fetchpriority="high">'
        return crumbs + f'<header class="hero on-dark">{bg}<div class="veil"></div>{inner}</header>'
    grad = h.get("grad","grad-pizarra")
    return crumbs + f'<header class="hero on-dark {grad}"><div class="veil"></div>{inner}</header>'

# ---------- JSON-LD ----------
def jsonld_org():
    return {"@context":"https://schema.org","@type":"NGO","name":SITE["org_legal_name"],
            "alternateName":SITE["name"],"url":ORIGIN+"/","email":SITE["email"],
            "logo":ORIGIN+"/assets/img/logo-corrales.png","foundingDate":str(SITE["founded_year"]),
            "areaServed":SITE["place"],"sameAs":[SITE["youtube_channel"]],
            "address":{"@type":"PostalAddress","addressLocality":"Rota","addressRegion":"Cádiz","addressCountry":"ES"}}

def jsonld_website(lang_code):
    return {"@context":"https://schema.org","@type":"WebSite","name":SITE["name"],
            "url":page_url(PAGE_BY_ID["home"],lang_code,absolute=True),"inLanguage":lang_code}

def jsonld_attraction(page, c, lang_code):
    h=c.get("hero",{})
    return {"@context":"https://schema.org","@type":"TouristAttraction","name":h.get("h1",SITE["name"]),
            "description":c.get("meta_description",""),"url":page_url(page,lang_code,absolute=True),
            "image":h.get("img",ORIGIN+"/assets/img/og-default.jpg"),
            "isAccessibleForFree":False,"inLanguage":lang_code,
            "address":{"@type":"PostalAddress","addressLocality":"Rota","addressRegion":"Cádiz","addressCountry":"ES"}}

def jsonld_breadcrumb(page, c, lang_code, ui):
    home=page_url(PAGE_BY_ID["home"],lang_code,absolute=True)
    items=[{"@type":"ListItem","position":1,"name":ui.get("nav",{}).get("home","Inicio"),"item":home}]
    if page["type"]!="hub":
        items.append({"@type":"ListItem","position":2,"name":c.get("hero",{}).get("h1",page["id"]),
                      "item":page_url(page,lang_code,absolute=True)})
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items}

def jsonld_video(b, lang_code):
    return {"@context":"https://schema.org","@type":"VideoObject","name":b.get("title","Vídeo"),
            "description":b.get("desc",b.get("title","")),
            "thumbnailUrl":b.get("thumb") or f'https://i.ytimg.com/vi/{b["yt"]}/hqdefault.jpg',
            "uploadDate":b.get("date","2025-01-01"),"embedUrl":f'https://www.youtube-nocookie.com/embed/{b["yt"]}',
            "contentUrl":f'https://www.youtube.com/watch?v={b["yt"]}'}

def jsonld_faq(b):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q["q"],"acceptedAnswer":{"@type":"Answer","text":q["a"]}} for q in b["items"]]}

def collect_jsonld(page, c, lang_code, ui):
    graphs=[jsonld_org(), jsonld_breadcrumb(page,c,lang_code,ui)]
    if page["type"]=="hub": graphs.append(jsonld_website(lang_code))
    if page["type"] in ("visita","joya"): graphs.append(jsonld_attraction(page,c,lang_code))
    for b in c.get("sections",[]):
        if b["type"]=="video": graphs.append(jsonld_video(b,lang_code))
        if b["type"]=="faq": graphs.append(jsonld_faq(b))
    return graphs

# ---------- head ----------
def render_head(page, c, lang_code):
    title=c.get("title", SITE["name"])
    desc=c.get("meta_description","")
    canonical=page_url(page,lang_code,absolute=True)
    alts="".join(f'\n<link rel="alternate" hreflang="{hl}" href="{esc(u)}">' for hl,u in alternates(page))
    og_img = c.get("hero",{}).get("img") or (ORIGIN+"/assets/img/og-default.jpg")
    if og_img.startswith("/"): og_img=ORIGIN+og_img
    gtm = GTM_HEAD.replace("__GTM_ID__", TRACK["gtm_id"])
    graphs=collect_jsonld(page,c,lang_code,load_ui(lang_code))
    ld="".join(f'\n<script type="application/ld+json">{json.dumps(g,ensure_ascii=False)}</script>' for g in graphs)
    fonts=('<link rel="preconnect" href="https://fonts.googleapis.com">'
           '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
           '<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Spectral:wght@400;500;600;700&display=swap" rel="stylesheet">')
    return f"""<!doctype html>
<html lang="{lang_code}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canonical)}">{alts}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITE['name'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(og_img)}">
<meta property="og:locale" content="{lang_code}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#35494E">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{fonts}
{gtm}
<style>{CSS}</style>{ld}
{LANG_REDIRECT if page['type']=='hub' else ''}
</head>"""

def render_page(page, lang_code):
    c=load_content(page["id"], lang_code)
    ui=load_ui(lang_code)
    if not c:
        c={"title":SITE["name"],"meta_description":"","hero":{"h1":page["id"],"sub":""},"sections":[]}
    head=render_head(page,c,lang_code)
    body_gtm=GTM_BODY.replace("__GTM_ID__", TRACK["gtm_id"])
    nav=render_nav(page,lang_code,ui)
    hero=render_hero(page,c,lang_code,ui)
    def wrap(b):
        h=render_block(b,lang_code)
        return h if b["type"]=="band" else f'<section>{h}</section>'
    sections="".join(wrap(b) for b in c.get("sections",[]))
    footer=render_footer(lang_code,ui)
    skip=f'<a class="skip-link" href="#main">{esc(ui.get("skip","Saltar al contenido"))}</a>'
    return f"""{head}
<body>
{body_gtm}
{skip}
{nav}
<main id="main">
{hero}
{sections}
</main>
{footer}
{NAV_JS}
</body>
</html>"""

# ---------- sitemap / robots ----------
def write_sitemap():
    ns=('xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml"')
    urls=[]
    for page in PAGES:
        for l in LANGS:
            loc=page_url(page,l["code"],absolute=True)
            alt="".join(f'\n    <xhtml:link rel="alternate" hreflang="{hl}" href="{u}"/>' for hl,u in alternates(page))
            urls.append(f'  <url>\n    <loc>{loc}</loc>{alt}\n    <changefreq>{page.get("changefreq","monthly")}</changefreq>\n    <priority>{page.get("priority",0.5)}</priority>\n  </url>')
    xml=f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset {ns}>\n'+"\n".join(urls)+"\n</urlset>\n"
    (DIST/"sitemap.xml").write_text(xml,encoding="utf-8")

def write_robots():
    (DIST/"robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n",encoding="utf-8")

def write_favicon():
    fav=('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">'
         '<rect width="120" height="120" rx="27" fill="#2C3B40"/>'
         '<path d="M30 80 A28 22 0 0 1 90 80 Z" fill="#7FA0A6"/>'
         '<path d="M24 80 A34 27 0 0 1 96 80" fill="none" stroke="#F4F1E9" stroke-width="9" stroke-linecap="round"/>'
         '<line x1="19" y1="80" x2="101" y2="80" stroke="#F4F1E9" stroke-width="3.4" stroke-linecap="round"/></svg>')
    (DIST/"favicon.svg").write_text(fav,encoding="utf-8")

def main():
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    # assets
    if (ROOT/"assets").exists():
        shutil.copytree(ROOT/"assets", DIST/"assets")
    count=0
    for page in PAGES:
        for l in LANGS:
            url=page_url(page,l["code"])
            outdir=DIST/(url.strip("/"))
            outdir.mkdir(parents=True, exist_ok=True)
            (outdir/"index.html").write_text(render_page(page,l["code"]),encoding="utf-8")
            count+=1
    write_sitemap(); write_robots(); write_favicon()
    print(f"OK: {count} páginas · {len(PAGES)} plantillas × {len(LANGS)} idiomas")
    print(f"    sitemap.xml ({len(PAGES)*len(LANGS)} URLs), robots.txt, favicon.svg")

if __name__=="__main__":
    main()
