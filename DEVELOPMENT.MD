# PentaImageCompress Geliştirici Dokümantasyonu

## İçindekiler

1. Kurulum
2. Geliştirme
3. Build
4. Test
5. Dağıtım
6. Sorun Giderme

## 1. Kurulum

### Sistem Gereksinimleri

- macOS
- Python 3.12+
- Git

### Başlangıç Kurulumu

1. Projeyi klonla:
   ```
   git clone [repo-url]
   cd compressApp
   ```
2. Virtual environment oluştur:
   ```
   python3 -m venv venv
   ```
3. Virtual environment'ı aktifleştir:
   ```
   source venv/bin/activate
   ```
4. Bağımlılıkları yükle:
   ```
   pip install -r requirements.txt
   ```

## 2. Geliştirme

### Geliştirme Ortamını Başlatma

1. Virtual environment'ı aktifleştir:
   ```
   source venv/bin/activate
   ```

2. Uygulamayı çalıştır:
   ```
   python3 compressor.py
   ```

### Kod Yapısı

- `compressor.py`: Ana uygulama kodu
- `PentaImageCompress.spec`: PyInstaller yapılandırması
- `requirements.txt`: Bağımlılıklar
- `penta-compressor.icns`: Uygulama ikonu

## 3. Build

### Build Alma

1. Eski build'leri temizle:
   ```
   rm -rf build dist
   ```
2. PyInstaller ile build al:
   ```
   pyinstaller PentaImageCompress.spec
   ```
3. Gereksiz dosyaları temizle:
   ```
   rm -rf __pycache__
   rm -rf build
   rm -f .DS_Store
   ```

### Build Kontrol Listesi

- [ ] Virtual environment aktif
- [ ] Tüm bağımlılıklar güncel
- [ ] Testler başarılı
- [ ] Build başarıyla oluştu
- [ ] Uygulama çalışıyor

## 4. Test

### Uygulama Testi

1. Temel Fonksiyonlar:
   - Klasör seçimi çalışıyor mu?
   - Görsel sıkıştırma işlemi başarılı mı?
   - Progress bar doğru çalışıyor mu?

2. Format Testleri:
   - JPEG sıkıştırma
   - PNG sıkıştırma
   - WEBP sıkıştırma

3. Hata Senaryoları:
   - Boş klasör seçimi
   - Desteklenmeyen dosya formatları
   - İzin hataları

## 5. Dağıtım

### Dağıtım Öncesi

1. Version kontrolü
2. README güncellemesi
3. Bağımlılık kontrolü
4. Final testler

### Dağıtım Adımları

1. Son build'i al:
   ```
   pyinstaller PentaImageCompress.spec
   ```
2. Uygulamayı test et:
   ```
   open dist/PentaImageCompress.app
   ```
3. Applications klasörüne kopyala:
   ```
   cp -r dist/PentaImageCompress.app /Applications/
   ```

## 6. Sorun Giderme

### Genel Sorunlar

1. Virtual Environment Sorunları:
   ```bash
   deactivate
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. PyQt5 Hataları:
   ```bash
   pip uninstall PyQt5 PyQt5-Qt5 PyQt5-sip
   pip install PyQt5==5.15.11
   pip install PyQt5-Qt5==5.15.16
   pip install PyQt5-sip==12.13.0
   ```

3. Uygulama Açılmama Sorunu:
   ```bash
   # Terminal'den hata mesajlarını görmek için:
   ./dist/PentaImageCompress.app/Contents/MacOS/PentaImageCompress
   
   # İzin hatası varsa:
   chmod +x dist/PentaImageCompress.app/Contents/MacOS/PentaImageCompress
   
   # Quarantine (Karantina) özelliğini kaldırmak için:
   xattr -cr dist/PentaImageCompress.app
   ```

4. Build Sorunları:
   ```bash
   # Temiz build için:
   rm -rf build dist
   rm -rf __pycache__
   rm -f .DS_Store
   rm -rf build dist
   pyinstaller PentaImageCompress.spec
   chmod +x dist/PentaImageCompress.app/Contents/MacOS/PentaImageCompress
   xattr -cr dist/PentaImageCompress.app
   
   # Yeniden build al:
   pyinstaller PentaImageCompress.spec
   ```

### Hata Ayıklama Adımları

1. Terminal'den çalıştırarak hata mesajlarını kontrol edin
2. Uygulama izinlerini kontrol edin
3. macOS güvenlik ayarlarını kontrol edin:
   - System Preferences > Security & Privacy > General
   - "Allow apps downloaded from: App Store and identified developers"
4. Karantina özelliğini kaldırın
5. Gerekirse temiz build alın

### macOS Güvenlik Sorunları

1. Bilinmeyen Geliştirici Uyarısı:
   - Uygulamaya Finder'da sağ tıklayın
   - "Open" seçeneğini seçin
   - Açılan uyarı penceresinde tekrar "Open" tıklayın

2. Güvenlik İzinleri:
   - System Preferences > Security & Privacy
   - "Open Anyway" butonuna tıklayın

## Notlar

- Her değişiklik sonrası test yapın
- Commit öncesi build alın
- Version numarasını güncelleyin
- Dokümantasyonu güncel tutun

## İletişim

Sorularınız için: [iletişim bilgileri]
