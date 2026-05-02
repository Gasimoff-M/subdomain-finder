# 🌐 Subdomain Bulucu (Subdomain Enumerator)

Hedef domain için aktif subdomainleri DNS sorguları ve wordlist ile tespit eden Python tabanlı keşif aracı.

## 🚀 Özellikler

- 50 eş zamanlı thread ile hızlı DNS tarama
- 55 kelimelik yerleşik wordlist (api, dev, admin, vpn, vb.)
- Özel wordlist dosyası desteği
- Bulunan subdomainleri otomatik `.txt` dosyasına kaydeder
- Domain geçerlilik kontrolü
- Renkli terminal çıktısı ve detaylı rapor

## 📦 Kurulum

```bash
git clone https://github.com/Gasimoff-M/subdomain-finder
cd subdomain-finder
python subdomain_finder.py
```

> Python 3.x gereklidir. Harici kütüphane gerekmez.

## 💻 Kullanım

```
  Hedef domain: example.com

  Wordlist seçin:
  1 - Varsayılan liste (hızlı, 55 kelime)
  2 - Özel wordlist dosyası
  Seçiminiz [1/2]: 1
```

## 📊 Örnek Çıktı

```
  [*] Tarama başlıyor... (55 subdomain denenecek)
  [*] Aktif thread sayısı: 50

  [+] Bulundu: www.example.com                → 93.184.216.34
  [+] Bulundu: mail.example.com               → 93.184.216.50
  [+] Bulundu: api.example.com                → 93.184.216.60
  [+] Bulundu: dev.example.com                → 93.184.216.70

============================================================
  SUBDOMAIN TARAMA RAPORU
  Hedef  : example.com
  Tarih  : 02.05.2025 15:00:00
  Süre   : 3.42 saniye
============================================================
  [✓] 4 subdomain bulundu

  [✓] Sonuçlar kaydedildi: subdomains_example.com_20250502_150000.txt
```

## ⚠️ Yasal Uyarı

Bu araç yalnızca **eğitim amaçlı** ve **izin verilen domainlerde** kullanım içindir.

## 👤 Geliştirici

**Gasimoff-M** — [github.com/Gasimoff-M](https://github.com/Gasimoff-M)
