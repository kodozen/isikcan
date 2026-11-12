#!/usr/bin/env python3
"""Işıkcan Flora Shop — Lefkoşa Surlariçi'ndeki çiçekçinin sitesi.

Ürünler ve saksı fiyat listesi urunler.json dosyasından okunuyor; sayfalar
buradan üretiliyor. Fiyat ya da ürün değişince dosyayı düzeltip
`python3 uret.py` demek yeterli. Fotoğraf eklenince önce `bash gorseller.sh`.
"""

import html
import json
import re
import urllib.parse
from pathlib import Path

KOK = Path(__file__).parent
VERI = json.loads((KOK / "urunler.json").read_text(encoding="utf-8"))
M = VERI["marka"]
KATEGORILER = VERI["kategoriler"]
URUNLER = VERI["urunler"]
SAKSI = VERI["saksi"]
OLCU = {s.split("\t")[0]: tuple(map(int, s.split("\t")[2].split(",")))
        for s in (KOK / "img/ham/liste.tsv").read_text().splitlines() if s.strip()}

SURUM = "11"
SITE = "https://kodozen.github.io/isikcan/"   # önizleme adresi; dükkânın alan adı alınınca değişir


def e(metin):
    return html.escape(metin, quote=True)


def tl(sayi):
    if sayi != int(sayi):
        return f"{sayi:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " ₺"
    return f"{int(sayi):,}".replace(",", ".") + " ₺"


def wa(metin):
    return f"https://wa.me/{M['whatsapp']}?text={urllib.parse.quote(metin)}"


WA_GENEL = wa("Merhaba, çiçek siparişi vermek istiyorum.")
IG = f"https://www.instagram.com/{M['instagram']}/"
IG_DM = f"https://ig.me/m/{M['instagram']}"


def foto(ad, tur, boyutlar, sizes, alt, sinif="", oncelik=False, en_boy=None):
    """tur: 'k' kart kırpımı (4:5), 'b' tam kadraj."""
    kucuk, buyuk = (400, 700) if tur == "k" else (800, 1300)
    g, y = OLCU[ad]
    if tur == "k":
        w, h = 400, 500 if y / g >= 1.25 else round(400 * y / g)
    else:
        w, h = 800, round(800 * y / g)
    srcset = ", ".join(f"img/{ad}-{tur}-{b}.webp {min(b, g)}w" for b in (kucuk, buyuk))
    ek = ' fetchpriority="high"' if oncelik else ' loading="lazy" decoding="async"'
    return (f'<img src="img/{ad}-{tur}-{kucuk}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{e(alt)}"{f" class={chr(34)}{sinif}{chr(34)}" if sinif else ""}{ek}>')


# --- ortak parçalar --------------------------------------------------------

GEZINTI = [
    ("cicekler.html", "Çiçekler"),
    ("saksi-fiyatlari.html", "Saksı fiyatları"),
    ("ozel-gunler.html", "Özel günler"),
    ("teslimat.html", "Teslimat"),
    ("dukkan.html", "Dükkân"),
]

IKON_WA = ('<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" '
           'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
           '<path d="M3.5 20.5l1.3-4.2A8.5 8.5 0 1 1 8 19.4l-4.5 1.1Z"/>'
           '<path d="M9 8.5c-.3 2.8 3 6.2 6 6.2l1-1.5-2-1.2-.9.8c-1-.5-1.8-1.3-2.3-2.3l.8-.9-1.2-2.1-1.4 1Z"/></svg>')
IKON_TEL = ('<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="none" stroke="currentColor" '
            'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
            'd="M5 4h3.5l1.5 4-2 1.5a11 11 0 0 0 6.5 6.5l1.5-2 4 1.5V19a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg>')
IKON_IG = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.2" cy="6.8" r="1.1" fill="currentColor"/></svg>'
IKON_OK = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6"/></svg>'

MARKA_YAZI = '<span class="marka__ad">IŞIKCAN</span><span class="marka__alt">Flora Shop</span>'


def kafa(baslik, aciklama, dosya, og="paylasim.jpg", govde="", onyukle=""):
    yerel = {
        "@context": "https://schema.org", "@type": "Florist", "name": M["ad"],
        "telephone": M["tel_href"], "url": SITE, "image": SITE + "img/paylasim.jpg",
        "address": {"@type": "PostalAddress",
                    "streetAddress": f"{M['adres_satir1']}, {M['adres_satir2']}",
                    "addressLocality": "Lefkoşa", "addressCountry": "CY"},
        "areaServed": "Kuzey Kıbrıs", "sameAs": [IG],
    }
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(baslik)}</title>
<meta name="description" content="{e(aciklama)}">
<meta name="theme-color" content="#1F3B30">
<meta name="robots" content="noindex">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(M['ad'])}">
<meta property="og:title" content="{e(baslik)}">
<meta property="og:description" content="{e(aciklama)}">
<meta property="og:image" content="{SITE}img/{og}">
<meta property="og:locale" content="tr_TR">
<link rel="canonical" href="{SITE}{'' if dosya == 'index.html' else dosya}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" as="font" type="font/woff2" href="yazi/marcellus-latin.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="yazi/figtree-latin.woff2" crossorigin>
{onyukle}<link rel="stylesheet" href="yazi/yazi.css?v={SURUM}">
<link rel="stylesheet" href="styles.css?v={SURUM}">
<script>document.documentElement.classList.add("js");(function(){{function s(e){{var g=e.viewTransition;if(!g)return;var y=function(){{}};g.ready.catch(y);g.finished.catch(y);g.updateCallbackDone.catch(y)}}addEventListener("pagereveal",s);addEventListener("pageswap",s)}})();</script>
<script type="speculationrules">{{"prefetch":[{{"where":{{"href_matches":"/*"}},"eagerness":"moderate"}}]}}</script>
<script type="application/ld+json">{json.dumps(yerel, ensure_ascii=False)}</script>
</head>
<body{f' class="{govde}"' if govde else ''}>
<a class="atla" href="#icerik">İçeriğe geç</a>
"""


def ust(etkin=""):
    baglar = "".join(
        f'<a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == etkin else ""}>{a}</a>'
        for h, a in GEZINTI)
    return f"""<header class="ust">
  <a class="marka" href="index.html" aria-label="{e(M['ad'])}, ana sayfa">{MARKA_YAZI}</a>
  <nav class="ust__gezinti" aria-label="Ana gezinti">{baglar}</nav>
  <div class="ust__sag">
    <a class="ust__tel" href="tel:{M['tel_href']}">{IKON_TEL}<span>{M['telefon']}</span></a>
    <a class="dugme dugme--kucuk" href="{WA_GENEL}" target="_blank" rel="noopener">Sipariş ver</a>
    <button class="ust__menu" type="button" data-ac="menu" aria-haspopup="dialog" aria-label="Menüyü aç"><span></span><span></span></button>
  </div>
