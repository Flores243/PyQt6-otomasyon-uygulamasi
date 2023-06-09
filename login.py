# kendi sınıf ve metotlarımızı oluituracağımız program

import sqlite3
from PyQt6.QtWidgets import *
from login_python import Ui_LoginForm
# anasayfayı buradan projeye ekliyoruz
from anasayfa import AnasayfaForm

class LoginForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.loginForm = Ui_LoginForm()
        self.loginForm.setupUi(self)
        self.anasayfa = AnasayfaForm()
        
        
        # eklediğim metotlar
        self.loginForm.btn_giris.clicked.connect(self.mesaj)
        self.loginForm.btn_cikis.clicked.connect(self.cikis)
        self.loginForm.btn_uyeol.clicked.connect(self.uyeol)
        self.loginForm.btn_parolaUnuttum.clicked.connect(self.parolaUnuttum)
    
    def baglan(self):
        try:
            with sqlite3.connect("otomasyon.db") as baglanti:
                self.imlec = baglanti.cursor()
                self.imlec.execute("create table if not exists tbl_kullanicilar(sicilno INT, username TEXT, password TEXT, eposta TEXT, rolu TEXT)")
                return baglanti
            
        except Exception as hata:
            print(hata)
    
    def parolaUnuttum(self):
        self.username = self.loginForm.txt_username.text()
        self.password = self.loginForm.txt_password.text()
        
        try:
            if(self.username != ""):
                self.baglan()
                self.imlec.execute("select * from tbl_kullanicilar")
                for kullanici in self.imlec.fetchall():
                    if(kullanici[1] == self.username):
                        QMessageBox.information(self, "Parola Hatırlat", f"{kullanici[2]} Listelendi")
                    else:
                        continue
            else:
                QMessageBox.critical(self, "Hata", "Kullanıcı Adı Boş Geçilemez")
                
        except Exception as hata:
            QMessageBox.critical(self, "Hata", f"{hata}\nHata Oluştu.")

    def cikis(self):
        exit(0)
        
    def giris(self):
        self.hide()
        self.anasayfa.show()
    
    def uyeol(self):
        from random import randint  # random modülü dahil ettik
        self.sicilNo = randint(10000, 99999)
        self.uyeUsername = self.loginForm.txt_uyeUsername.text()
        self.uyePassword = self.loginForm.txt_uyePassword.text()
        self.uyeEposta = self.loginForm.txt_uyeEmail.text()
        self.rol = self.loginForm.comboBox_rol.currentText() # combobox içindeki veriyi çek
        
        self.baglanti = self.baglan()
        self.imlec.execute(f"insert into tbl_kullanicilar values({self.sicilNo}, '{self.uyeUsername.lower()}', '{self.uyePassword}', '{self.uyeEposta}', '{self.rol}')")
        self.baglanti.commit()
        
        QMessageBox.information(self, "Üye Kayıt", f"{self.uyeUsername} Kullanıcısı Başarılı Bir Şekilde Kaydedilmiştir")

        # Temizleme
        self.loginForm.txt_uyeUsername.clear()
        self.loginForm.txt_uyePassword.clear()
        self.loginForm.txt_uyeEmail.clear()
        
    def mesaj(self):
        self.username = self.loginForm.txt_username.text()
        self.password = self.loginForm.txt_password.text()
        
        self.baglan()  # veritabanı oluşturuyoruz
        self.imlec.execute("select * from tbl_kullanicilar")
        
        
        for kullanici in self.imlec.fetchall():
            
            if (self.username == kullanici[1] and self.password == kullanici[2]):
                print(kullanici[1], kullanici[2])
                self.giris()
            else:
                print("Aranan Kayıt Bulunamadı")
                continue
                
        