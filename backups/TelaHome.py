from PySide6.QtWidgets import QApplication, QMainWindow, QTextBrowser, QPlainTextEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Define o tamanho inicial da janela
        self.resize(1366, 768)

        # Cria o widget central
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.layout = QVBoxLayout(self.central_widget)

        # Cria um QTextBrowser
        self.textBrowser = QTextBrowser()
        self.layout.addWidget(self.textBrowser)

        # Cria um QPlainTextEdit
        self.plainTextEdit = QPlainTextEdit()
        self.layout.addWidget(self.plainTextEdit)

        # Cria um QTextEdit
        self.textEdit = QTextEdit()
        self.layout.addWidget(self.textEdit)

        # Cria botões
        self.button_layout = QHBoxLayout()
        self.pushButton_5 = QPushButton("Configurações")
        self.pushButton_6 = QPushButton("Relatórios")
        self.pushButton_7 = QPushButton("Conexões")
        self.pushButton_8 = QPushButton("Home")

        self.button_layout.addWidget(self.pushButton_5)
        self.button_layout.addWidget(self.pushButton_6)
        self.button_layout.addWidget(self.pushButton_7)
        self.button_layout.addWidget(self.pushButton_8)
        self.layout.addLayout(self.button_layout)

    def resizeEvent(self, event):
        """
        Método chamado sempre que a janela é redimensionada.
        Aqui, ajustamos o tamanho dos widgets manualmente.
        """
        super().resizeEvent(event)

        # Obtém o tamanho atual da janela
        window_width = self.width()
        window_height = self.height()

        # Ajusta o tamanho do QTextBrowser
        self.textBrowser.setGeometry(10, 10, window_width - 20, window_height // 3)

        # Ajusta o tamanho do QPlainTextEdit
        self.plainTextEdit.setGeometry(10, window_height // 3 + 20, window_width - 20, window_height // 3)

        # Ajusta o tamanho do QTextEdit
        self.textEdit.setGeometry(10, 2 * window_height // 3 + 30, window_width - 20, window_height // 3 - 40)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()