</header>
<dialog class="menu" id="menu" aria-label="Menü">
  <div class="menu__ust">
    <span class="marka">{MARKA_YAZI}</span>
    <button class="menu__kapat" type="button" data-kapat aria-label="Menüyü kapat">Kapat</button>
  </div>
  <nav class="menu__baglar" aria-label="Menü">{baglar}</nav>
  <div class="menu__alt">
    <a class="dugme" href="{WA_GENEL}" target="_blank" rel="noopener">{IKON_WA}WhatsApp'tan yazın</a>
    <a class="dugme dugme--cizgi" href="tel:{M['tel_href']}">{IKON_TEL}{M['telefon']}</a>
  </div>
</dialog>
"""


def alt():
    baglar = "".join(f'<li><a href="{h}">{a}</a></li>' for h, a in GEZINTI)
    return f"""<footer class="alt">
  <div class="alt__ic">
    <div class="alt__marka">
      <span class="marka marka--buyuk">{MARKA_YAZI}</span>
      <p>Lefkoşa Surlariçi'nde çiçekçi. Buketler dükkânda hazırlanır, KKTC'nin her yerine gönderilir.</p>
    </div>
    <div>
      <h2 class="alt__baslik">Dükkân</h2>
      <address>{M['adres_satir1']}<br>{M['adres_satir2']}<br>{M['adres_sehir']}</address>
      <p><a href="{M['harita']}" target="_blank" rel="noopener">Yol tarifi al</a></p>
    </div>
    <div>
      <h2 class="alt__baslik">Sipariş</h2>
      <ul class="alt__liste">
        <li><a href="{WA_GENEL}" target="_blank" rel="noopener">WhatsApp</a></li>
        <li><a href="tel:{M['tel_href']}">{M['telefon']}</a></li>
        <li><a href="{IG}" target="_blank" rel="noopener">Instagram: @{M['instagram']}</a></li>
      </ul>
    </div>
    <div>
      <h2 class="alt__baslik">Site</h2>
      <ul class="alt__liste">{baglar}</ul>
    </div>
  </div>
  <p class="alt__not">Fiyatlar, yanlarında yazan tarihteki Instagram paylaşımlarından alındı. Güncel fiyatı siparişten önce bizden teyit edin.</p>
  <p class="alt__not alt__not--ornek">Bu sayfa, <a href="https://kodozen.github.io" target="_blank" rel="noopener">Kodozen</a>'in Işıkcan Flora Shop için hazırladığı bir önizlemedir; dükkânın onayıyla yayına alınacaktır.</p>
</footer>
<a class="yuzen" href="{WA_GENEL}" target="_blank" rel="noopener" aria-label="WhatsApp'tan yazın">{IKON_WA}</a>
<script src="app.js?v={SURUM}" defer></script>
</body>
</html>
"""


def fiyat_satiri(u):
    if u["fiyat"]:
        return f'<span class="kart__fiyat">{tl(u["fiyat"])}</span>'
    return '<span class="kart__fiyat kart__fiyat--sor">Fiyatını sorun</span>'


def kart(u, sizes="(min-width: 1100px) 23vw, (min-width: 700px) 31vw, 46vw", gecis=True):
    ad = u["fotolar"][0]
    vt = f' style="view-transition-name:u-{u["slug"]}"' if gecis else ""
    return f"""<article class="kart" data-kat="{' '.join(u['kat'])}">
  <a class="kart__bag" href="urun/{u['slug']}.html">
    <span class="kart__foto"{vt}>{foto(ad, 'k', None, sizes, u['alt'])}</span>
    <span class="kart__ad">{e(u['ad'])}</span>
    {fiyat_satiri(u)}
  </a>
</article>"""


# --- ana sayfa -------------------------------------------------------------

def ana_sayfa():
    u_by = {u["slug"]: u for u in URUNLER}
    kasim = [u_by[s] for s in ("mavi-kasimpati-buketi", "saksi-kasimpati", "pembe-sari-kasimpati-buketi",
                               "lila-kasimpati-buketi", "somon-kasimpati-buketi", "sapka-kutusunda-kasimpati")]
    ray = "".join(kart(u, "(min-width: 900px) 260px, 62vw", gecis=False) for u in kasim)
    sayi = {k["k"]: sum(1 for u in URUNLER if k["k"] in u["kat"]) for k in KATEGORILER}
    kutular = "".join(f"""<a class="tur tur--{i + 1}" href="cicekler.html#{k['k']}">
      {foto(k['foto'], 'k', None, '(min-width: 900px) 30vw, 92vw', k['ad'])}
      <span class="tur__yazi"><span class="tur__ad">{k['ad']}</span><span class="tur__alt">{k['metin']}</span></span>
      <span class="tur__sayi">{sayi[k['k']]} çeşit</span>
    </a>""" for i, k in enumerate(KATEGORILER))
    onyukle = ('<link rel="preload" as="image" href="img/sokak-buket-b-800.webp" '
               'imagesrcset="img/sokak-buket-b-800.webp 800w, img/sokak-buket-b-1300.webp 1300w" '
               'imagesizes="(min-width: 900px) 42vw, 86vw" fetchpriority="high">\n')
    return kafa(
        "Işıkcan Flora Shop | Lefkoşa'da çiçekçi, KKTC'ye çiçek gönderimi",
        "Lefkoşa Surlariçi'ndeki Işıkcan Flora Shop: buket, orkide, kutu aranjman ve saksı çiçekleri. Lefkoşa içi ve KKTC geneli teslimat, WhatsApp'tan sipariş.",
        "index.html", govde="ana", onyukle=onyukle) + ust() + f"""<main id="icerik">

