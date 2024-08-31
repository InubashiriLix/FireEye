# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSlider, QStatusBar, QTabWidget,
    QTableView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(907, 546)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.actionHelp = QAction(MainWindow)
        self.actionHelp.setObjectName(u"actionHelp")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_8 = QGridLayout(self.centralwidget)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.Tabs = QTabWidget(self.centralwidget)
        self.Tabs.setObjectName(u"Tabs")
        self.OutputTab = QWidget()
        self.OutputTab.setObjectName(u"OutputTab")
        self.gridLayout = QGridLayout(self.OutputTab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.playButton = QPushButton(self.OutputTab)
        self.playButton.setObjectName(u"playButton")

        self.gridLayout.addWidget(self.playButton, 2, 1, 1, 1)

        self.horizontalSlider = QSlider(self.OutputTab)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(18)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy1)
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout.addWidget(self.horizontalSlider, 2, 2, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.OutputTab)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label)

        self.label_2 = QLabel(self.OutputTab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_2)


        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 1, 1, 2)

        self.widget = QWidget(self.OutputTab)
        self.widget.setObjectName(u"widget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(2)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy2)
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.sourceDisplayLabel = QLabel(self.widget)
        self.sourceDisplayLabel.setObjectName(u"sourceDisplayLabel")
        self.sourceDisplayLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.sourceDisplayLabel)

        self.outputDisplayLabel = QLabel(self.widget)
        self.outputDisplayLabel.setObjectName(u"outputDisplayLabel")
        self.outputDisplayLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.outputDisplayLabel)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.gridLayout.addWidget(self.widget, 1, 1, 1, 2)

        self.detectStartButton = QPushButton(self.OutputTab)
        self.detectStartButton.setObjectName(u"detectStartButton")

        self.gridLayout.addWidget(self.detectStartButton, 2, 3, 1, 1)

        self.label_3 = QLabel(self.OutputTab)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 0, 3, 1, 1)

        self.listTableView = QTableView(self.OutputTab)
        self.listTableView.setObjectName(u"listTableView")

        self.gridLayout.addWidget(self.listTableView, 1, 3, 1, 1)

        self.Tabs.addTab(self.OutputTab, "")
        self.ConfigTab = QWidget()
        self.ConfigTab.setObjectName(u"ConfigTab")
        self.gridLayout_7 = QGridLayout(self.ConfigTab)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.groupBox = QGroupBox(self.ConfigTab)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.inputFileSelectButton = QPushButton(self.groupBox)
        self.inputFileSelectButton.setObjectName(u"inputFileSelectButton")

        self.gridLayout_2.addWidget(self.inputFileSelectButton, 0, 0, 1, 1)

        self.outputPathSelectPathButton = QPushButton(self.groupBox)
        self.outputPathSelectPathButton.setObjectName(u"outputPathSelectPathButton")

        self.gridLayout_2.addWidget(self.outputPathSelectPathButton, 2, 0, 1, 1)

        self.outputLineEdit = QLineEdit(self.groupBox)
        self.outputLineEdit.setObjectName(u"outputLineEdit")

        self.gridLayout_2.addWidget(self.outputLineEdit, 2, 2, 1, 2)

        self.alertAfterCompleteCheckBox = QCheckBox(self.groupBox)
        self.alertAfterCompleteCheckBox.setObjectName(u"alertAfterCompleteCheckBox")

        self.gridLayout_2.addWidget(self.alertAfterCompleteCheckBox, 3, 0, 1, 1)

        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout_2.addWidget(self.comboBox, 0, 2, 1, 2)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.ConfigTab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_5 = QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.selectModelButton = QPushButton(self.groupBox_2)
        self.selectModelButton.setObjectName(u"selectModelButton")

        self.gridLayout_4.addWidget(self.selectModelButton, 0, 0, 1, 2)

        self.modelPathLineEdit = QLineEdit(self.groupBox_2)
        self.modelPathLineEdit.setObjectName(u"modelPathLineEdit")
        self.modelPathLineEdit.setReadOnly(True)

        self.gridLayout_4.addWidget(self.modelPathLineEdit, 0, 2, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_4.addWidget(self.label_4, 1, 0, 1, 1)

        self.confidenceLineEdit = QLineEdit(self.groupBox_2)
        self.confidenceLineEdit.setObjectName(u"confidenceLineEdit")

        self.gridLayout_4.addWidget(self.confidenceLineEdit, 1, 1, 1, 2)


        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox_2, 1, 0, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout_6, 0, 0, 1, 1)

        self.Tabs.addTab(self.ConfigTab, "")

        self.gridLayout_8.addWidget(self.Tabs, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 907, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.Tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionHelp.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.playButton.setText(QCoreApplication.translate("MainWindow", u"paly/pause", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Source", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Output", None))
        self.sourceDisplayLabel.setText(QCoreApplication.translate("MainWindow", u"Source", None))
        self.outputDisplayLabel.setText(QCoreApplication.translate("MainWindow", u"Output", None))
        self.detectStartButton.setText(QCoreApplication.translate("MainWindow", u"Start Detect", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Source List", None))
        self.Tabs.setTabText(self.Tabs.indexOf(self.OutputTab), QCoreApplication.translate("MainWindow", u"TransformPage", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Common Config", None))
        self.inputFileSelectButton.setText(QCoreApplication.translate("MainWindow", u"Select Source File/Path", None))
        self.outputPathSelectPathButton.setText(QCoreApplication.translate("MainWindow", u"Select Output Path", None))
        self.alertAfterCompleteCheckBox.setText(QCoreApplication.translate("MainWindow", u"Altert After Complete", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Single File", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Floder", None))

        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Model", None))
        self.selectModelButton.setText(QCoreApplication.translate("MainWindow", u"Select Model", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Confidence", None))
        self.Tabs.setTabText(self.Tabs.indexOf(self.ConfigTab), QCoreApplication.translate("MainWindow", u"ConfigPage", None))
    # retranslateUi

