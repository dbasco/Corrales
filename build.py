#!/usr/bin/env python3
"""
Generador estático — Los Corrales de Rota (web v1).

Reglas duras (ver CLAUDE.md / docs/02-DECISIONES.md):
- Una página = un idioma = una URL. HTML autocontenido y estático.
- Marca Monumento verbatim: base.css (tokens :root) NO se toca. site.css añade
  componentes de ritmo que heredan los tokens. Ambos se inlinean en cada página.
- Imágenes como ficheros externos con width/height (Pillow los calcula: anti-CLS).
- Vídeo con fachada + youtube-nocookie + VideoObject.
- El motor de reservas NO entra en v1: la visita se reserva por la Oficina de
  Turismo de Rota (no hay reserva online, ni botón que lo sugiera).

v1 = español. EN/DE/FR se generan solo cuando exista su content/<lang>/*.json
(no se publican páginas vacías; el hreflang solo anuncia idiomas que existen).

Uso:  python3 build.py   ->   dist/
"""
import json, os, shutil, html, pathlib, re
from functools import lru_cache

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / "dist"
CFG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
CSS = (ROOT / "templates" / "base.css").read_text(encoding="utf-8")
CSS += "\n" + (ROOT / "templates" / "site.css").read_text(encoding="utf-8")

SITE = CFG["site"]
LANGS = CFG["languages"]
PAGES = CFG["pages"]
TRACK = CFG["tracking"]
ORIGIN = SITE["canonical_origin"].rstrip("/")
LANG_BY_CODE = {l["code"]: l for l in LANGS}
PAGE_BY_ID = {p["id"]: p for p in PAGES}

try:
    from PIL import Image
    _HAVE_PIL = True
except Exception:
    _HAVE_PIL = False

# ---------- logo / iconos ----------
LOGO_LIGHT = ('<svg width="{w}" height="{h}" viewBox="0 0 120 120" aria-hidden="true">'
  '<path d="M25 82 A38 30 0 0 1 95 82 Z" fill="#35494E"/>'
  '<path d="M17 82 A45 37 0 0 1 103 82" fill="none" stroke="#23201C" stroke-width="10.5" stroke-linecap="round" stroke-dasharray="7.5 3.2"/>'
  '<line x1="11" y1="82" x2="109" y2="82" stroke="#23201C" stroke-width="3.6" stroke-linecap="round"/></svg>')

PLAY_SVG = ('<svg viewBox="0 0 74 74" aria-hidden="true"><circle cx="37" cy="37" r="37" fill="#F4F1E9" opacity=".92"/>'
  '<path d="M30 24 L52 37 L30 50 Z" fill="#35494E"/></svg>')

# ---------- diagrama: 3 escenas de cómo funciona un corral ----------
DIAG_1 = ('<svg viewBox="0 0 320 200" role="img" aria-label="Con la marea alta, el agua y los peces pasan por encima del muro de piedra.">'
  '<rect x="0" y="64" width="320" height="136" fill="#5a7a80"/>'
  '<rect x="0" y="64" width="320" height="6" fill="#87a7ad" opacity=".8"/>'
  '<path d="M40 168 Q160 120 280 168" fill="none" stroke="#7f8a80" stroke-width="17" stroke-linecap="round"/>'
  '<path d="M40 168 Q160 120 280 168" fill="none" stroke="#5f6a62" stroke-width="17" stroke-linecap="round" stroke-dasharray="2.5 14" opacity=".5"/>'
  '<g fill="#23201C">'
  '<g transform="translate(126,104)"><ellipse rx="10" ry="5"/><path d="M9 0 L18 -6 L18 6 Z"/></g>'
  '<g transform="translate(178,120)"><ellipse rx="8" ry="4"/><path d="M7 0 L15 -5 L15 5 Z"/></g>'
  '<g transform="translate(158,88)"><ellipse rx="7" ry="3.5"/><path d="M6 0 L13 -4 L13 4 Z"/></g></g>'
  '<path d="M256 92 Q176 56 122 128" fill="none" stroke="#A85A32" stroke-width="3" stroke-dasharray="1 6" stroke-linecap="round"/>'
  '<path d="M122 128 l-2 -10 l10 4 z" fill="#A85A32"/>'
  '<g stroke="#F4F1E9" stroke-width="3" fill="none" opacity=".9"><line x1="24" y1="150" x2="24" y2="94"/><path d="M24 94 l-6 10 M24 94 l6 10"/></g>'
  '</svg>')