<section class="vitrin">
  <div class="vitrin__metin">
    <h1>Lefkoşa'nın sokaklarından, sevdiğinizin kapısına.</h1>
    <p class="vitrin__giris">Buketi Surlariçi'ndeki dükkânımızda hazırlıyoruz. Lefkoşa'nın içine de, KKTC'nin öbür ucuna da biz götürüyoruz.</p>
    <div class="vitrin__dugmeler">
      <a class="dugme" href="cicekler.html">Çiçekleri görün</a>
      <a class="dugme dugme--cizgi" href="{WA_GENEL}" target="_blank" rel="noopener">{IKON_WA}WhatsApp'tan yazın</a>
    </div>
    <dl class="ucret">
      <div><dt>Lefkoşa içi teslimat</dt><dd>{tl(M['kargo_ic'])}</dd></div>
      <div><dt>Lefkoşa dışı teslimat</dt><dd>{tl(M['kargo_dis'])}</dd></div>
      <div><dt>Dükkândan teslim</dt><dd>Ücretsiz</dd></div>
    </dl>
  </div>
  <figure class="vitrin__kemer">
    <div class="kemer kemer--tas" aria-hidden="true"></div>
    <div class="kemer kemer--foto">{foto('sokak-buket', 'b', None, '(min-width: 900px) 42vw, 86vw',
        "Kraft kâğıda sarılı mevsim buketi, Lefkoşa Surlariçi'nde bir sokakta havaya kaldırılmış", oncelik=True)}</div>
    <figcaption>Fotoğraflarımızı dükkânın sokağında çekiyoruz. Gördüğünüz buket, elinize ulaşan bukettir.</figcaption>
  </figure>
</section>

<section class="mevsim" aria-labelledby="mevsim-b">
  <div class="mevsim__metin">
    <h2 id="mevsim-b">Kasım, kasımpatı ayı.</h2>
    <p>Bu ay tezgâhın yarısı kasımpatı: mavi, lila, somon, pembe sarı. Buket de bağlıyoruz, saksıda da veriyoruz.</p>
    <ul class="mevsim__fiyat">
      <li><span>Saksı kasımpatı, papatya tipi</span><b>{tl(500)}</b></li>
      <li><span>Saksı kasımpatı, top</span><b>{tl(650)}</b></li>
      <li><span>Kasımpatı buketi</span><b class="sor">Boyuna göre, sorun</b></li>
    </ul>
    <a class="bag" href="cicekler.html#buket">Bütün buketler {IKON_OK}</a>
  </div>
  <div class="ray" tabindex="0" role="group" aria-label="Kasımpatı çeşitleri, yana kaydırılır">{ray}</div>
</section>

<section class="turler" aria-labelledby="tur-b">
  <div class="bolum-bas">
    <h2 id="tur-b">Ne göndermek istersiniz?</h2>
    <p>Hepsinin fotoğrafı bizim tezgâhtan. Aklınızdaki çiçek listede yoksa yazın, bulalım.</p>
  </div>
  <div class="turler__izgara">{kutular}</div>
</section>

<section class="notbant" aria-labelledby="not-b">
  <div class="notbant__metin">
    <h2 id="not-b">Kartına ne yazalım?</h2>
    <p>Her siparişin yanında bir kart gider. Notunuzu şimdi yazın; çiçeği seçerken hazır bulursunuz.</p>
    <label class="alan">
      <span class="alan__etiket">Kart notunuz</span>
      <textarea id="ana-not" rows="3" maxlength="160" placeholder="İyi ki doğdun, Ayşe. Bu sene de yanındayım."></textarea>
    </label>
    <label class="alan">
      <span class="alan__etiket">İmza</span>
      <input id="ana-imza" type="text" maxlength="40" placeholder="Mert" autocomplete="off">
    </label>
    <a class="dugme dugme--acik" href="cicekler.html" id="ana-not-git">Bu notla çiçek seçin</a>
  </div>
  <div class="kartnot" aria-hidden="true">
    <div class="kartnot__kagit">
      <span class="kartnot__marka">IŞIKCAN</span>
      <p class="kartnot__yazi" data-not-onizleme data-bos="İyi ki doğdun, Ayşe. Bu sene de yanındayım.">İyi ki doğdun, Ayşe. Bu sene de yanındayım.</p>
      <p class="kartnot__imza" data-imza-onizleme data-bos="Mert">Mert</p>
    </div>
  </div>
</section>

