# Programın sürekli çalışmasını sağlayan program

from PyQt6.QtWidgets import QApplication
from login import LoginForm

app = QApplication([])

pencere = LoginForm()
pencere.show()

app.exec()