DIAG_2 = ('<svg viewBox="0 0 320 200" role="img" aria-label="Cuando baja la marea, el muro retiene el agua y los peces quedan atrapados dentro.">'
  '<rect x="0" y="150" width="320" height="50" fill="#cdbb9a" opacity=".55"/>'
  '<path d="M55 174 Q160 142 265 174 Q160 188 55 174 Z" fill="#5a7a80"/>'
  '<g fill="#23201C">'
  '<g transform="translate(148,172)"><ellipse rx="9" ry="4.5"/><path d="M8 0 L16 -5 L16 5 Z"/></g>'
  '<g transform="translate(192,174)"><ellipse rx="7" ry="3.5"/><path d="M6 0 L13 -4 L13 4 Z"/></g></g>'
  '<path d="M40 166 Q160 118 280 166" fill="none" stroke="#9A8F7C" stroke-width="16" stroke-linecap="round"/>'
  '<path d="M40 166 Q160 118 280 166" fill="none" stroke="#7c715c" stroke-width="16" stroke-linecap="round" stroke-dasharray="2 12" opacity=".55"/>'
  '<g stroke="#8a9a93" stroke-width="3" fill="none"><line x1="298" y1="96" x2="298" y2="150"/><path d="M298 150 l-6 -10 M298 150 l6 -10"/></g>'
  '</svg>')
DIAG_3 = ('<svg viewBox="0 0 320 200" role="img" aria-label="Con la bajamar se camina por dentro del corral y se recoge el pescado a pie.">'
  '<rect x="0" y="150" width="320" height="50" fill="#cdbb9a" opacity=".55"/>'
  '<path d="M55 176 Q160 148 265 176 Q160 190 55 176 Z" fill="#5a7a80"/>'
  '<g fill="#23201C"><g transform="translate(118,178)"><ellipse rx="7" ry="3.5"/><path d="M6 0 L13 -4 L13 4 Z"/></g></g>'
  '<path d="M40 170 Q160 124 280 170" fill="none" stroke="#9A8F7C" stroke-width="15" stroke-linecap="round"/>'
  '<g fill="#23201C" transform="translate(188,120)">'
  '<circle cx="0" cy="0" r="8"/>'
  '<path d="M-6 10 Q0 8 6 10 L4 46 L-4 46 Z"/>'
  '<rect x="-5" y="46" width="4" height="18"/><rect x="1" y="46" width="4" height="18"/>'
  '<path d="M6 22 L20 30" stroke="#23201C" stroke-width="3" fill="none"/></g>'
  '<path d="M206 148 h14 l-3 13 h-8 z" fill="#A85A32"/>'
  '</svg>')
DIAG_SCENES = [DIAG_1, DIAG_2, DIAG_3]

GTM_HEAD = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','__GTM_ID__');</script>
<!-- End Google Tag Manager -->"""
GTM_BODY = """<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=__GTM_ID__" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

LANG_REDIRECT = """<script>
(function(){try{
  if(location.pathname!=='/' && location.pathname!=='/index.html') return;
  var saved=localStorage.getItem('lcr_lang');
  var map=__LANGMAP__;
  var target=null;
  if(saved && map[saved]) target=map[saved];
  else{var n=(navigator.language||'').slice(0,2).toLowerCase(); if(map[n]) target=map[n];}
  if(target && !sessionStorage.getItem('lcr_redir')){sessionStorage.setItem('lcr_redir','1');location.replace(target);}
}catch(e){}})();
</script>"""