<section class="dukkan" aria-labelledby="dukkan-b">
  <figure class="dukkan__foto">
    <div class="kemer kemer--foto">{foto('dukkan-harita', 'b', None, '(min-width: 900px) 34vw, 86vw',
        "Dükkânın taş duvarındaki konum haritası; altında ayıcıklı gül aranjmanı")}</div>
  </figure>
  <div class="dukkan__metin">
    <h2 id="dukkan-b">Dükkân Surlariçi'nde, Girne Caddesi'nin üstünde.</h2>
    <address>{M['adres_satir1']}<br>{M['adres_satir2']}<br>{M['adres_sehir']}</address>
    <p>{M['tarif']}. Gelmeden bir arayın, buketiniz siz varana kadar hazır olsun.</p>
    <div class="vitrin__dugmeler">
      <a class="dugme" href="{M['harita']}" target="_blank" rel="noopener">Yol tarifi alın</a>
      <a class="dugme dugme--cizgi" href="tel:{M['tel_href']}">{IKON_TEL}{M['telefon']}</a>
    </div>
  </div>
</section>

</main>
""" + alt()


# --- çiçekler --------------------------------------------------------------

def cicekler():
    cipler = '<button class="cip" type="button" data-kat="hepsi" aria-pressed="true">Hepsi</button>' + "".join(
        f'<button class="cip" type="button" data-kat="{k["k"]}" aria-pressed="false">{k["ad"]}</button>'
        for k in KATEGORILER)
    kartlar = "".join(kart(u) for u in URUNLER)
    return kafa(
        "Çiçekler | Işıkcan Flora Shop, Lefkoşa",
        "Buketler, orkideler, kutu aranjmanlar, saksı çiçekleri ve ayıcıklı hediyeler. Hepsi Lefkoşa'daki dükkânımızda hazırlanıyor.",
        "cicekler.html") + ust("cicekler.html") + f"""<main id="icerik">
<section class="sayfa-bas">
  <h1>Çiçekler</h1>
  <p>Aşağıdakilerin hepsini biz hazırladık, fotoğraflarını da biz çektik. Fiyatı yazmayanlar boyuna ve mevsime göre değişiyor; yazın, hemen söyleyelim.</p>
</section>
<div class="arac">
  <div class="cipler" role="group" aria-label="Türe göre süz">{cipler}</div>
  <p class="arac__sayi" aria-live="polite"><span data-sayi>{len(URUNLER)}</span> çiçek</p>
</div>
<section class="izgara" aria-label="Çiçekler">{kartlar}</section>
<p class="izgara__bos" hidden>Bu türde şu an fotoğraflı ürün yok. <a href="{WA_GENEL}" target="_blank" rel="noopener">Yazın</a>, elimizdekini gönderelim.</p>
<aside class="yonlendir">
  <p>Saksı çiçeklerinin fiyatlarını ayrı bir listede topladık.</p>
  <a class="bag" href="saksi-fiyatlari.html">Saksı fiyat listesi {IKON_OK}</a>
</aside>
</main>
""" + alt()


# --- ürün sayfası ----------------------------------------------------------

def urun_sayfasi(u):
    ana = u["fotolar"][0]
    g, y = OLCU[ana]
    kucukler = ""
    if len(u["fotolar"]) > 1:
        kucukler = '<div class="galeri__kucuk" role="group" aria-label="Diğer fotoğraflar">' + "".join(
            f'<button type="button" data-foto="{f}" data-g="{OLCU[f][0]}" data-y="{OLCU[f][1]}" aria-label="{i + 1}. fotoğraf"'
            f'{" aria-current=" + chr(34) + "true" + chr(34) if i == 0 else ""}>'
            f'<img src="img/{f}-k-400.webp" width="80" height="100" alt="" loading="lazy"></button>'
            for i, f in enumerate(u["fotolar"])) + "</div>"
    icerik = ""
    if u.get("icerik"):
        icerik = '<ul class="urun__icerik">' + "".join(f"<li>{e(i)}</li>" for i in u["icerik"]) + "</ul>"
    bakim = f'<p class="urun__bakim"><b>Bakımı:</b> {e(u["bakim"])}</p>' if u.get("bakim") else ""
    if u["fiyat"]:
        fiyat = f'<p class="urun__fiyat">{tl(u["fiyat"])} <span>{u["tarih"]} fiyatı</span></p>'
    else:
        fiyat = '<p class="urun__fiyat urun__fiyat--sor">Fiyatı boyuna ve mevsime göre değişiyor. Yazın, hemen söyleyelim.</p>'
    benzer = [b for b in URUNLER if b["slug"] != u["slug"] and b["kat"][0] == u["kat"][0]][:4]
    if len(benzer) < 4:
        benzer += [b for b in URUNLER if b["slug"] != u["slug"] and b not in benzer][: 4 - len(benzer)]
    benzerler = "".join(kart(b, "(min-width: 900px) 22vw, 46vw", gecis=False) for b in benzer)
    kat_ad = next(k["ad"] for k in KATEGORILER if k["k"] == u["kat"][0])
    urun_ld = {"@context": "https://schema.org", "@type": "Product", "name": u["ad"],
               "description": u["metin"], "image": f"{SITE}img/{ana}-b-1300.webp",
               "brand": {"@type": "Brand", "name": M["ad"]}}
    if u["fiyat"]:
        urun_ld["offers"] = {"@type": "Offer", "price": u["fiyat"], "priceCurrency": "TRY",
                             "availability": "https://schema.org/InStock"}
    govde = kafa(f"{u['ad']} | Işıkcan Flora Shop, Lefkoşa", u["metin"], f"urun/{u['slug']}.html",
                 og=f"{ana}-b-1300.webp")
    govde = govde.replace("<head>", '<head>\n<base href="../">', 1)
    return govde + ust("cicekler.html") + f"""<main id="icerik">
