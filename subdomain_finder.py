# =====================================================
# Subdomain Bulucu (Subdomain Enumerator)
# Geliştirici: Gasimoff-M
# Açıklama: Hedef domain için aktif subdomainleri
#            wordlist ve DNS sorgusu ile tespit eder
# =====================================================

import socket
import threading
import os
from datetime import datetime
from queue import Queue

# ─── Renk Kodları ──────────────────────────────────────
KIRMIZI = "\033[91m"
YESIL   = "\033[92m"
SARI    = "\033[93m"
MAVI    = "\033[94m"
SIFIRLA = "\033[0m"

# ─── Ayarlar ───────────────────────────────────────────
MAX_THREAD   = 50       # Aynı anda çalışacak maksimum thread sayısı
DNS_TIMEOUT  = 2        # DNS sorgusu zaman aşımı (saniye)

# ─── Yaygın Subdomain Wordlist ─────────────────────────
VARSAYILAN_WORDLIST = [
    "www", "mail", "ftp", "smtp", "pop", "imap",
    "webmail", "admin", "portal", "vpn", "remote",
    "dev", "staging", "test", "beta", "alpha",
    "api", "api2", "v1", "v2", "graphql",
    "shop", "store", "blog", "forum", "wiki",
    "cdn", "static", "assets", "media", "img",
    "m", "mobile", "app", "apps",
    "db", "database", "mysql", "mongo", "redis",
    "git", "gitlab", "github", "bitbucket", "ci",
    "jenkins", "jira", "confluence", "docs",
    "support", "help", "ticket", "crm",
    "monitor", "status", "health", "metrics",
    "backup", "ns1", "ns2", "dns", "mx",
    "secure", "ssl", "auth", "login", "sso",
    "cloud", "aws", "azure", "gcp",
    "internal", "intranet", "corp", "office",
]

# Bulunan subdomainleri sakla
bulunan_subdomainler = []
kuyruk = Queue()
print_lock = threading.Lock()


def dns_sorgula(subdomain, domain):
    """
    Verilen subdomain için DNS A kaydı sorgusu yapar.
    Başarılıysa IP adresi döndürür.
    """
    tam_domain = f"{subdomain}.{domain}"
    try:
        socket.setdefaulttimeout(DNS_TIMEOUT)
        ip = socket.gethostbyname(tam_domain)
        return tam_domain, ip
    except (socket.gaierror, socket.timeout):
        return None, None


def worker(domain):
    """
    Kuyruktan subdomain alıp DNS sorgusu yapan thread işçisi.
    """
    while not kuyruk.empty():
        subdomain = kuyruk.get()
        tam_domain, ip = dns_sorgula(subdomain, domain)

        if tam_domain and ip:
            with print_lock:
                print(f"  {YESIL}[+] Bulundu:{SIFIRLA} {tam_domain:<40} → {MAVI}{ip}{SIFIRLA}")
                bulunan_subdomainler.append({"subdomain": tam_domain, "ip": ip})

        kuyruk.task_done()


def wordlist_yukle(dosya_yolu):
    """
    Dosyadan wordlist okur. Yoksa varsayılan listeyi kullanır.
    """
    if dosya_yolu and os.path.exists(dosya_yolu):
        with open(dosya_yolu, "r", encoding="utf-8", errors="ignore") as f:
            kelimeler = [satir.strip() for satir in f if satir.strip()]
        print(f"  {YESIL}[*] Wordlist yüklendi: {len(kelimeler)} kelime{SIFIRLA}")
        return kelimeler
    else:
        print(f"  {SARI}[*] Varsayılan wordlist kullanılıyor: {len(VARSAYILAN_WORDLIST)} kelime{SIFIRLA}")
        return VARSAYILAN_WORDLIST


def tarama_baslat(domain, wordlist):
    """
    Tüm subdomainleri kuyruğa ekler ve threadleri başlatır.
    """
    # Kuyruğu doldur
    for kelime in wordlist:
        kuyruk.put(kelime)

    print(f"\n  {MAVI}[*] Tarama başlıyor... ({len(wordlist)} subdomain denenecek){SIFIRLA}")
    print(f"  {MAVI}[*] Aktif thread sayısı: {MAX_THREAD}{SIFIRLA}\n")

    threadler = []
    for _ in range(min(MAX_THREAD, len(wordlist))):
        t = threading.Thread(target=worker, args=(domain,))
        t.daemon = True
        threadler.append(t)
        t.start()

    # Tüm threadlerin bitmesini bekle
    for t in threadler:
        t.join()


def rapor_yazdir(domain, sure):
    """
    Tarama sonuçlarını raporlar ve dosyaya kaydeder.
    """
    print("\n" + "=" * 60)
    print(f"  SUBDOMAIN TARAMA RAPORU")
    print(f"  Hedef  : {domain}")
    print(f"  Tarih  : {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"  Süre   : {sure:.2f} saniye")
    print("=" * 60)

    if not bulunan_subdomainler:
        print(f"  {SARI}[!] Hiç subdomain bulunamadı.{SIFIRLA}")
    else:
        print(f"  {YESIL}[✓] {len(bulunan_subdomainler)} subdomain bulundu:{SIFIRLA}\n")
        for i, s in enumerate(bulunan_subdomainler, 1):
            print(f"  {i:3}. {s['subdomain']:<45} {s['ip']}")

        # Sonuçları dosyaya kaydet
        dosya_adi = f"subdomains_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(dosya_adi, "w") as f:
            f.write(f"# Subdomain Tarama — {domain}\n")
            f.write(f"# Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
            for s in bulunan_subdomainler:
                f.write(f"{s['subdomain']} → {s['ip']}\n")

        print(f"\n  {YESIL}[✓] Sonuçlar kaydedildi: {dosya_adi}{SIFIRLA}")

    print("=" * 60 + "\n")


# ─── Ana Program ───────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{MAVI}╔══════════════════════════════════════════╗")
    print("║      Subdomain Bulucu (Enumerator) v1.0  ║")
    print("║         github.com/Gasimoff-M            ║")
    print(f"╚══════════════════════════════════════════╝{SIFIRLA}")

    print(f"\n{SARI}  ⚠️  Yalnızca izin verilen domainlerde kullanın!{SIFIRLA}\n")

    # Hedef domain
    domain = input("  Hedef domain (örn: example.com): ").strip()
    domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").strip("/")

    # Wordlist seçimi
    print("\n  Wordlist seçin:")
    print("  1 - Varsayılan liste (hızlı, 55 kelime)")
    print("  2 - Özel wordlist dosyası")
    secim = input("  Seçiminiz [1/2]: ").strip()

    if secim == "2":
        dosya = input("  Wordlist dosya yolu: ").strip()
        wordlist = wordlist_yukle(dosya)
    else:
        wordlist = wordlist_yukle(None)

    # Domain varlığını kontrol et
    try:
        ana_ip = socket.gethostbyname(domain)
        print(f"\n  {YESIL}[✓] Domain doğrulandı: {domain} → {ana_ip}{SIFIRLA}")
    except socket.gaierror:
        print(f"\n  {KIRMIZI}[!] Domain çözümlenemedi: {domain}{SIFIRLA}")
        exit()

    # Taramayı başlat ve süreyi ölç
    baslangic = datetime.now()
    tarama_baslat(domain, wordlist)
    sure = (datetime.now() - baslangic).total_seconds()

    # Raporu yazdır
    rapor_yazdir(domain, sure)
