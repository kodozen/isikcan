# Işıkcan Flora Shop

Lefkoşa Surlariçi'ndeki Işıkcan Flora Shop için hazırlanan web sitesinin
önizlemesi. Dükkânın onayıyla yayına alınacaktır; şu an arama motorlarına
kapalıdır.

Canlı önizleme: https://kodozen.github.io/isikcan/

## Sayfalar

| Dosya | İçerik |
|---|---|
| `index.html` | Ana sayfa: vitrin, kasımpatı sezonu, çiçek türleri, kart notu, dükkân |
| `cicekler.html` | 30 ürün, türe göre süzgeç |
| `urun/*.html` | Ürün fotoğrafları, açıklama, WhatsApp sipariş formu |
| `saksi-fiyatlari.html` | Saksı çiçeklerinin fiyatları ve bakım notları |
| `ozel-gunler.html` | Çiçekçi takvimi, hizmetler, özel gün hatırlatma |
| `teslimat.html` | Teslimat ücretleri, sipariş adımları, sık sorulanlar |
| `dukkan.html` | Adres, telefon, yol tarifi |

Fotoğraflar, fiyatlar ve ürün bilgileri dükkânın Instagram hesabından
(@isikcanflorashop) alınmıştır.

## Güncelleme

Ürünler, fiyatlar ve iletişim bilgileri `urunler.json` dosyasında. Değiştirip
sayfaları yeniden üretin:

```bash
python3 uret.py
```

Statik HTML, CSS ve JavaScript; kütüphane ya da derleme gerekmez.

## Yerelde açmak

```bash
python3 -m http.server 4177
```

Hazırlayan: [Kodozen](https://kodozen.github.io)