NAV_JS = """<script>
(function(){var t=document.querySelector('.nav-toggle'),l=document.getElementById('navlinks');
if(t&&l){t.addEventListener('click',function(){l.classList.toggle('open');var e=l.classList.contains('open');t.setAttribute('aria-expanded',e);});}
document.querySelectorAll('.video[data-yt]').forEach(function(v){function go(){
var id=v.getAttribute('data-yt');var f=document.createElement('iframe');f.width='100%';f.height='100%';f.allow='accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture';f.allowFullscreen=true;f.title=v.getAttribute('data-title')||'Vídeo';
f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0';f.style.border='0';f.style.position='absolute';f.style.inset='0';v.innerHTML='';v.appendChild(f);}
v.addEventListener('click',go);v.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();go();}});});
var d=document.getElementById('lang');if(d){document.addEventListener('click',function(e){if(!d.contains(e.target))d.removeAttribute('open');});}
})();
</script>"""

def esc(s): return html.escape(str(s), quote=True)

_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
def linkify(s):
    return _LINK_RE.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)

@lru_cache(maxsize=None)
def img_dims(src):
    if _HAVE_PIL and src.startswith("/assets/"):
        p = ROOT / src.lstrip("/")
        if p.exists():
            try:
                with Image.open(p) as im:
                    return im.size
            except Exception:
                return None
    return None

def img_tag(src, alt, cls="", eager=False, extra=""):
    d = img_dims(src)
    wh = f' width="{d[0]}" height="{d[1]}"' if d else ''
    c = f' class="{cls}"' if cls else ''
    load = ' fetchpriority="high"' if eager else ' loading="lazy"'
    return f'<img src="{esc(src)}"{c} alt="{esc(alt)}"{wh}{load}{extra}>'

# ---------- idiomas presentes ----------
def content_path(page_id, lang_code):
    return ROOT / "content" / lang_code / f"{page_id}.json"

def langs_for(page):
    out = []
    for l in LANGS:
        if content_path(page["id"], l["code"]).exists():
            out.append(l)
    return out

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
    present = langs_for(page)
    alts = [(l["hreflang"], page_url(page, l["code"], absolute=True)) for l in present]
    xd_codes = [l["code"] for l in present if l.get("x_default")] or (["es"] if any(l["code"]=="es" for l in present) else [present[0]["code"]] if present else [])
    if xd_codes:
        alts.append(("x-default", page_url(page, xd_codes[0], absolute=True)))
    return alts

def load_content(page_id, lang_code):
    f = content_path(page_id, lang_code)
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None

def load_ui(lang_code):
    f = ROOT / "content" / f"ui.{lang_code}.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}

# ---------- nav / footer ----------
def render_nav(page, lang_code, ui):
    home = page_url(PAGE_BY_ID["home"], lang_code)
    links = ui.get("nav", {})
    items = [
        (page_url(PAGE_BY_ID["visita"], lang_code), links.get("visita", "La visita")),
        (home + "#joyas", links.get("joyas", "Joyas de Rota")),
        (home + "#contacto", links.get("contacto", "Contacto")),
    ]
    lis = "".join(f'<a href="{esc(u)}">{esc(t)}</a>' for u, t in items)
    present = langs_for(page)
    lang_menu = ""
    if len(present) > 1:
        opts = []
        for l in present:
            u = page_url(page, l["code"])
            cur = ' aria-current="true"' if l["code"] == lang_code else ''
            opts.append(f'<a href="{esc(u)}" hreflang="{l["hreflang"]}"{cur}>{esc(l["label"])}</a>')
        lang_menu = ('<details class="lang" id="lang"><summary>' + esc(LANG_BY_CODE[lang_code]["label"]) +
                     ' ▾</summary><div class="lang-menu">' + "".join(opts) + '</div></details>')
    reserve = ui.get("reserve_cta", "Cómo visitar")
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
        for pid, t in [("aviso-legal", f.get("legal", "Aviso legal")), ("privacidad", f.get("privacy", "Privacidad"))]
    )
    return (f'<footer><div class="wrap">'
            f'<div class="fbrand">LOS CORRALES DE ROTA</div>'
            f'<p><b>{esc(f.get("pledge","El 100 % de lo recaudado va a la conservación del monumento."))}</b></p>'
            f'<p>{esc(SITE["org_legal_name"])} · {esc(SITE["place"])}<br>'
            f'<a href="mailto:{SITE["email"]}">{SITE["email"]}</a></p>'
            f'<p style="margin-top:14px">{legal}</p>'
            f'</div></footer>')