<nav class="iz" aria-label="Konum"><a href="cicekler.html">Çiçekler</a><span aria-hidden="true">/</span><a href="cicekler.html#{u['kat'][0]}">{kat_ad}</a></nav>
<article class="urun" data-urun="{e(u['ad'])}" data-fiyat="{u['fiyat'] or ''}" data-kargo-ic="{M['kargo_ic']}" data-kargo-dis="{M['kargo_dis']}" data-wa="{M['whatsapp']}">
  <div class="galeri">
    <div class="galeri__ana" style="view-transition-name:u-{u['slug']}">
      <img id="galeri-ana" src="img/{ana}-b-800.webp" srcset="img/{ana}-b-800.webp {min(800, g)}w, img/{ana}-b-1300.webp {min(1300, g)}w"
        sizes="(min-width: 900px) 46vw, 100vw" width="800" height="{round(800 * y / g)}" alt="{e(u['alt'])}" fetchpriority="high">
    </div>
    {kucukler}
  </div>
  <div class="urun__panel">
    <h1>{e(u['ad'])}</h1>
    {fiyat}
    <p class="urun__metin">{e(u['metin'])}</p>
    {icerik}
    {bakim}

    <form class="siparis" id="siparis" novalidate>
      <h2>Siparişinizi hazırlayın</h2>
      <fieldset class="secim">
        <legend>Nereye gidecek?</legend>
        <label><input type="radio" name="teslim" value="ic" checked><span>Lefkoşa içi<b>{tl(M['kargo_ic'])}</b></span></label>
        <label><input type="radio" name="teslim" value="dis"><span>Lefkoşa dışı<b>{tl(M['kargo_dis'])}</b></span></label>
        <label><input type="radio" name="teslim" value="dukkan"><span>Dükkândan alacağım<b>Ücretsiz</b></span></label>
      </fieldset>
      <div class="siparis__ikili">
        <label class="alan"><span class="alan__etiket">Teslim günü</span><input type="date" name="gun"></label>
        <label class="alan"><span class="alan__etiket">Kime gidecek?</span><input type="text" name="alici" maxlength="60" placeholder="Alıcının adı" autocomplete="off"></label>
      </div>
      <label class="alan" data-adres><span class="alan__etiket">Teslimat adresi</span><input type="text" name="adres" maxlength="140" placeholder="Mahalle, sokak, bina" autocomplete="off"></label>
      <label class="alan"><span class="alan__etiket">Kart notu</span>
        <textarea name="not" rows="3" maxlength="160" placeholder="Karta ne yazalım?"></textarea>
        <span class="alan__say"><span data-not-say>0</span>/160</span></label>
      <label class="alan"><span class="alan__etiket">Karttaki imza</span><input type="text" name="imza" maxlength="40" placeholder="Adınız ya da isimsiz" autocomplete="off"></label>
      <div class="kartnot kartnot--kucuk" aria-hidden="true"><div class="kartnot__kagit">
        <span class="kartnot__marka">IŞIKCAN</span>
        <p class="kartnot__yazi" data-not-onizleme data-bos="Notunuz kartta böyle görünecek.">Notunuz kartta böyle görünecek.</p>
        <p class="kartnot__imza" data-imza-onizleme data-bos=""></p>
      </div></div>
      <dl class="siparis__ozet" aria-live="polite">
        <div><dt>Çiçek</dt><dd data-oz-cicek>{tl(u['fiyat']) if u['fiyat'] else 'Mesajda söyleyeceğiz'}</dd></div>
        <div><dt>Teslimat</dt><dd data-oz-kargo>{tl(M['kargo_ic'])}</dd></div>
        {'<div class="siparis__toplam"><dt>Toplam</dt><dd data-oz-toplam>' + tl(u['fiyat'] + M['kargo_ic']) + '</dd></div>' if u['fiyat'] else ''}
      </dl>
      <button class="dugme dugme--genis" type="submit">{IKON_WA}WhatsApp'tan siparişi gönderin</button>
      <p class="siparis__not">Düğme, yazdıklarınızı WhatsApp mesajına çevirir; göndermeden önce görürsünüz. Fiyatı ve teslim saatini mesajınıza dönerek onaylıyoruz.</p>
      <p class="siparis__diger">Aramayı mı tercih edersiniz? <a href="tel:{M['tel_href']}">{M['telefon']}</a> ya da <a href="{IG_DM}" target="_blank" rel="noopener">Instagram'dan yazın</a>.</p>
    </form>
  </div>
</article>
<section class="benzer" aria-labelledby="benzer-b">
  <h2 id="benzer-b">Buna da bakın</h2>
  <div class="izgara izgara--dort">{benzerler}</div>
</section>
<script type="application/ld+json">{json.dumps(urun_ld, ensure_ascii=False)}</script>
</main>
""" + alt()


# --- saksı fiyatları -------------------------------------------------------

def saksi_sayfasi():
    gruplar = []
    for s in SAKSI:
        if s["grup"] not in gruplar:
            gruplar.append(s["grup"])
    bolumler = ""
    for g in gruplar:
        satirlar = ""
        for s in (x for x in SAKSI if x["grup"] == g):
            ad = e(s["ad"]) + (f' <span class="fl__not">{e(s["not"])}</span>' if s.get("not") else "")
            if s.get("urun"):
                ad = f'<a href="urun/{s["urun"]}.html">{ad}</a>'
            ek = f' <span class="fl__ek">{s["ek"]}</span>' if s.get("ek") else ""
            mesaj = wa(f"Merhaba, {s['ad']}{' (' + s['not'] + ')' if s.get('not') else ''} için bilgi almak istiyorum. Listede {tl(s['fiyat'])} yazıyor.")
            satirlar += f"""<li class="fl__satir" data-ara="{e((s['ad'] + ' ' + s.get('not', '')).lower())}">
        <div class="fl__ad">{ad}<span class="fl__bakim">{e(s['bakim'])}</span></div>
        <div class="fl__tarih">{s['tarih']}</div>
        <div class="fl__fiyat">{tl(s['fiyat'])}{ek}</div>
        <a class="fl__sor" href="{mesaj}" target="_blank" rel="noopener" aria-label="{e(s['ad'])} için WhatsApp'tan yazın">Sorun</a>
      </li>"""
        bolumler += f'<section class="fl__grup" data-grup><h2>{g}</h2><ul class="fl">{satirlar}</ul></section>'
    return kafa(
        "Saksı çiçeği fiyatları | Işıkcan Flora Shop, Lefkoşa",
        "Kasımpatı, orkide, zamia, difenbahya, paşa kılıcı ve diğer saksı çiçeklerinin fiyatları ve kısa bakım notları.",
        "saksi-fiyatlari.html") + ust("saksi-fiyatlari.html") + f"""<main id="icerik">
