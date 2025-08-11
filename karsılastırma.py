import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import os

class KitapKarsilastirmaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.tum_veriler = pd.DataFrame()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Modern Veri Seti Karşılaştırma Uygulaması')
        self.setGeometry(100, 100, 800, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                color: #333;
                font-family: Arial, sans-serif;
            }
            QLabel#header {
                font-size: 24px;
                font-weight: bold;
                color: #1877f2;
                margin-bottom: 20px;
            }
            QPushButton {
                background-color: #1877f2;
                color: white;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #125699;
            }
            QLineEdit {
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            QTextEdit {
                border-radius: 5px;
                border: 1px solid #ccc;
                padding: 10px;
            }
            #loadedFiles {
                font-style: italic;
                color: #555;
            }
            #duplicatesButton {
                background-color: #e44d3a;
            }
            #duplicatesButton:hover {
                background-color: #b3392b;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        header = QLabel('Veri Seti Karşılaştırması')
        header.setObjectName("header")
        main_layout.addWidget(header, alignment=Qt.AlignCenter)

        load_layout = QHBoxLayout()
        self.load_button = QPushButton('Veri Seti Yükle')
        self.load_button.clicked.connect(self.verileri_yukle)
        self.file_label = QLabel('Yüklü Dosyalar: Hiçbiri')
        self.file_label.setObjectName("loadedFiles")
        load_layout.addWidget(self.load_button)
        load_layout.addWidget(self.file_label)
        main_layout.addLayout(load_layout)

        search_layout = QHBoxLayout()
        search_label = QLabel('Aramak İstediğiniz Kelime:')
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Örn: Sefiller")
        self.search_button = QPushButton('Karşılaştır')
        self.search_button.clicked.connect(self.kitap_karsilastir)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        main_layout.addLayout(search_layout)

        self.duplicates_button = QPushButton('Aynı Başlığa Sahip Verileri Göster')
        self.duplicates_button.setObjectName("duplicatesButton")
        self.duplicates_button.clicked.connect(self.ayni_kitaplari_goster)
        main_layout.addWidget(self.duplicates_button)

        result_label = QLabel('Sonuçlar:')
        self.result_output = QTextEdit()
        font = QFont("Courier", 10)
        self.result_output.setFont(font)
        self.result_output.setReadOnly(True)
        main_layout.addWidget(result_label)
        main_layout.addWidget(self.result_output)

        self.setLayout(main_layout)

    def verileri_yukle(self):
        options = QFileDialog.Options()
        filenames, _ = QFileDialog.getOpenFileNames(self, "Veri Setlerini Seçin", "", "CSV Dosyaları (*.csv)", options=options)

        if filenames:
            self.tum_veriler = pd.DataFrame()
            yuklenen_dosyalar = []

            for filename in filenames:
                try:
                    df = pd.read_csv(filename, encoding="utf-8-sig")

                    if 'Baslik' in df.columns:
                        df.rename(columns={'Baslik': 'Başlık'}, inplace=True)

                    if 'Başlık' not in df.columns:
                        QMessageBox.warning(self, "Hata", f"{os.path.basename(filename)} dosyasında 'Başlık' sütunu bulunamadı. Lütfen geçerli bir dosya seçin.")
                        continue

                    df['Kaynak'] = os.path.basename(filename).split('.')[0]

                    self.tum_veriler = pd.concat([self.tum_veriler, df], ignore_index=True)
                    yuklenen_dosyalar.append(os.path.basename(filename))
                except Exception as e:
                    QMessageBox.warning(self, "Hata", f"{os.path.basename(filename)} dosyası yüklenirken bir hata oluştu: {e}")

            if not self.tum_veriler.empty:
                self.file_label.setText(f"Yüklü Dosyalar: {', '.join(yuklenen_dosyalar)}")
                QMessageBox.information(self, "Başarılı", f"Toplam {len(self.tum_veriler)} adet veri yüklendi.")
            else:
                self.file_label.setText("Yüklü Dosyalar: Hiçbiri")

    def kitap_karsilastir(self):
        arama_kelimesi = self.search_input.text().strip().lower()
        self.result_output.clear()

        if self.tum_veriler.empty:
            self.result_output.setText("Hata: Lütfen önce bir veri seti yükleyin.")
            return

        if 'Başlık' not in self.tum_veriler.columns:
            self.result_output.setText("Hata: Yüklenen veri setinde 'Başlık' sütunu bulunamadı.")
            return

        if not arama_kelimesi:
            self.result_output.setText("Lütfen aramak istediğiniz kelimeyi girin.")
            return

        bulunan_kayitlar = self.tum_veriler[self.tum_veriler['Başlık'].str.lower().str.contains(arama_kelimesi, na=False)]

        if not bulunan_kayitlar.empty:
            sonuc_metni = f"'{arama_kelimesi}' kelimesini içeren kayıtlar:\n"
            sonuc_metni += "=" * 50 + "\n"

            for index, row in bulunan_kayitlar.iterrows():
                sonuc_metni += f"Başlık: {row.get('Başlık', 'Yok')}\n"

                for col in row.index:
                    if col != 'Başlık' and pd.notna(row[col]):
                        sonuc_metni += f"{col}: {row[col]}\n"

                sonuc_metni += "=" * 50 + "\n"

            self.result_output.setText(sonuc_metni)
        else:
            self.result_output.setText(f"'{arama_kelimesi}' kelimesini içeren bir kayıt bulunamadı.")

    def ayni_kitaplari_goster(self):
        self.result_output.clear()

        if self.tum_veriler.empty:
            self.result_output.setText("Hata: Lütfen önce bir veri seti yükleyin.")
            return

        if 'Başlık' not in self.tum_veriler.columns:
            self.result_output.setText("Hata: Yüklenen veri setinde 'Başlık' sütunu bulunamadı.")
            return

        ayni_basliklar = self.tum_veriler[self.tum_veriler.duplicated(subset=['Başlık'], keep=False)].sort_values(by='Başlık')

        if not ayni_basliklar.empty:
            sonuc_metni = "Farklı sitelerde bulunan aynı kitaplar:\n"
            sonuc_metni += "=" * 50 + "\n"

            for baslik, grup in ayni_basliklar.groupby('Başlık'):
                sonuc_metni += f"Kitap Adı: {baslik}\n"

                grup_kayitlari = [row for index, row in grup.iterrows()]

                kayit_verileri = []
                for row in grup_kayitlari:
                    kayit = ""
                    kayit += f"Kaynak: {row.get('Kaynak', 'Bilinmiyor')}\n"
                    kayit += f"Yazar: {row.get('Yazar', 'Yok')}\n"
                    kayit += f"Yayınevi: {row.get('Yayınevi', 'Yok')}\n"

                    fiyatlar = []
                    if pd.notna(row.get('İndirimli Fiyat (TL)')):
                        fiyatlar.append(f"İndirimli: {row['İndirimli Fiyat (TL)']} TL")
                    if pd.notna(row.get('İndirimsiz Fiyat (TL)')):
                        fiyatlar.append(f"Normal: {row['İndirimsiz Fiyat (TL)']} TL")
                    if pd.notna(row.get('Fiyat (TL)')):
                        fiyatlar.append(f"Fiyat: {row['Fiyat (TL)']} TL")
                    if pd.notna(row.get('Sepette Fiyat (TL)')):
                        fiyatlar.append(f"Sepette Fiyat: {row['Sepette Fiyat (TL)']} TL")

                    kayit += f"Fiyat Bilgileri: {', '.join(fiyatlar)}\n"
                    kayit_verileri.append(kayit)

                max_lines = max([len(k.split('\n')) for k in kayit_verileri])

                for i in range(max_lines):
                    satir = ""
                    for kayit in kayit_verileri:
                        satirlar = kayit.split('\n')
                        satir += f"{satirlar[i]:<40}"
                    sonuc_metni += satir + "\n"

                sonuc_metni += "=" * 50 + "\n"

            self.result_output.setText(sonuc_metni)
        else:
            self.result_output.setText("Farklı veri setlerinde aynı başlığa sahip kayıt bulunamadı.")


if __name__ == '__main__':
    try:
        if sys.getdefaultencoding() != 'utf-8':
            import importlib
            importlib.reload(sys)
            sys.setdefaultencoding('utf-8')
    except:
        pass

    app = QApplication(sys.argv)
    ex = KitapKarsilastirmaApp()
    ex.show()
    sys.exit(app.exec_())