# ---------- bloques ----------
def block_prose(b):
    out = ['<div class="prose wide">']
    if b.get("kicker"): out.append(f'<span class="kicker">{esc(b["kicker"])}</span>')
    if b.get("h2"): out.append(f'<h2>{esc(b["h2"])}</h2>')
    if b.get("lead"): out.append(f'<p class="lead">{linkify(esc(b["lead"]))}</p>')
    for p in b.get("paras", []): out.append(f'<p>{linkify(esc(p))}</p>')
    out.append('</div>')
    anchor = f' id="{esc(b["anchor"])}"' if b.get("anchor") else ''
    return f'<div class="wrap"{anchor}>' + "".join(out) + '</div>'

def block_split(b):
    media = f'<div class="split-media">{img_tag(b["img"], b.get("alt",""))}</div>'
    body = ['<div class="split-body">']
    if b.get("kicker"): body.append(f'<span class="kicker">{esc(b["kicker"])}</span>')
    if b.get("h2"): body.append(f'<h2>{esc(b["h2"])}</h2>')
    if b.get("lead"): body.append(f'<p class="lead">{linkify(esc(b["lead"]))}</p>')
    for p in b.get("paras", []): body.append(f'<p>{linkify(esc(p))}</p>')
    if b.get("cta") and b.get("cta_href"):
        body.append(f'<a class="btn btn-primary" href="{esc(b["cta_href"])}">{esc(b["cta"])}</a>')
    body.append('</div>')
    rev = " reverse" if b.get("reverse") else ""
    return f'<div class="wrap"><div class="split{rev}">{media}{"".join(body)}</div></div>'

def block_diagram(b):
    steps = b.get("steps", [])[:3]
    cards = ""
    for i, st in enumerate(steps):
        cards += (f'<div class="step">{DIAG_SCENES[i]}'
                  f'<div class="cap"><span class="kicker"><span class="num">{i+1}.</span>{esc(st.get("kicker",""))}</span>'
                  f'<p>{esc(st.get("text",""))}</p></div></div>')
    head = ''
    if b.get("h2"):
        head = (f'<div class="sec-head"><span class="kicker">{esc(b.get("kicker",""))}</span>'
                f'<h2>{esc(b["h2"])}</h2><p>{esc(b.get("intro",""))}</p></div>')
    return f'<div class="wrap diagram">{head}<div class="steps">{cards}</div></div>'

def block_stats(b):
    cells = "".join(f'<div><div class="n">{esc(s["n"])}</div><div class="l">{esc(s["l"])}</div></div>' for s in b["items"])
    return f'<div class="wrap"><div class="stats">{cells}</div></div>'

def block_jewels(b, lang_code):
    cards = []
    for jid in CFG["joyas_order"]:
        jp = PAGE_BY_ID[jid]
        meta = b.get("cards", {}).get(jid, {})
        tag = meta.get("tag", jid); title = meta.get("title", jid); desc = meta.get("desc", "")
        img = meta.get("img")
        grad = meta.get("grad", "grad-pizarra").replace("grad-", "")
        if img:
            ph = f'style="background-image:linear-gradient(120deg,rgba(20,30,33,.12),rgba(20,30,33,.34)),url({esc(img)})"'
        else:
            g = {"pizarra":"linear-gradient(135deg,#4a666c,#35494E)","stone":"linear-gradient(135deg,#9A8F7C,#7a715f)","oxido":"linear-gradient(135deg,#A85A32,#8a4526)"}.get(grad,"linear-gradient(135deg,#4a666c,#35494E)")
            ph = f'style="background:{g}"'
        cards.append(
            f'<a class="jewel" href="{esc(page_url(jp,lang_code))}">'
            f'<div class="ph" {ph}><span class="tag">{esc(tag)}</span></div>'
            f'<div class="body"><h3>{esc(title)}</h3><p>{esc(desc)}</p>'
            f'<div class="more">{esc(b.get("more","Descúbrela →"))}</div></div></a>')
    head = ''
    if b.get("h2"):
        head = (f'<div class="sec-head"><span class="kicker">{esc(b.get("kicker",""))}</span>'
                f'<h2>{esc(b["h2"])}</h2><p>{esc(b.get("intro",""))}</p></div>')
    return f'<div class="wrap" id="joyas">{head}<div class="grid g3">{"".join(cards)}</div></div>'

