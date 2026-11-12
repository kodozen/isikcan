/* Işıkcan Flora Shop — sayfa etkileşimleri. Kütüphane yok. */
(function () {
  "use strict";

  var $ = function (s, k) { return (k || document).querySelector(s); };
  var $$ = function (s, k) { return Array.prototype.slice.call((k || document).querySelectorAll(s)); };

  // Kart notu sayfalar arasında taşınsın; depo kapalıysa bellekte kalır.
  var bellek = {};
  var depo = {
    al: function (a) { try { return sessionStorage.getItem(a) || ""; } catch (e) { return bellek[a] || ""; } },
    yaz: function (a, d) { try { sessionStorage.setItem(a, d); } catch (e) { bellek[a] = d; } }
  };

  function tl(sayi) {
    return Math.round(sayi).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".") + " ₺";
  }

  function gecisle(is) {
    if (document.startViewTransition && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
      var g = document.startViewTransition(is);
      var yut = function () {};
      g.ready.catch(yut); g.finished.catch(yut); g.updateCallbackDone.catch(yut);
    } else { is(); }
  }

  /* --- üst bant ve menü --- */
  var kaydiMi = function () { document.documentElement.classList.toggle("kaydi", scrollY > 8); };
  kaydiMi();
  addEventListener("scroll", kaydiMi, { passive: true });

  var menu = $("#menu");
  if (menu) {
    $$('[data-ac="menu"]').forEach(function (d) {
      d.addEventListener("click", function () { menu.showModal(); });
    });
    menu.addEventListener("click", function (o) {
      if (o.target.closest("[data-kapat]") || o.target.closest("a")) menu.close();
    });
  }

  /* --- kart notu önizlemesi --- */
  function notBagla(kok, notAlani, imzaAlani) {
    if (!notAlani) return;
    var kutu = $(".kartnot", kok);
    var yazi = $("[data-not-onizleme]", kok);
    var imza = $("[data-imza-onizleme]", kok);
    var say = $("[data-not-say]", kok);
    var zaman;
    function ciz() {
      var n = notAlani.value.trim();
      yazi.textContent = n || yazi.dataset.bos;
      yazi.classList.toggle("bos", !n);
      if (imza && imzaAlani) {
        var i = imzaAlani.value.trim();
        imza.textContent = i || imza.dataset.bos;
        imza.classList.toggle("bos", !i && !!imza.dataset.bos);
      }
      if (say) say.textContent = notAlani.value.length;
    }
    function yazildi() {
      depo.yaz("isikcan-not", notAlani.value);
      if (imzaAlani) depo.yaz("isikcan-imza", imzaAlani.value);
      ciz();
      if (kutu) {
        kutu.classList.add("yaziyor");
        clearTimeout(zaman);
        zaman = setTimeout(function () { kutu.classList.remove("yaziyor"); }, 700);
      }
    }
    notAlani.value = depo.al("isikcan-not");
    if (imzaAlani) imzaAlani.value = depo.al("isikcan-imza");
    notAlani.addEventListener("input", yazildi);
    if (imzaAlani) imzaAlani.addEventListener("input", yazildi);
    ciz();
  }
  notBagla($(".notbant"), $("#ana-not"), $("#ana-imza"));

  /* --- çiçekler: süzgeç --- */
  var izgara = $("main > .izgara");
  var cipler = $$(".cip");
  if (izgara && cipler.length) {
    var kartlar = $$(".kart", izgara);
    var sayi = $("[data-sayi]");
    var bos = $("main > .izgara__bos");
    var gecerli = cipler.map(function (c) { return c.dataset.kat; });

    var uygula = function (kat) {
      var gorunen = 0;
      kartlar.forEach(function (k) {
        var uyar = kat === "hepsi" || k.dataset.kat.split(" ").indexOf(kat) > -1;
        k.hidden = !uyar;
        if (uyar) gorunen++;
      });
      cipler.forEach(function (c) { c.setAttribute("aria-pressed", String(c.dataset.kat === kat)); });
      if (sayi) sayi.textContent = gorunen;
      if (bos) bos.hidden = gorunen > 0;
    };

    $(".cipler").addEventListener("click", function (o) {
      var c = o.target.closest(".cip");
      if (!c) return;
      var kat = c.dataset.kat;
      history.replaceState(null, "", kat === "hepsi" ? location.pathname : "#" + kat);
      gecisle(function () { uygula(kat); });
    });

    var ilk = location.hash.slice(1);
    if (gecerli.indexOf(ilk) > -1) uygula(ilk);
    addEventListener("hashchange", function () {
      var k = location.hash.slice(1);
      uygula(gecerli.indexOf(k) > -1 ? k : "hepsi");
    });
  }

  /* --- ürün: galeri --- */
  var ana = $("#galeri-ana");
  if (ana) {
    $$(".galeri__kucuk button").forEach(function (d) {
      d.addEventListener("click", function () {
        if (d.hasAttribute("aria-current")) return;
        var f = d.dataset.foto, g = +d.dataset.g, y = +d.dataset.y;
        var v = (ana.getAttribute("src").split("?")[1] || "");
        v = v ? "?" + v : "";
        $$(".galeri__kucuk button").forEach(function (b) { b.removeAttribute("aria-current"); });
        d.setAttribute("aria-current", "true");
        ana.classList.add("degisiyor");
        var yeni = new Image();
        var tak = function () {
          ana.srcset = "img/" + f + "-b-800.webp" + v + " " + Math.min(800, g) + "w, img/" + f + "-b-1300.webp" + v + " " + Math.min(1300, g) + "w";
          ana.src = "img/" + f + "-b-800.webp" + v;
          ana.height = Math.round(800 * y / g);
          ana.classList.remove("degisiyor");
        };
        yeni.onload = tak; yeni.onerror = tak;
        yeni.src = "img/" + f + "-b-800.webp" + v;
      });
    });
  }

  /* --- ürün: sipariş formu --- */
  var form = $("#siparis");
  if (form) {
    var urun = $(".urun");
    var fiyat = parseFloat(urun.dataset.fiyat) || 0;
    var kargo = { ic: +urun.dataset.kargoIc, dis: +urun.dataset.kargoDis, dukkan: 0 };
    var yerAd = { ic: "Lefkoşa içi", dis: "Lefkoşa dışı", dukkan: "Dükkândan alacağım" };
    var gun = form.elements.gun;
    var adresAlani = $("[data-adres]", form);

    var bugun = new Date();
    var iso = function (t) {
      return t.getFullYear() + "-" + ("0" + (t.getMonth() + 1)).slice(-2) + "-" + ("0" + t.getDate()).slice(-2);
    };
    gun.min = iso(bugun);

    notBagla(form, form.elements.not, form.elements.imza);

    var ozetle = function () {
      var t = form.elements.teslim.value;
      $("[data-oz-kargo]", form).textContent = kargo[t] ? tl(kargo[t]) : "Ücretsiz";
      var top = $("[data-oz-toplam]", form);
      if (top) top.textContent = tl(fiyat + kargo[t]);
      adresAlani.hidden = t === "dukkan";
    };
    form.addEventListener("change", ozetle);
    ozetle();

    var hataGoster = function (alan, metin) {
      alan.classList.add("hata");
      if (!$(".alan__hata", alan)) {
        var h = document.createElement("span");
        h.className = "alan__hata";
        h.textContent = metin;
        alan.appendChild(h);
      }
      $("input", alan).focus();
    };
    form.elements.adres.addEventListener("input", function () {
      adresAlani.classList.remove("hata");
      var h = $(".alan__hata", adresAlani);
      if (h) h.remove();
    });

    form.addEventListener("submit", function (o) {
      o.preventDefault();
      var t = form.elements.teslim.value;
      var adres = form.elements.adres.value.trim();
      if (t !== "dukkan" && !adres) {
        hataGoster(adresAlani, "Çiçeğin gideceği adresi yazın.");
        return;
      }
      var s = ["Merhaba, sipariş vermek istiyorum.", ""];
      s.push("Çiçek: " + urun.dataset.urun + (fiyat ? " (" + tl(fiyat) + ")" : ""));
      s.push("Teslimat: " + yerAd[t] + (kargo[t] ? " (" + tl(kargo[t]) + ")" : ""));
      if (t !== "dukkan") s.push("Adres: " + adres);
      if (gun.value) {
        var p = gun.value.split("-");
        var tarih = new Date(+p[0], +p[1] - 1, +p[2]);
        s.push((t === "dukkan" ? "Alacağım gün: " : "Teslim günü: ") +
          tarih.toLocaleDateString("tr-TR", { day: "numeric", month: "long", year: "numeric", weekday: "long" }));
      }
      var alici = form.elements.alici.value.trim();
      if (alici) s.push("Alıcı: " + alici);
      var not = form.elements.not.value.trim();
      if (not) s.push("Kart notu: " + not);
      var imza = form.elements.imza.value.trim();
      if (not || imza) s.push("İmza: " + (imza || "isimsiz"));
      if (fiyat) s.push("Toplam: " + tl(fiyat + kargo[t]));
      s.push("", location.href.split("?")[0].split("#")[0]);
      window.open("https://wa.me/" + urun.dataset.wa + "?text=" + encodeURIComponent(s.join("\n")), "_blank", "noopener");
    });
  }

  /* --- saksı fiyat listesi: arama --- */
  var ara = $("#fl-ara");
  if (ara) {
    var satirlar = $$(".fl__satir");
    var sade = function (m) {
      return m.toLocaleLowerCase("tr").replace(/ç/g, "c").replace(/ğ/g, "g").replace(/ı/g, "i")
        .replace(/ö/g, "o").replace(/ş/g, "s").replace(/ü/g, "u");
    };
    satirlar.forEach(function (s) { s.dataset.ara = sade(s.dataset.ara); });
    ara.addEventListener("input", function () {
      var q = sade(ara.value.trim());
      var n = 0;
      satirlar.forEach(function (s) {
        var uyar = !q || s.dataset.ara.indexOf(q) > -1;
        s.hidden = !uyar;
        if (uyar) n++;
      });
      $$("[data-grup]").forEach(function (g) { g.hidden = !$(".fl__satir:not([hidden])", g); });
      $("[data-fl-sayi]").textContent = n;
      $("[data-fl-bos]").hidden = n > 0;
    });
  }

  /* --- özel günler: takvim ve hatırlatma --- */
  var takvim = $(".takvim__liste");
  if (takvim) {
    var simdi = new Date();
    simdi.setHours(0, 0, 0, 0);
    var anneler = function (yil) { // mayısın ikinci pazarı
      var g = new Date(yil, 4, 1);
      return new Date(yil, 4, 1 + ((7 - g.getDay()) % 7) + 7);
    };
    var maddeler = $$("li", takvim).map(function (li) {
      var t;
      if (li.dataset.gun === "anne") {
        t = anneler(simdi.getFullYear());
        if (t < simdi) t = anneler(simdi.getFullYear() + 1);
      } else {
        var p = li.dataset.gun.split("-");
        t = new Date(simdi.getFullYear(), +p[0] - 1, +p[1]);
        if (t < simdi) t.setFullYear(t.getFullYear() + 1);
      }
      return { li: li, kalan: Math.round((t - simdi) / 864e5) };
    }).sort(function (a, b) { return a.kalan - b.kalan; });
    maddeler.forEach(function (m, i) {
      var e = document.createElement("em");
      e.textContent = m.kalan === 0 ? "Bugün" : m.kalan + " gün kaldı";
      m.li.appendChild(e);
      if (i === 0) m.li.classList.add("yakin");
      takvim.appendChild(m.li);
    });
  }

  var hat = $("#hatirlat");
  if (hat) {
    hat.elements.tarih.min = new Date().toISOString().slice(0, 10);
    hat.addEventListener("submit", function (o) {
      o.preventDefault();
      var ad = hat.elements.gun_adi.value.trim();
      var t = hat.elements.tarih.value;
      var alan = hat.elements.tarih.closest(".alan");
      if (!t) {
        alan.classList.add("hata");
        if (!$(".alan__hata", alan)) {
          var h = document.createElement("span");
          h.className = "alan__hata";
          h.textContent = "Hatırlatacağımız tarihi seçin.";
          alan.appendChild(h);
        }
        hat.elements.tarih.focus();
        return;
      }
      var p = t.split("-");
      var gunYazi = new Date(+p[0], +p[1] - 1, +p[2]).toLocaleDateString("tr-TR", { day: "numeric", month: "long", year: "numeric" });
      var m = "Merhaba, özel gün hatırlatması istiyorum.\n\n" + (ad ? "Gün: " + ad + "\n" : "") +
        "Tarih: " + gunYazi + "\n\nYedi gün kala haber verir misiniz?";
      window.open("https://wa.me/" + hat.dataset.wa + "?text=" + encodeURIComponent(m), "_blank", "noopener");
    });
    hat.elements.tarih.addEventListener("input", function () {
      var alan = hat.elements.tarih.closest(".alan");
      alan.classList.remove("hata");
      var h = $(".alan__hata", alan);
      if (h) h.remove();
    });
  }
})();
