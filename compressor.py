import os
from PIL import Image
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QFileDialog, 
                            QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, 
                            QComboBox, QProgressBar, QMessageBox, QGroupBox, 
                            QGridLayout, QListWidget, QMenu)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class ImageCompressor(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Ana widget'ı oluştur
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Giriş ve çıkış klasörü seçimi için grup
        folder_group = QGroupBox("Klasör Seçimi")
        folder_layout = QVBoxLayout()
        folder_layout.setContentsMargins(0, 0, 0, 0)
        folder_layout.setSpacing(0)
        
        # Butonları ve etiketleri içeren container
        folder_container = QVBoxLayout()
        folder_container.setSpacing(0)
        
        # Butonları yan yana yerleştir
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)
        
        # Giriş butonu
        self.input_button = QPushButton("Giriş Klasörü Seç")
        self.input_button.setFixedHeight(30)
        
        # Çıkış butonu
        self.output_button = QPushButton("Çıkış Klasörü Seç")
        self.output_button.setFixedHeight(30)
        
        button_layout.addWidget(self.input_button)
        button_layout.addWidget(self.output_button)
        folder_container.addLayout(button_layout)
        
        # Seçilen klasör etiketleri
        self.input_folder_label = QLabel("")
        self.output_folder_label = QLabel("")
        self.input_folder_label.setStyleSheet("color: gray; margin: 0px 20px;")
        self.output_folder_label.setStyleSheet("color: gray; margin: 0px 0;")
        
        labels_layout = QHBoxLayout()
        labels_layout.setContentsMargins(0, 0, 0, 0)
        labels_layout.setSpacing(0)
        labels_layout.addWidget(self.input_folder_label)
        labels_layout.addWidget(self.output_folder_label)
        folder_container.addLayout(labels_layout)
        
        folder_layout.addLayout(folder_container)
        folder_group.setLayout(folder_layout)
        layout.addWidget(folder_group)
        
        # Dosya listesi bölümü
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(QLabel("Sıkıştırılacak Dosyalar:"))
        layout.addWidget(self.file_list)
        
        # Dosya işlem butonları
        file_actions = QHBoxLayout()
        self.undo_button = QPushButton("Geri Al")
        self.remove_button = QPushButton("Seçili Dosyaları Çıkar")
        self.sort_button = QPushButton("Dosyaları Sırala")
        file_actions.addWidget(self.undo_button)
        file_actions.addWidget(self.remove_button)
        file_actions.addWidget(self.sort_button)
        layout.addLayout(file_actions)
        
        # Ayarlar grubu
        settings_group = QGroupBox("Sıkıştırma Ayarları")
        settings_layout = QGridLayout()
        settings_layout.setContentsMargins(10, 10, 10, 10)
        settings_layout.setSpacing(5)
        
        # Kalite ayarı
        quality_label = QLabel("Kalite (1-100):")
        self.quality_spinbox = QSpinBox()
        self.quality_spinbox.setRange(1, 100)
        self.quality_spinbox.setValue(85)
        self.quality_spinbox.setFixedWidth(70)
        settings_layout.addWidget(quality_label, 0, 0)
        settings_layout.addWidget(self.quality_spinbox, 0, 1)
        
        # Maksimum boyut ayarı
        size_label = QLabel("Maksimum Boyut (px):")
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(100, 10000)
        self.size_spinbox.setValue(800)
        self.size_spinbox.setFixedWidth(70)
        settings_layout.addWidget(size_label, 1, 0)
        settings_layout.addWidget(self.size_spinbox, 1, 1)
        
        # Format seçimi
        format_label = QLabel("Çıktı Formatı:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["JPEG", "PNG", "WEBP"])
        self.format_combo.setFixedWidth(70)
        settings_layout.addWidget(format_label, 2, 0)
        settings_layout.addWidget(self.format_combo, 2, 1)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Sıkıştırma butonu
        compress_button = QPushButton("Sıkıştırmayı Başlat")
        compress_button.setFixedHeight(35)
        layout.addWidget(compress_button)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        
        # Buton bağlantıları
        self.input_button.clicked.connect(self.select_input_folder)
        self.output_button.clicked.connect(self.select_output_folder)
        self.undo_button.clicked.connect(self.undo_removal)
        self.remove_button.clicked.connect(self.remove_selected_files)
        self.sort_button.clicked.connect(self.sort_files)
        compress_button.clicked.connect(self.compress_images)
        
        # Başlangıç değerlerini ayarla
        self.input_folder = ""
        self.output_folder = ""
        
        # Pencere boyutu
        self.setFixedSize(380, 400)
        
        # Geri alma işlemi için geçmiş listesi
        self.removed_files = []

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Giriş Klasörü Seç")
        if folder:
            self.input_folder = folder
            self.input_folder_label.setText(f"Giriş: {os.path.basename(folder)}")
            self.refresh_file_list()
            self.removed_files.clear()  # Yeni klasör seçildiğinde geçmişi temizle

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Çıkış Klasörü Seç")
        if folder:
            self.output_folder = folder
            self.output_folder_label.setText(f"Çıkış: {os.path.basename(folder)}")

    def refresh_file_list(self):
        if not self.input_folder:
            return
        
        self.file_list.clear()
        for file in os.listdir(self.input_folder):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                self.file_list.addItem(file)

    def remove_selected_files(self):
        selected_items = self.file_list.selectedItems()
        # Silinen öğeleri geçmişe kaydet
        for item in selected_items:
            self.removed_files.append({
                'text': item.text(),
                'index': self.file_list.row(item)
            })
            self.file_list.takeItem(self.file_list.row(item))

    def undo_removal(self):
        if not self.removed_files:
            QMessageBox.information(self, "Bilgi", "Geri alınacak işlem bulunmuyor!")
            return
        
        # En son silinen öğeyi geri al
        last_removed = self.removed_files.pop()
        self.file_list.insertItem(last_removed['index'], last_removed['text'])

    def sort_files(self):
        # Sıralama seçenekleri için bir menü göster
        menu = QMenu(self)
        menu.addAction("A-Z", lambda: self.perform_sort(reverse=False))
        menu.addAction("Z-A", lambda: self.perform_sort(reverse=True))
        menu.addAction("Boyuta Göre (Büyükten Küçüğe)", lambda: self.perform_sort_by_size(reverse=True))
        menu.addAction("Boyuta Göre (Küçükten Büyüğe)", lambda: self.perform_sort_by_size(reverse=False))
        
        # Menüyü butonun altında göster
        menu.exec_(self.sort_button.mapToGlobal(self.sort_button.rect().bottomLeft()))

    def perform_sort(self, reverse=False):
        items = []
        for i in range(self.file_list.count()):
            items.append(self.file_list.item(i).text())
        
        items.sort(reverse=reverse)
        self.file_list.clear()
        self.file_list.addItems(items)

    def perform_sort_by_size(self, reverse=False):
        items = []
        for i in range(self.file_list.count()):
            file_name = self.file_list.item(i).text()
            file_path = os.path.join(self.input_folder, file_name)
            file_size = os.path.getsize(file_path)
            items.append((file_name, file_size))
        
        items.sort(key=lambda x: x[1], reverse=reverse)
        self.file_list.clear()
        self.file_list.addItems([item[0] for item in items])

    def compress_images(self):
        if not self.input_folder or not self.output_folder:
            QMessageBox.warning(self, "Uyarı", "Lütfen giriş ve çıkış klasörlerini seçin!")
            return
        
        # Sadece listede kalan dosyaları işle
        image_files = []
        for i in range(self.file_list.count()):
            file_name = self.file_list.item(i).text()
            image_files.append(os.path.join(self.input_folder, file_name))
        
        if not image_files:
            QMessageBox.warning(self, "Uyarı", "İşlenecek görüntü dosyası bulunamadı!")
            return
        
        self.progress_bar.setMaximum(len(image_files))
        self.progress_bar.setValue(0)
        
        error_shown = False
        
        for i, image_path in enumerate(image_files):
            try:
                # Görüntüyü aç
                img = Image.open(image_path)
                output_format = self.format_combo.currentText().lower()
                
                # RGBA'dan RGB'ye dönüşümü sadece JPEG için yap
                if output_format == 'jpeg' and img.mode == 'RGBA':
                    img = img.convert('RGB')
                
                # Boyut ayarla
                max_size = self.size_spinbox.value()
                ratio = min(max_size/float(img.size[0]), max_size/float(img.size[1]))
                if ratio < 1:
                    new_size = tuple([int(x*ratio) for x in img.size])
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Çıktı dosya adını oluştur
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                output_path = os.path.join(self.output_folder, f"{base_name}.{output_format}")
                
                # Kaydet
                if output_format == 'jpg':
                    output_format = 'jpeg'
                img.save(output_path, output_format, quality=self.quality_spinbox.value())
                
                self.progress_bar.setValue(i + 1)
                QApplication.processEvents()
                
            except Exception as e:
                if not error_shown:
                    QMessageBox.warning(self, "Hata", f"Görüntü işlenirken hata oluştu: {str(e)}")
                    error_shown = True
        
        QMessageBox.information(self, "Başarılı", "Görüntü sıkıştırma tamamlandı!")
        self.progress_bar.setValue(0)

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = ImageCompressor()
    window.show()
    sys.exit(app.exec_())