def block_video(b):
    thumb = b.get("thumb") or f'https://i.ytimg.com/vi/{b["yt"]}/hqdefault.jpg'
    return (f'<div class="wrap"><div class="video" data-yt="{esc(b["yt"])}" data-title="{esc(b.get("title",""))}" role="button" tabindex="0" aria-label="{esc(b.get("title","Reproducir vídeo"))}">'
            f'<img src="{esc(thumb)}" alt="{esc(b.get("alt",b.get("title","")))}" loading="lazy" width="1280" height="720">'
            f'<div class="play">{PLAY_SVG}</div>'
            f'<div class="vlabel">{esc(b.get("title",""))}</div></div></div>')

def block_faq(b):
    items = "".join(f'<details><summary>{esc(q["q"])}</summary><p>{linkify(esc(q["a"]))}</p></details>' for q in b["items"])
    head = (f'<div class="sec-head"><span class="kicker">{esc(b.get("kicker","FAQ"))}</span><h2>{esc(b.get("h2","Preguntas frecuentes"))}</h2></div>')
    return f'<div class="wrap">{head}<div class="faq">{items}</div></div>'

def block_keys(b):
    head = ''
    if b.get("h2"):
        head = (f'<div class="sec-head"><span class="kicker">{esc(b.get("kicker",""))}</span><h2>{esc(b["h2"])}</h2></div>')
    cells = "".join(f'<div class="key"><span class="kicker">{esc(k.get("k",""))}</span><h3>{esc(k.get("t",""))}</h3><p>{esc(k.get("d",""))}</p></div>' for k in b.get("items", []))
    return f'<div class="wrap">{head}<div class="keys">{cells}</div></div>'

def block_turismo(b):
    phone = b.get("phone", "956 846345"); email = b.get("email", "turismorota@gmail.com")
    tel = "tel:+34" + phone.replace(" ", "")
    left = (f'<div class="tcard dark"><span class="kicker">{esc(b.get("kicker","Reserva"))}</span>'
            f'<div class="big">{esc(b.get("title","La reserva la gestiona la Oficina de Turismo de Rota"))}</div>'
            f'<div class="line"><b>Teléfono</b><a href="{tel}">{esc(phone)}</a></div>'
            f'<div class="line"><b>Correo</b><a href="mailto:{esc(email)}">{esc(email)}</a></div>'
            f'<p style="color:#cdd4d3;margin-top:14px;font-size:.92rem">{esc(b.get("note",""))}</p></div>')
    tips = "".join(f'<li>{esc(t)}</li>' for t in b.get("tips", []))
    right = (f'<div class="tcard"><span class="kicker">{esc(b.get("r_kicker","Antes de ir"))}</span>'
             f'<div class="big">{esc(b.get("r_title","Ten en cuenta"))}</div><ul>{tips}</ul></div>')
    head = (f'<div class="sec-head"><span class="kicker">{esc(b.get("head_kicker","Cómo visitar"))}</span>'
            f'<h2>{esc(b.get("h2","Reserva tu visita"))}</h2><p>{esc(b.get("intro",""))}</p></div>')
    anchor = f' id="{esc(b["anchor"])}"' if b.get("anchor") else ''
    return f'<div class="wrap"{anchor}>{head}<div class="turismo">{left}{right}</div></div>'

