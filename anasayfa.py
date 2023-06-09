from PyQt6.QtWidgets import *
from anasayfa_python import Ui_Form_Anasayfa
import sqlite3
from PyQt6.QtGui import QPixmap   # gorseli ekrana bastırma
from random import randint  # ogrno için rasgele sayı üret


class AnasayfaForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.anasayfa = Ui_Form_Anasayfa()
        self.anasayfa.setupUi(self)    
        
        # Metotlarım
        self.anasayfa.btn_fotoEkle.clicked.connect(self.fileDialog)
        self.anasayfa.btn_ekle.clicked.connect(self.ekle)
        self.anasayfa.btn_listele.clicked.connect(self.listele)
        
    def baglan(self):
        try:
            with sqlite3.connect("otomasyon.db") as baglanti:
                self.imlec = baglanti.cursor()
                self.imlec.execute("create table if not exists tbl_ogrenciler(ogrNo TEXT, ogrenciAdi TEXT, ogrenciSoyadi TEXT, dogumtarihi TEXT, telefon TEXT, eposta TEXT, fakulte TEXT, bolum TEXT, sinif TEXT, egitimTuru TEXT, fotograf TEXT)")
                return baglanti
            
        except Exception as hata:
            QMessageBox.critical(self, "Veritabanı Hatası", f"{hata} \nHata Oluştu.")
        
    def fileDialog(self):
        # filedialog nesnesi eklediğimiz yer
        self.dosyaYol = QFileDialog.getOpenFileName(self, "Fotoğraf Seç", "Görsel Seç", "jpg Dosyası (*.jpg);; png Dosyası (*.png)",)
        
        # görseli ekrana bastırma
        label = self.anasayfa.label_foto  # hangi nesnede gösterileceğini belirtiyoruz
        pixmap = QPixmap(self.dosyaYol[0])  # dosya yolunu belirtiyoruz
        label.setPixmap(pixmap)  # label ve pixmap verilerini birleştir
    
    def ekle(self):
        rasgele = randint(1000, 9999)
        self.ogrNo = self.anasayfa.txt_ogrNo.text()
        self.adi = self.anasayfa.txt_ad.text()
        self.soyadi = self.anasayfa.txt_soyad.text()
        self.dtarihi = self.anasayfa.date_dtarihi.text()
        self.telefon = self.anasayfa.txt_telefon.text()
        self.eposta = self.anasayfa.txt_eposta.text()
        
        self.fakulte = self.anasayfa.comboBox_fakulte.currentText()
        self.bolum = self.anasayfa.comboBox_bolum.currentText()
        self.sinif = self.anasayfa.comboBox_sinif.currentText()
        self.egitimTuru = self.anasayfa.comboBox_egitimTuru.currentText()
        
        self.ogrNo = (self.fakulte[0] + self.bolum[0] + str(rasgele)).upper()
        
        try:
            if(self.adi != "" and self.soyadi != "" and self.telefon != "" and self.eposta != ""):
                baglanti = self.baglan()
                self.imlec.execute(f"insert into tbl_ogrenciler values('{self.ogrNo}','{self.adi}','{self.soyadi}','{self.dtarihi}','{self.telefon}','{self.eposta}','{self.fakulte}','{self.bolum}','{self.sinif}','{self.egitimTuru}','{self.dosyaYol[0]}') ")   
                baglanti.commit()  # eklemeyi onaylıyoruz
                QMessageBox.information(self, "Ekle", f"{self.ogrNo} Kayıtlı Öğrenci Sisteme Kaydedilmiştir.")
            else:
                QMessageBox.warning(self, "Ekle", "Bilgiler Boş Geçilemez")
            
        except Exception as hata:
            QMessageBox.critical(self, "Ekle Hatası", f"Bilinmeyen Hata Oluştu\n{hata}")
            print(hata)
            
    def listele(self):
        # tablo üzerinde işlemler
        tablo = self.anasayfa.tableWidget
        tablo.clear()
        try:
            self.baglan()
            self.imlec.execute("select * from tbl_ogrenciler")
            ogrenciler = self.imlec.fetchall()
            kolonlar = ["Öğrenci No", "Adı", "Soyadı", "Doğum Tarihi", "Telefon", "E-Posta", "Fakülte", "Bölüm", "Sınıf", "Eğitim Türü", "Fotoğraf", "Özelleştir"]
            # tablonun başlık bilgilerini Ayarla
            tablo.setHorizontalHeaderLabels(kolonlar)
            
            # Öğrenci tablosu doluysa verileri Satır olarak getir
            if (ogrenciler != False):
                # öğrenci tablosunda kaç kayıt varsa o kadar satır oluştur
                tablo.setRowCount(len(ogrenciler))
                satirSayisi = 0
                
                for ogrenci in ogrenciler:
                    tablo.setItem(satirSayisi, 0, QTableWidgetItem(str(ogrenci[0])))
                    tablo.setItem(satirSayisi, 1, QTableWidgetItem(str(ogrenci[1])))
                    tablo.setItem(satirSayisi, 2, QTableWidgetItem(str(ogrenci[2])))
                    tablo.setItem(satirSayisi, 3, QTableWidgetItem(str(ogrenci[3])))
                    tablo.setItem(satirSayisi, 4, QTableWidgetItem(str(ogrenci[4])))
                    tablo.setItem(satirSayisi, 5, QTableWidgetItem(str(ogrenci[5])))
                    tablo.setItem(satirSayisi, 6, QTableWidgetItem(str(ogrenci[6])))
                    tablo.setItem(satirSayisi, 7, QTableWidgetItem(str(ogrenci[7])))
                    tablo.setItem(satirSayisi, 8, QTableWidgetItem(str(ogrenci[8])))
                    tablo.setItem(satirSayisi, 9, QTableWidgetItem(str(ogrenci[9])))
                    tablo.setItem(satirSayisi, 10, QTableWidgetItem(str(ogrenci[10])))
                    tablo.setItem(satirSayisi, 11, QTableWidgetItem("Güncelle / Sil"))
                    

                    satirSayisi += 1  
            else:
                QMessageBox.warning(self, "Sistem Hatası", "Öğrenci Tablosu Boş")
            
        except Exception as hata:
            QMessageBox.critical(self, "Listele Hatası", f"Bilinmeyen bir hata oluştu\n{hata}")