<section class="sayfa-bas">
  <h1>Saksı çiçeği fiyatları</h1>
  <p>Her hafta bir saksı çiçeğini fiyatıyla paylaşıyoruz. Bu liste o paylaşımlardan derlendi; her satırın yanında fiyatın hangi aya ait olduğu yazıyor. Kargo ayrı: Lefkoşa içi {tl(M['kargo_ic'])}, Lefkoşa dışı {tl(M['kargo_dis'])}.</p>
</section>
<div class="arac arac--ara">
  <label class="ara"><span class="gizli">Listede ara</span><input type="search" id="fl-ara" placeholder="Bitki adı yazın: orkide, zamia, kasımpatı" autocomplete="off"></label>
  <p class="arac__sayi" aria-live="polite"><span data-fl-sayi>{len(SAKSI)}</span> bitki</p>
</div>
{bolumler}
<p class="izgara__bos" data-fl-bos hidden>Listede bu adla bitki yok. <a href="{WA_GENEL}" target="_blank" rel="noopener">Yazın</a>, dükkânda var mı bakalım.</p>
<aside class="yonlendir">
  <p>Nilüfer, su sümbülü gibi su bitkilerini sipariş üzerine getiriyoruz.</p>
  <a class="bag" href="ozel-gunler.html#siparis-uzerine">Sipariş üzerine gelenler {IKON_OK}</a>
</aside>
</main>
""" + alt()


# --- özel günler -----------------------------------------------------------

def ozel_gunler():
    return kafa(
        "Özel günler ve hizmetler | Işıkcan Flora Shop, Lefkoşa",
        "Araç süsleme, açılış çiçeği, bebek ve geçmiş olsun aranjmanları, kutlama süslemeleri ve özel gün hatırlatma.",
        "ozel-gunler.html") + ust("ozel-gunler.html") + f"""<main id="icerik">
<section class="sayfa-bas">
  <h1>Özel günler</h1>
  <p>Buketin dışında kalan işler: süsleme, kutlama, isme özel tasarım. Hepsini konuşarak planlıyoruz; tarihi ve aklınızdakini yazmanız yeter.</p>
</section>

<section class="takvim" aria-labelledby="takvim-b">
  <h2 id="takvim-b">Çiçekçinin takvimi</h2>
  <ol class="takvim__liste">
    <li data-gun="12-31"><b>Yılbaşı</b><span>Kokina ve yeni yıl aranjmanları</span></li>
    <li data-gun="02-14"><b>14 Şubat</b><span>Gül kutuları, ayıcıklı aranjmanlar</span></li>
    <li data-gun="03-08"><b>8 Mart</b><span>Kadınlar Günü buketleri</span></li>
    <li data-gun="anne"><b>Anneler Günü</b><span>Mayısın ikinci pazarı</span></li>
    <li data-gun="06-12"><b>12 Haziran</b><span>Kırmızı Gül Günü</span></li>
  </ol>
  <p class="takvim__not">Bu günlerde siparişler erken doluyor. Birkaç gün önceden yazarsanız çiçeğinizi ayırırız.</p>
</section>

<section class="hizmetler">
  <article class="hizmet">
    <div class="hizmet__foto">{foto('harf-kutusu-2', 'k', None, '(min-width: 900px) 28vw, 92vw', "E harfi biçimindeki siyah kutuda kırmızı güller")}</div>
    <div>
      <h2>İsme özel tasarımlar</h2>
      <p>Harf kutusu, şeffaf akrilik kutu, üzerine isim ve tarih yazılan silindir kutular. Harfi, ismi ya da tarihi yazmanız yeterli.</p>
      <a class="bag" href="urun/harf-kutusunda-kirmizi-gul.html">Harf kutusuna bakın {IKON_OK}</a>
    </div>
  </article>
  <article class="hizmet">
    <div class="hizmet__foto">{foto('ayicikli-sepet-1', 'k', None, '(min-width: 900px) 28vw, 92vw', "Beyaz peluş ayıcıklı, çikolatalı gül aranjmanı")}</div>
    <div>
      <h2>Bebek, doğum günü ve geçmiş olsun</h2>
      <p>Peluşlu aranjmanları en çok şu günler için hazırlıyoruz:</p>
      <ul class="hizmet__liste">
        <li>Baby shower ve cinsiyet partisi</li>
        <li>Hoş geldin bebek ziyareti</li>
        <li>Hastane odası süslemesi</li>
        <li>Geçmiş olsun ziyareti</li>
        <li>Doğum günü</li>
      </ul>
      <a class="bag" href="cicekler.html#ayicikli">Ayıcıklı hediyeler {IKON_OK}</a>
    </div>
  </article>
  <article class="hizmet hizmet--yazi">
    <div>
      <h2>Araç süsleme</h2>
      <p>Düğün, nişan ve sünnet arabaları için çiçek ve kurdele süslemesi. Aracın rengini ve töreni yazın, ona göre tasarlayalım.</p>
    </div>
    <div>
      <h2>Açılış ve tebrik çiçekleri</h2>
      <p>Açılış günü için ayaklı aranjmanlar ve canlı bitkiler. Kurdeleye yazılacak ismi siparişte alıyoruz.</p>
    </div>
    <div>
      <h2>Kutlama süslemeleri</h2>
      <p>Yarım yaş, doğum günü, evlilik teklifi gibi kutlamalar için çiçek tasarımı. Büyük organizasyonlar için Işıkcan Organizasyon ile birlikte çalışıyoruz.</p>
    </div>
    <div id="siparis-uzerine">
      <h2>Sipariş üzerine gelenler</h2>
      <p>Nilüfer, su sümbülü ve su marulu gibi su bitkilerini sipariş üzerine getiriyoruz. Listede olmayan bir çiçek arıyorsanız da yazın.</p>
    </div>
  </article>