def block_contact(b):
    return (f'<div class="wrap" id="contacto"><div class="sec-head"><span class="kicker">{esc(b.get("kicker","Contacto"))}</span>'
            f'<h2>{esc(b.get("h2","Contacto"))}</h2><p>{esc(b.get("intro",""))}</p></div>'
            f'<div class="grid g2"><div class="prose"><p><b>Email</b><br><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></p>'
            f'<p><b>{esc(b.get("place_label","Dónde estamos"))}</b><br>{esc(SITE["place"])}</p></div>'
            f'<form class="prose" onsubmit="return false" aria-label="{esc(b.get("h2","Contacto"))}">'
            f'<div class="field"><label>{esc(b.get("f_name","Nombre"))}</label><input type="text" name="name"></div>'
            f'<div class="field"><label>{esc(b.get("f_email","Email"))}</label><input type="email" name="email"></div>'
            f'<div class="field"><label>{esc(b.get("f_msg","Mensaje"))}</label><textarea name="msg"></textarea></div>'
            f'<button class="btn btn-primary" type="submit">{esc(b.get("f_send","Enviar"))}</button>'
            f'<p class="muted" style="font-size:.8rem;margin-top:10px">{esc(b.get("form_note",""))}</p>'
            f'</form></div></div>')

def block_figure(b):
    cap = f'<figcaption>{esc(b["caption"])}</figcaption>' if b.get("caption") else ''
    return f'<div class="wrap"><figure class="figure">{img_tag(b["img"], b.get("alt",""))}{cap}</figure></div>'

def block_band(b):
    cap = ''
    if b.get("caption") or b.get("kicker"):
        k = f'<span class="kicker">{esc(b.get("kicker",""))}</span>' if b.get("kicker") else ''
        p = f'<p>{esc(b.get("caption",""))}</p>' if b.get("caption") else ''
        cap = f'<div class="band-cap">{k}{p}</div>'
    return (f'<div class="band">{img_tag(b["img"], b.get("alt",""), cls="bg")}'
            f'<div class="band-veil"></div>{cap}</div>')

def block_gallery(b):
    head = ''
    if b.get("h2"):
        head = (f'<div class="sec-head"><span class="kicker">{esc(b.get("kicker",""))}</span>'
                f'<h2>{esc(b["h2"])}</h2><p>{esc(b.get("intro",""))}</p></div>')
    items = ''
    for it in b.get("items", []):
        cap = f'<figcaption>{esc(it["caption"])}</figcaption>' if it.get("caption") else ''
        items += f'<figure>{img_tag(it["img"], it.get("alt",""))}{cap}</figure>'
    cols = b.get("cols", 3)
    return f'<div class="wrap">{head}<div class="grid g{cols} gallery">{items}</div></div>'

def block_pull(b):
    cite = f'<cite>{esc(b["cite"])}</cite>' if b.get("cite") else ''
    return f'<div class="wrap"><blockquote class="pull"><p>{esc(b["text"])}</p>{cite}</blockquote></div>'

def block_cta(b, lang_code):
    href = b.get("href") or page_url(PAGE_BY_ID["visita"], lang_code)
    btn = f'<a class="btn btn-accent" href="{esc(href)}">{esc(b.get("cta","La visita a los corrales"))}</a>'
    txt = f'<p>{esc(b.get("text",""))}</p>' if b.get("text") else ''
    return (f'<div class="wrap"><div class="cta-node">'
            f'<div><span class="kicker">{esc(b.get("kicker","El plan"))}</span>'
            f'<h2>{esc(b.get("h2","Todo lleva al mismo sitio: caminar por dentro de un corral"))}</h2>{txt}</div>'
            f'<div class="cta-side">{btn}</div></div></div>')

