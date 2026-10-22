# BeePower Stok Takip Sistemi

Robot modülü bakım kayıtları ve stok takibi için masaüstü uygulama.

## Özellikler

- 🤖 **Robot Yönetimi** — Robot ekle/düzenle/sil
- 📋 **Kayıt Yönetimi** — Bakım ve değişim kayıtları (tamir tarihi, teknisyen, maliyet vb.)
- 📦 **Stok Yönetimi** — Modül envanteri; Kullanılabilir / Sorunlu / Kullanılamaz sekmeleri
- 🔍 **Akıllı Otomatik Tamamlama** — Kayıt girerken stoktaki modüller otomatik önerilir
- 🌐 **İki Dil** — Türkçe / İngilizce
- 🌙 **Koyu Tema** — Modern dark UI

## Kurulum

```bash
# 1. Gerekli kütüphaneleri yükle
pip install -r requirements.txt

# 2. Uygulamayı başlat
python main.py
```

> Python 3.11+ önerilir.

## Proje Yapısı

```
├── main.py           # Giriş noktası
├── database.py       # SQLite CRUD işlemleri
├── styles.py         # Renk paleti & stylesheet
├── i18n.py           # TR/EN çeviri sistemi
├── ui_main.py        # Ana pencere & navigasyon
├── ui_dashboard.py   # Dashboard sayfası
├── ui_robots.py      # Robot yönetim sayfası
├── ui_records.py     # Kayıt yönetim sayfası
├── ui_inventory.py   # Stok yönetim sayfası
└── requirements.txt
```

## Veritabanı

SQLite — `beepower_stock.db` dosyası uygulama ile aynı klasörde oluşturulur.
Sunucu gerekmez, veriler tamamen yerel bilgisayarda saklanır.

## Geliştirme

Katkı yapmak için fork'layıp PR açabilirsiniz.
# beepowerstoktakipsystem