</section>

<section class="hatirlat" aria-labelledby="hat-b">
  <div class="hatirlat__metin">
    <h2 id="hat-b">Tarihi bize bırakın.</h2>
    <p>Doğum gününü, yıl dönümünü yazın; yedi gün kala biz size haber verelim. Çiçeği o zaman seçersiniz.</p>
  </div>
  <form class="hatirlat__form" id="hatirlat" novalidate data-wa="{M['whatsapp']}">
    <label class="alan"><span class="alan__etiket">Hangi gün?</span><input type="text" name="gun_adi" maxlength="60" placeholder="Annemin doğum günü" autocomplete="off"></label>
    <label class="alan"><span class="alan__etiket">Tarihi</span><input type="date" name="tarih"></label>
    <button class="dugme dugme--acik" type="submit">{IKON_WA}Hatırlatma isteyin</button>
    <p class="siparis__not">Düğme bir WhatsApp mesajı hazırlar; gönderince tarihi not alıyoruz.</p>
  </form>
</section>
</main>
""" + alt()


# --- teslimat --------------------------------------------------------------

def teslimat():
    sss = [
        ("Nasıl sipariş veririm?",
         "Çiçeğin sayfasındaki formu doldurun; düğme yazdıklarınızı WhatsApp mesajına çevirir. İsterseniz doğrudan arayın ya da Instagram'dan yazın. Fiyatı ve teslim saatini mesajınıza dönerek onaylıyoruz."),
        ("KKTC dışından sipariş verebilir miyim?",
         "Evet. Türkiye'den ya da başka bir ülkeden yazıp KKTC'deki bir adrese çiçek gönderebilirsiniz. Ödeme seçeneklerini sipariş sırasında iletiyoruz."),
        ("Fotoğraftaki çiçeğin aynısı mı gelir?",
         "Fotoğraflar bizim hazırladığımız buketlerin fotoğrafı. Çiçek mevsime göre değiştiği için birebir aynısı olmayabilir; fark olacaksa hazırlamadan önce size söyleriz."),
        ("Kart notu nasıl gidiyor?",
         "Sipariş formundaki notu karta biz yazıp çiçeğin yanına koyuyoruz. İmza kısmını boş bırakırsanız kart isimsiz gider."),
        ("Fiyatı yazmayan çiçekler neden öyle?",
         "Buket ve kutu fiyatı boyuna, çiçeğin cinsine ve mevsime göre değişiyor. Yazdığınızda o günün fiyatını söylüyoruz."),
    ]
    sorular = "".join(f'<details class="soru" name="sss"><summary>{e(s)}</summary><p>{e(c)}</p></details>' for s, c in sss)
    sss_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": s, "acceptedAnswer": {"@type": "Answer", "text": c}} for s, c in sss]}
    return kafa(
        "Teslimat ve sipariş | Işıkcan Flora Shop, Lefkoşa",
        f"Lefkoşa içi teslimat {tl(M['kargo_ic'])}, Lefkoşa dışı {tl(M['kargo_dis'])}, dükkândan teslim ücretsiz. KKTC'ye çiçek gönderimi ve sipariş adımları.",
        "teslimat.html") + ust("teslimat.html") + f"""<main id="icerik">
<section class="sayfa-bas">
  <h1>Teslimat ve sipariş</h1>
  <p>Çiçeği Lefkoşa'daki dükkânda hazırlayıp adrese biz götürüyoruz. KKTC dışından da sipariş verebilirsiniz.</p>
</section>

<section class="ucretler" aria-labelledby="ucret-b">
  <h2 id="ucret-b" class="gizli">Teslimat ücretleri</h2>
  <div class="ucretler__kutu"><span class="ucretler__yer">Lefkoşa içi</span><b>{tl(M['kargo_ic'])}</b><span>Adrese teslim</span></div>
  <div class="ucretler__kutu"><span class="ucretler__yer">Lefkoşa dışı</span><b>{tl(M['kargo_dis'])}</b><span>Girne, Gazimağusa, Güzelyurt, İskele ve diğer bölgeler</span></div>
  <div class="ucretler__kutu"><span class="ucretler__yer">Dükkândan teslim</span><b>Ücretsiz</b><span>{M['tarif']}</span></div>
</section>

<section class="adimlar" aria-labelledby="adim-b">
  <h2 id="adim-b">Sipariş üç adım</h2>
  <ol class="adimlar__liste">
    <li><h3>Çiçeği seçin</h3><p>Çiçekler sayfasından beğendiğinizi açın. Aklınızdaki listede yoksa doğrudan yazın.</p></li>
    <li><h3>Yeri, günü ve notu yazın</h3><p>Nereye ve hangi gün gideceğini, alıcının adını ve kart notunu forma girin.</p></li>
    <li><h3>WhatsApp'tan gönderin</h3><p>Form mesajı hazırlar. Biz fiyatı ve teslim saatini dönerek onaylarız.</p></li>
  </ol>
  <a class="dugme" href="cicekler.html">Çiçekleri görün</a>
</section>

<section class="sss" aria-labelledby="sss-b">
  <h2 id="sss-b">Sık sorulanlar</h2>
  <div class="sss__liste">{sorular}</div>
