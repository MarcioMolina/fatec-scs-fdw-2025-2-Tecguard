# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Home_tabwidget_dark_hdiFczNU.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QComboBox, QFormLayout, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QRadioButton, QSizePolicy,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1360, 768)
        MainWindow.setStyleSheet(u"background-color: #202020")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tabHome = QTabWidget(self.centralwidget)
        self.tabHome.setObjectName(u"tabHome")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabHome.sizePolicy().hasHeightForWidth())
        self.tabHome.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(12)
        self.tabHome.setFont(font)
        self.tabHome.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.tabHome.setStyleSheet(u"background-color:#202020;\n"
"color: white")
        self.tabHome.setElideMode(Qt.TextElideMode.ElideNone)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.label_Background = QLabel(self.tab)
        self.label_Background.setObjectName(u"label_Background")
        self.label_Background.setEnabled(True)
        self.label_Background.setGeometry(QRect(510, 130, 811, 491))
        self.label_Background.setTextFormat(Qt.TextFormat.PlainText)
        self.label_Background.setPixmap(QPixmap(u"images/imagem_logo-removebg-preview_new.png"))
        self.label_Background.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_Alertanotif = QLabel(self.tab)
        self.label_Alertanotif.setObjectName(u"label_Alertanotif")
        self.label_Alertanotif.setGeometry(QRect(430, 170, 241, 36))
        self.label_Alertanotif.setStyleSheet(u"font: 16pt \"Segoe UI\";")
        self.label_CoEstabelecidas = QLabel(self.tab)
        self.label_CoEstabelecidas.setObjectName(u"label_CoEstabelecidas")
        self.label_CoEstabelecidas.setGeometry(QRect(420, 360, 281, 21))
        self.label_CoEstabelecidas.setStyleSheet(u"font: 16pt \"Segoe UI\";")
        self.button_Conexoes = QPushButton(self.tab)
        self.button_Conexoes.setObjectName(u"button_Conexoes")
        self.button_Conexoes.setGeometry(QRect(500, 410, 96, 24))
        self.button_Conexoes.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_Conexoes.setStyleSheet(u"color: black;\n"
"background-color:darkorange")
        self.button_Conexoes.setAutoDefault(False)
        self.button_Conexoes.setFlat(False)
        self.label_SetaDownload = QLabel(self.tab)
        self.label_SetaDownload.setObjectName(u"label_SetaDownload")
        self.label_SetaDownload.setGeometry(QRect(450, 590, 31, 31))
        self.label_SetaDownload.setPixmap(QPixmap(u"images/imgsetacima.png"))
        self.label_SetaDownload.setScaledContents(True)
        self.verticalWidget = QWidget(self.tab)
        self.verticalWidget.setObjectName(u"verticalWidget")
        self.verticalWidget.setGeometry(QRect(170, 50, 211, 581))
        self.verticalLayout_imagens = QVBoxLayout(self.verticalWidget)
        self.verticalLayout_imagens.setObjectName(u"verticalLayout_imagens")
        self.label_ImgAlerta = QLabel(self.verticalWidget)
        self.label_ImgAlerta.setObjectName(u"label_ImgAlerta")
        self.label_ImgAlerta.setPixmap(QPixmap(u"images/iconeataquepequeno_menor.png"))

        self.verticalLayout_imagens.addWidget(self.label_ImgAlerta, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.label_ImgConexoes = QLabel(self.verticalWidget)
        self.label_ImgConexoes.setObjectName(u"label_ImgConexoes")
        self.label_ImgConexoes.setPixmap(QPixmap(u"images/iconeconexoespequeno_menor.png"))

        self.verticalLayout_imagens.addWidget(self.label_ImgConexoes, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.label_ImgRede = QLabel(self.verticalWidget)
        self.label_ImgRede.setObjectName(u"label_ImgRede")
        self.label_ImgRede.setEnabled(False)
        self.label_ImgRede.setMaximumSize(QSize(16777215, 512))
        self.label_ImgRede.setTextFormat(Qt.TextFormat.RichText)
        self.label_ImgRede.setPixmap(QPixmap(u"images/interneticonepequeno_menor.png"))
        self.label_ImgRede.setScaledContents(False)

        self.verticalLayout_imagens.addWidget(self.label_ImgRede, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.label_Download = QLabel(self.tab)
        self.label_Download.setObjectName(u"label_Download")
        self.label_Download.setGeometry(QRect(510, 520, 131, 41))
        self.label_Download.setMinimumSize(QSize(0, 41))
        self.label_Download.setStyleSheet(u"font: 16pt \"Segoe UI\";")
        self.label_ConexoesAtivas = QLabel(self.tab)
        self.label_ConexoesAtivas.setObjectName(u"label_ConexoesAtivas")
        self.label_ConexoesAtivas.setGeometry(QRect(420, 292, 231, 41))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(24)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_ConexoesAtivas.setFont(font1)
        self.label_ConexoesAtivas.setStyleSheet(u"font: 24pt \"Segoe UI\";")
        self.label_UsodaRede = QLabel(self.tab)
        self.label_UsodaRede.setObjectName(u"label_UsodaRede")
        self.label_UsodaRede.setGeometry(QRect(420, 470, 171, 31))
        self.label_UsodaRede.setStyleSheet(u"font: 24pt \"Segoe UI\";")
        self.label_SetaUpload = QLabel(self.tab)
        self.label_SetaUpload.setObjectName(u"label_SetaUpload")
        self.label_SetaUpload.setGeometry(QRect(450, 530, 31, 31))
        self.label_SetaUpload.setPixmap(QPixmap(u"images/imgsetabaixo2.png"))
        self.label_SetaUpload.setScaledContents(True)
        self.label_Alerta = QLabel(self.tab)
        self.label_Alerta.setObjectName(u"label_Alerta")
        self.label_Alerta.setGeometry(QRect(430, 90, 311, 51))
        self.label_Alerta.setFont(font1)
        self.label_Alerta.setStyleSheet(u"font: 24pt \"Segoe UI\";")
        self.label_Alerta.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_Upload = QLabel(self.tab)
        self.label_Upload.setObjectName(u"label_Upload")
        self.label_Upload.setGeometry(QRect(510, 590, 131, 31))
        self.label_Upload.setStyleSheet(u"font: 16pt \"Segoe UI\";")
        self.tabHome.addTab(self.tab, "")
        self.TabPolitica = QWidget()
        self.TabPolitica.setObjectName(u"TabPolitica")
        self.TabPolitica.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.label_background = QLabel(self.TabPolitica)
        self.label_background.setObjectName(u"label_background")
        self.label_background.setGeometry(QRect(710, 30, 1422, 800))
        self.label_background.setPixmap(QPixmap(u"images/imgbackground.png"))
        self.label_background.setScaledContents(True)
        self.label_background.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.verticalWidget_2 = QWidget(self.TabPolitica)
        self.verticalWidget_2.setObjectName(u"verticalWidget_2")
        self.verticalWidget_2.setGeometry(QRect(170, 90, 471, 451))
        self.verticalWidget_2.setStyleSheet(u"color: white;")
        self.verticalLayout_CriacaoACL = QVBoxLayout(self.verticalWidget_2)
        self.verticalLayout_CriacaoACL.setObjectName(u"verticalLayout_CriacaoACL")
        self.label_CriacaoACL = QLabel(self.verticalWidget_2)
        self.label_CriacaoACL.setObjectName(u"label_CriacaoACL")
        self.label_CriacaoACL.setStyleSheet(u"background-color: 	#FF8C00;\n"
"font: 20pt \"Segoe UI\"")

        self.verticalLayout_CriacaoACL.addWidget(self.label_CriacaoACL)

        self.horizontalWidget_CriacaoACL = QWidget(self.verticalWidget_2)
        self.horizontalWidget_CriacaoACL.setObjectName(u"horizontalWidget_CriacaoACL")
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalWidget_CriacaoACL)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalFrame_nomeOpes = QFrame(self.horizontalWidget_CriacaoACL)
        self.verticalFrame_nomeOpes.setObjectName(u"verticalFrame_nomeOpes")
        self.verticalLayout = QVBoxLayout(self.verticalFrame_nomeOpes)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_nomeACL = QLabel(self.verticalFrame_nomeOpes)
        self.label_nomeACL.setObjectName(u"label_nomeACL")
        font2 = QFont()
        font2.setPointSize(11)
        self.label_nomeACL.setFont(font2)

        self.verticalLayout.addWidget(self.label_nomeACL)

        self.label_comecoIP = QLabel(self.verticalFrame_nomeOpes)
        self.label_comecoIP.setObjectName(u"label_comecoIP")
        self.label_comecoIP.setFont(font)

        self.verticalLayout.addWidget(self.label_comecoIP)

        self.label_FinalIP = QLabel(self.verticalFrame_nomeOpes)
        self.label_FinalIP.setObjectName(u"label_FinalIP")
        self.label_FinalIP.setFont(font)

        self.verticalLayout.addWidget(self.label_FinalIP)

        self.label_Protocolo = QLabel(self.verticalFrame_nomeOpes)
        self.label_Protocolo.setObjectName(u"label_Protocolo")
        self.label_Protocolo.setFont(font)

        self.verticalLayout.addWidget(self.label_Protocolo)

        self.label_Direcao = QLabel(self.verticalFrame_nomeOpes)
        self.label_Direcao.setObjectName(u"label_Direcao")
        self.label_Direcao.setFont(font)

        self.verticalLayout.addWidget(self.label_Direcao)

        self.label_Acao = QLabel(self.verticalFrame_nomeOpes)
        self.label_Acao.setObjectName(u"label_Acao")
        self.label_Acao.setFont(font)

        self.verticalLayout.addWidget(self.label_Acao)


        self.horizontalLayout_2.addWidget(self.verticalFrame_nomeOpes)

        self.verticalWidget_opcoes = QWidget(self.horizontalWidget_CriacaoACL)
        self.verticalWidget_opcoes.setObjectName(u"verticalWidget_opcoes")
        self.verticalLayout_3 = QVBoxLayout(self.verticalWidget_opcoes)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lineEdit_nomeACL = QLineEdit(self.verticalWidget_opcoes)
        self.lineEdit_nomeACL.setObjectName(u"lineEdit_nomeACL")
        self.lineEdit_nomeACL.setFont(font)

        self.verticalLayout_3.addWidget(self.lineEdit_nomeACL)

        self.lineEdit_comecoIP = QLineEdit(self.verticalWidget_opcoes)
        self.lineEdit_comecoIP.setObjectName(u"lineEdit_comecoIP")
        self.lineEdit_comecoIP.setFont(font)

        self.verticalLayout_3.addWidget(self.lineEdit_comecoIP)

        self.lineEdit_FinalIP = QLineEdit(self.verticalWidget_opcoes)
        self.lineEdit_FinalIP.setObjectName(u"lineEdit_FinalIP")
        self.lineEdit_FinalIP.setFont(font)

        self.verticalLayout_3.addWidget(self.lineEdit_FinalIP)

        self.comboBox_protocolo = QComboBox(self.verticalWidget_opcoes)
        self.comboBox_protocolo.addItem("")
        self.comboBox_protocolo.addItem("")
        self.comboBox_protocolo.setObjectName(u"comboBox_protocolo")
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.comboBox_protocolo.setFont(font3)
        self.comboBox_protocolo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.comboBox_protocolo.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.verticalLayout_3.addWidget(self.comboBox_protocolo)

        self.comboBox_direcao = QComboBox(self.verticalWidget_opcoes)
        self.comboBox_direcao.addItem("")
        self.comboBox_direcao.addItem("")
        self.comboBox_direcao.setObjectName(u"comboBox_direcao")
        self.comboBox_direcao.setFont(font3)
        self.comboBox_direcao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.comboBox_direcao.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.verticalLayout_3.addWidget(self.comboBox_direcao)

        self.comboBox_acao = QComboBox(self.verticalWidget_opcoes)
        self.comboBox_acao.addItem("")
        self.comboBox_acao.addItem("")
        self.comboBox_acao.setObjectName(u"comboBox_acao")
        self.comboBox_acao.setFont(font3)
        self.comboBox_acao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.comboBox_acao.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.verticalLayout_3.addWidget(self.comboBox_acao)


        self.horizontalLayout_2.addWidget(self.verticalWidget_opcoes)


        self.verticalLayout_CriacaoACL.addWidget(self.horizontalWidget_CriacaoACL)

        self.widget = QWidget(self.verticalWidget_2)
        self.widget.setObjectName(u"widget")
        self.gridLayout_Servicos = QGridLayout(self.widget)
        self.gridLayout_Servicos.setObjectName(u"gridLayout_Servicos")
        self.checkBox_SSH = QCheckBox(self.widget)
        self.checkBox_SSH.setObjectName(u"checkBox_SSH")
        self.checkBox_SSH.setFont(font3)
        self.checkBox_SSH.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.checkBox_SSH.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.gridLayout_Servicos.addWidget(self.checkBox_SSH, 2, 1, 1, 1)

        self.checkBox_Telnet = QCheckBox(self.widget)
        self.checkBox_Telnet.setObjectName(u"checkBox_Telnet")
        self.checkBox_Telnet.setFont(font3)
        self.checkBox_Telnet.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.checkBox_Telnet.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.gridLayout_Servicos.addWidget(self.checkBox_Telnet, 3, 1, 1, 1)

        self.checkBox_RPC = QCheckBox(self.widget)
        self.checkBox_RPC.setObjectName(u"checkBox_RPC")
        self.checkBox_RPC.setFont(font3)
        self.checkBox_RPC.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.checkBox_RPC.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.gridLayout_Servicos.addWidget(self.checkBox_RPC, 5, 1, 1, 1)

        self.label_outros = QLabel(self.widget)
        self.label_outros.setObjectName(u"label_outros")
        self.label_outros.setFont(font3)
        self.label_outros.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.gridLayout_Servicos.addWidget(self.label_outros, 9, 0, 1, 1)

        self.checkBox_HTTP = QCheckBox(self.widget)
        self.checkBox_HTTP.setObjectName(u"checkBox_HTTP")
        self.checkBox_HTTP.setFont(font3)
        self.checkBox_HTTP.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.checkBox_HTTP.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.gridLayout_Servicos.addWidget(self.checkBox_HTTP, 0, 1, 1, 1)

        self.checkBox_DNS = QCheckBox(self.widget)
        self.checkBox_DNS.setObjectName(u"checkBox_DNS")
        self.checkBox_DNS.setFont(font3)
        self.checkBox_DNS.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.checkBox_DNS.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.gridLayout_Servicos.addWidget(self.checkBox_DNS, 8, 1, 1, 1)

        self.checkBox_FTP = QCheckBox(self.widget)
        self.checkBox_FTP.setObjectName(u"checkBox_FTP")
        self.checkBox_FTP.setFont(font3)
        self.checkBox_FTP.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.checkBox_FTP.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.gridLayout_Servicos.addWidget(self.checkBox_FTP, 1, 1, 1, 1)

        self.label_servicos = QLabel(self.widget)
        self.label_servicos.setObjectName(u"label_servicos")
        self.label_servicos.setFont(font3)
        self.label_servicos.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.gridLayout_Servicos.addWidget(self.label_servicos, 0, 0, 2, 1)

        self.lineEdit_outros = QLineEdit(self.widget)
        self.lineEdit_outros.setObjectName(u"lineEdit_outros")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit_outros.sizePolicy().hasHeightForWidth())
        self.lineEdit_outros.setSizePolicy(sizePolicy1)
        self.lineEdit_outros.setFont(font3)
        self.lineEdit_outros.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.gridLayout_Servicos.addWidget(self.lineEdit_outros, 9, 1, 1, 1)

        self.checkBox_NetBIOS = QCheckBox(self.widget)
        self.checkBox_NetBIOS.setObjectName(u"checkBox_NetBIOS")
        self.checkBox_NetBIOS.setFont(font3)
        self.checkBox_NetBIOS.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.checkBox_NetBIOS.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.gridLayout_Servicos.addWidget(self.checkBox_NetBIOS, 6, 1, 1, 1)

        self.checkBox_iCMP = QCheckBox(self.widget)
        self.checkBox_iCMP.setObjectName(u"checkBox_iCMP")
        self.checkBox_iCMP.setFont(font3)
        self.checkBox_iCMP.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.checkBox_iCMP.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.gridLayout_Servicos.addWidget(self.checkBox_iCMP, 4, 1, 1, 1)

        self.checkBox_SNMP = QCheckBox(self.widget)
        self.checkBox_SNMP.setObjectName(u"checkBox_SNMP")
        self.checkBox_SNMP.setFont(font3)
        self.checkBox_SNMP.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.checkBox_SNMP.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.gridLayout_Servicos.addWidget(self.checkBox_SNMP, 7, 1, 1, 1)


        self.verticalLayout_CriacaoACL.addWidget(self.widget)

        self.label_TabACL = QLabel(self.TabPolitica)
        self.label_TabACL.setObjectName(u"label_TabACL")
        self.label_TabACL.setGeometry(QRect(710, 10, 621, 33))
        self.label_TabACL.setMinimumSize(QSize(0, 33))
        self.label_TabACL.setStyleSheet(u"background-color:#FF8C00;\n"
"font: 20pt \"Segoe UI\"")
        self.tableWidget = QTableWidget(self.TabPolitica)
        if (self.tableWidget.columnCount() < 7):
            self.tableWidget.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font);
        __qtablewidgetitem.setBackground(QColor(54, 54, 54));
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font);
        __qtablewidgetitem1.setBackground(QColor(54, 54, 54));
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font);
        __qtablewidgetitem2.setBackground(QColor(54, 54, 54));
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font);
        __qtablewidgetitem3.setBackground(QColor(54, 54, 54));
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font);
        __qtablewidgetitem4.setBackground(QColor(54, 54, 54));
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFont(font);
        __qtablewidgetitem5.setBackground(QColor(54, 54, 54));
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setFont(font);
        __qtablewidgetitem6.setBackground(QColor(54, 54, 54));
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(710, 50, 621, 281))
        self.tableWidget.setStyleSheet(u"color:white;")
        self.tableWidget.horizontalHeader().setDefaultSectionSize(155)
        self.button_CriarACL = QPushButton(self.TabPolitica)
        self.button_CriarACL.setObjectName(u"button_CriarACL")
        self.button_CriarACL.setGeometry(QRect(190, 560, 75, 25))
        self.button_CriarACL.setFont(font3)
        self.button_CriarACL.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_CriarACL.setStyleSheet(u"color: black;\n"
"background-color: 	#FF8C00;\n"
"font: 10pt \"Segoe UI\";")
        self.button_CriarACL.setAutoDefault(False)
        self.button_CriarACL.setFlat(False)
        self.label_TabACL_2 = QLabel(self.TabPolitica)
        self.label_TabACL_2.setObjectName(u"label_TabACL_2")
        self.label_TabACL_2.setGeometry(QRect(710, 340, 621, 33))
        self.label_TabACL_2.setStyleSheet(u"background-color: #FF8C00;\n"
"font: 20pt \"Segoe UI\";\n"
"color:White;")
        self.button_RemoverACL = QPushButton(self.TabPolitica)
        self.button_RemoverACL.setObjectName(u"button_RemoverACL")
        self.button_RemoverACL.setGeometry(QRect(540, 560, 86, 25))
        self.button_RemoverACL.setFont(font3)
        self.button_RemoverACL.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_RemoverACL.setStyleSheet(u"color: black;\n"
"background-color: 	#FF8C00;\n"
"font: 10pt \"Segoe UI\";")
        self.button_RemoverACL.setAutoDefault(False)
        self.button_RemoverACL.setFlat(False)
        self.button_ImportarACL = QPushButton(self.TabPolitica)
        self.button_ImportarACL.setObjectName(u"button_ImportarACL")
        self.button_ImportarACL.setGeometry(QRect(360, 560, 86, 25))
        self.button_ImportarACL.setFont(font3)
        self.button_ImportarACL.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_ImportarACL.setStyleSheet(u"color: black;\n"
"background-color: 	#FF8C00;\n"
"font: 10pt \"Segoe UI\";")
        self.button_ImportarACL.setAutoDefault(False)
        self.button_ImportarACL.setFlat(False)
        self.tableWidget_2 = QTableWidget(self.TabPolitica)
        if (self.tableWidget_2.columnCount() < 7):
            self.tableWidget_2.setColumnCount(7)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setFont(font);
        __qtablewidgetitem7.setBackground(QColor(54, 54, 54));
        self.tableWidget_2.setHorizontalHeaderItem(0, __qtablewidgetitem7)
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.NoBrush)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setFont(font);
        __qtablewidgetitem8.setBackground(QColor(54, 54, 54));
        __qtablewidgetitem8.setForeground(brush);
        self.tableWidget_2.setHorizontalHeaderItem(1, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setFont(font);
        __qtablewidgetitem9.setBackground(QColor(54, 54, 54));
        self.tableWidget_2.setHorizontalHeaderItem(2, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setFont(font);
        __qtablewidgetitem10.setBackground(QColor(54, 54, 54));
        self.tableWidget_2.setHorizontalHeaderItem(3, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setFont(font);
        __qtablewidgetitem11.setBackground(QColor(54, 54, 54));
        self.tableWidget_2.setHorizontalHeaderItem(4, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setFont(font);
        __qtablewidgetitem12.setBackground(QColor(54, 54, 54));
        self.tableWidget_2.setHorizontalHeaderItem(5, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setFont(font);
        __qtablewidgetitem13.setBackground(QColor(54, 54, 54));
        self.tableWidget_2.setHorizontalHeaderItem(6, __qtablewidgetitem13)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        self.tableWidget_2.setGeometry(QRect(710, 380, 621, 301))
        self.tableWidget_2.setStyleSheet(u"color: white;")
        self.tableWidget_2.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_2.setTabKeyNavigation(True)
        self.tableWidget_2.setProperty(u"showDropIndicator", True)
        self.tableWidget_2.setDragDropOverwriteMode(True)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(155)
        self.tabHome.addTab(self.TabPolitica, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.label_Background_2 = QLabel(self.tab_3)
        self.label_Background_2.setObjectName(u"label_Background_2")
        self.label_Background_2.setEnabled(True)
        self.label_Background_2.setGeometry(QRect(800, 60, 1281, 761))
        self.label_Background_2.setPixmap(QPixmap(u"images/ChatGPT_Image_12_de_abr._de_2025__18_25_05-removebg-preview new.png"))
        self.label_Background_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.table_Conexoes = QTableWidget(self.tab_3)
        if (self.table_Conexoes.columnCount() < 7):
            self.table_Conexoes.setColumnCount(7)
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setFont(font);
        __qtablewidgetitem14.setBackground(QColor(255, 140, 0));
        __qtablewidgetitem14.setForeground(brush1);
        self.table_Conexoes.setHorizontalHeaderItem(0, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setFont(font);
        __qtablewidgetitem15.setBackground(QColor(255, 140, 0));
        self.table_Conexoes.setHorizontalHeaderItem(1, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setFont(font);
        __qtablewidgetitem16.setBackground(QColor(255, 140, 0));
        self.table_Conexoes.setHorizontalHeaderItem(2, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        __qtablewidgetitem17.setFont(font);
        __qtablewidgetitem17.setBackground(QColor(255, 140, 0));
        self.table_Conexoes.setHorizontalHeaderItem(3, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        __qtablewidgetitem18.setFont(font);
        __qtablewidgetitem18.setBackground(QColor(255, 140, 0));
        self.table_Conexoes.setHorizontalHeaderItem(4, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        __qtablewidgetitem19.setFont(font);
        __qtablewidgetitem19.setBackground(QColor(255, 140, 0));
        self.table_Conexoes.setHorizontalHeaderItem(5, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        __qtablewidgetitem20.setFont(font);
        __qtablewidgetitem20.setBackground(QColor(255, 140, 0));
        self.table_Conexoes.setHorizontalHeaderItem(6, __qtablewidgetitem20)
        self.table_Conexoes.setObjectName(u"table_Conexoes")
        self.table_Conexoes.setGeometry(QRect(0, 0, 1360, 768))
        self.table_Conexoes.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.PointingHandCursor))
        self.table_Conexoes.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.table_Conexoes.setAutoFillBackground(False)
        self.table_Conexoes.setStyleSheet(u"color: white;\n"
"")
        self.table_Conexoes.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.table_Conexoes.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.table_Conexoes.setAlternatingRowColors(False)
        self.table_Conexoes.setShowGrid(True)
        self.table_Conexoes.setGridStyle(Qt.PenStyle.SolidLine)
        self.table_Conexoes.setSortingEnabled(False)
        self.table_Conexoes.horizontalHeader().setVisible(True)
        self.table_Conexoes.horizontalHeader().setCascadingSectionResizes(True)
        self.table_Conexoes.horizontalHeader().setDefaultSectionSize(183)
        self.table_Conexoes.horizontalHeader().setHighlightSections(True)
        self.table_Conexoes.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.table_Conexoes.horizontalHeader().setStretchLastSection(False)
        self.table_Conexoes.verticalHeader().setVisible(False)
        self.table_Conexoes.verticalHeader().setCascadingSectionResizes(False)
        self.table_Conexoes.verticalHeader().setHighlightSections(False)
        self.table_Conexoes.verticalHeader().setProperty(u"showSortIndicator", False)
        self.table_Conexoes.verticalHeader().setStretchLastSection(False)
        self.tabHome.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.widget1 = QWidget(self.tab_4)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(810, 660, 201, 51))
        self.horizontalLayout = QHBoxLayout(self.widget1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_relatorio = QPushButton(self.widget1)
        self.pushButton_relatorio.setObjectName(u"pushButton_relatorio")
        self.pushButton_relatorio.setStyleSheet(u"background-color: rgb(54,54,54);\n"
"color: white")

        self.horizontalLayout.addWidget(self.pushButton_relatorio)

        self.tableWidget_relatorio = QTableWidget(self.tab_4)
        if (self.tableWidget_relatorio.columnCount() < 6):
            self.tableWidget_relatorio.setColumnCount(6)
        __qtablewidgetitem21 = QTableWidgetItem()
        __qtablewidgetitem21.setFont(font);
        __qtablewidgetitem21.setBackground(QColor(255, 140, 0));
        self.tableWidget_relatorio.setHorizontalHeaderItem(0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        __qtablewidgetitem22.setFont(font);
        __qtablewidgetitem22.setBackground(QColor(255, 140, 0));
        self.tableWidget_relatorio.setHorizontalHeaderItem(1, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        __qtablewidgetitem23.setFont(font);
        __qtablewidgetitem23.setBackground(QColor(255, 140, 0));
        self.tableWidget_relatorio.setHorizontalHeaderItem(2, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        __qtablewidgetitem24.setFont(font);
        __qtablewidgetitem24.setBackground(QColor(255, 140, 0));
        self.tableWidget_relatorio.setHorizontalHeaderItem(3, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        __qtablewidgetitem25.setFont(font);
        __qtablewidgetitem25.setBackground(QColor(255, 140, 0));
        self.tableWidget_relatorio.setHorizontalHeaderItem(4, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        __qtablewidgetitem26.setFont(font);
        __qtablewidgetitem26.setBackground(QColor(255, 140, 0));
        self.tableWidget_relatorio.setHorizontalHeaderItem(5, __qtablewidgetitem26)
        self.tableWidget_relatorio.setObjectName(u"tableWidget_relatorio")
        self.tableWidget_relatorio.setGeometry(QRect(-10, 0, 1360, 650))
        self.tableWidget_relatorio.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_relatorio.horizontalHeader().setDefaultSectionSize(313)
        self.tabHome.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.label_Background_3 = QLabel(self.tab_5)
        self.label_Background_3.setObjectName(u"label_Background_3")
        self.label_Background_3.setGeometry(QRect(420, 40, 941, 631))
        self.label_Background_3.setPixmap(QPixmap(u"images/ChatGPT_Image_12_de_abr._de_2025__18_25_05-removebg-preview-lallala.png"))
        self.label_Background_3.setScaledContents(True)
        self.label_Background_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.widget_configuracaodeIA_2 = QWidget(self.tab_5)
        self.widget_configuracaodeIA_2.setObjectName(u"widget_configuracaodeIA_2")
        self.widget_configuracaodeIA_2.setGeometry(QRect(110, 310, 341, 93))
        self.gridLayout_2 = QGridLayout(self.widget_configuracaodeIA_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_ConfiguracaodeIA_2 = QLabel(self.widget_configuracaodeIA_2)
        self.label_ConfiguracaodeIA_2.setObjectName(u"label_ConfiguracaodeIA_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_ConfiguracaodeIA_2.sizePolicy().hasHeightForWidth())
        self.label_ConfiguracaodeIA_2.setSizePolicy(sizePolicy2)
        self.label_ConfiguracaodeIA_2.setMinimumSize(QSize(20, 20))
        font4 = QFont()
        self.label_ConfiguracaodeIA_2.setFont(font4)
        self.label_ConfiguracaodeIA_2.setStyleSheet(u"background-color: #FF8C00;\n"
"font-size: 16px;")

        self.gridLayout_2.addWidget(self.label_ConfiguracaodeIA_2, 0, 0, 1, 2)

        self.label_Tema = QLabel(self.widget_configuracaodeIA_2)
        self.label_Tema.setObjectName(u"label_Tema")
        self.label_Tema.setFont(font)
        self.label_Tema.setStyleSheet(u"color: white\n"
"")
        self.label_Tema.setFrameShape(QFrame.Shape.NoFrame)
        self.label_Tema.setFrameShadow(QFrame.Shadow.Plain)
        self.label_Tema.setLineWidth(1)
        self.label_Tema.setTextFormat(Qt.TextFormat.AutoText)

        self.gridLayout_2.addWidget(self.label_Tema, 1, 0, 1, 1)

        self.comboBox_Tema = QComboBox(self.widget_configuracaodeIA_2)
        self.comboBox_Tema.addItem("")
        self.comboBox_Tema.addItem("")
        self.comboBox_Tema.addItem("")
        self.comboBox_Tema.setObjectName(u"comboBox_Tema")
        self.comboBox_Tema.setEnabled(True)
        self.comboBox_Tema.setFont(font3)
        self.comboBox_Tema.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.comboBox_Tema.setStyleSheet(u"font: 10pt \"Segoe UI\";")
        self.comboBox_Tema.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.comboBox_Tema.setFrame(True)

        self.gridLayout_2.addWidget(self.comboBox_Tema, 1, 1, 1, 1)

        self.label_Resolucao = QLabel(self.widget_configuracaodeIA_2)
        self.label_Resolucao.setObjectName(u"label_Resolucao")
        self.label_Resolucao.setFont(font)
        self.label_Resolucao.setStyleSheet(u"color: white\n"
"")
        self.label_Resolucao.setFrameShape(QFrame.Shape.NoFrame)
        self.label_Resolucao.setFrameShadow(QFrame.Shadow.Plain)
        self.label_Resolucao.setLineWidth(1)
        self.label_Resolucao.setTextFormat(Qt.TextFormat.AutoText)

        self.gridLayout_2.addWidget(self.label_Resolucao, 2, 0, 1, 1)

        self.comboBox_Resolucao = QComboBox(self.widget_configuracaodeIA_2)
        self.comboBox_Resolucao.addItem("")
        self.comboBox_Resolucao.addItem("")
        self.comboBox_Resolucao.setObjectName(u"comboBox_Resolucao")
        self.comboBox_Resolucao.setEnabled(True)
        self.comboBox_Resolucao.setFont(font3)
        self.comboBox_Resolucao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.comboBox_Resolucao.setStyleSheet(u"font: 10pt \"Segoe UI\";")
        self.comboBox_Resolucao.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.comboBox_Resolucao.setFrame(True)

        self.gridLayout_2.addWidget(self.comboBox_Resolucao, 2, 1, 1, 1)

        self.verticalWidget_ConfGeral_2 = QWidget(self.tab_5)
        self.verticalWidget_ConfGeral_2.setObjectName(u"verticalWidget_ConfGeral_2")
        self.verticalWidget_ConfGeral_2.setGeometry(QRect(110, 440, 331, 231))
        self.verticalLayout_4 = QVBoxLayout(self.verticalWidget_ConfGeral_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_ConfLog = QLabel(self.verticalWidget_ConfGeral_2)
        self.label_ConfLog.setObjectName(u"label_ConfLog")
        self.label_ConfLog.setFont(font4)
        self.label_ConfLog.setStyleSheet(u"background-color: #FF8C00;\n"
"font-size: 16px;")

        self.verticalLayout_4.addWidget(self.label_ConfLog)

        self.formWidget_2 = QWidget(self.verticalWidget_ConfGeral_2)
        self.formWidget_2.setObjectName(u"formWidget_2")
        self.formLayout_2 = QFormLayout(self.formWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.comboBox_RetencaoLog = QComboBox(self.formWidget_2)
        self.comboBox_RetencaoLog.addItem("")
        self.comboBox_RetencaoLog.addItem("")
        self.comboBox_RetencaoLog.addItem("")
        self.comboBox_RetencaoLog.addItem("")
        self.comboBox_RetencaoLog.addItem("")
        self.comboBox_RetencaoLog.setObjectName(u"comboBox_RetencaoLog")
        self.comboBox_RetencaoLog.setFont(font3)
        self.comboBox_RetencaoLog.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.comboBox_RetencaoLog)

        self.label_RetencaoLog_2 = QLabel(self.formWidget_2)
        self.label_RetencaoLog_2.setObjectName(u"label_RetencaoLog_2")
        self.label_RetencaoLog_2.setFont(font)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_RetencaoLog_2)

        self.label_RetencaoOutros = QLabel(self.formWidget_2)
        self.label_RetencaoOutros.setObjectName(u"label_RetencaoOutros")
        self.label_RetencaoOutros.setFont(font)
        self.label_RetencaoOutros.setStyleSheet(u"")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_RetencaoOutros)

        self.lineEdit_RetencaoOutros = QLineEdit(self.formWidget_2)
        self.lineEdit_RetencaoOutros.setObjectName(u"lineEdit_RetencaoOutros")
        sizePolicy1.setHeightForWidth(self.lineEdit_RetencaoOutros.sizePolicy().hasHeightForWidth())
        self.lineEdit_RetencaoOutros.setSizePolicy(sizePolicy1)
        self.lineEdit_RetencaoOutros.setFont(font)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.lineEdit_RetencaoOutros)

        self.label_EnvioLogs = QLabel(self.formWidget_2)
        self.label_EnvioLogs.setObjectName(u"label_EnvioLogs")
        self.label_EnvioLogs.setFont(font)

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_EnvioLogs)

        self.radioButton_EnvioLogsSim = QRadioButton(self.formWidget_2)
        self.radioButton_EnvioLogsSim.setObjectName(u"radioButton_EnvioLogsSim")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.radioButton_EnvioLogsSim)

        self.radioButton_EnvioLogsNo = QRadioButton(self.formWidget_2)
        self.radioButton_EnvioLogsNo.setObjectName(u"radioButton_EnvioLogsNo")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.radioButton_EnvioLogsNo)

        self.lineEdit_IP = QLineEdit(self.formWidget_2)
        self.lineEdit_IP.setObjectName(u"lineEdit_IP")
        sizePolicy1.setHeightForWidth(self.lineEdit_IP.sizePolicy().hasHeightForWidth())
        self.lineEdit_IP.setSizePolicy(sizePolicy1)
        self.lineEdit_IP.setFont(font)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.lineEdit_IP)

        self.label_IP = QLabel(self.formWidget_2)
        self.label_IP.setObjectName(u"label_IP")
        self.label_IP.setFont(font)

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_IP)

        self.label_Porta = QLabel(self.formWidget_2)
        self.label_Porta.setObjectName(u"label_Porta")
        self.label_Porta.setFont(font)

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.label_Porta)

        self.lineEdit_Porta = QLineEdit(self.formWidget_2)
        self.lineEdit_Porta.setObjectName(u"lineEdit_Porta")
        sizePolicy1.setHeightForWidth(self.lineEdit_Porta.sizePolicy().hasHeightForWidth())
        self.lineEdit_Porta.setSizePolicy(sizePolicy1)
        self.lineEdit_Porta.setFont(font)

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.lineEdit_Porta)


        self.verticalLayout_4.addWidget(self.formWidget_2)

        self.verticalWidget_ConfGeral_3 = QWidget(self.tab_5)
        self.verticalWidget_ConfGeral_3.setObjectName(u"verticalWidget_ConfGeral_3")
        self.verticalWidget_ConfGeral_3.setGeometry(QRect(110, 40, 333, 231))
        self.verticalLayout_5 = QVBoxLayout(self.verticalWidget_ConfGeral_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_ConfGeral_4 = QLabel(self.verticalWidget_ConfGeral_3)
        self.label_ConfGeral_4.setObjectName(u"label_ConfGeral_4")
        self.label_ConfGeral_4.setFont(font4)
        self.label_ConfGeral_4.setStyleSheet(u"background-color: #FF8C00;\n"
"font-size: 16px;")

        self.verticalLayout_5.addWidget(self.label_ConfGeral_4)

        self.widget_Opcoesgeral_4 = QWidget(self.verticalWidget_ConfGeral_3)
        self.widget_Opcoesgeral_4.setObjectName(u"widget_Opcoesgeral_4")
        self.formLayout_6 = QFormLayout(self.widget_Opcoesgeral_4)
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.label_MododeOperacao = QLabel(self.widget_Opcoesgeral_4)
        self.label_MododeOperacao.setObjectName(u"label_MododeOperacao")
        self.label_MododeOperacao.setFont(font3)
        self.label_MododeOperacao.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.formLayout_6.setWidget(2, QFormLayout.LabelRole, self.label_MododeOperacao)

        self.comboBox_operacao = QComboBox(self.widget_Opcoesgeral_4)
        self.comboBox_operacao.addItem("")
        self.comboBox_operacao.addItem("")
        self.comboBox_operacao.addItem("")
        self.comboBox_operacao.setObjectName(u"comboBox_operacao")
        self.comboBox_operacao.setFont(font3)
        self.comboBox_operacao.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.formLayout_6.setWidget(2, QFormLayout.FieldRole, self.comboBox_operacao)

        self.label_PerfisRede = QLabel(self.widget_Opcoesgeral_4)
        self.label_PerfisRede.setObjectName(u"label_PerfisRede")
        self.label_PerfisRede.setFont(font3)
        self.label_PerfisRede.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.formLayout_6.setWidget(3, QFormLayout.LabelRole, self.label_PerfisRede)

        self.comboBox_PerfisRede = QComboBox(self.widget_Opcoesgeral_4)
        self.comboBox_PerfisRede.addItem("")
        self.comboBox_PerfisRede.addItem("")
        self.comboBox_PerfisRede.addItem("")
        self.comboBox_PerfisRede.setObjectName(u"comboBox_PerfisRede")
        self.comboBox_PerfisRede.setFont(font3)
        self.comboBox_PerfisRede.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.formLayout_6.setWidget(3, QFormLayout.FieldRole, self.comboBox_PerfisRede)

        self.label_FiltrodeInvasoes = QLabel(self.widget_Opcoesgeral_4)
        self.label_FiltrodeInvasoes.setObjectName(u"label_FiltrodeInvasoes")
        self.label_FiltrodeInvasoes.setFont(font3)
        self.label_FiltrodeInvasoes.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.formLayout_6.setWidget(4, QFormLayout.LabelRole, self.label_FiltrodeInvasoes)

        self.comboBox_filtro = QComboBox(self.widget_Opcoesgeral_4)
        self.comboBox_filtro.addItem("")
        self.comboBox_filtro.addItem("")
        self.comboBox_filtro.setObjectName(u"comboBox_filtro")
        self.comboBox_filtro.setFont(font3)
        self.comboBox_filtro.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.formLayout_6.setWidget(4, QFormLayout.FieldRole, self.comboBox_filtro)

        self.label_ModoGamer = QLabel(self.widget_Opcoesgeral_4)
        self.label_ModoGamer.setObjectName(u"label_ModoGamer")
        self.label_ModoGamer.setFont(font3)
        self.label_ModoGamer.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.formLayout_6.setWidget(5, QFormLayout.LabelRole, self.label_ModoGamer)

        self.comboBox_ModoGamer = QComboBox(self.widget_Opcoesgeral_4)
        self.comboBox_ModoGamer.addItem("")
        self.comboBox_ModoGamer.addItem("")
        self.comboBox_ModoGamer.setObjectName(u"comboBox_ModoGamer")
        self.comboBox_ModoGamer.setFont(font3)
        self.comboBox_ModoGamer.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.formLayout_6.setWidget(5, QFormLayout.FieldRole, self.comboBox_ModoGamer)

        self.label_PopupdeNotif = QLabel(self.widget_Opcoesgeral_4)
        self.label_PopupdeNotif.setObjectName(u"label_PopupdeNotif")
        self.label_PopupdeNotif.setFont(font3)
        self.label_PopupdeNotif.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.formLayout_6.setWidget(6, QFormLayout.LabelRole, self.label_PopupdeNotif)

        self.comboBox_PopupdeNotif = QComboBox(self.widget_Opcoesgeral_4)
        self.comboBox_PopupdeNotif.addItem("")
        self.comboBox_PopupdeNotif.addItem("")
        self.comboBox_PopupdeNotif.setObjectName(u"comboBox_PopupdeNotif")
        self.comboBox_PopupdeNotif.setFont(font3)
        self.comboBox_PopupdeNotif.setStyleSheet(u"font: 10pt \"Segoe UI\";")

        self.formLayout_6.setWidget(6, QFormLayout.FieldRole, self.comboBox_PopupdeNotif)

        self.label_ModeloIA = QLabel(self.widget_Opcoesgeral_4)
        self.label_ModeloIA.setObjectName(u"label_ModeloIA")
        self.label_ModeloIA.setFont(font3)
        self.label_ModeloIA.setStyleSheet(u"font: 10pt \"Segoe UI\";")
        self.label_ModeloIA.setFrameShape(QFrame.Shape.NoFrame)
        self.label_ModeloIA.setFrameShadow(QFrame.Shadow.Plain)
        self.label_ModeloIA.setLineWidth(1)
        self.label_ModeloIA.setTextFormat(Qt.TextFormat.AutoText)

        self.formLayout_6.setWidget(7, QFormLayout.LabelRole, self.label_ModeloIA)

        self.comboBox_ModeloIA = QComboBox(self.widget_Opcoesgeral_4)
        self.comboBox_ModeloIA.addItem("")
        self.comboBox_ModeloIA.addItem("")
        self.comboBox_ModeloIA.setObjectName(u"comboBox_ModeloIA")
        self.comboBox_ModeloIA.setEnabled(True)
        self.comboBox_ModeloIA.setFont(font3)
        self.comboBox_ModeloIA.setStyleSheet(u"font: 10pt \"Segoe UI\";")
        self.comboBox_ModeloIA.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.comboBox_ModeloIA.setFrame(True)

        self.formLayout_6.setWidget(7, QFormLayout.FieldRole, self.comboBox_ModeloIA)


        self.verticalLayout_5.addWidget(self.widget_Opcoesgeral_4)

        self.tabHome.addTab(self.tab_5, "")

        self.horizontalLayout_3.addWidget(self.tabHome)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabHome.setCurrentIndex(4)
        self.button_Conexoes.setDefault(False)
        self.button_CriarACL.setDefault(False)
        self.button_RemoverACL.setDefault(False)
        self.button_ImportarACL.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_Background.setText("")
        self.label_Alertanotif.setText(QCoreApplication.translate("MainWindow", u"Nenhuma alerta", None))
        self.label_CoEstabelecidas.setText(QCoreApplication.translate("MainWindow", u"87 Conex\u00f5es estabelecidas", None))
        self.button_Conexoes.setText(QCoreApplication.translate("MainWindow", u"Ir para Conex\u00f5es", None))
        self.label_SetaDownload.setText("")
        self.label_ImgAlerta.setText("")
        self.label_ImgConexoes.setText("")
        self.label_ImgRede.setText("")
        self.label_Download.setText(QCoreApplication.translate("MainWindow", u"0 Kbs/s", None))
        self.label_ConexoesAtivas.setText(QCoreApplication.translate("MainWindow", u"Conex\u00f5es ativas", None))
        self.label_UsodaRede.setText(QCoreApplication.translate("MainWindow", u"Uso da rede", None))
        self.label_SetaUpload.setText("")
        self.label_Alerta.setText(QCoreApplication.translate("MainWindow", u"Alertas", None))
        self.label_Upload.setText(QCoreApplication.translate("MainWindow", u"0 Kbs/s", None))
        self.tabHome.setTabText(self.tabHome.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Home", None))
        self.label_background.setText("")
        self.label_CriacaoACL.setText(QCoreApplication.translate("MainWindow", u"Cria\u00e7\u00e3o de ACLs", None))
        self.label_nomeACL.setText(QCoreApplication.translate("MainWindow", u"Nome da ACL:", None))
        self.label_comecoIP.setText(QCoreApplication.translate("MainWindow", u"Come\u00e7o do bloco IP:", None))
        self.label_FinalIP.setText(QCoreApplication.translate("MainWindow", u"Final do bloco IP:", None))
        self.label_Protocolo.setText(QCoreApplication.translate("MainWindow", u"Protocolo:", None))
        self.label_Direcao.setText(QCoreApplication.translate("MainWindow", u"Dire\u00e7\u00e3o:", None))
        self.label_Acao.setText(QCoreApplication.translate("MainWindow", u"A\u00e7\u00e3o:", None))
        self.lineEdit_nomeACL.setText("")
        self.lineEdit_comecoIP.setText("")
        self.comboBox_protocolo.setItemText(0, QCoreApplication.translate("MainWindow", u"TCP", None))
        self.comboBox_protocolo.setItemText(1, QCoreApplication.translate("MainWindow", u"UDP", None))

        self.comboBox_direcao.setItemText(0, QCoreApplication.translate("MainWindow", u"IN", None))
        self.comboBox_direcao.setItemText(1, QCoreApplication.translate("MainWindow", u"OUT", None))

        self.comboBox_acao.setItemText(0, QCoreApplication.translate("MainWindow", u"PERMITIR", None))
        self.comboBox_acao.setItemText(1, QCoreApplication.translate("MainWindow", u"NEGAR", None))

        self.checkBox_SSH.setText(QCoreApplication.translate("MainWindow", u"SSH", None))
        self.checkBox_Telnet.setText(QCoreApplication.translate("MainWindow", u"Telnet", None))
        self.checkBox_RPC.setText(QCoreApplication.translate("MainWindow", u"RPC ", None))
        self.label_outros.setText(QCoreApplication.translate("MainWindow", u"Outros:", None))
        self.checkBox_HTTP.setText(QCoreApplication.translate("MainWindow", u"HTTP", None))
        self.checkBox_DNS.setText(QCoreApplication.translate("MainWindow", u"DNS", None))
        self.checkBox_FTP.setText(QCoreApplication.translate("MainWindow", u"FTP", None))
        self.label_servicos.setText(QCoreApplication.translate("MainWindow", u"Servi\u00e7os:", None))
        self.checkBox_NetBIOS.setText(QCoreApplication.translate("MainWindow", u"NetBIOS ", None))
        self.checkBox_iCMP.setText(QCoreApplication.translate("MainWindow", u"ICMP", None))
        self.checkBox_SNMP.setText(QCoreApplication.translate("MainWindow", u"SNMPv1/v2", None))
        self.label_TabACL.setText(QCoreApplication.translate("MainWindow", u"Tabela de ACLs Tecguard", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Nome", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Come\u00e7o do bloco", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Fim do bloco", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Protocolo", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Dire\u00e7\u00e3o", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Servi\u00e7os", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Portas", None));
        self.button_CriarACL.setText(QCoreApplication.translate("MainWindow", u"Criar ACL", None))
        self.label_TabACL_2.setText(QCoreApplication.translate("MainWindow", u"Tabela de ACLs Windows", None))
        self.button_RemoverACL.setText(QCoreApplication.translate("MainWindow", u"Remover ACL", None))
        self.button_ImportarACL.setText(QCoreApplication.translate("MainWindow", u"Importar ACL", None))
        ___qtablewidgetitem7 = self.tableWidget_2.horizontalHeaderItem(0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Nome", None));
        ___qtablewidgetitem8 = self.tableWidget_2.horizontalHeaderItem(1)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Portas", None));
        ___qtablewidgetitem9 = self.tableWidget_2.horizontalHeaderItem(2)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Come\u00e7o do bloco", None));
        ___qtablewidgetitem10 = self.tableWidget_2.horizontalHeaderItem(3)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Fim do bloco", None));
        ___qtablewidgetitem11 = self.tableWidget_2.horizontalHeaderItem(4)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Protocolo", None));
        ___qtablewidgetitem12 = self.tableWidget_2.horizontalHeaderItem(5)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Dire\u00e7\u00e3o", None));
        ___qtablewidgetitem13 = self.tableWidget_2.horizontalHeaderItem(6)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Servi\u00e7os", None));
        self.tabHome.setTabText(self.tabHome.indexOf(self.TabPolitica), QCoreApplication.translate("MainWindow", u"Pol\u00edticas", None))
        self.label_Background_2.setText("")
        ___qtablewidgetitem14 = self.table_Conexoes.horizontalHeaderItem(0)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Nome", None));
        ___qtablewidgetitem15 = self.table_Conexoes.horizontalHeaderItem(1)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Protocolo", None));
        ___qtablewidgetitem16 = self.table_Conexoes.horizontalHeaderItem(2)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Fonte externa", None));
        ___qtablewidgetitem17 = self.table_Conexoes.horizontalHeaderItem(3)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Estado", None));
        ___qtablewidgetitem18 = self.table_Conexoes.horizontalHeaderItem(4)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"PID", None));
        ___qtablewidgetitem19 = self.table_Conexoes.horizontalHeaderItem(5)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"Upload", None));
        ___qtablewidgetitem20 = self.table_Conexoes.horizontalHeaderItem(6)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"Download", None));
        self.tabHome.setTabText(self.tabHome.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Conex\u00f5es", None))
        self.pushButton_relatorio.setText(QCoreApplication.translate("MainWindow", u"Fazer relat\u00f3rio", None))
        ___qtablewidgetitem21 = self.tableWidget_relatorio.horizontalHeaderItem(0)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Data do evento", None));
        ___qtablewidgetitem22 = self.tableWidget_relatorio.horizontalHeaderItem(1)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"Classifica\u00e7\u00e3o", None));
        ___qtablewidgetitem23 = self.tableWidget_relatorio.horizontalHeaderItem(2)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"Evento", None));
        ___qtablewidgetitem24 = self.tableWidget_relatorio.horizontalHeaderItem(3)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"IP", None));
        ___qtablewidgetitem25 = self.tableWidget_relatorio.horizontalHeaderItem(4)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"Porta", None));
        ___qtablewidgetitem26 = self.tableWidget_relatorio.horizontalHeaderItem(5)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"Servi\u00e7o", None));
        self.tabHome.setTabText(self.tabHome.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Relat\u00f3rios", None))
        self.label_Background_3.setText("")
        self.label_ConfiguracaodeIA_2.setText(QCoreApplication.translate("MainWindow", u"Configura\u00e7\u00e3o de tela", None))
        self.label_Tema.setText(QCoreApplication.translate("MainWindow", u"Tema", None))
        self.comboBox_Tema.setItemText(0, QCoreApplication.translate("MainWindow", u"Claro", None))
        self.comboBox_Tema.setItemText(1, QCoreApplication.translate("MainWindow", u"Escuro", None))
        self.comboBox_Tema.setItemText(2, QCoreApplication.translate("MainWindow", u"Op\u00e7\u00f5es", None))

        self.label_Resolucao.setText(QCoreApplication.translate("MainWindow", u"Resolu\u00e7\u00e3o", None))
        self.comboBox_Resolucao.setItemText(0, QCoreApplication.translate("MainWindow", u"1360x768", None))
        self.comboBox_Resolucao.setItemText(1, QCoreApplication.translate("MainWindow", u"1920x1080", None))

        self.label_ConfLog.setText(QCoreApplication.translate("MainWindow", u"Configura\u00e7\u00e3o de log", None))
        self.comboBox_RetencaoLog.setItemText(0, QCoreApplication.translate("MainWindow", u"3 dias", None))
        self.comboBox_RetencaoLog.setItemText(1, QCoreApplication.translate("MainWindow", u"5 dias", None))
        self.comboBox_RetencaoLog.setItemText(2, QCoreApplication.translate("MainWindow", u"7 dias", None))
        self.comboBox_RetencaoLog.setItemText(3, QCoreApplication.translate("MainWindow", u"15 dias", None))
        self.comboBox_RetencaoLog.setItemText(4, QCoreApplication.translate("MainWindow", u"30 dias", None))

        self.label_RetencaoLog_2.setText(QCoreApplication.translate("MainWindow", u"Reten\u00e7\u00e3o de log", None))
        self.label_RetencaoOutros.setText(QCoreApplication.translate("MainWindow", u"Personalizado", None))
        self.lineEdit_RetencaoOutros.setText("")
        self.label_EnvioLogs.setText(QCoreApplication.translate("MainWindow", u"Envio de logs", None))
        self.radioButton_EnvioLogsSim.setText(QCoreApplication.translate("MainWindow", u"Sim", None))
        self.radioButton_EnvioLogsNo.setText(QCoreApplication.translate("MainWindow", u"N\u00e3o", None))
        self.lineEdit_IP.setText("")
        self.label_IP.setText(QCoreApplication.translate("MainWindow", u"IP:", None))
        self.label_Porta.setText(QCoreApplication.translate("MainWindow", u"Porta:", None))
        self.lineEdit_Porta.setText("")
        self.label_ConfGeral_4.setText(QCoreApplication.translate("MainWindow", u"Configura\u00e7\u00e3o geral", None))
        self.label_MododeOperacao.setText(QCoreApplication.translate("MainWindow", u"Modo de opera\u00e7\u00e3o", None))
        self.comboBox_operacao.setItemText(0, QCoreApplication.translate("MainWindow", u"Modo autom\u00e1tico", None))
        self.comboBox_operacao.setItemText(1, QCoreApplication.translate("MainWindow", u"Modo Interativo", None))
        self.comboBox_operacao.setItemText(2, QCoreApplication.translate("MainWindow", u"Modo personalizado", None))

        self.label_PerfisRede.setText(QCoreApplication.translate("MainWindow", u"Perfis de rede", None))
        self.comboBox_PerfisRede.setItemText(0, QCoreApplication.translate("MainWindow", u"P\u00fablico (Restrito)", None))
        self.comboBox_PerfisRede.setItemText(1, QCoreApplication.translate("MainWindow", u"Privado (Casa/trabalho)", None))
        self.comboBox_PerfisRede.setItemText(2, QCoreApplication.translate("MainWindow", u"Dominio(Corporativo)", None))

        self.label_FiltrodeInvasoes.setText(QCoreApplication.translate("MainWindow", u"Filtro de invas\u00f5es", None))
        self.comboBox_filtro.setItemText(0, QCoreApplication.translate("MainWindow", u"Ligado", None))
        self.comboBox_filtro.setItemText(1, QCoreApplication.translate("MainWindow", u"Desligado", None))

        self.label_ModoGamer.setText(QCoreApplication.translate("MainWindow", u"Modo gamer", None))
        self.comboBox_ModoGamer.setItemText(0, QCoreApplication.translate("MainWindow", u"Ligado", None))
        self.comboBox_ModoGamer.setItemText(1, QCoreApplication.translate("MainWindow", u"Desligado", None))

        self.label_PopupdeNotif.setText(QCoreApplication.translate("MainWindow", u"Popup de notifica\u00e7\u00e3o", None))
        self.comboBox_PopupdeNotif.setItemText(0, QCoreApplication.translate("MainWindow", u"Ligado", None))
        self.comboBox_PopupdeNotif.setItemText(1, QCoreApplication.translate("MainWindow", u"Desligado", None))

        self.label_ModeloIA.setText(QCoreApplication.translate("MainWindow", u"Modelo IA", None))
        self.comboBox_ModeloIA.setItemText(0, QCoreApplication.translate("MainWindow", u"XDGBoost", None))
        self.comboBox_ModeloIA.setItemText(1, QCoreApplication.translate("MainWindow", u"Random Forest", None))

        self.tabHome.setTabText(self.tabHome.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Configura\u00e7\u00f5es", None))
    # retranslateUi

