# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Home_tabwidgetVwixcU.ui'
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
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QTableWidget, QTableWidgetItem, QToolButton,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setStyleSheet(u"background-color: black")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabHome = QTabWidget(self.centralwidget)
        self.tabHome.setObjectName(u"tabHome")
        self.tabHome.setGeometry(QRect(0, 0, 1971, 1081))
        self.tabHome.setStyleSheet(u"background-color: black;\n"
"color: white")
        self.tabHome.setElideMode(Qt.TextElideMode.ElideNone)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.label_Background = QLabel(self.tab)
        self.label_Background.setObjectName(u"label_Background")
        self.label_Background.setEnabled(True)
        self.label_Background.setGeometry(QRect(60, -50, 2041, 1080))
        self.label_Background.setTextFormat(Qt.TextFormat.PlainText)
        self.label_Background.setPixmap(QPixmap(u"../images/imgbackground.png"))
        self.label_Background.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_Alertanotif = QLabel(self.tab)
        self.label_Alertanotif.setObjectName(u"label_Alertanotif")
        self.label_Alertanotif.setGeometry(QRect(430, 320, 201, 51))
        self.label_Alertanotif.setStyleSheet(u"font: 20pt \"Segoe UI\";")
        self.label_CoEstabelecidas = QLabel(self.tab)
        self.label_CoEstabelecidas.setObjectName(u"label_CoEstabelecidas")
        self.label_CoEstabelecidas.setGeometry(QRect(450, 630, 321, 41))
        self.label_CoEstabelecidas.setStyleSheet(u"font: 20pt \"Segoe UI\";")
        self.button_Conexoes = QPushButton(self.tab)
        self.button_Conexoes.setObjectName(u"button_Conexoes")
        self.button_Conexoes.setGeometry(QRect(590, 710, 131, 31))
        self.button_Conexoes.setStyleSheet(u"color: black;\n"
"background-color: #ffd700")
        self.button_Conexoes.setAutoDefault(False)
        self.button_Conexoes.setFlat(False)
        self.label_SetaDownload = QLabel(self.tab)
        self.label_SetaDownload.setObjectName(u"label_SetaDownload")
        self.label_SetaDownload.setGeometry(QRect(430, 960, 31, 31))
        self.label_SetaDownload.setPixmap(QPixmap(u"../images/setacima.png"))
        self.label_SetaDownload.setScaledContents(True)
        self.verticalLayoutWidget = QWidget(self.tab)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(-10, 170, 411, 851))
        self.verticalLayout_imagens = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_imagens.setObjectName(u"verticalLayout_imagens")
        self.verticalLayout_imagens.setContentsMargins(0, 0, 0, 0)
        self.label_ImgAlerta = QLabel(self.verticalLayoutWidget)
        self.label_ImgAlerta.setObjectName(u"label_ImgAlerta")
        self.label_ImgAlerta.setPixmap(QPixmap(u"../images/iconeataquepequeno (2).png"))

        self.verticalLayout_imagens.addWidget(self.label_ImgAlerta, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_imagens.addItem(self.verticalSpacer)

        self.label_ImgConexoes = QLabel(self.verticalLayoutWidget)
        self.label_ImgConexoes.setObjectName(u"label_ImgConexoes")
        self.label_ImgConexoes.setPixmap(QPixmap(u"../images/iconeconexoespequeno (2).png"))

        self.verticalLayout_imagens.addWidget(self.label_ImgConexoes, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_imagens.addItem(self.verticalSpacer_2)

        self.label_ImgRede = QLabel(self.verticalLayoutWidget)
        self.label_ImgRede.setObjectName(u"label_ImgRede")
        self.label_ImgRede.setEnabled(False)
        self.label_ImgRede.setMaximumSize(QSize(16777215, 512))
        self.label_ImgRede.setTextFormat(Qt.TextFormat.RichText)
        self.label_ImgRede.setPixmap(QPixmap(u"../images/interneticonepequeno (2).png"))
        self.label_ImgRede.setScaledContents(False)

        self.verticalLayout_imagens.addWidget(self.label_ImgRede, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_Download = QLabel(self.tab)
        self.label_Download.setObjectName(u"label_Download")
        self.label_Download.setGeometry(QRect(500, 900, 131, 41))
        self.label_Download.setStyleSheet(u"font: 20pt \"Segoe UI\";")
        self.label_ConexoesAtivas = QLabel(self.tab)
        self.label_ConexoesAtivas.setObjectName(u"label_ConexoesAtivas")
        self.label_ConexoesAtivas.setGeometry(QRect(430, 530, 335, 63))
        self.label_ConexoesAtivas.setStyleSheet(u"font: 35pt \"Segoe UI\";")
        self.label_UsodaRede = QLabel(self.tab)
        self.label_UsodaRede.setObjectName(u"label_UsodaRede")
        self.label_UsodaRede.setGeometry(QRect(390, 810, 335, 63))
        self.label_UsodaRede.setStyleSheet(u"font: 35pt \"Segoe UI\";")
        self.label_SetaUpload = QLabel(self.tab)
        self.label_SetaUpload.setObjectName(u"label_SetaUpload")
        self.label_SetaUpload.setGeometry(QRect(430, 900, 31, 31))
        self.label_SetaUpload.setPixmap(QPixmap(u"../images/imgsetabaixo2.png"))
        self.label_SetaUpload.setScaledContents(True)
        self.label_Alerta = QLabel(self.tab)
        self.label_Alerta.setObjectName(u"label_Alerta")
        self.label_Alerta.setGeometry(QRect(440, 240, 335, 63))
        self.label_Alerta.setStyleSheet(u"font: 35pt \"Segoe UI\";")
        self.label_Alerta.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_Upload = QLabel(self.tab)
        self.label_Upload.setObjectName(u"label_Upload")
        self.label_Upload.setGeometry(QRect(500, 960, 131, 41))
        self.label_Upload.setStyleSheet(u"font: 20pt \"Segoe UI\";")
        self.tabHome.addTab(self.tab, "")
        self.TabPolitica = QWidget()
        self.TabPolitica.setObjectName(u"TabPolitica")
        self.label_background = QLabel(self.TabPolitica)
        self.label_background.setObjectName(u"label_background")
        self.label_background.setGeometry(QRect(722, 30, 1422, 800))
        self.label_background.setPixmap(QPixmap(u"../images/imgbackground.png"))
        self.label_background.setScaledContents(True)
        self.label_background.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.verticalWidget_2 = QWidget(self.TabPolitica)
        self.verticalWidget_2.setObjectName(u"verticalWidget_2")
        self.verticalWidget_2.setGeometry(QRect(170, 140, 531, 501))
        self.verticalWidget_2.setStyleSheet(u"color: white;")
        self.verticalLayout_CriacaoACL = QVBoxLayout(self.verticalWidget_2)
        self.verticalLayout_CriacaoACL.setObjectName(u"verticalLayout_CriacaoACL")
        self.label_CriacaoACL = QLabel(self.verticalWidget_2)
        self.label_CriacaoACL.setObjectName(u"label_CriacaoACL")
        self.label_CriacaoACL.setStyleSheet(u"background-color: rgb(244, 203, 0);\n"
"font-size: 25px")

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

        self.verticalLayout.addWidget(self.label_nomeACL)

        self.label_comecoIP = QLabel(self.verticalFrame_nomeOpes)
        self.label_comecoIP.setObjectName(u"label_comecoIP")

        self.verticalLayout.addWidget(self.label_comecoIP)

        self.label_FinalIP = QLabel(self.verticalFrame_nomeOpes)
        self.label_FinalIP.setObjectName(u"label_FinalIP")

        self.verticalLayout.addWidget(self.label_FinalIP)

        self.label_Protocolo = QLabel(self.verticalFrame_nomeOpes)
        self.label_Protocolo.setObjectName(u"label_Protocolo")

        self.verticalLayout.addWidget(self.label_Protocolo)

        self.label_Direcao = QLabel(self.verticalFrame_nomeOpes)
        self.label_Direcao.setObjectName(u"label_Direcao")

        self.verticalLayout.addWidget(self.label_Direcao)

        self.label_Acao = QLabel(self.verticalFrame_nomeOpes)
        self.label_Acao.setObjectName(u"label_Acao")

        self.verticalLayout.addWidget(self.label_Acao)


        self.horizontalLayout_2.addWidget(self.verticalFrame_nomeOpes)

        self.verticalWidget_opcoes = QWidget(self.horizontalWidget_CriacaoACL)
        self.verticalWidget_opcoes.setObjectName(u"verticalWidget_opcoes")
        self.verticalLayout_3 = QVBoxLayout(self.verticalWidget_opcoes)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lineEdit_nomeACL = QLineEdit(self.verticalWidget_opcoes)
        self.lineEdit_nomeACL.setObjectName(u"lineEdit_nomeACL")

        self.verticalLayout_3.addWidget(self.lineEdit_nomeACL)

        self.lineEdit_comecoIP = QLineEdit(self.verticalWidget_opcoes)
        self.lineEdit_comecoIP.setObjectName(u"lineEdit_comecoIP")

        self.verticalLayout_3.addWidget(self.lineEdit_comecoIP)

        self.lineEdit_FinalIP = QLineEdit(self.verticalWidget_opcoes)
        self.lineEdit_FinalIP.setObjectName(u"lineEdit_FinalIP")

        self.verticalLayout_3.addWidget(self.lineEdit_FinalIP)

        self.comboBox_protocolo = QComboBox(self.verticalWidget_opcoes)
        self.comboBox_protocolo.addItem("")
        self.comboBox_protocolo.addItem("")
        self.comboBox_protocolo.setObjectName(u"comboBox_protocolo")

        self.verticalLayout_3.addWidget(self.comboBox_protocolo)

        self.comboBox_direcao = QComboBox(self.verticalWidget_opcoes)
        self.comboBox_direcao.addItem("")
        self.comboBox_direcao.addItem("")
        self.comboBox_direcao.setObjectName(u"comboBox_direcao")

        self.verticalLayout_3.addWidget(self.comboBox_direcao)

        self.comboBox_acao = QComboBox(self.verticalWidget_opcoes)
        self.comboBox_acao.addItem("")
        self.comboBox_acao.addItem("")
        self.comboBox_acao.setObjectName(u"comboBox_acao")

        self.verticalLayout_3.addWidget(self.comboBox_acao)


        self.horizontalLayout_2.addWidget(self.verticalWidget_opcoes)


        self.verticalLayout_CriacaoACL.addWidget(self.horizontalWidget_CriacaoACL)

        self.gridLayout_Servicos = QGridLayout()
        self.gridLayout_Servicos.setObjectName(u"gridLayout_Servicos")
        self.checkBox_SSH = QCheckBox(self.verticalWidget_2)
        self.checkBox_SSH.setObjectName(u"checkBox_SSH")

        self.gridLayout_Servicos.addWidget(self.checkBox_SSH, 2, 1, 1, 1)

        self.checkBox_Telnet = QCheckBox(self.verticalWidget_2)
        self.checkBox_Telnet.setObjectName(u"checkBox_Telnet")

        self.gridLayout_Servicos.addWidget(self.checkBox_Telnet, 3, 1, 1, 1)

        self.checkBox_RPC = QCheckBox(self.verticalWidget_2)
        self.checkBox_RPC.setObjectName(u"checkBox_RPC")

        self.gridLayout_Servicos.addWidget(self.checkBox_RPC, 5, 1, 1, 1)

        self.label_outros = QLabel(self.verticalWidget_2)
        self.label_outros.setObjectName(u"label_outros")

        self.gridLayout_Servicos.addWidget(self.label_outros, 9, 0, 1, 1)

        self.checkBox_HTTP = QCheckBox(self.verticalWidget_2)
        self.checkBox_HTTP.setObjectName(u"checkBox_HTTP")

        self.gridLayout_Servicos.addWidget(self.checkBox_HTTP, 0, 1, 1, 1)

        self.checkBox_DNS = QCheckBox(self.verticalWidget_2)
        self.checkBox_DNS.setObjectName(u"checkBox_DNS")

        self.gridLayout_Servicos.addWidget(self.checkBox_DNS, 8, 1, 1, 1)

        self.checkBox_FTP = QCheckBox(self.verticalWidget_2)
        self.checkBox_FTP.setObjectName(u"checkBox_FTP")

        self.gridLayout_Servicos.addWidget(self.checkBox_FTP, 1, 1, 1, 1)

        self.label_servicos = QLabel(self.verticalWidget_2)
        self.label_servicos.setObjectName(u"label_servicos")

        self.gridLayout_Servicos.addWidget(self.label_servicos, 0, 0, 2, 1)

        self.lineEdit_outros = QLineEdit(self.verticalWidget_2)
        self.lineEdit_outros.setObjectName(u"lineEdit_outros")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_outros.sizePolicy().hasHeightForWidth())
        self.lineEdit_outros.setSizePolicy(sizePolicy)

        self.gridLayout_Servicos.addWidget(self.lineEdit_outros, 9, 1, 1, 1)

        self.checkBox_NetBIOS = QCheckBox(self.verticalWidget_2)
        self.checkBox_NetBIOS.setObjectName(u"checkBox_NetBIOS")

        self.gridLayout_Servicos.addWidget(self.checkBox_NetBIOS, 6, 1, 1, 1)

        self.checkBox_iCMP = QCheckBox(self.verticalWidget_2)
        self.checkBox_iCMP.setObjectName(u"checkBox_iCMP")

        self.gridLayout_Servicos.addWidget(self.checkBox_iCMP, 4, 1, 1, 1)

        self.checkBox_SNMP = QCheckBox(self.verticalWidget_2)
        self.checkBox_SNMP.setObjectName(u"checkBox_SNMP")

        self.gridLayout_Servicos.addWidget(self.checkBox_SNMP, 7, 1, 1, 1)


        self.verticalLayout_CriacaoACL.addLayout(self.gridLayout_Servicos)

        self.label_TabACL = QLabel(self.TabPolitica)
        self.label_TabACL.setObjectName(u"label_TabACL")
        self.label_TabACL.setGeometry(QRect(797, 20, 1087, 33))
        self.label_TabACL.setStyleSheet(u"background-color: rgb(244, 203, 0);\n"
"font-size: 25px")
        self.tableWidget = QTableWidget(self.TabPolitica)
        if (self.tableWidget.columnCount() < 7):
            self.tableWidget.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setBackground(QColor(54, 54, 54));
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setBackground(QColor(54, 54, 54));
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setBackground(QColor(54, 54, 54));
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setBackground(QColor(54, 54, 54));
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setBackground(QColor(54, 54, 54));
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setBackground(QColor(54, 54, 54));
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setBackground(QColor(54, 54, 54));
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(797, 70, 1087, 521))
        self.tableWidget.setStyleSheet(u"color:white;")
        self.tableWidget.horizontalHeader().setDefaultSectionSize(155)
        self.button_CriarACL = QPushButton(self.TabPolitica)
        self.button_CriarACL.setObjectName(u"button_CriarACL")
        self.button_CriarACL.setGeometry(QRect(250, 680, 131, 31))
        self.button_CriarACL.setStyleSheet(u"color: black;\n"
"background-color: #ffd700")
        self.button_CriarACL.setAutoDefault(False)
        self.button_CriarACL.setFlat(False)
        self.label_TabACL_2 = QLabel(self.TabPolitica)
        self.label_TabACL_2.setObjectName(u"label_TabACL_2")
        self.label_TabACL_2.setGeometry(QRect(800, 660, 1087, 33))
        self.label_TabACL_2.setStyleSheet(u"background-color: rgb(244, 203, 0);\n"
"font-size: 25px;\n"
"color:White;")
        self.tableWidget_2 = QTableWidget(self.TabPolitica)
        if (self.tableWidget_2.columnCount() < 7):
            self.tableWidget_2.setColumnCount(7)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setBackground(QColor(54, 54, 54));
        self.tableWidget_2.setHorizontalHeaderItem(0, __qtablewidgetitem7)
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.NoBrush)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setBackground(QColor(54, 54, 54));
        __qtablewidgetitem8.setForeground(brush);
        self.tableWidget_2.setHorizontalHeaderItem(1, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setBackground(QColor(54, 54, 54));
        self.tableWidget_2.setHorizontalHeaderItem(2, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setBackground(QColor(54, 54, 54));
        self.tableWidget_2.setHorizontalHeaderItem(3, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setBackground(QColor(54, 54, 54));
        self.tableWidget_2.setHorizontalHeaderItem(4, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setBackground(QColor(54, 54, 54));
        self.tableWidget_2.setHorizontalHeaderItem(5, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setBackground(QColor(54, 54, 54));
        self.tableWidget_2.setHorizontalHeaderItem(6, __qtablewidgetitem13)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        self.tableWidget_2.setGeometry(QRect(800, 710, 1087, 301))
        self.tableWidget_2.setStyleSheet(u"color: white;")
        self.tableWidget_2.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_2.setTabKeyNavigation(True)
        self.tableWidget_2.setProperty(u"showDropIndicator", True)
        self.tableWidget_2.setDragDropOverwriteMode(True)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(155)
        self.button_RemoverACL = QPushButton(self.TabPolitica)
        self.button_RemoverACL.setObjectName(u"button_RemoverACL")
        self.button_RemoverACL.setGeometry(QRect(480, 680, 131, 31))
        self.button_RemoverACL.setStyleSheet(u"color: black;\n"
"background-color: #ffd700")
        self.button_RemoverACL.setAutoDefault(False)
        self.button_RemoverACL.setFlat(False)
        self.tabHome.addTab(self.TabPolitica, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.label_Background_2 = QLabel(self.tab_3)
        self.label_Background_2.setObjectName(u"label_Background_2")
        self.label_Background_2.setEnabled(True)
        self.label_Background_2.setGeometry(QRect(170, -80, 1920, 1080))
        self.label_Background_2.setPixmap(QPixmap(u"../images/imgbackground.png"))
        self.label_Background_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.table_Conexoes = QTableWidget(self.tab_3)
        if (self.table_Conexoes.columnCount() < 7):
            self.table_Conexoes.setColumnCount(7)
        brush1 = QBrush(QColor(0, 0, 0, 255))
        brush1.setStyle(Qt.NoBrush)
        font = QFont()
        font.setBold(False)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setFont(font);
        __qtablewidgetitem14.setBackground(QColor(255, 215, 0));
        __qtablewidgetitem14.setForeground(brush1);
        self.table_Conexoes.setHorizontalHeaderItem(0, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setBackground(QColor(255, 215, 0));
        self.table_Conexoes.setHorizontalHeaderItem(1, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setBackground(QColor(255, 215, 0));
        self.table_Conexoes.setHorizontalHeaderItem(2, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        __qtablewidgetitem17.setBackground(QColor(255, 215, 0));
        self.table_Conexoes.setHorizontalHeaderItem(3, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        __qtablewidgetitem18.setBackground(QColor(255, 215, 0));
        self.table_Conexoes.setHorizontalHeaderItem(4, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        __qtablewidgetitem19.setBackground(QColor(255, 215, 0));
        self.table_Conexoes.setHorizontalHeaderItem(5, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        __qtablewidgetitem20.setBackground(QColor(255, 215, 0));
        self.table_Conexoes.setHorizontalHeaderItem(6, __qtablewidgetitem20)
        self.table_Conexoes.setObjectName(u"table_Conexoes")
        self.table_Conexoes.setGeometry(QRect(310, 0, 1291, 841))
        self.table_Conexoes.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.table_Conexoes.setAutoFillBackground(False)
        self.table_Conexoes.setStyleSheet(u"color: white;\n"
"")
        self.table_Conexoes.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.table_Conexoes.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.table_Conexoes.setAlternatingRowColors(True)
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
        self.layoutWidget = QWidget(self.tab_4)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(104, 13, 201, 51))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_Verlogs = QPushButton(self.layoutWidget)
        self.pushButton_Verlogs.setObjectName(u"pushButton_Verlogs")
        self.pushButton_Verlogs.setStyleSheet(u"background-color: rgb(54,54,54);\n"
"color: white")

        self.horizontalLayout.addWidget(self.pushButton_Verlogs)

        self.pushButton_relatrio = QPushButton(self.layoutWidget)
        self.pushButton_relatrio.setObjectName(u"pushButton_relatrio")
        self.pushButton_relatrio.setStyleSheet(u"background-color: rgb(54,54,54);\n"
"color: white")

        self.horizontalLayout.addWidget(self.pushButton_relatrio)

        self.tableWidget_relatorio = QTableWidget(self.tab_4)
        if (self.tableWidget_relatorio.columnCount() < 6):
            self.tableWidget_relatorio.setColumnCount(6)
        __qtablewidgetitem21 = QTableWidgetItem()
        __qtablewidgetitem21.setBackground(QColor(255, 215, 0));
        self.tableWidget_relatorio.setHorizontalHeaderItem(0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        __qtablewidgetitem22.setBackground(QColor(255, 215, 0));
        self.tableWidget_relatorio.setHorizontalHeaderItem(1, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        __qtablewidgetitem23.setBackground(QColor(255, 215, 0));
        self.tableWidget_relatorio.setHorizontalHeaderItem(2, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        __qtablewidgetitem24.setBackground(QColor(255, 215, 0));
        self.tableWidget_relatorio.setHorizontalHeaderItem(3, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        __qtablewidgetitem25.setBackground(QColor(255, 215, 0));
        self.tableWidget_relatorio.setHorizontalHeaderItem(4, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        __qtablewidgetitem26.setBackground(QColor(255, 215, 0));
        self.tableWidget_relatorio.setHorizontalHeaderItem(5, __qtablewidgetitem26)
        self.tableWidget_relatorio.setObjectName(u"tableWidget_relatorio")
        self.tableWidget_relatorio.setGeometry(QRect(104, 13, 1881, 821))
        self.tableWidget_relatorio.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_relatorio.horizontalHeader().setDefaultSectionSize(313)
        self.tabHome.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalWidget_ConfGeral = QWidget(self.tab_5)
        self.verticalWidget_ConfGeral.setObjectName(u"verticalWidget_ConfGeral")
        self.verticalWidget_ConfGeral.setGeometry(QRect(10, 50, 331, 251))
        self.verticalLayout_2 = QVBoxLayout(self.verticalWidget_ConfGeral)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_ConfGeral = QLabel(self.verticalWidget_ConfGeral)
        self.label_ConfGeral.setObjectName(u"label_ConfGeral")
        self.label_ConfGeral.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(244, 203, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
"font-size: 16px;")

        self.verticalLayout_2.addWidget(self.label_ConfGeral)

        self.widget_Opcoesgeral = QWidget(self.verticalWidget_ConfGeral)
        self.widget_Opcoesgeral.setObjectName(u"widget_Opcoesgeral")
        self.formLayout_2 = QFormLayout(self.widget_Opcoesgeral)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_Tema = QLabel(self.widget_Opcoesgeral)
        self.label_Tema.setObjectName(u"label_Tema")
        self.label_Tema.setStyleSheet(u"color: white\n"
"")
        self.label_Tema.setFrameShape(QFrame.Shape.NoFrame)
        self.label_Tema.setFrameShadow(QFrame.Shadow.Plain)
        self.label_Tema.setLineWidth(1)
        self.label_Tema.setTextFormat(Qt.TextFormat.AutoText)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_Tema)

        self.comboBox_Tema = QComboBox(self.widget_Opcoesgeral)
        self.comboBox_Tema.addItem("")
        self.comboBox_Tema.addItem("")
        self.comboBox_Tema.addItem("")
        self.comboBox_Tema.setObjectName(u"comboBox_Tema")
        self.comboBox_Tema.setEnabled(True)
        self.comboBox_Tema.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.comboBox_Tema.setFrame(True)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.comboBox_Tema)

        self.label_Atalhos = QLabel(self.widget_Opcoesgeral)
        self.label_Atalhos.setObjectName(u"label_Atalhos")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_Atalhos)

        self.toolButton_Atalhos = QToolButton(self.widget_Opcoesgeral)
        self.toolButton_Atalhos.setObjectName(u"toolButton_Atalhos")
        self.toolButton_Atalhos.setStyleSheet(u"background-color: grey;")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.toolButton_Atalhos)

        self.label_MododeOperacao = QLabel(self.widget_Opcoesgeral)
        self.label_MododeOperacao.setObjectName(u"label_MododeOperacao")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_MododeOperacao)

        self.comboBox_operacao = QComboBox(self.widget_Opcoesgeral)
        self.comboBox_operacao.addItem("")
        self.comboBox_operacao.addItem("")
        self.comboBox_operacao.addItem("")
        self.comboBox_operacao.setObjectName(u"comboBox_operacao")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.comboBox_operacao)

        self.label_PerfisRede = QLabel(self.widget_Opcoesgeral)
        self.label_PerfisRede.setObjectName(u"label_PerfisRede")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_PerfisRede)

        self.comboBox_PerfisRede = QComboBox(self.widget_Opcoesgeral)
        self.comboBox_PerfisRede.addItem("")
        self.comboBox_PerfisRede.addItem("")
        self.comboBox_PerfisRede.addItem("")
        self.comboBox_PerfisRede.setObjectName(u"comboBox_PerfisRede")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.comboBox_PerfisRede)

        self.label_FiltrodeInvasoes = QLabel(self.widget_Opcoesgeral)
        self.label_FiltrodeInvasoes.setObjectName(u"label_FiltrodeInvasoes")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_FiltrodeInvasoes)

        self.comboBox_filtro = QComboBox(self.widget_Opcoesgeral)
        self.comboBox_filtro.addItem("")
        self.comboBox_filtro.addItem("")
        self.comboBox_filtro.setObjectName(u"comboBox_filtro")

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.comboBox_filtro)

        self.label_ModoGamer = QLabel(self.widget_Opcoesgeral)
        self.label_ModoGamer.setObjectName(u"label_ModoGamer")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.label_ModoGamer)

        self.comboBox_ModoGamer = QComboBox(self.widget_Opcoesgeral)
        self.comboBox_ModoGamer.addItem("")
        self.comboBox_ModoGamer.addItem("")
        self.comboBox_ModoGamer.setObjectName(u"comboBox_ModoGamer")

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.comboBox_ModoGamer)

        self.label_PopupdeNotif = QLabel(self.widget_Opcoesgeral)
        self.label_PopupdeNotif.setObjectName(u"label_PopupdeNotif")

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.label_PopupdeNotif)

        self.comboBox_PopupdeNotif = QComboBox(self.widget_Opcoesgeral)
        self.comboBox_PopupdeNotif.addItem("")
        self.comboBox_PopupdeNotif.addItem("")
        self.comboBox_PopupdeNotif.setObjectName(u"comboBox_PopupdeNotif")

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.comboBox_PopupdeNotif)


        self.verticalLayout_2.addWidget(self.widget_Opcoesgeral)

        self.label_Background_3 = QLabel(self.tab_5)
        self.label_Background_3.setObjectName(u"label_Background_3")
        self.label_Background_3.setGeometry(QRect(760, 20, 1422, 800))
        self.label_Background_3.setPixmap(QPixmap(u"../images/imgbackground.png"))
        self.label_Background_3.setScaledContents(True)
        self.label_Background_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.widget_configuracaodeIA = QWidget(self.tab_5)
        self.widget_configuracaodeIA.setObjectName(u"widget_configuracaodeIA")
        self.widget_configuracaodeIA.setGeometry(QRect(380, 50, 331, 251))
        self.formLayout_4 = QFormLayout(self.widget_configuracaodeIA)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.checkBox_BruteForce = QCheckBox(self.widget_configuracaodeIA)
        self.checkBox_BruteForce.setObjectName(u"checkBox_BruteForce")

        self.formLayout_4.setWidget(4, QFormLayout.FieldRole, self.checkBox_BruteForce)

        self.checkBox_AcessoRemoto = QCheckBox(self.widget_configuracaodeIA)
        self.checkBox_AcessoRemoto.setObjectName(u"checkBox_AcessoRemoto")

        self.formLayout_4.setWidget(3, QFormLayout.FieldRole, self.checkBox_AcessoRemoto)

        self.checkBox_PortScan = QCheckBox(self.widget_configuracaodeIA)
        self.checkBox_PortScan.setObjectName(u"checkBox_PortScan")

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.checkBox_PortScan)

        self.checkBox_DDOS = QCheckBox(self.widget_configuracaodeIA)
        self.checkBox_DDOS.setObjectName(u"checkBox_DDOS")

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.checkBox_DDOS)

        self.label_Bruteforce = QLabel(self.widget_configuracaodeIA)
        self.label_Bruteforce.setObjectName(u"label_Bruteforce")

        self.formLayout_4.setWidget(4, QFormLayout.LabelRole, self.label_Bruteforce)

        self.label_AcessoRemoto = QLabel(self.widget_configuracaodeIA)
        self.label_AcessoRemoto.setObjectName(u"label_AcessoRemoto")

        self.formLayout_4.setWidget(3, QFormLayout.LabelRole, self.label_AcessoRemoto)

        self.label_PortScan = QLabel(self.widget_configuracaodeIA)
        self.label_PortScan.setObjectName(u"label_PortScan")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.label_PortScan)

        self.label_DDOS = QLabel(self.widget_configuracaodeIA)
        self.label_DDOS.setObjectName(u"label_DDOS")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_DDOS)

        self.label_ConfiguracaodeIA = QLabel(self.widget_configuracaodeIA)
        self.label_ConfiguracaodeIA.setObjectName(u"label_ConfiguracaodeIA")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_ConfiguracaodeIA.sizePolicy().hasHeightForWidth())
        self.label_ConfiguracaodeIA.setSizePolicy(sizePolicy1)
        self.label_ConfiguracaodeIA.setMinimumSize(QSize(20, 20))
        self.label_ConfiguracaodeIA.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(244, 203, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
"font-size: 16px;")

        self.formLayout_4.setWidget(0, QFormLayout.SpanningRole, self.label_ConfiguracaodeIA)

        self.tabHome.addTab(self.tab_5, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabHome.setCurrentIndex(3)
        self.button_Conexoes.setDefault(False)
        self.button_CriarACL.setDefault(False)
        self.button_RemoverACL.setDefault(False)


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
        self.label_Direcao.setText(QCoreApplication.translate("MainWindow", u"Dire\u00e7\u00e3o", None))
        self.label_Acao.setText(QCoreApplication.translate("MainWindow", u"A\u00e7\u00e3o", None))
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
        self.button_RemoverACL.setText(QCoreApplication.translate("MainWindow", u"Remover ACL", None))
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
        self.pushButton_Verlogs.setText(QCoreApplication.translate("MainWindow", u"Ver Logs", None))
        self.pushButton_relatrio.setText(QCoreApplication.translate("MainWindow", u"Fazer relat\u00f3rio", None))
        ___qtablewidgetitem21 = self.tableWidget_relatorio.horizontalHeaderItem(0)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Data do evento", None));
        ___qtablewidgetitem22 = self.tableWidget_relatorio.horizontalHeaderItem(1)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"Evento", None));
        ___qtablewidgetitem23 = self.tableWidget_relatorio.horizontalHeaderItem(2)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"IP", None));
        ___qtablewidgetitem24 = self.tableWidget_relatorio.horizontalHeaderItem(3)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"Porta", None));
        ___qtablewidgetitem25 = self.tableWidget_relatorio.horizontalHeaderItem(4)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"Servi\u00e7o", None));
        ___qtablewidgetitem26 = self.tableWidget_relatorio.horizontalHeaderItem(5)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"Sugest\u00e3o", None));
        self.tabHome.setTabText(self.tabHome.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Relat\u00f3rios", None))
        self.label_ConfGeral.setText(QCoreApplication.translate("MainWindow", u"Configura\u00e7\u00e3o geral", None))
        self.label_Tema.setText(QCoreApplication.translate("MainWindow", u"Tema", None))
        self.comboBox_Tema.setItemText(0, QCoreApplication.translate("MainWindow", u"Claro", None))
        self.comboBox_Tema.setItemText(1, QCoreApplication.translate("MainWindow", u"Escuro", None))
        self.comboBox_Tema.setItemText(2, QCoreApplication.translate("MainWindow", u"Op\u00e7\u00f5es", None))

        self.label_Atalhos.setText(QCoreApplication.translate("MainWindow", u"Atalhos", None))
        self.toolButton_Atalhos.setText(QCoreApplication.translate("MainWindow", u"...", None))
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

        self.label_Background_3.setText("")
        self.checkBox_BruteForce.setText(QCoreApplication.translate("MainWindow", u"Ativar", None))
        self.checkBox_AcessoRemoto.setText(QCoreApplication.translate("MainWindow", u"Ativar", None))
        self.checkBox_PortScan.setText(QCoreApplication.translate("MainWindow", u"Ativar", None))
        self.checkBox_DDOS.setText(QCoreApplication.translate("MainWindow", u"Ativar", None))
        self.label_Bruteforce.setText(QCoreApplication.translate("MainWindow", u"Brutofor\u00e7a", None))
        self.label_AcessoRemoto.setText(QCoreApplication.translate("MainWindow", u"Acesso remoto", None))
        self.label_PortScan.setText(QCoreApplication.translate("MainWindow", u"Port Scan", None))
        self.label_DDOS.setText(QCoreApplication.translate("MainWindow", u"DDoS", None))
        self.label_ConfiguracaodeIA.setText(QCoreApplication.translate("MainWindow", u"Configura\u00e7\u00e3o de IA", None))
        self.tabHome.setTabText(self.tabHome.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Configura\u00e7\u00f5es", None))
    # retranslateUi