def render_block(b, lang_code):
    t = b["type"]
    if t == "prose": return block_prose(b)
    if t == "split": return block_split(b)
    if t == "diagram": return block_diagram(b)
    if t == "stats": return block_stats(b)
    if t == "jewels": return block_jewels(b, lang_code)
    if t == "video": return block_video(b)
    if t == "faq": return block_faq(b)
    if t == "keys": return block_keys(b)
    if t == "turismo": return block_turismo(b)
    if t == "contact": return block_contact(b)
    if t == "figure": return block_figure(b)
    if t == "band": return block_band(b)
    if t == "gallery": return block_gallery(b)
    if t == "pull": return block_pull(b)
    if t == "cta": return block_cta(b, lang_code)
    return ""

# ---------- hero ----------
def render_hero(page, c, lang_code, ui):
    h = c.get("hero", {})
    crumbs = ""
    if page["type"] != "hub":
        home = page_url(PAGE_BY_ID["home"], lang_code)
        crumbs = (f'<div class="wrap"><nav class="crumbs" aria-label="breadcrumb">'
                  f'<a href="{esc(home)}">{esc(ui.get("nav",{}).get("home","Inicio"))}</a> / {esc(h.get("h1",""))}</nav></div>')
    ctas = []
    if h.get("cta1"):
        cta1_href = h.get("cta1_href") or page_url(PAGE_BY_ID["visita"], lang_code)
        ctas.append(f'<a class="btn btn-accent" href="{esc(cta1_href)}">{esc(h["cta1"])}</a>')
    if h.get("cta2"):
        ctas.append(f'<a class="btn btn-secondary" href="{esc(h.get("cta2_href","#joyas"))}">{esc(h["cta2"])}</a>')
    cta_row = f'<div class="cta-row">{"".join(ctas)}</div>' if ctas else ''
    inner = (f'<div class="content"><span class="kicker">{esc(h.get("kicker",""))}</span>'
             f'<h1>{esc(h.get("h1",""))}</h1><p>{esc(h.get("sub",""))}</p>{cta_row}</div>')
    img = h.get("img")
    if img:
        bg = img_tag(img, h.get("img_alt", ""), cls="bg", eager=True)
        return crumbs + f'<header class="hero on-dark">{bg}<div class="veil"></div>{inner}</header>'
    grad = h.get("grad", "grad-pizarra")
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
    h = c.get("hero", {})
    img = h.get("img", "/assets/img/og-default.jpg")
    if img.startswith("/"): img = ORIGIN + img
    return {"@context":"https://schema.org","@type":"TouristAttraction","name":h.get("h1",SITE["name"]),
            "description":c.get("meta_description",""),"url":page_url(page,lang_code,absolute=True),
            "image":img,"isAccessibleForFree":False,"inLanguage":lang_code,
            "address":{"@type":"PostalAddress","addressLocality":"Rota","addressRegion":"Cádiz","addressCountry":"ES"}}

def jsonld_breadcrumb(page, c, lang_code, ui):
    home = page_url(PAGE_BY_ID["home"], lang_code, absolute=True)
    items = [{"@type":"ListItem","position":1,"name":ui.get("nav",{}).get("home","Inicio"),"item":home}]
    if page["type"] != "hub":
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
    graphs = [jsonld_org(), jsonld_breadcrumb(page, c, lang_code, ui)]
    if page["type"] == "hub": graphs.append(jsonld_website(lang_code))
    if page["type"] in ("visita", "joya"): graphs.append(jsonld_attraction(page, c, lang_code))
    for b in c.get("sections", []):
        if b["type"] == "video": graphs.append(jsonld_video(b, lang_code))
        if b["type"] == "faq": graphs.append(jsonld_faq(b))
    return graphs