</section>
<script type="application/ld+json">{json.dumps(sss_ld, ensure_ascii=False)}</script>
</main>
""" + alt()


# --- dükkân ----------------------------------------------------------------

def dukkan():
    return kafa(
        "Dükkân ve iletişim | Işıkcan Flora Shop, Lefkoşa",
        "Işıkcan Flora Shop: Girne Caddesi, İplik Pazarı, Vakıflar Pasajı No: 2, Lefkoşa. Telefon 0533 859 20 51.",
        "dukkan.html") + ust("dukkan.html") + f"""<main id="icerik">
<section class="sayfa-bas">
  <h1>Dükkân</h1>
  <p>Lefkoşa Surlariçi'nde, Girne Caddesi'ndeki Vakıflar Pasajı'ndayız. Eski Cemaat Meclisi binası diye de bilinir.</p>
</section>

<section class="yer">
  <figure class="yer__foto">
    <div class="kemer kemer--foto">{foto('dukkan-harita', 'b', None, '(min-width: 900px) 36vw, 86vw',
        "Dükkânın taş duvarındaki konum haritası; altında ayıcıklı gül aranjmanı", oncelik=True)}</div>
  </figure>
  <div class="yer__bilgi">
    <dl class="kunye">
      <div><dt>Adres</dt><dd><address>{M['adres_satir1']}<br>{M['adres_satir2']}<br>{M['adres_sehir']}</address></dd></div>
      <div><dt>Tarif</dt><dd>{M['tarif']}</dd></div>
      <div><dt>Telefon</dt><dd><a href="tel:{M['tel_href']}">{M['telefon']}</a></dd></div>
      <div><dt>Instagram</dt><dd><a href="{IG}" target="_blank" rel="noopener">@{M['instagram']}</a></dd></div>
    </dl>
    <div class="vitrin__dugmeler">
      <a class="dugme" href="{M['harita']}" target="_blank" rel="noopener">Yol tarifi alın</a>
      <a class="dugme dugme--cizgi" href="{WA_GENEL}" target="_blank" rel="noopener">{IKON_WA}WhatsApp'tan yazın</a>
    </div>
    <p class="yer__not">Gelmeden bir arayın; buketiniz siz varana kadar hazır olsun.</p>
  </div>
</section>

<section class="sokak" aria-labelledby="sokak-b">
  <div class="bolum-bas">
    <h2 id="sokak-b">Fotoğrafları neden sokakta çekiyoruz?</h2>
    <p>Çünkü çiçek bu sokaklardan geçip gidiyor. Büyük Han'ın avlusu, köşedeki kırmızı posta kutusu, Girne Caddesi'nin taş kaldırımı: buketi bitirince kapının önüne çıkıp öyle çekiyoruz. Stüdyo ışığı yok, gördüğünüz neyse o.</p>
  </div>
  <div class="sokak__sira">
    <figure>{foto('buyuk-han', 'k', None, '(min-width: 900px) 22vw, 46vw', "Pembe buket, Büyük Han'ın avlusunda")}<figcaption>Büyük Han</figcaption></figure>
    <figure>{foto('posta-kutusu', 'k', None, '(min-width: 900px) 22vw, 46vw', "Ayıcıklı gül aranjmanı, kırmızı posta kutusunun yanında")}<figcaption>Posta kutusunun yanı</figcaption></figure>
    <figure>{foto('bes-buket', 'k', None, '(min-width: 900px) 22vw, 46vw', "Beş kasımpatı buketi, Girne Caddesi'nin kaldırımında")}<figcaption>Girne Caddesi</figcaption></figure>
    <figure>{foto('bank-orkide', 'k', None, '(min-width: 900px) 22vw, 46vw', "Orkide ve kasımpatı aranjmanı, sokaktaki bankın üstünde")}<figcaption>Dükkânın önündeki bank</figcaption></figure>
  </div>
</section>
</main>
""" + alt()


# --- yardımcı dosyalar -----------------------------------------------------

def site_haritasi():
    sayfalar = [""] + [h for h, _ in GEZINTI] + [f"urun/{u['slug']}.html" for u in URUNLER]
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"  <url><loc>{SITE}{s}</loc></url>\n" for s in sayfalar) + "</urlset>\n")


def favicon():
    # Sekiz yapraklı rozet: logodaki altın çiçeğin sadeleştirilmiş hâli.
    yapraklar = "".join(
        f'<ellipse cx="32" cy="15" rx="5.5" ry="12" fill="#D9B45A" transform="rotate({a} 32 32)"/>'
        for a in range(0, 360, 45))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#1F3B30"/>{yapraklar}<circle cx="32" cy="32" r="6" fill="#1F3B30"/></svg>\n'


def main():
    def yaz(ad, icerik):
        # fotoğraf değişince tarayıcı eskisini önbellekten göstermesin
        icerik = re.sub(r'(img/[\w-]+\.(?:webp|jpg))(?=[" ])', r"\1?v=" + SURUM, icerik)
        (KOK / ad).write_text(icerik, encoding="utf-8")

    yaz("index.html", ana_sayfa())
    yaz("cicekler.html", cicekler())
    yaz("saksi-fiyatlari.html", saksi_sayfasi())
    yaz("ozel-gunler.html", ozel_gunler())
    yaz("teslimat.html", teslimat())
    yaz("dukkan.html", dukkan())
    (KOK / "urun").mkdir(exist_ok=True)
    for eski in (KOK / "urun").glob("*.html"):
        eski.unlink()
    for u in URUNLER:
        yaz(f"urun/{u['slug']}.html", urun_sayfasi(u))
    (KOK / "sitemap.xml").write_text(site_haritasi(), encoding="utf-8")
    (KOK / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n", encoding="utf-8")
    (KOK / "favicon.svg").write_text(favicon(), encoding="utf-8")
    print(f"{6 + len(URUNLER)} sayfa üretildi ({len(URUNLER)} ürün, {len(SAKSI)} saksı satırı).")


if __name__ == "__main__":
    main()