# ---------- head ----------
def render_head(page, c, lang_code):
    title = c.get("title", SITE["name"]); desc = c.get("meta_description", "")
    canonical = page_url(page, lang_code, absolute=True)
    alts = "".join(f'\n<link rel="alternate" hreflang="{hl}" href="{esc(u)}">' for hl, u in alternates(page))
    og_img = c.get("hero", {}).get("img") or "/assets/img/og-default.jpg"
    if og_img.startswith("/"): og_img = ORIGIN + og_img
    gtm = GTM_HEAD.replace("__GTM_ID__", TRACK["gtm_id"])
    graphs = collect_jsonld(page, c, lang_code, load_ui(lang_code))
    ld = "".join(f'\n<script type="application/ld+json">{json.dumps(g,ensure_ascii=False)}</script>' for g in graphs)
    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Spectral:wght@400;500;600;700&display=swap" rel="stylesheet">')
    present = langs_for(page)
    langmap = {l["code"]: l["path_prefix"] + "/" for l in present if l["path_prefix"]}
    redirect = LANG_REDIRECT.replace("__LANGMAP__", json.dumps(langmap)) if (page["type"] == "hub" and langmap) else ''
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
{redirect}
</head>"""

TONES = {"surface": "tone-surface", "pizarra": "tone-pizarra", "sand": "tone-sand"}

def render_page(page, lang_code):
    c = load_content(page["id"], lang_code)
    ui = load_ui(lang_code)
    if not c:
        return None
    head = render_head(page, c, lang_code)
    body_gtm = GTM_BODY.replace("__GTM_ID__", TRACK["gtm_id"])
    nav = render_nav(page, lang_code, ui)
    hero = render_hero(page, c, lang_code, ui)
    def wrap(b):
        h = render_block(b, lang_code)
        if b.get("full") or b["type"] == "band":
            return h
        t = TONES.get(b.get("tone"))
        return f'<section class="{t}">{h}</section>' if t else f'<section>{h}</section>'
    sections = "".join(wrap(b) for b in c.get("sections", []))
    footer = render_footer(lang_code, ui)
    skip = f'<a class="skip-link" href="#main">{esc(ui.get("skip","Saltar al contenido"))}</a>'
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

# ---------- sitemap / robots / favicon ----------
def write_sitemap():
    ns = ('xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:xhtml="http://www.w3.org/1999/xhtml"')
    urls = []
    for page in PAGES:
        for l in langs_for(page):
            loc = page_url(page, l["code"], absolute=True)
            alt = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{hl}" href="{u}"/>' for hl, u in alternates(page))
            urls.append(f'  <url>\n    <loc>{loc}</loc>{alt}\n    <changefreq>{page.get("changefreq","monthly")}</changefreq>\n    <priority>{page.get("priority",0.5)}</priority>\n  </url>')
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset {ns}>\n' + "\n".join(urls) + "\n</urlset>\n"
    (DIST / "sitemap.xml").write_text(xml, encoding="utf-8")

def write_robots():
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n", encoding="utf-8")

def write_favicon():
    fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">'
           '<rect width="120" height="120" rx="27" fill="#2C3B40"/>'
           '<path d="M30 80 A28 22 0 0 1 90 80 Z" fill="#7FA0A6"/>'
           '<path d="M24 80 A34 27 0 0 1 96 80" fill="none" stroke="#F4F1E9" stroke-width="9" stroke-linecap="round"/>'
           '<line x1="19" y1="80" x2="101" y2="80" stroke="#F4F1E9" stroke-width="3.4" stroke-linecap="round"/></svg>')
    (DIST / "favicon.svg").write_text(fav, encoding="utf-8")

def main():
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    if (ROOT / "assets").exists():
        shutil.copytree(ROOT / "assets", DIST / "assets")
    count = 0
    for page in PAGES:
        for l in langs_for(page):
            out = render_page(page, l["code"])
            if out is None: continue
            url = page_url(page, l["code"])
            outdir = DIST / url.strip("/")
            outdir.mkdir(parents=True, exist_ok=True)
            (outdir / "index.html").write_text(out, encoding="utf-8")
            count += 1
    write_sitemap(); write_robots(); write_favicon()
    print(f"OK: {count} páginas generadas (idiomas con contenido)")
    if not _HAVE_PIL:
        print("AVISO: Pillow no disponible; imágenes sin width/height (instala pillow para evitar CLS).")

if __name__ == "__main__":
    main()
