import os, platform, subprocess, shutil, stat, boto3, json, paramiko, time
from pathlib import Path
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, 
    QFont, QFontDatabase, QGradient, QIcon, QImage, QKeySequence,
    QLinearGradient, QPainter, QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QCheckBox, QGridLayout, QFrame,
    QVBoxLayout, QLabel, QLayout, QLineEdit, QMainWindow, QMessageBox, QPushButton, QSizePolicy,
    QSpacerItem, QSplitter, QStatusBar, QTabWidget, QTextBrowser, QTextEdit, QToolButton, QWidget)


class GenerateTemplate(object):

    def __init__(self):
        self.os_name = platform.system()

        try: 
            if os.environ.get('GIT_LOCAL_REPO') is None:
                raise KeyError()
            if os.environ.get('GIT_LOCAL_REPO') == '':
                raise KeyError()
        except (KeyError):
            self.proj_dir = Path(os.path.dirname(os.path.realpath(__file__)))
        else:
            self.proj_dir = os.environ.get('GIT_LOCAL_REPO')
            
        self.GITHUB_USER = subprocess.run([ "git", "config", "--file", os.path.join(self.proj_dir, ".git", "config"), "user.name" ], capture_output=True, text=True, shell=False).stdout.strip()
        self.GITHUB_EMAIL = subprocess.run([ "git", "config", "--file", os.path.join(self.proj_dir, ".git", "config"), "user.email" ], capture_output=True, text=True, shell=False).stdout.strip()
        
        try:
            if self.GITHUB_USER == '':
                raise Exception()
            if self.GITHUB_EMAIL == '':
                raise Exception()
        except (Exception):
            self.GITHUB_USER = subprocess.run([ "git", "config", "--global", "user.name" ], capture_output=True, text=True, shell=False).stdout.strip()
            self.GITHUB_EMAIL = subprocess.run([ "git", "config", "--global", "user.email" ], capture_output=True, text=True, shell=False).stdout.strip()

        self.GIT_BRANCH = subprocess.run([ "git", f"--git-dir={os.path.join(self.proj_dir, '.git')}", f"--work-tree={self.proj_dir}", "rev-parse", "--abbrev-ref", "HEAD" ], capture_output=True, text=True, shell=False).stdout.strip()
        
        self.INSTANCE_TYPES = self.get_instance_types(os.path.join(self.proj_dir, "instance_types.txt"))
        self.EXPORTED = []
        self.VARS = []
        self.AWS_ALIAS = ''
        self.AWS_ACCT = ''
        self.AWS_RGN = ''
        self.AWS_REGNAME = None
        self.AWS_HOSTID = ''
        self.AWS_ENV = ''
        self.AWS_FINCODE = ''
        self.AWS_AUTOMATIONID = None
        self.AWS_SHAREDID = None
        self.RUNNER_COUNT = 0
        self.DC_COUNT = 0
        self.HANA_COUNT = 0
        self.WIN_COUNT = 0
        self.HANAMGMT_COUNT = 0
        self.IS_COUNT = 0
        self.RDS_COUNT = 0
        self.CITRIX_COUNT = 0
        self.SQL_COUNT = 0
        self.EC2_APP_LIST = []
        self.EC2_DATA_LIST = []
        self.DC_LIST = []
        self.HANA_LIST = []
        self.HANAMGMT_LIST = []
        self.IS_LIST = []
        self.RDS_LIST = []
        self.CITRIX_LIST = []
        self.SQL_LIST = []
        self.DC_TYPE_LIST = []
        self.DC1_TYPE = ''
        self.DC2_TYPE = ''
        self.HANA_TYPE_LIST = []
        self.HANA_TYPE = ''
        self.HANAMGMT_TYPE_LIST = []
        self.IS_TYPE_LIST = []
        self.RDS_TYPE_LIST = []
        self.CITRIX_TYPE_LIST = []
        self.SQL_TYPE_LIST = []
        self.WIN1_TYPE = ''
        self.WIN2_TYPE = ''
        self.WIN3_TYPE = ''
        self.WIN4_TYPE = ''
        self.WIN5_TYPE = ''
        self.WIN6_TYPE = ''
        self.WIN1_BOX = ''
        self.WIN2_BOX = ''
        self.WIN3_BOX = ''
        self.WIN4_BOX = ''
        self.WIN5_BOX = ''
        self.WIN6_BOX = ''
        self.HANA_REVISION = ''
        self.HANA_REVISION_NAME = ''
        self.HANA_PATCH = ''
        self.HANA_PATCH_NAME = ''
        self.HANA_COCKPIT = False
        self.HANA_DEMO_DB = False

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.WindowModality.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.setFixedSize(594, 839)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(False)
        font.setKerning(True)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(u"background-color: rgb(146, 144, 0)")
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 20, 571, 801))
        self.mainGridLayout = QGridLayout(self.layoutWidget)
        self.mainGridLayout.setObjectName(u"mainGridLayout")
        self.mainGridLayout.setContentsMargins(0, 0, 0, 0)
        self.dcSplitter = QSplitter(self.layoutWidget)
        self.dcSplitter.setObjectName(u"dcSplitter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dcSplitter.sizePolicy().hasHeightForWidth())
        self.dcSplitter.setSizePolicy(sizePolicy1)
        self.dcSplitter.setOrientation(Qt.Orientation.Horizontal)
        self.dcLbl = QLabel(self.dcSplitter)
        self.dcLbl.setObjectName(u"dcLbl")
        self.dcLbl.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.dcLbl.sizePolicy().hasHeightForWidth())
        self.dcLbl.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setFamilies([u"Futura"])
        font1.setPointSize(13)
        font1.setBold(True)
        font1.setUnderline(False)
        font1.setKerning(True)
        self.dcLbl.setFont(font1)
        self.dcLbl.setStyleSheet(u"color: rgb(18, 57, 79);")
        self.dcLbl.setFrameShape(QFrame.Shape.Box)
        self.dcLbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dcLbl.setWordWrap(False)
        self.dcLbl.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.dcSplitter.addWidget(self.dcLbl)
        self.dcComboBox = QComboBox(self.dcSplitter)
        self.dcComboBox.addItem("")
        self.dcComboBox.addItem("")
        self.dcComboBox.addItem("")
        self.dcComboBox.setObjectName(u"dcComboBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.dcComboBox.sizePolicy().hasHeightForWidth())
        self.dcComboBox.setSizePolicy(sizePolicy3)
        self.dcComboBox.setMaximumSize(QSize(80, 16777215))
        font2 = QFont()
        font2.setFamilies([u"Heiti TC"])
        font2.setBold(True)
        font2.setUnderline(False)
        font2.setKerning(True)
        self.dcComboBox.setFont(font2)
        self.dcComboBox.setMouseTracking(False)
        self.dcComboBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.dcComboBox.setAutoFillBackground(False)
        self.dcComboBox.setStyleSheet(u"background-color: rgb(192, 192, 192);\n"
"color: rgb(153, 0, 0);")
        self.dcComboBox.setEditable(False)
        self.dcComboBox.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.dcSplitter.addWidget(self.dcComboBox)
        self.dcLine = QFrame(self.dcSplitter)
        self.dcLine.setObjectName(u"dcLine")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.dcLine.sizePolicy().hasHeightForWidth())
        self.dcLine.setSizePolicy(sizePolicy4)
        self.dcLine.setMinimumSize(QSize(0, 0))
        self.dcLine.setMaximumSize(QSize(120, 16777215))
        self.dcLine.setFrameShape(QFrame.Shape.HLine)
        self.dcLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.dcSplitter.addWidget(self.dcLine)

        self.mainGridLayout.addWidget(self.dcSplitter, 2, 0, 1, 1)

        self.wkVerticalSpacer = QSpacerItem(20, 3, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.mainGridLayout.addItem(self.wkVerticalSpacer, 7, 0, 1, 1)

        self.startVerticalLayout = QVBoxLayout()
        self.startVerticalLayout.setObjectName(u"startVerticalLayout")
        self.startBtn = QPushButton(self.layoutWidget)
        self.startBtn.setObjectName(u"startBtn")
        font3 = QFont()
        font3.setFamilies([u"Futura"])
        font3.setPointSize(26)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setUnderline(False)
        font3.setStrikeOut(False)
        font3.setKerning(True)
        self.startBtn.setFont(font3)
        self.startBtn.setAutoFillBackground(False)
        self.startBtn.setStyleSheet(u"background-color: rgb(18, 57, 79);\n"
"color: rgb(255, 255, 255)")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart))
        self.startBtn.setIcon(icon)
        self.startBtn.setIconSize(QSize(30, 16))
        self.startBtn.setFlat(False)

        self.startVerticalLayout.addWidget(self.startBtn)

        self.consoleLog = QTextBrowser(self.layoutWidget)
        self.consoleLog.setObjectName(u"consoleLog")
        font4 = QFont()
        font4.setFamilies([u"Futura"])
        font4.setPointSize(11)
        font4.setWeight(QFont.Thin)
        font4.setKerning(True)
        self.consoleLog.setFont(font4)
        self.consoleLog.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(33, 33, 33)")
        self.consoleLog.setFrameShape(QFrame.Shape.Box)
        self.consoleLog.setFrameShadow(QFrame.Shadow.Raised)
        self.consoleLog.setLineWidth(2)
        self.consoleLog.setMidLineWidth(0)
        self.consoleLog.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoBulletList)
        self.consoleLog.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.consoleLog.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.startVerticalLayout.addWidget(self.consoleLog)


        self.mainGridLayout.addLayout(self.startVerticalLayout, 10, 0, 1, 1)

        self.winGridLayout = QGridLayout()
        self.winGridLayout.setObjectName(u"winGridLayout")
        self.winGridLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.winTypeSplitter2 = QSplitter(self.layoutWidget)
        self.winTypeSplitter2.setObjectName(u"winTypeSplitter2")
        sizePolicy.setHeightForWidth(self.winTypeSplitter2.sizePolicy().hasHeightForWidth())
        self.winTypeSplitter2.setSizePolicy(sizePolicy)
        self.winTypeSplitter2.setOrientation(Qt.Orientation.Horizontal)
        self.winTypeComboBox2 = QComboBox(self.winTypeSplitter2)
        self.winTypeComboBox2.setObjectName(u"winTypeComboBox2")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.winTypeComboBox2.sizePolicy().hasHeightForWidth())
        self.winTypeComboBox2.setSizePolicy(sizePolicy5)
        self.winTypeComboBox2.setMinimumSize(QSize(100, 0))
        font5 = QFont()
        font5.setFamilies([u"Heiti TC"])
        self.winTypeComboBox2.setFont(font5)
        self.winTypeComboBox2.setStyleSheet(u"color: rgb(214, 214, 214);")
        self.winTypeComboBox2.setEditable(True)
        self.winTypeSplitter2.addWidget(self.winTypeComboBox2)
        self.winToolBtn2 = QToolButton(self.winTypeSplitter2)
        self.winToolBtn2.setObjectName(u"winToolBtn2")
        sizePolicy.setHeightForWidth(self.winToolBtn2.sizePolicy().hasHeightForWidth())
        self.winToolBtn2.setSizePolicy(sizePolicy)
        self.winToolBtn2.setMaximumSize(QSize(35, 16777215))
        font6 = QFont()
        font6.setFamilies([u"Heiti TC"])
        font6.setKerning(True)
        self.winToolBtn2.setFont(font6)
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DriveHarddisk))
        self.winToolBtn2.setIcon(icon1)
        self.winToolBtn2.setAutoRaise(True)
        self.winTypeSplitter2.addWidget(self.winToolBtn2)

        self.winGridLayout.addWidget(self.winTypeSplitter2, 2, 3, 1, 1)

        self.winTypeLbl4 = QLabel(self.layoutWidget)
        self.winTypeLbl4.setObjectName(u"winTypeLbl4")
        sizePolicy.setHeightForWidth(self.winTypeLbl4.sizePolicy().hasHeightForWidth())
        self.winTypeLbl4.setSizePolicy(sizePolicy)
        font7 = QFont()
        font7.setFamilies([u"Futura"])
        font7.setKerning(True)
        self.winTypeLbl4.setFont(font7)
        self.winTypeLbl4.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winTypeLbl4.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winTypeLbl4, 5, 2, 1, 1)

        self.winHostnameLineEdit5 = QLineEdit(self.layoutWidget)
        self.winHostnameLineEdit5.setObjectName(u"winHostnameLineEdit5")
        self.winHostnameLineEdit5.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.winHostnameLineEdit5.sizePolicy().hasHeightForWidth())
        self.winHostnameLineEdit5.setSizePolicy(sizePolicy4)
        self.winHostnameLineEdit5.setMaximumSize(QSize(140, 16777215))
        font8 = QFont()
        font8.setFamilies([u"Heiti TC"])
        font8.setBold(True)
        font8.setKerning(True)
        self.winHostnameLineEdit5.setFont(font8)
        self.winHostnameLineEdit5.setStyleSheet(u"color: rgb(148, 23, 81);")

        self.winGridLayout.addWidget(self.winHostnameLineEdit5, 6, 1, 1, 1)

        self.winBoxLbl2 = QLabel(self.layoutWidget)
        self.winBoxLbl2.setObjectName(u"winBoxLbl2")
        sizePolicy.setHeightForWidth(self.winBoxLbl2.sizePolicy().hasHeightForWidth())
        self.winBoxLbl2.setSizePolicy(sizePolicy)
        self.winBoxLbl2.setFont(font7)
        self.winBoxLbl2.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winBoxLbl2.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winBoxLbl2, 1, 2, 1, 1)

        self.winBoxLbl1 = QLabel(self.layoutWidget)
        self.winBoxLbl1.setObjectName(u"winBoxLbl1")
        sizePolicy.setHeightForWidth(self.winBoxLbl1.sizePolicy().hasHeightForWidth())
        self.winBoxLbl1.setSizePolicy(sizePolicy)
        self.winBoxLbl1.setFont(font7)
        self.winBoxLbl1.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winBoxLbl1.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winBoxLbl1, 1, 0, 1, 1)

        self.winBoxLbl6 = QLabel(self.layoutWidget)
        self.winBoxLbl6.setObjectName(u"winBoxLbl6")
        sizePolicy.setHeightForWidth(self.winBoxLbl6.sizePolicy().hasHeightForWidth())
        self.winBoxLbl6.setSizePolicy(sizePolicy)
        self.winBoxLbl6.setFont(font7)
        self.winBoxLbl6.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winBoxLbl6.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winBoxLbl6, 7, 2, 1, 1)

        self.winTypeSplitter1 = QSplitter(self.layoutWidget)
        self.winTypeSplitter1.setObjectName(u"winTypeSplitter1")
        sizePolicy.setHeightForWidth(self.winTypeSplitter1.sizePolicy().hasHeightForWidth())
        self.winTypeSplitter1.setSizePolicy(sizePolicy)
        self.winTypeSplitter1.setOrientation(Qt.Orientation.Horizontal)
        self.winTypeComboBox1 = QComboBox(self.winTypeSplitter1)
        self.winTypeComboBox1.setObjectName(u"winTypeComboBox1")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.winTypeComboBox1.sizePolicy().hasHeightForWidth())
        self.winTypeComboBox1.setSizePolicy(sizePolicy6)
        self.winTypeComboBox1.setMinimumSize(QSize(100, 0))
        self.winTypeComboBox1.setFont(font5)
        self.winTypeComboBox1.setStyleSheet(u"color: rgb(214, 214, 214);")
        self.winTypeComboBox1.setEditable(True)
        self.winTypeSplitter1.addWidget(self.winTypeComboBox1)
        self.winToolBtn1 = QToolButton(self.winTypeSplitter1)
        self.winToolBtn1.setObjectName(u"winToolBtn1")
        sizePolicy.setHeightForWidth(self.winToolBtn1.sizePolicy().hasHeightForWidth())
        self.winToolBtn1.setSizePolicy(sizePolicy)
        self.winToolBtn1.setMaximumSize(QSize(35, 16777215))
        self.winToolBtn1.setFont(font6)
        self.winToolBtn1.setIcon(icon1)
        self.winToolBtn1.setAutoRaise(True)
        self.winTypeSplitter1.addWidget(self.winToolBtn1)

        self.winGridLayout.addWidget(self.winTypeSplitter1, 2, 1, 1, 1)

        self.winTypeSplitter5 = QSplitter(self.layoutWidget)
        self.winTypeSplitter5.setObjectName(u"winTypeSplitter5")
        sizePolicy.setHeightForWidth(self.winTypeSplitter5.sizePolicy().hasHeightForWidth())
        self.winTypeSplitter5.setSizePolicy(sizePolicy)
        self.winTypeSplitter5.setOrientation(Qt.Orientation.Horizontal)
        self.winTypeComboBox5 = QComboBox(self.winTypeSplitter5)
        self.winTypeComboBox5.setObjectName(u"winTypeComboBox5")
        sizePolicy5.setHeightForWidth(self.winTypeComboBox5.sizePolicy().hasHeightForWidth())
        self.winTypeComboBox5.setSizePolicy(sizePolicy5)
        self.winTypeComboBox5.setMinimumSize(QSize(100, 0))
        self.winTypeComboBox5.setFont(font5)
        self.winTypeComboBox5.setStyleSheet(u"color: rgb(214, 214, 214);")
        self.winTypeComboBox5.setEditable(True)
        self.winTypeSplitter5.addWidget(self.winTypeComboBox5)
        self.winToolBtn5 = QToolButton(self.winTypeSplitter5)
        self.winToolBtn5.setObjectName(u"winToolBtn5")
        sizePolicy.setHeightForWidth(self.winToolBtn5.sizePolicy().hasHeightForWidth())
        self.winToolBtn5.setSizePolicy(sizePolicy)
        self.winToolBtn5.setMaximumSize(QSize(35, 16777215))
        self.winToolBtn5.setFont(font6)
        self.winToolBtn5.setIcon(icon1)
        self.winToolBtn5.setAutoRaise(True)
        self.winTypeSplitter5.addWidget(self.winToolBtn5)

        self.winGridLayout.addWidget(self.winTypeSplitter5, 8, 1, 1, 1)

        self.winTypeSplitter4 = QSplitter(self.layoutWidget)
        self.winTypeSplitter4.setObjectName(u"winTypeSplitter4")
        sizePolicy.setHeightForWidth(self.winTypeSplitter4.sizePolicy().hasHeightForWidth())
        self.winTypeSplitter4.setSizePolicy(sizePolicy)
        self.winTypeSplitter4.setOrientation(Qt.Orientation.Horizontal)
        self.winTypeComboBox4 = QComboBox(self.winTypeSplitter4)
        self.winTypeComboBox4.setObjectName(u"winTypeComboBox4")
        sizePolicy5.setHeightForWidth(self.winTypeComboBox4.sizePolicy().hasHeightForWidth())
        self.winTypeComboBox4.setSizePolicy(sizePolicy5)
        self.winTypeComboBox4.setMinimumSize(QSize(100, 0))
        self.winTypeComboBox4.setFont(font5)
        self.winTypeComboBox4.setStyleSheet(u"color: rgb(214, 214, 214);")
        self.winTypeComboBox4.setEditable(True)
        self.winTypeSplitter4.addWidget(self.winTypeComboBox4)
        self.winToolBtn4 = QToolButton(self.winTypeSplitter4)
        self.winToolBtn4.setObjectName(u"winToolBtn4")
        sizePolicy.setHeightForWidth(self.winToolBtn4.sizePolicy().hasHeightForWidth())
        self.winToolBtn4.setSizePolicy(sizePolicy)
        self.winToolBtn4.setMaximumSize(QSize(35, 16777215))
        self.winToolBtn4.setFont(font6)
        self.winToolBtn4.setIcon(icon1)
        self.winToolBtn4.setAutoRaise(True)
        self.winTypeSplitter4.addWidget(self.winToolBtn4)

        self.winGridLayout.addWidget(self.winTypeSplitter4, 5, 3, 1, 1)

        self.winBoxComboBox3 = QComboBox(self.layoutWidget)
        self.winBoxComboBox3.addItem("")
        self.winBoxComboBox3.addItem("")
        self.winBoxComboBox3.addItem("")
        self.winBoxComboBox3.addItem("")
        self.winBoxComboBox3.addItem("")
        self.winBoxComboBox3.setObjectName(u"winBoxComboBox3")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.winBoxComboBox3.sizePolicy().hasHeightForWidth())
        self.winBoxComboBox3.setSizePolicy(sizePolicy7)
        self.winBoxComboBox3.setFont(font5)
        self.winBoxComboBox3.setStyleSheet(u"color: rgb(214, 214, 214);")

        self.winGridLayout.addWidget(self.winBoxComboBox3, 4, 1, 1, 1)

        self.winBoxComboBox4 = QComboBox(self.layoutWidget)
        self.winBoxComboBox4.addItem("")
        self.winBoxComboBox4.addItem("")
        self.winBoxComboBox4.addItem("")
        self.winBoxComboBox4.addItem("")
        self.winBoxComboBox4.addItem("")
        self.winBoxComboBox4.setObjectName(u"winBoxComboBox4")
        sizePolicy7.setHeightForWidth(self.winBoxComboBox4.sizePolicy().hasHeightForWidth())
        self.winBoxComboBox4.setSizePolicy(sizePolicy7)
        self.winBoxComboBox4.setFont(font5)
        self.winBoxComboBox4.setStyleSheet(u"color: rgb(214, 214, 214);")

        self.winGridLayout.addWidget(self.winBoxComboBox4, 4, 3, 1, 1)

        self.winHostnameLineEdit2 = QLineEdit(self.layoutWidget)
        self.winHostnameLineEdit2.setObjectName(u"winHostnameLineEdit2")
        self.winHostnameLineEdit2.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.winHostnameLineEdit2.sizePolicy().hasHeightForWidth())
        self.winHostnameLineEdit2.setSizePolicy(sizePolicy4)
        self.winHostnameLineEdit2.setMaximumSize(QSize(140, 16777215))
        self.winHostnameLineEdit2.setFont(font8)
        self.winHostnameLineEdit2.setStyleSheet(u"color: rgb(148, 23, 81);")

        self.winGridLayout.addWidget(self.winHostnameLineEdit2, 0, 3, 1, 1)

        self.winBoxLbl4 = QLabel(self.layoutWidget)
        self.winBoxLbl4.setObjectName(u"winBoxLbl4")
        sizePolicy.setHeightForWidth(self.winBoxLbl4.sizePolicy().hasHeightForWidth())
        self.winBoxLbl4.setSizePolicy(sizePolicy)
        self.winBoxLbl4.setFont(font7)
        self.winBoxLbl4.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winBoxLbl4.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winBoxLbl4, 4, 2, 1, 1)

        self.winHostnameLbl6 = QLabel(self.layoutWidget)
        self.winHostnameLbl6.setObjectName(u"winHostnameLbl6")
        self.winHostnameLbl6.setEnabled(True)
        sizePolicy.setHeightForWidth(self.winHostnameLbl6.sizePolicy().hasHeightForWidth())
        self.winHostnameLbl6.setSizePolicy(sizePolicy)
        self.winHostnameLbl6.setFont(font7)
        self.winHostnameLbl6.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winHostnameLbl6.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winHostnameLbl6, 6, 2, 1, 1)

        self.winHostnameLbl1 = QLabel(self.layoutWidget)
        self.winHostnameLbl1.setObjectName(u"winHostnameLbl1")
        self.winHostnameLbl1.setEnabled(True)
        sizePolicy.setHeightForWidth(self.winHostnameLbl1.sizePolicy().hasHeightForWidth())
        self.winHostnameLbl1.setSizePolicy(sizePolicy)
        self.winHostnameLbl1.setFont(font7)
        self.winHostnameLbl1.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winHostnameLbl1.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winHostnameLbl1, 0, 0, 1, 1)

        self.winHostnameLbl2 = QLabel(self.layoutWidget)
        self.winHostnameLbl2.setObjectName(u"winHostnameLbl2")
        self.winHostnameLbl2.setEnabled(True)
        sizePolicy.setHeightForWidth(self.winHostnameLbl2.sizePolicy().hasHeightForWidth())
        self.winHostnameLbl2.setSizePolicy(sizePolicy)
        self.winHostnameLbl2.setFont(font7)
        self.winHostnameLbl2.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winHostnameLbl2.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winHostnameLbl2, 0, 2, 1, 1)

        self.winBoxLbl5 = QLabel(self.layoutWidget)
        self.winBoxLbl5.setObjectName(u"winBoxLbl5")
        sizePolicy.setHeightForWidth(self.winBoxLbl5.sizePolicy().hasHeightForWidth())
        self.winBoxLbl5.setSizePolicy(sizePolicy)
        self.winBoxLbl5.setFont(font7)
        self.winBoxLbl5.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winBoxLbl5.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winBoxLbl5, 7, 0, 1, 1)

        self.winHostnameLbl4 = QLabel(self.layoutWidget)
        self.winHostnameLbl4.setObjectName(u"winHostnameLbl4")
        self.winHostnameLbl4.setEnabled(True)
        sizePolicy.setHeightForWidth(self.winHostnameLbl4.sizePolicy().hasHeightForWidth())
        self.winHostnameLbl4.setSizePolicy(sizePolicy)
        self.winHostnameLbl4.setFont(font7)
        self.winHostnameLbl4.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winHostnameLbl4.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winHostnameLbl4, 3, 2, 1, 1)

        self.winHostnameLineEdit6 = QLineEdit(self.layoutWidget)
        self.winHostnameLineEdit6.setObjectName(u"winHostnameLineEdit6")
        self.winHostnameLineEdit6.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.winHostnameLineEdit6.sizePolicy().hasHeightForWidth())
        self.winHostnameLineEdit6.setSizePolicy(sizePolicy4)
        self.winHostnameLineEdit6.setMaximumSize(QSize(140, 16777215))
        self.winHostnameLineEdit6.setFont(font8)
        self.winHostnameLineEdit6.setStyleSheet(u"color: rgb(148, 23, 81);")

        self.winGridLayout.addWidget(self.winHostnameLineEdit6, 6, 3, 1, 1)

        self.winTypeLbl6 = QLabel(self.layoutWidget)
        self.winTypeLbl6.setObjectName(u"winTypeLbl6")
        sizePolicy.setHeightForWidth(self.winTypeLbl6.sizePolicy().hasHeightForWidth())
        self.winTypeLbl6.setSizePolicy(sizePolicy)
        self.winTypeLbl6.setFont(font7)
        self.winTypeLbl6.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winTypeLbl6.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winTypeLbl6, 8, 2, 1, 1)

        self.winTypeLbl3 = QLabel(self.layoutWidget)
        self.winTypeLbl3.setObjectName(u"winTypeLbl3")
        sizePolicy.setHeightForWidth(self.winTypeLbl3.sizePolicy().hasHeightForWidth())
        self.winTypeLbl3.setSizePolicy(sizePolicy)
        self.winTypeLbl3.setFont(font7)
        self.winTypeLbl3.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winTypeLbl3.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winTypeLbl3, 5, 0, 1, 1)

        self.winTypeLbl5 = QLabel(self.layoutWidget)
        self.winTypeLbl5.setObjectName(u"winTypeLbl5")
        sizePolicy.setHeightForWidth(self.winTypeLbl5.sizePolicy().hasHeightForWidth())
        self.winTypeLbl5.setSizePolicy(sizePolicy)
        self.winTypeLbl5.setFont(font7)
        self.winTypeLbl5.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winTypeLbl5.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winTypeLbl5, 8, 0, 1, 1)

        self.winBoxLbl3 = QLabel(self.layoutWidget)
        self.winBoxLbl3.setObjectName(u"winBoxLbl3")
        sizePolicy.setHeightForWidth(self.winBoxLbl3.sizePolicy().hasHeightForWidth())
        self.winBoxLbl3.setSizePolicy(sizePolicy)
        self.winBoxLbl3.setFont(font7)
        self.winBoxLbl3.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winBoxLbl3.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winBoxLbl3, 4, 0, 1, 1)

        self.winTypeSplitter6 = QSplitter(self.layoutWidget)
        self.winTypeSplitter6.setObjectName(u"winTypeSplitter6")
        sizePolicy.setHeightForWidth(self.winTypeSplitter6.sizePolicy().hasHeightForWidth())
        self.winTypeSplitter6.setSizePolicy(sizePolicy)
        self.winTypeSplitter6.setOrientation(Qt.Orientation.Horizontal)
        self.winTypeComboBox6 = QComboBox(self.winTypeSplitter6)
        self.winTypeComboBox6.setObjectName(u"winTypeComboBox6")
        sizePolicy5.setHeightForWidth(self.winTypeComboBox6.sizePolicy().hasHeightForWidth())
        self.winTypeComboBox6.setSizePolicy(sizePolicy5)
        self.winTypeComboBox6.setMinimumSize(QSize(100, 0))
        self.winTypeComboBox6.setFont(font5)
        self.winTypeComboBox6.setStyleSheet(u"color: rgb(214, 214, 214);")
        self.winTypeComboBox6.setEditable(True)
        self.winTypeSplitter6.addWidget(self.winTypeComboBox6)
        self.winToolBtn6 = QToolButton(self.winTypeSplitter6)
        self.winToolBtn6.setObjectName(u"winToolBtn6")
        sizePolicy.setHeightForWidth(self.winToolBtn6.sizePolicy().hasHeightForWidth())
        self.winToolBtn6.setSizePolicy(sizePolicy)
        self.winToolBtn6.setMaximumSize(QSize(35, 16777215))
        self.winToolBtn6.setFont(font6)
        self.winToolBtn6.setIcon(icon1)
        self.winToolBtn6.setAutoRaise(True)
        self.winTypeSplitter6.addWidget(self.winToolBtn6)

        self.winGridLayout.addWidget(self.winTypeSplitter6, 8, 3, 1, 1)

        self.winHostnameLineEdit1 = QLineEdit(self.layoutWidget)
        self.winHostnameLineEdit1.setObjectName(u"winHostnameLineEdit1")
        self.winHostnameLineEdit1.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.winHostnameLineEdit1.sizePolicy().hasHeightForWidth())
        self.winHostnameLineEdit1.setSizePolicy(sizePolicy4)
        self.winHostnameLineEdit1.setMaximumSize(QSize(140, 16777215))
        self.winHostnameLineEdit1.setFont(font8)
        self.winHostnameLineEdit1.setStyleSheet(u"color: rgb(148, 23, 81);")

        self.winGridLayout.addWidget(self.winHostnameLineEdit1, 0, 1, 1, 1)

        self.winBoxComboBox1 = QComboBox(self.layoutWidget)
        self.winBoxComboBox1.addItem("")
        self.winBoxComboBox1.addItem("")
        self.winBoxComboBox1.addItem("")
        self.winBoxComboBox1.addItem("")
        self.winBoxComboBox1.addItem("")
        self.winBoxComboBox1.setObjectName(u"winBoxComboBox1")
        sizePolicy7.setHeightForWidth(self.winBoxComboBox1.sizePolicy().hasHeightForWidth())
        self.winBoxComboBox1.setSizePolicy(sizePolicy7)
        self.winBoxComboBox1.setFont(font5)
        self.winBoxComboBox1.setStyleSheet(u"color: rgb(214, 214, 214);")

        self.winGridLayout.addWidget(self.winBoxComboBox1, 1, 1, 1, 1)

        self.winTypeLbl1 = QLabel(self.layoutWidget)
        self.winTypeLbl1.setObjectName(u"winTypeLbl1")
        sizePolicy.setHeightForWidth(self.winTypeLbl1.sizePolicy().hasHeightForWidth())
        self.winTypeLbl1.setSizePolicy(sizePolicy)
        self.winTypeLbl1.setFont(font7)
        self.winTypeLbl1.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winTypeLbl1.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winTypeLbl1, 2, 0, 1, 1)

        self.winHostnameLineEdit3 = QLineEdit(self.layoutWidget)
        self.winHostnameLineEdit3.setObjectName(u"winHostnameLineEdit3")
        self.winHostnameLineEdit3.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.winHostnameLineEdit3.sizePolicy().hasHeightForWidth())
        self.winHostnameLineEdit3.setSizePolicy(sizePolicy4)
        self.winHostnameLineEdit3.setMaximumSize(QSize(140, 16777215))
        self.winHostnameLineEdit3.setFont(font8)
        self.winHostnameLineEdit3.setStyleSheet(u"color: rgb(148, 23, 81);")

        self.winGridLayout.addWidget(self.winHostnameLineEdit3, 3, 1, 1, 1)

        self.winBoxComboBox2 = QComboBox(self.layoutWidget)
        self.winBoxComboBox2.addItem("")
        self.winBoxComboBox2.addItem("")
        self.winBoxComboBox2.addItem("")
        self.winBoxComboBox2.addItem("")
        self.winBoxComboBox2.addItem("")
        self.winBoxComboBox2.setObjectName(u"winBoxComboBox2")
        sizePolicy7.setHeightForWidth(self.winBoxComboBox2.sizePolicy().hasHeightForWidth())
        self.winBoxComboBox2.setSizePolicy(sizePolicy7)
        self.winBoxComboBox2.setFont(font5)
        self.winBoxComboBox2.setStyleSheet(u"color: rgb(214, 214, 214);")

        self.winGridLayout.addWidget(self.winBoxComboBox2, 1, 3, 1, 1)

        self.winBoxComboBox5 = QComboBox(self.layoutWidget)
        self.winBoxComboBox5.addItem("")
        self.winBoxComboBox5.addItem("")
        self.winBoxComboBox5.addItem("")
        self.winBoxComboBox5.addItem("")
        self.winBoxComboBox5.addItem("")
        self.winBoxComboBox5.setObjectName(u"winBoxComboBox5")
        sizePolicy7.setHeightForWidth(self.winBoxComboBox5.sizePolicy().hasHeightForWidth())
        self.winBoxComboBox5.setSizePolicy(sizePolicy7)
        self.winBoxComboBox5.setFont(font5)
        self.winBoxComboBox5.setStyleSheet(u"color: rgb(214, 214, 214);")

        self.winGridLayout.addWidget(self.winBoxComboBox5, 7, 1, 1, 1)

        self.winHostnameLbl3 = QLabel(self.layoutWidget)
        self.winHostnameLbl3.setObjectName(u"winHostnameLbl3")
        self.winHostnameLbl3.setEnabled(True)
        sizePolicy.setHeightForWidth(self.winHostnameLbl3.sizePolicy().hasHeightForWidth())
        self.winHostnameLbl3.setSizePolicy(sizePolicy)
        self.winHostnameLbl3.setFont(font7)
        self.winHostnameLbl3.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winHostnameLbl3.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winHostnameLbl3, 3, 0, 1, 1)

        self.winTypeLbl2 = QLabel(self.layoutWidget)
        self.winTypeLbl2.setObjectName(u"winTypeLbl2")
        sizePolicy.setHeightForWidth(self.winTypeLbl2.sizePolicy().hasHeightForWidth())
        self.winTypeLbl2.setSizePolicy(sizePolicy)
        self.winTypeLbl2.setFont(font7)
        self.winTypeLbl2.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winTypeLbl2.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winTypeLbl2, 2, 2, 1, 1)

        self.winHostnameLineEdit4 = QLineEdit(self.layoutWidget)
        self.winHostnameLineEdit4.setObjectName(u"winHostnameLineEdit4")
        self.winHostnameLineEdit4.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.winHostnameLineEdit4.sizePolicy().hasHeightForWidth())
        self.winHostnameLineEdit4.setSizePolicy(sizePolicy4)
        self.winHostnameLineEdit4.setMaximumSize(QSize(140, 16777215))
        self.winHostnameLineEdit4.setFont(font8)
        self.winHostnameLineEdit4.setStyleSheet(u"color: rgb(148, 23, 81);")

        self.winGridLayout.addWidget(self.winHostnameLineEdit4, 3, 3, 1, 1)

        self.winTypeSplitter3 = QSplitter(self.layoutWidget)
        self.winTypeSplitter3.setObjectName(u"winTypeSplitter3")
        sizePolicy.setHeightForWidth(self.winTypeSplitter3.sizePolicy().hasHeightForWidth())
        self.winTypeSplitter3.setSizePolicy(sizePolicy)
        self.winTypeSplitter3.setOrientation(Qt.Orientation.Horizontal)
        self.winTypeComboBox3 = QComboBox(self.winTypeSplitter3)
        self.winTypeComboBox3.setObjectName(u"winTypeComboBox3")
        sizePolicy5.setHeightForWidth(self.winTypeComboBox3.sizePolicy().hasHeightForWidth())
        self.winTypeComboBox3.setSizePolicy(sizePolicy5)
        self.winTypeComboBox3.setMinimumSize(QSize(100, 0))
        self.winTypeComboBox3.setFont(font5)
        self.winTypeComboBox3.setStyleSheet(u"color: rgb(214, 214, 214);")
        self.winTypeComboBox3.setEditable(True)
        self.winTypeSplitter3.addWidget(self.winTypeComboBox3)
        self.winToolBtn3 = QToolButton(self.winTypeSplitter3)
        self.winToolBtn3.setObjectName(u"winToolBtn3")
        sizePolicy.setHeightForWidth(self.winToolBtn3.sizePolicy().hasHeightForWidth())
        self.winToolBtn3.setSizePolicy(sizePolicy)
        self.winToolBtn3.setMaximumSize(QSize(35, 16777215))
        self.winToolBtn3.setFont(font6)
        self.winToolBtn3.setIcon(icon1)
        self.winToolBtn3.setAutoRaise(True)
        self.winTypeSplitter3.addWidget(self.winToolBtn3)

        self.winGridLayout.addWidget(self.winTypeSplitter3, 5, 1, 1, 1)

        self.winBoxComboBox6 = QComboBox(self.layoutWidget)
        self.winBoxComboBox6.addItem("")
        self.winBoxComboBox6.addItem("")
        self.winBoxComboBox6.addItem("")
        self.winBoxComboBox6.addItem("")
        self.winBoxComboBox6.addItem("")
        self.winBoxComboBox6.setObjectName(u"winBoxComboBox6")
        sizePolicy7.setHeightForWidth(self.winBoxComboBox6.sizePolicy().hasHeightForWidth())
        self.winBoxComboBox6.setSizePolicy(sizePolicy7)
        self.winBoxComboBox6.setFont(font5)
        self.winBoxComboBox6.setStyleSheet(u"color: rgb(214, 214, 214);")

        self.winGridLayout.addWidget(self.winBoxComboBox6, 7, 3, 1, 1)

        self.winHostnameLbl5 = QLabel(self.layoutWidget)
        self.winHostnameLbl5.setObjectName(u"winHostnameLbl5")
        self.winHostnameLbl5.setEnabled(True)
        sizePolicy.setHeightForWidth(self.winHostnameLbl5.sizePolicy().hasHeightForWidth())
        self.winHostnameLbl5.setSizePolicy(sizePolicy)
        self.winHostnameLbl5.setFont(font7)
        self.winHostnameLbl5.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.winHostnameLbl5.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.winGridLayout.addWidget(self.winHostnameLbl5, 6, 0, 1, 1)


        self.mainGridLayout.addLayout(self.winGridLayout, 9, 0, 1, 1)

        self.winSplitter = QSplitter(self.layoutWidget)
        self.winSplitter.setObjectName(u"winSplitter")
        sizePolicy1.setHeightForWidth(self.winSplitter.sizePolicy().hasHeightForWidth())
        self.winSplitter.setSizePolicy(sizePolicy1)
        self.winSplitter.setOrientation(Qt.Orientation.Horizontal)
        self.winLbl = QLabel(self.winSplitter)
        self.winLbl.setObjectName(u"winLbl")
        self.winLbl.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.winLbl.sizePolicy().hasHeightForWidth())
        self.winLbl.setSizePolicy(sizePolicy2)
        self.winLbl.setFont(font1)
        self.winLbl.setStyleSheet(u"color: rgb(18, 57, 79);")
        self.winLbl.setFrameShape(QFrame.Shape.Box)
        self.winLbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.winLbl.setWordWrap(False)
        self.winLbl.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.winSplitter.addWidget(self.winLbl)
        self.winComboBox = QComboBox(self.winSplitter)
        self.winComboBox.addItem("")
        self.winComboBox.addItem("")
        self.winComboBox.addItem("")
        self.winComboBox.addItem("")
        self.winComboBox.addItem("")
        self.winComboBox.addItem("")
        self.winComboBox.addItem("")
        self.winComboBox.setObjectName(u"winComboBox")
        sizePolicy3.setHeightForWidth(self.winComboBox.sizePolicy().hasHeightForWidth())
        self.winComboBox.setSizePolicy(sizePolicy3)
        self.winComboBox.setMaximumSize(QSize(80, 16777215))
        font9 = QFont()
        font9.setFamilies([u"Heiti TC"])
        font9.setBold(True)
        self.winComboBox.setFont(font9)
        self.winComboBox.setStyleSheet(u"background-color: rgb(192, 192, 192);\n"
"color: rgb(153, 0, 0);")
        self.winComboBox.setEditable(False)
        self.winComboBox.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.winSplitter.addWidget(self.winComboBox)
        self.winLine = QFrame(self.winSplitter)
        self.winLine.setObjectName(u"winLine")
        sizePolicy4.setHeightForWidth(self.winLine.sizePolicy().hasHeightForWidth())
        self.winLine.setSizePolicy(sizePolicy4)
        self.winLine.setMaximumSize(QSize(120, 16777215))
        self.winLine.setFrameShape(QFrame.Shape.HLine)
        self.winLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.winSplitter.addWidget(self.winLine)

        self.mainGridLayout.addWidget(self.winSplitter, 8, 0, 1, 1)

        self.dcGridLayout = QGridLayout()
        self.dcGridLayout.setObjectName(u"dcGridLayout")
        self.dcGridLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.dcTypeLbl2 = QLabel(self.layoutWidget)
        self.dcTypeLbl2.setObjectName(u"dcTypeLbl2")
        sizePolicy.setHeightForWidth(self.dcTypeLbl2.sizePolicy().hasHeightForWidth())
        self.dcTypeLbl2.setSizePolicy(sizePolicy)
        self.dcTypeLbl2.setFont(font7)
        self.dcTypeLbl2.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.dcTypeLbl2.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.dcGridLayout.addWidget(self.dcTypeLbl2, 2, 2, 1, 1)

        self.dcTypeSplitter1 = QSplitter(self.layoutWidget)
        self.dcTypeSplitter1.setObjectName(u"dcTypeSplitter1")
        sizePolicy.setHeightForWidth(self.dcTypeSplitter1.sizePolicy().hasHeightForWidth())
        self.dcTypeSplitter1.setSizePolicy(sizePolicy)
        self.dcTypeSplitter1.setOrientation(Qt.Orientation.Horizontal)
        self.dcTypeComboBox1 = QComboBox(self.dcTypeSplitter1)
        self.dcTypeComboBox1.setObjectName(u"dcTypeComboBox1")
        sizePolicy5.setHeightForWidth(self.dcTypeComboBox1.sizePolicy().hasHeightForWidth())
        self.dcTypeComboBox1.setSizePolicy(sizePolicy5)
        self.dcTypeComboBox1.setMinimumSize(QSize(100, 0))
        self.dcTypeComboBox1.setFont(font5)
        self.dcTypeComboBox1.setStyleSheet(u"color: rgb(214, 214, 214);")
        self.dcTypeComboBox1.setEditable(True)
        self.dcTypeSplitter1.addWidget(self.dcTypeComboBox1)
        self.dcToolBtn1 = QToolButton(self.dcTypeSplitter1)
        self.dcToolBtn1.setObjectName(u"dcToolBtn1")
        sizePolicy.setHeightForWidth(self.dcToolBtn1.sizePolicy().hasHeightForWidth())
        self.dcToolBtn1.setSizePolicy(sizePolicy)
        self.dcToolBtn1.setMaximumSize(QSize(35, 16777215))
        self.dcToolBtn1.setFont(font6)
        self.dcToolBtn1.setStyleSheet(u"")
        self.dcToolBtn1.setIcon(icon1)
        self.dcToolBtn1.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.dcToolBtn1.setAutoRaise(True)
        self.dcTypeSplitter1.addWidget(self.dcToolBtn1)

        self.dcGridLayout.addWidget(self.dcTypeSplitter1, 2, 1, 1, 1, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.dcHostnameLbl2 = QLabel(self.layoutWidget)
        self.dcHostnameLbl2.setObjectName(u"dcHostnameLbl2")
        self.dcHostnameLbl2.setEnabled(True)
        sizePolicy.setHeightForWidth(self.dcHostnameLbl2.sizePolicy().hasHeightForWidth())
        self.dcHostnameLbl2.setSizePolicy(sizePolicy)
        font10 = QFont()
        font10.setFamilies([u"Futura"])
        font10.setPointSize(13)
        font10.setBold(False)
        font10.setKerning(True)
        self.dcHostnameLbl2.setFont(font10)
        self.dcHostnameLbl2.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.dcHostnameLbl2.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.dcGridLayout.addWidget(self.dcHostnameLbl2, 1, 2, 1, 1)

        self.dcHostnameLbl1 = QLabel(self.layoutWidget)
        self.dcHostnameLbl1.setObjectName(u"dcHostnameLbl1")
        self.dcHostnameLbl1.setEnabled(True)
        sizePolicy.setHeightForWidth(self.dcHostnameLbl1.sizePolicy().hasHeightForWidth())
        self.dcHostnameLbl1.setSizePolicy(sizePolicy)
        self.dcHostnameLbl1.setFont(font10)
        self.dcHostnameLbl1.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.dcHostnameLbl1.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.dcGridLayout.addWidget(self.dcHostnameLbl1, 1, 0, 1, 1)

        self.dcHostnameLineEdit2 = QLineEdit(self.layoutWidget)
        self.dcHostnameLineEdit2.setObjectName(u"dcHostnameLineEdit2")
        self.dcHostnameLineEdit2.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.dcHostnameLineEdit2.sizePolicy().hasHeightForWidth())
        self.dcHostnameLineEdit2.setSizePolicy(sizePolicy4)
        self.dcHostnameLineEdit2.setMaximumSize(QSize(140, 16777215))
        self.dcHostnameLineEdit2.setFont(font8)
        self.dcHostnameLineEdit2.setStyleSheet(u"color: rgb(148, 23, 81);")
        self.dcHostnameLineEdit2.setCursorMoveStyle(Qt.CursorMoveStyle.LogicalMoveStyle)

        self.dcGridLayout.addWidget(self.dcHostnameLineEdit2, 1, 3, 1, 1)

        self.dcTypeSplitter2 = QSplitter(self.layoutWidget)
        self.dcTypeSplitter2.setObjectName(u"dcTypeSplitter2")
        sizePolicy.setHeightForWidth(self.dcTypeSplitter2.sizePolicy().hasHeightForWidth())
        self.dcTypeSplitter2.setSizePolicy(sizePolicy)
        self.dcTypeSplitter2.setOrientation(Qt.Orientation.Horizontal)
        self.dcTypeComboBox2 = QComboBox(self.dcTypeSplitter2)
        self.dcTypeComboBox2.setObjectName(u"dcTypeComboBox2")
        sizePolicy5.setHeightForWidth(self.dcTypeComboBox2.sizePolicy().hasHeightForWidth())
        self.dcTypeComboBox2.setSizePolicy(sizePolicy5)
        self.dcTypeComboBox2.setMinimumSize(QSize(100, 0))
        self.dcTypeComboBox2.setFont(font5)
        self.dcTypeComboBox2.setStyleSheet(u"color: rgb(214, 214, 214);")
        self.dcTypeComboBox2.setEditable(True)
        self.dcTypeSplitter2.addWidget(self.dcTypeComboBox2)
        self.dcToolBtn2 = QToolButton(self.dcTypeSplitter2)
        self.dcToolBtn2.setObjectName(u"dcToolBtn2")
        sizePolicy.setHeightForWidth(self.dcToolBtn2.sizePolicy().hasHeightForWidth())
        self.dcToolBtn2.setSizePolicy(sizePolicy)
        self.dcToolBtn2.setMaximumSize(QSize(35, 16777215))
        self.dcToolBtn2.setFont(font6)
        self.dcToolBtn2.setStyleSheet(u"")
        self.dcToolBtn2.setIcon(icon1)
        self.dcToolBtn2.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.dcToolBtn2.setAutoRaise(True)
        self.dcTypeSplitter2.addWidget(self.dcToolBtn2)

        self.dcGridLayout.addWidget(self.dcTypeSplitter2, 2, 3, 1, 1, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.dcHostnameLineEdit1 = QLineEdit(self.layoutWidget)
        self.dcHostnameLineEdit1.setObjectName(u"dcHostnameLineEdit1")
        self.dcHostnameLineEdit1.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.dcHostnameLineEdit1.sizePolicy().hasHeightForWidth())
        self.dcHostnameLineEdit1.setSizePolicy(sizePolicy4)
        self.dcHostnameLineEdit1.setMaximumSize(QSize(140, 16777215))
        self.dcHostnameLineEdit1.setFont(font8)
        self.dcHostnameLineEdit1.setStyleSheet(u"color: rgb(148, 23, 81);")
        self.dcHostnameLineEdit1.setCursorMoveStyle(Qt.CursorMoveStyle.LogicalMoveStyle)

        self.dcGridLayout.addWidget(self.dcHostnameLineEdit1, 1, 1, 1, 1)

        self.dcTypeLbl1 = QLabel(self.layoutWidget)
        self.dcTypeLbl1.setObjectName(u"dcTypeLbl1")
        sizePolicy.setHeightForWidth(self.dcTypeLbl1.sizePolicy().hasHeightForWidth())
        self.dcTypeLbl1.setSizePolicy(sizePolicy)
        self.dcTypeLbl1.setFont(font7)
        self.dcTypeLbl1.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.dcTypeLbl1.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.dcGridLayout.addWidget(self.dcTypeLbl1, 2, 0, 1, 1)


        self.mainGridLayout.addLayout(self.dcGridLayout, 3, 0, 1, 1)

        self.hanaSplitter = QSplitter(self.layoutWidget)
        self.hanaSplitter.setObjectName(u"hanaSplitter")
        sizePolicy1.setHeightForWidth(self.hanaSplitter.sizePolicy().hasHeightForWidth())
        self.hanaSplitter.setSizePolicy(sizePolicy1)
        self.hanaSplitter.setOrientation(Qt.Orientation.Horizontal)
        self.dcLbl_2 = QLabel(self.hanaSplitter)
        self.dcLbl_2.setObjectName(u"dcLbl_2")
        self.dcLbl_2.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.dcLbl_2.sizePolicy().hasHeightForWidth())
        self.dcLbl_2.setSizePolicy(sizePolicy2)
        self.dcLbl_2.setFont(font1)
        self.dcLbl_2.setStyleSheet(u"color: rgb(18, 57, 79);")
        self.dcLbl_2.setFrameShape(QFrame.Shape.Box)
        self.dcLbl_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dcLbl_2.setWordWrap(False)
        self.dcLbl_2.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.hanaSplitter.addWidget(self.dcLbl_2)
        self.hanaComboBox = QComboBox(self.hanaSplitter)
        self.hanaComboBox.addItem("")
        self.hanaComboBox.addItem("")
        self.hanaComboBox.setObjectName(u"hanaComboBox")
        sizePolicy3.setHeightForWidth(self.hanaComboBox.sizePolicy().hasHeightForWidth())
        self.hanaComboBox.setSizePolicy(sizePolicy3)
        self.hanaComboBox.setMaximumSize(QSize(80, 16777215))
        self.hanaComboBox.setFont(font9)
        self.hanaComboBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.hanaComboBox.setAutoFillBackground(False)
        self.hanaComboBox.setStyleSheet(u"background-color: rgb(192, 192, 192);\n"
"color: rgb(153, 0, 0);")
        self.hanaComboBox.setEditable(False)
        self.hanaComboBox.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.hanaSplitter.addWidget(self.hanaComboBox)
        self.hanaLine = QFrame(self.hanaSplitter)
        self.hanaLine.setObjectName(u"hanaLine")
        sizePolicy4.setHeightForWidth(self.hanaLine.sizePolicy().hasHeightForWidth())
        self.hanaLine.setSizePolicy(sizePolicy4)
        self.hanaLine.setMaximumSize(QSize(120, 16777215))
        self.hanaLine.setFrameShape(QFrame.Shape.HLine)
        self.hanaLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.hanaSplitter.addWidget(self.hanaLine)

        self.mainGridLayout.addWidget(self.hanaSplitter, 5, 0, 1, 1)

        self.hanaGridLayout = QGridLayout()
        self.hanaGridLayout.setObjectName(u"hanaGridLayout")
        self.hanaGridLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.hanaHostnameLbl = QLabel(self.layoutWidget)
        self.hanaHostnameLbl.setObjectName(u"hanaHostnameLbl")
        self.hanaHostnameLbl.setEnabled(True)
        sizePolicy.setHeightForWidth(self.hanaHostnameLbl.sizePolicy().hasHeightForWidth())
        self.hanaHostnameLbl.setSizePolicy(sizePolicy)
        self.hanaHostnameLbl.setFont(font7)
        self.hanaHostnameLbl.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.hanaHostnameLbl.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.hanaGridLayout.addWidget(self.hanaHostnameLbl, 0, 0, 1, 1)

        self.hanaTypeLbl = QLabel(self.layoutWidget)
        self.hanaTypeLbl.setObjectName(u"hanaTypeLbl")
        sizePolicy.setHeightForWidth(self.hanaTypeLbl.sizePolicy().hasHeightForWidth())
        self.hanaTypeLbl.setSizePolicy(sizePolicy)
        self.hanaTypeLbl.setFont(font7)
        self.hanaTypeLbl.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.hanaTypeLbl.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.hanaGridLayout.addWidget(self.hanaTypeLbl, 1, 0, 1, 1)

        self.hanaCockpitCheckBox = QCheckBox(self.layoutWidget)
        self.hanaCockpitCheckBox.setObjectName(u"hanaCockpitCheckBox")
        sizePolicy.setHeightForWidth(self.hanaCockpitCheckBox.sizePolicy().hasHeightForWidth())
        self.hanaCockpitCheckBox.setSizePolicy(sizePolicy)
        self.hanaCockpitCheckBox.setChecked(True)

        self.hanaGridLayout.addWidget(self.hanaCockpitCheckBox, 4, 1, 1, 1)

        self.hanaTypeSplitter = QSplitter(self.layoutWidget)
        self.hanaTypeSplitter.setObjectName(u"hanaTypeSplitter")
        sizePolicy.setHeightForWidth(self.hanaTypeSplitter.sizePolicy().hasHeightForWidth())
        self.hanaTypeSplitter.setSizePolicy(sizePolicy)
        self.hanaTypeSplitter.setOrientation(Qt.Orientation.Horizontal)
        self.hanaTypeComboBox = QComboBox(self.hanaTypeSplitter)
        self.hanaTypeComboBox.setObjectName(u"hanaTypeComboBox")
        sizePolicy5.setHeightForWidth(self.hanaTypeComboBox.sizePolicy().hasHeightForWidth())
        self.hanaTypeComboBox.setSizePolicy(sizePolicy5)
        self.hanaTypeComboBox.setMinimumSize(QSize(100, 0))
        self.hanaTypeComboBox.setFont(font5)
        self.hanaTypeComboBox.setStyleSheet(u"color: rgb(214, 214, 214);")
        self.hanaTypeComboBox.setEditable(True)
        self.hanaTypeSplitter.addWidget(self.hanaTypeComboBox)
        self.hanaToolBtn = QToolButton(self.hanaTypeSplitter)
        self.hanaToolBtn.setObjectName(u"hanaToolBtn")
        sizePolicy.setHeightForWidth(self.hanaToolBtn.sizePolicy().hasHeightForWidth())
        self.hanaToolBtn.setSizePolicy(sizePolicy)
        self.hanaToolBtn.setMaximumSize(QSize(35, 16777215))
        self.hanaToolBtn.setFont(font6)
        self.hanaToolBtn.setIcon(icon1)
        self.hanaToolBtn.setAutoRaise(True)
        self.hanaTypeSplitter.addWidget(self.hanaToolBtn)

        self.hanaGridLayout.addWidget(self.hanaTypeSplitter, 1, 1, 1, 1)

        self.hanaClientPkgComboBox = QComboBox(self.layoutWidget)
        self.hanaClientPkgComboBox.addItem("")
        self.hanaClientPkgComboBox.addItem("")
        self.hanaClientPkgComboBox.addItem("")
        self.hanaClientPkgComboBox.addItem("")
        self.hanaClientPkgComboBox.setObjectName(u"hanaClientPkgComboBox")
        self.hanaClientPkgComboBox.setEnabled(True)
        sizePolicy7.setHeightForWidth(self.hanaClientPkgComboBox.sizePolicy().hasHeightForWidth())
        self.hanaClientPkgComboBox.setSizePolicy(sizePolicy7)
        self.hanaClientPkgComboBox.setFont(font6)
        self.hanaClientPkgComboBox.setStyleSheet(u"color: rgb(214, 214, 214);")

        self.hanaGridLayout.addWidget(self.hanaClientPkgComboBox, 1, 3, 1, 1)

        self.hanaDemoDbCheckBox = QCheckBox(self.layoutWidget)
        self.hanaDemoDbCheckBox.setObjectName(u"hanaDemoDbCheckBox")
        sizePolicy.setHeightForWidth(self.hanaDemoDbCheckBox.sizePolicy().hasHeightForWidth())
        self.hanaDemoDbCheckBox.setSizePolicy(sizePolicy)
        self.hanaDemoDbCheckBox.setChecked(True)

        self.hanaGridLayout.addWidget(self.hanaDemoDbCheckBox, 4, 2, 1, 1)

        self.hanaRevisionComboBox = QComboBox(self.layoutWidget)
        self.hanaRevisionComboBox.addItem("")
        self.hanaRevisionComboBox.addItem("")
        self.hanaRevisionComboBox.addItem("")
        self.hanaRevisionComboBox.addItem("")
        self.hanaRevisionComboBox.addItem("")
        self.hanaRevisionComboBox.setObjectName(u"hanaRevisionComboBox")
        self.hanaRevisionComboBox.setEnabled(True)
        sizePolicy7.setHeightForWidth(self.hanaRevisionComboBox.sizePolicy().hasHeightForWidth())
        self.hanaRevisionComboBox.setSizePolicy(sizePolicy7)
        palette = QPalette()
        brush = QBrush(QColor(214, 214, 214, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(146, 144, 0, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush2 = QBrush(QColor(214, 214, 214, 128))
        brush2.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush2)
#endif
        self.hanaRevisionComboBox.setPalette(palette)
        font11 = QFont()
        font11.setFamilies([u"Heiti TC"])
        font11.setPointSize(13)
        font11.setKerning(True)
        self.hanaRevisionComboBox.setFont(font11)
        self.hanaRevisionComboBox.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.hanaRevisionComboBox.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.hanaRevisionComboBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.hanaRevisionComboBox.setAutoFillBackground(False)
        self.hanaRevisionComboBox.setStyleSheet(u"color: rgb(214, 214, 214);")
        self.hanaRevisionComboBox.setEditable(False)
        self.hanaRevisionComboBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAtBottom)
        self.hanaRevisionComboBox.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContentsOnFirstShow)

        self.hanaGridLayout.addWidget(self.hanaRevisionComboBox, 0, 3, 1, 1)

        self.hanaRevisionLbl = QLabel(self.layoutWidget)
        self.hanaRevisionLbl.setObjectName(u"hanaRevisionLbl")
        self.hanaRevisionLbl.setEnabled(True)
        sizePolicy.setHeightForWidth(self.hanaRevisionLbl.sizePolicy().hasHeightForWidth())
        self.hanaRevisionLbl.setSizePolicy(sizePolicy)
        self.hanaRevisionLbl.setFont(font7)
        self.hanaRevisionLbl.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.hanaRevisionLbl.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.hanaGridLayout.addWidget(self.hanaRevisionLbl, 0, 2, 1, 1)

        self.hanaClientPkgLbl = QLabel(self.layoutWidget)
        self.hanaClientPkgLbl.setObjectName(u"hanaClientPkgLbl")
        self.hanaClientPkgLbl.setEnabled(True)
        sizePolicy.setHeightForWidth(self.hanaClientPkgLbl.sizePolicy().hasHeightForWidth())
        self.hanaClientPkgLbl.setSizePolicy(sizePolicy)
        self.hanaClientPkgLbl.setFont(font7)
        self.hanaClientPkgLbl.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.hanaClientPkgLbl.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.hanaGridLayout.addWidget(self.hanaClientPkgLbl, 1, 2, 1, 1)

        self.hanaHostnameLineEdit = QLineEdit(self.layoutWidget)
        self.hanaHostnameLineEdit.setObjectName(u"hanaHostnameLineEdit")
        self.hanaHostnameLineEdit.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.hanaHostnameLineEdit.sizePolicy().hasHeightForWidth())
        self.hanaHostnameLineEdit.setSizePolicy(sizePolicy4)
        self.hanaHostnameLineEdit.setMaximumSize(QSize(140, 16777215))
        self.hanaHostnameLineEdit.setFont(font8)
        self.hanaHostnameLineEdit.setStyleSheet(u"color: rgb(148, 23, 81);")

        self.hanaGridLayout.addWidget(self.hanaHostnameLineEdit, 0, 1, 1, 1)

        self.mainGridLayout.addLayout(self.hanaGridLayout, 6, 0, 1, 1)

        self.dcVerticalSpacer = QSpacerItem(20, 3, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.mainGridLayout.addItem(self.dcVerticalSpacer, 1, 0, 1, 1)

        self.hanaVerticalSpacer = QSpacerItem(20, 3, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.mainGridLayout.addItem(self.hanaVerticalSpacer, 4, 0, 1, 1)

        self.finCodeGridLayout = QGridLayout()
        self.finCodeGridLayout.setObjectName(u"finCodeGridLayout")
        self.finCodeLbl = QLabel(self.layoutWidget)
        self.finCodeLbl.setObjectName(u"finCodeLbl")
        self.finCodeLbl.setEnabled(True)
        sizePolicy.setHeightForWidth(self.finCodeLbl.sizePolicy().hasHeightForWidth())
        self.finCodeLbl.setSizePolicy(sizePolicy)
        self.finCodeLbl.setFont(font10)
        self.finCodeLbl.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.finCodeLbl.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.finCodeGridLayout.addWidget(self.finCodeLbl, 0, 0, 1, 1)

        self.finCodeLineEdit = QLineEdit(self.layoutWidget)
        self.finCodeLineEdit.setObjectName(u"finCodeLineEdit")
        self.finCodeLineEdit.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.finCodeLineEdit.sizePolicy().hasHeightForWidth())
        self.finCodeLineEdit.setSizePolicy(sizePolicy4)
        self.finCodeLineEdit.setMaximumSize(QSize(140, 16777215))
        self.finCodeLineEdit.setFont(font8)
        self.finCodeLineEdit.setStyleSheet(u"color: rgb(148, 23, 81);")
        self.finCodeLineEdit.setCursorMoveStyle(Qt.CursorMoveStyle.LogicalMoveStyle)

        self.finCodeGridLayout.addWidget(self.finCodeLineEdit, 0, 1, 1, 1)

        self.mainGridLayout.addLayout(self.finCodeGridLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.startBtn.setDefault(False)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Customer Onboarding Automation", None))
        self.dcLbl.setText(QCoreApplication.translate("MainWindow", u"DOMAIN CONTROLLER", None))
        self.dcComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.dcComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"1", None))
        self.dcComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"2", None))

#if QT_CONFIG(tooltip)
        self.dcComboBox.setToolTip(QCoreApplication.translate("MainWindow", u"# of instances to provision", None))
#endif // QT_CONFIG(tooltip)
        self.startBtn.setText(QCoreApplication.translate("MainWindow", u"S T A R T", None))
        self.consoleLog.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Futura'; font-size:11pt; font-weight:100; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Heiti TC'; font-size:12pt; font-weight:400;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Helvetica'; font-size:10pt; font-weight:400;\"><br /></p></body></html>", None))
        self.winTypeLbl4.setText(QCoreApplication.translate("MainWindow", u"Instance Type", None))
        self.winBoxLbl2.setText(QCoreApplication.translate("MainWindow", u"Box Type", None))
        self.winBoxLbl1.setText(QCoreApplication.translate("MainWindow", u"Box Type", None))
        self.winBoxLbl6.setText(QCoreApplication.translate("MainWindow", u"Box Type", None))
        self.winBoxComboBox3.setItemText(0, QCoreApplication.translate("MainWindow", u"HANA Management", None))
        self.winBoxComboBox3.setItemText(1, QCoreApplication.translate("MainWindow", u"Integration Server", None))
        self.winBoxComboBox3.setItemText(2, QCoreApplication.translate("MainWindow", u"RDS", None))
        self.winBoxComboBox3.setItemText(3, QCoreApplication.translate("MainWindow", u"Citrix", None))
        self.winBoxComboBox3.setItemText(4, QCoreApplication.translate("MainWindow", u"SQL", None))

        self.winBoxComboBox4.setItemText(0, QCoreApplication.translate("MainWindow", u"HANA Management", None))
        self.winBoxComboBox4.setItemText(1, QCoreApplication.translate("MainWindow", u"Integration Server", None))
        self.winBoxComboBox4.setItemText(2, QCoreApplication.translate("MainWindow", u"RDS", None))
        self.winBoxComboBox4.setItemText(3, QCoreApplication.translate("MainWindow", u"Citrix", None))
        self.winBoxComboBox4.setItemText(4, QCoreApplication.translate("MainWindow", u"SQL", None))

        self.winBoxLbl4.setText(QCoreApplication.translate("MainWindow", u"Box Type", None))
        self.winHostnameLbl6.setText(QCoreApplication.translate("MainWindow", u"Hostname", None))
        self.winHostnameLbl1.setText(QCoreApplication.translate("MainWindow", u"Hostname", None))
        self.winHostnameLbl2.setText(QCoreApplication.translate("MainWindow", u"Hostname", None))
        self.winBoxLbl5.setText(QCoreApplication.translate("MainWindow", u"Box Type", None))
        self.winHostnameLbl4.setText(QCoreApplication.translate("MainWindow", u"Hostname", None))
        self.winTypeLbl6.setText(QCoreApplication.translate("MainWindow", u"Instance Type", None))
        self.winTypeLbl3.setText(QCoreApplication.translate("MainWindow", u"Instance Type", None))
        self.winTypeLbl5.setText(QCoreApplication.translate("MainWindow", u"Instance Type", None))
        self.winBoxLbl3.setText(QCoreApplication.translate("MainWindow", u"Box Type", None))
        self.winBoxComboBox1.setItemText(0, QCoreApplication.translate("MainWindow", u"HANA Management", None))
        self.winBoxComboBox1.setItemText(1, QCoreApplication.translate("MainWindow", u"Integration Server", None))
        self.winBoxComboBox1.setItemText(2, QCoreApplication.translate("MainWindow", u"RDS", None))
        self.winBoxComboBox1.setItemText(3, QCoreApplication.translate("MainWindow", u"Citrix", None))
        self.winBoxComboBox1.setItemText(4, QCoreApplication.translate("MainWindow", u"SQL", None))

        self.winTypeLbl1.setText(QCoreApplication.translate("MainWindow", u"Instance Type", None))
        self.winBoxComboBox2.setItemText(0, QCoreApplication.translate("MainWindow", u"HANA Management", None))
        self.winBoxComboBox2.setItemText(1, QCoreApplication.translate("MainWindow", u"Integration Server", None))
        self.winBoxComboBox2.setItemText(2, QCoreApplication.translate("MainWindow", u"RDS", None))
        self.winBoxComboBox2.setItemText(3, QCoreApplication.translate("MainWindow", u"Citrix", None))
        self.winBoxComboBox2.setItemText(4, QCoreApplication.translate("MainWindow", u"SQL", None))

        self.winBoxComboBox5.setItemText(0, QCoreApplication.translate("MainWindow", u"HANA Management", None))
        self.winBoxComboBox5.setItemText(1, QCoreApplication.translate("MainWindow", u"Integration Server", None))
        self.winBoxComboBox5.setItemText(2, QCoreApplication.translate("MainWindow", u"RDS", None))
        self.winBoxComboBox5.setItemText(3, QCoreApplication.translate("MainWindow", u"Citrix", None))
        self.winBoxComboBox5.setItemText(4, QCoreApplication.translate("MainWindow", u"SQL", None))

        self.winHostnameLbl3.setText(QCoreApplication.translate("MainWindow", u"Hostname", None))
        self.winTypeLbl2.setText(QCoreApplication.translate("MainWindow", u"Instance Type", None))
        self.winBoxComboBox6.setItemText(0, QCoreApplication.translate("MainWindow", u"HANA Management", None))
        self.winBoxComboBox6.setItemText(1, QCoreApplication.translate("MainWindow", u"Integration Server", None))
        self.winBoxComboBox6.setItemText(2, QCoreApplication.translate("MainWindow", u"RDS", None))
        self.winBoxComboBox6.setItemText(3, QCoreApplication.translate("MainWindow", u"Citrix", None))
        self.winBoxComboBox6.setItemText(4, QCoreApplication.translate("MainWindow", u"SQL", None))

        self.winHostnameLbl5.setText(QCoreApplication.translate("MainWindow", u"Hostname", None))
        self.winLbl.setText(QCoreApplication.translate("MainWindow", u" WINDOWS GEN BOX", None))
        self.winComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.winComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"1", None))
        self.winComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"2", None))
        self.winComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"3", None))
        self.winComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"4", None))
        self.winComboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"5", None))
        self.winComboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"6", None))

#if QT_CONFIG(tooltip)
        self.winComboBox.setToolTip(QCoreApplication.translate("MainWindow", u"# of instances to provision", None))
#endif // QT_CONFIG(tooltip)
        self.dcTypeLbl2.setText(QCoreApplication.translate("MainWindow", u"Instance Type", None))
        self.dcHostnameLbl2.setText(QCoreApplication.translate("MainWindow", u"Hostname", None))
        self.dcHostnameLbl1.setText(QCoreApplication.translate("MainWindow", u"Hostname", None))
        self.dcTypeLbl1.setText(QCoreApplication.translate("MainWindow", u"Instance Type", None))
        self.dcLbl_2.setText(QCoreApplication.translate("MainWindow", u"SAP HANA DB", None))
        self.hanaComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.hanaComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"1", None))

#if QT_CONFIG(tooltip)
        self.hanaComboBox.setToolTip(QCoreApplication.translate("MainWindow", u"# of instances to provision", None))
#endif // QT_CONFIG(tooltip)
        self.hanaHostnameLbl.setText(QCoreApplication.translate("MainWindow", u"Hostname", None))
        self.hanaTypeLbl.setText(QCoreApplication.translate("MainWindow", u"Instance Type", None))
        self.hanaCockpitCheckBox.setText(QCoreApplication.translate("MainWindow", u"SAP HANA Cockpit", None))
        self.hanaClientPkgComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"2411 (Patch Level)", None))
        self.hanaClientPkgComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"2408 (Patch Level)", None))
        self.hanaClientPkgComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"2405 (Patch Level)", None))
        self.hanaClientPkgComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"2402 (Patch Level)", None))

        self.hanaDemoDbCheckBox.setText(QCoreApplication.translate("MainWindow", u"Demo Databases", None))
        self.hanaRevisionComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Rev59.13 ( 2.20.22)", None))
        self.hanaRevisionComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Rev59.09 ( 2.17.22)", None))
        self.hanaRevisionComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Rev59.04 ( 2.7.26)", None))
        self.hanaRevisionComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Rev56 ( 2.7.26)", None))
        self.hanaRevisionComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Rev50 ( 2.7.26)", None))

        self.hanaRevisionComboBox.setCurrentText(QCoreApplication.translate("MainWindow", u"Rev59.13 ( 2.20.22)", None))
        self.hanaRevisionLbl.setText(QCoreApplication.translate("MainWindow", u"HANA Revision", None))
        self.hanaClientPkgLbl.setText(QCoreApplication.translate("MainWindow", u"HANA B1 Patch", None))
        self.finCodeLbl.setText(QCoreApplication.translate("MainWindow", u"Finance Code", None))
    # retranslateUi

        self.dcTypeComboBox1.addItems(self.INSTANCE_TYPES)
        self.dcTypeComboBox2.addItems(self.INSTANCE_TYPES)
        self.hanaTypeComboBox.addItems(self.INSTANCE_TYPES)
        self.winTypeComboBox1.addItems(self.INSTANCE_TYPES)
        self.winTypeComboBox2.addItems(self.INSTANCE_TYPES)
        self.winTypeComboBox3.addItems(self.INSTANCE_TYPES)
        self.winTypeComboBox4.addItems(self.INSTANCE_TYPES)
        self.winTypeComboBox5.addItems(self.INSTANCE_TYPES)
        self.winTypeComboBox6.addItems(self.INSTANCE_TYPES)

        self.dcHostnameLbl1.setVisible(False)
        self.dcHostnameLbl2.setVisible(False)
        self.dcHostnameLineEdit1.setVisible(False)
        self.dcHostnameLineEdit2.setVisible(False)
        self.dcTypeLbl1.setVisible(False)
        self.dcTypeLbl2.setVisible(False)
        self.dcTypeComboBox1.setVisible(False)
        self.dcTypeComboBox2.setVisible(False)
        self.dcTypeComboBox1.setCurrentText("r5.xlarge")
        self.dcTypeComboBox2.setCurrentText("r5.xlarge")
        self.dcToolBtn1.setVisible(False)
        self.dcToolBtn2.setVisible(False)
        self.hanaHostnameLbl.setVisible(False)
        self.hanaHostnameLineEdit.setVisible(False)
        self.hanaTypeLbl.setVisible(False)
        self.hanaTypeComboBox.setVisible(False)
        self.hanaTypeComboBox.setCurrentText("r6i.2xlarge")
        self.hanaToolBtn.setVisible(False)
        self.hanaRevisionLbl.setVisible(False)
        self.hanaRevisionComboBox.setVisible(False)
        self.hanaClientPkgLbl.setVisible(False)
        self.hanaClientPkgComboBox.setVisible(False)
        self.hanaCockpitCheckBox.setVisible(False)
        self.hanaCockpitCheckBox.setChecked(False)
        self.hanaDemoDbCheckBox.setVisible(False)
        self.hanaDemoDbCheckBox.setChecked(False)
        self.winHostnameLbl1.setVisible(False)
        self.winHostnameLbl2.setVisible(False)
        self.winHostnameLbl3.setVisible(False)
        self.winHostnameLbl4.setVisible(False)
        self.winHostnameLbl5.setVisible(False)
        self.winHostnameLbl6.setVisible(False)
        self.winHostnameLineEdit1.setVisible(False)
        self.winHostnameLineEdit2.setVisible(False)
        self.winHostnameLineEdit3.setVisible(False)
        self.winHostnameLineEdit4.setVisible(False)
        self.winHostnameLineEdit5.setVisible(False)
        self.winHostnameLineEdit6.setVisible(False)
        self.winBoxLbl1.setVisible(False)
        self.winBoxLbl2.setVisible(False)
        self.winBoxLbl3.setVisible(False)
        self.winBoxLbl4.setVisible(False)
        self.winBoxLbl5.setVisible(False)
        self.winBoxLbl6.setVisible(False)
        self.winBoxComboBox1.setVisible(False)
        self.winBoxComboBox2.setVisible(False)
        self.winBoxComboBox3.setVisible(False)
        self.winBoxComboBox4.setVisible(False)
        self.winBoxComboBox5.setVisible(False)
        self.winBoxComboBox6.setVisible(False)
        self.winTypeLbl1.setVisible(False)
        self.winTypeLbl2.setVisible(False)
        self.winTypeLbl3.setVisible(False)
        self.winTypeLbl4.setVisible(False)
        self.winTypeLbl5.setVisible(False)
        self.winTypeLbl6.setVisible(False)
        self.winTypeComboBox1.setVisible(False)
        self.winTypeComboBox2.setVisible(False)
        self.winTypeComboBox3.setVisible(False)
        self.winTypeComboBox4.setVisible(False)
        self.winTypeComboBox5.setVisible(False)
        self.winTypeComboBox6.setVisible(False)
        self.winTypeComboBox1.setCurrentText("r5.xlarge")
        self.winTypeComboBox2.setCurrentText("r5.xlarge")
        self.winTypeComboBox3.setCurrentText("r5.xlarge")
        self.winTypeComboBox4.setCurrentText("r5.xlarge")
        self.winTypeComboBox5.setCurrentText("r5.xlarge")
        self.winTypeComboBox6.setCurrentText("r5.xlarge")
        self.winToolBtn1.setVisible(False)
        self.winToolBtn2.setVisible(False)
        self.winToolBtn3.setVisible(False)
        self.winToolBtn4.setVisible(False)
        self.winToolBtn5.setVisible(False)
        self.winToolBtn6.setVisible(False)
        self.startBtn.setDisabled(True)

        self.init_account()

        self.dcComboBox.currentIndexChanged.connect(self.dc_num_change)
        self.hanaComboBox.currentIndexChanged.connect(self.hana_num_change)
        self.winComboBox.currentIndexChanged.connect(self.win_num_change)

        self.dcTypeComboBox1.currentIndexChanged.connect(self.dc1_type_change)
        self.dcTypeComboBox2.currentIndexChanged.connect(self.dc2_type_change)
        self.hanaTypeComboBox.currentIndexChanged.connect(self.hana_type_change)
        self.winTypeComboBox1.currentIndexChanged.connect(self.win_type1_change)
        self.winTypeComboBox2.currentIndexChanged.connect(self.win_type2_change)
        self.winTypeComboBox3.currentIndexChanged.connect(self.win_type3_change)
        self.winTypeComboBox4.currentIndexChanged.connect(self.win_type4_change)
        self.winTypeComboBox5.currentIndexChanged.connect(self.win_type5_change)
        self.winTypeComboBox6.currentIndexChanged.connect(self.win_type6_change)

        self.hanaRevisionComboBox.currentIndexChanged.connect(self.hana_rev_change)
        self.hanaClientPkgComboBox.currentIndexChanged.connect(self.hana_patch_change)
        self.hanaCockpitCheckBox.stateChanged.connect(self.hana_cockpit_select)
        self.hanaDemoDbCheckBox.stateChanged.connect(self.hana_demodb_select)

        self.winBoxComboBox1.currentIndexChanged.connect(self.win_box1_change)
        self.winBoxComboBox2.currentIndexChanged.connect(self.win_box2_change)
        self.winBoxComboBox3.currentIndexChanged.connect(self.win_box3_change)
        self.winBoxComboBox4.currentIndexChanged.connect(self.win_box4_change)
        self.winBoxComboBox5.currentIndexChanged.connect(self.win_box5_change)
        self.winBoxComboBox6.currentIndexChanged.connect(self.win_box6_change)

        self.startBtn.clicked.connect(self.validation)

    def get_instance_types(self, filename):
        try:
            with open(filename, 'r') as file:
                return [ line.strip() for line in file.readlines() if line.strip() ]
        except (FileNotFoundError):
            self.logger(f"Error: { filename } not found.", 'e')
            return []
    
    def dc_num_change(self):
        if self.dcComboBox.currentText() != "None":
            if self.dcComboBox.currentText() == "1":
                self.dcHostnameLbl1.setVisible(True)
                self.dcHostnameLineEdit1.setVisible(True)
                self.dcHostnameLineEdit1.setText(f"{ self.AWS_HOSTID }DC{ self.AWS_ENV[0] }01")
                self.dcHostnameLbl2.setVisible(False)
                self.dcHostnameLineEdit2.setVisible(False)
                self.dcHostnameLineEdit2.clear()
                self.dcTypeLbl1.setVisible(True)
                self.dcTypeLbl2.setVisible(False)
                self.dcTypeComboBox1.setVisible(True)
                self.dcTypeComboBox1.setCurrentText("r5.xlarge")
                self.dcTypeComboBox2.setVisible(False)
                self.dcTypeComboBox2.setCurrentText("r5.xlarge")
                self.dcToolBtn1.setVisible(True)
                self.dcToolBtn2.setVisible(False)
            else:
                self.dcHostnameLbl1.setVisible(True)
                self.dcHostnameLineEdit1.setVisible(True)
                self.dcHostnameLineEdit1.setText(f"{ self.AWS_HOSTID }DC{ self.AWS_ENV[0] }01")
                self.dcHostnameLbl2.setVisible(True)
                self.dcHostnameLineEdit2.setVisible(True)
                self.dcHostnameLineEdit2.setText(f"{ self.AWS_HOSTID }DC{ self.AWS_ENV[0] }02")
                self.dcTypeLbl1.setVisible(True)
                self.dcTypeLbl2.setVisible(True)
                self.dcTypeComboBox1.setVisible(True)
                self.dcTypeComboBox1.setCurrentText("r5.xlarge")
                self.dcTypeComboBox2.setVisible(True)
                self.dcTypeComboBox2.setCurrentText("r5.xlarge")
                self.dcToolBtn1.setVisible(True)
                self.dcToolBtn2.setVisible(True)

            self.DC_COUNT = int(self.dcComboBox.currentText())
            self.dc1_type_change()
            self.dc2_type_change()
        else:
            self.dcHostnameLbl1.setVisible(False)
            self.dcHostnameLineEdit1.setVisible(False)
            self.dcHostnameLineEdit1.clear()
            self.dcHostnameLbl2.setVisible(False)
            self.dcHostnameLineEdit2.setVisible(False)
            self.dcHostnameLineEdit2.clear()
            self.dcTypeLbl1.setVisible(False)
            self.dcTypeLbl2.setVisible(False)
            self.dcTypeComboBox1.setVisible(False)
            self.dcTypeComboBox1.setCurrentText("r5.xlarge")
            self.dcTypeComboBox2.setVisible(False)
            self.dcTypeComboBox2.setCurrentText("r5.xlarge")
            self.dcToolBtn1.setVisible(False)
            self.dcToolBtn2.setVisible(False)
            self.DC_COUNT = 0
            self.DC_LIST = []
            self.DC_TYPE_LIST = []
            self.DC1_TYPE = ''
            self.DC2_TYPE = ''

        self.enable_start()

    def hana_num_change(self):
        if self.hanaComboBox.currentText() != "None":
            if self.hanaComboBox.currentText() == "1":
                self.hanaHostnameLbl.setVisible(True)
                self.hanaHostnameLineEdit.setVisible(True)
                self.hanaHostnameLineEdit.setText(f"{ self.AWS_HOSTID }HANA{ self.AWS_ENV[0] }01")
                self.hanaTypeLbl.setVisible(True)
                self.hanaTypeComboBox.setVisible(True)
                self.hanaTypeComboBox.setCurrentText("r6i.2xlarge")
                self.hanaRevisionLbl.setVisible(True)
                self.hanaRevisionComboBox.setVisible(True)
                self.hanaClientPkgLbl.setVisible(True)
                self.hanaClientPkgComboBox.setVisible(True)
                self.hanaToolBtn.setVisible(True)
                self.hanaCockpitCheckBox.setVisible(True)
                self.hanaCockpitCheckBox.setChecked(True)
                self.hanaDemoDbCheckBox.setVisible(True)
                self.hanaDemoDbCheckBox.setChecked(True)
            else:
                self.hanaHostnameLbl.setVisible(True)
                self.hanaHostnameLineEdit.setVisible(True)
                self.hanaHostnameLineEdit.setText(f"{ self.AWS_HOSTID }HANA{ self.AWS_ENV[0] }01")
                self.hanaTypeLbl.setVisible(True)
                self.hanaTypeComboBox.setVisible(True)
                self.hanaTypeComboBox.setCurrentText("r6i.2xlarge")
                self.hanaRevisionLbl.setVisible(True)
                self.hanaRevisionComboBox.setVisible(True)
                self.hanaClientPkgLbl.setVisible(True)
                self.hanaClientPkgComboBox.setVisible(True)
                self.hanaToolBtn.setVisible(True)
                self.hanaCockpitCheckBox.setVisible(True)
                self.hanaCockpitCheckBox.setChecked(True)
                self.hanaDemoDbCheckBox.setVisible(True)
                self.hanaDemoDbCheckBox.setChecked(True)

            self.HANA_COUNT = int(self.hanaComboBox.currentText())
            self.hana_type_change()
            self.hana_rev_change()
            self.hana_patch_change()
        else:
            self.hanaHostnameLbl.setVisible(False)
            self.hanaHostnameLineEdit.setVisible(False)
            self.hanaHostnameLineEdit.clear()
            self.hanaTypeLbl.setVisible(False)
            self.hanaTypeComboBox.setVisible(False)
            self.hanaTypeComboBox.setCurrentText("r6i.2xlarge")
            self.hanaRevisionLbl.setVisible(False)
            self.hanaRevisionComboBox.setVisible(False)
            self.hanaRevisionComboBox.setCurrentIndex(0)
            self.hanaClientPkgLbl.setVisible(False)
            self.hanaClientPkgComboBox.setVisible(False)
            self.hanaClientPkgComboBox.setCurrentIndex(0)
            self.hanaToolBtn.setVisible(False)
            self.hanaCockpitCheckBox.setVisible(False)
            self.hanaCockpitCheckBox.setChecked(False)
            self.hanaDemoDbCheckBox.setVisible(False)
            self.hanaDemoDbCheckBox.setChecked(False)
            self.HANA_COUNT = 0
            self.HANA_LIST = []
            self.HANA_TYPE_LIST = []
            self.HANA_TYPE = ''
            self.HANA_REVISION = ''
            self.HANA_REVISION_NAME = ''
            self.HANA_PATCH = ''
            self.HANA_PATCH_NAME = ''
            self.HANA_COCKPIT = False
            self.HANA_DEMO_DB = False

        self.enable_start()

    def win_num_change(self):
        if self.winComboBox.currentText() != "None":
            if self.winComboBox.currentText() == "1":
                self.winHostnameLbl1.setVisible(True)
                self.winHostnameLbl2.setVisible(False)
                self.winHostnameLbl3.setVisible(False)
                self.winHostnameLbl4.setVisible(False)
                self.winHostnameLbl5.setVisible(False)
                self.winHostnameLbl6.setVisible(False)
                self.winHostnameLineEdit1.setVisible(True)
                self.winHostnameLineEdit2.setVisible(False)
                self.winHostnameLineEdit3.setVisible(False)
                self.winHostnameLineEdit4.setVisible(False)
                self.winHostnameLineEdit5.setVisible(False)
                self.winHostnameLineEdit6.setVisible(False)
                self.WIN2_BOX = ''
                self.WIN3_BOX = ''
                self.WIN4_BOX = ''
                self.WIN5_BOX = ''
                self.WIN6_BOX = ''
                self.winHostnameLineEdit1.setText(f"{ self.AWS_HOSTID }HM{ self.AWS_ENV[0] }01") if self.WIN1_BOX == '' else self.win_box1_change()
                self.winHostnameLineEdit2.setText(f"{ self.AWS_HOSTID }INT{ self.AWS_ENV[0] }01") if self.WIN2_BOX == '' else self.win_box2_change()
                self.winHostnameLineEdit3.setText(f"{ self.AWS_HOSTID }RDS{ self.AWS_ENV[0] }01") if self.WIN3_BOX == '' else self.win_box3_change()
                self.winHostnameLineEdit4.setText(f"{ self.AWS_HOSTID }VDA{ self.AWS_ENV[0] }01") if self.WIN4_BOX == '' else self.win_box4_change()
                self.winHostnameLineEdit5.setText(f"{ self.AWS_HOSTID }SQL{ self.AWS_ENV[0] }01") if self.WIN5_BOX == '' else self.win_box5_change()
                self.winHostnameLineEdit6.setText(f"{ self.AWS_HOSTID }VDA{ self.AWS_ENV[0] }01") if self.WIN6_BOX == '' else self.win_box6_change()
                self.winBoxLbl1.setVisible(True)
                self.winBoxLbl2.setVisible(False)
                self.winBoxLbl3.setVisible(False)
                self.winBoxLbl4.setVisible(False)
                self.winBoxLbl5.setVisible(False)
                self.winBoxLbl6.setVisible(False)
                self.winBoxComboBox1.setVisible(True)
                self.winBoxComboBox2.setVisible(False)
                self.winBoxComboBox3.setVisible(False)
                self.winBoxComboBox4.setVisible(False)
                self.winBoxComboBox5.setVisible(False)
                self.winBoxComboBox6.setVisible(False)
                self.winBoxComboBox1.setCurrentText("HANA Management") if self.WIN1_BOX == '' else self.win_box1_change()
                self.winTypeLbl1.setVisible(True)
                self.winTypeLbl2.setVisible(False)
                self.winTypeLbl3.setVisible(False)
                self.winTypeLbl4.setVisible(False)
                self.winTypeLbl5.setVisible(False)
                self.winTypeLbl6.setVisible(False)
                self.winTypeComboBox1.setVisible(True)
                self.winTypeComboBox2.setVisible(False)
                self.winTypeComboBox3.setVisible(False)
                self.winTypeComboBox4.setVisible(False)
                self.winTypeComboBox5.setVisible(False)
                self.winTypeComboBox6.setVisible(False)
                self.winTypeComboBox1.setCurrentText("r5.xlarge") if self.WIN1_BOX == '' else self.win_type1_change()
                self.winTypeComboBox2.setCurrentText("r5.xlarge") if self.WIN2_BOX == '' else self.win_type2_change()
                self.winTypeComboBox3.setCurrentText("r5.xlarge") if self.WIN3_BOX == '' else self.win_type3_change()
                self.winTypeComboBox4.setCurrentText("r5.xlarge") if self.WIN4_BOX == '' else self.win_type4_change()
                self.winTypeComboBox5.setCurrentText("r5.xlarge") if self.WIN5_BOX == '' else self.win_type5_change()
                self.winTypeComboBox6.setCurrentText("r5.xlarge") if self.WIN6_BOX == '' else self.win_type6_change()
                self.winToolBtn1.setVisible(True)
                self.winToolBtn2.setVisible(False)
                self.winToolBtn3.setVisible(False)
                self.winToolBtn4.setVisible(False)
                self.winToolBtn5.setVisible(False)
                self.winToolBtn6.setVisible(False)
            elif self.winComboBox.currentText() == "2":
                self.winHostnameLbl1.setVisible(True)
                self.winHostnameLbl2.setVisible(True)
                self.winHostnameLbl3.setVisible(False)
                self.winHostnameLbl4.setVisible(False)
                self.winHostnameLbl5.setVisible(False)
                self.winHostnameLbl6.setVisible(False)
                self.winHostnameLineEdit1.setVisible(True)
                self.winHostnameLineEdit2.setVisible(True)
                self.winHostnameLineEdit3.setVisible(False)
                self.winHostnameLineEdit4.setVisible(False)
                self.winHostnameLineEdit5.setVisible(False)
                self.winHostnameLineEdit6.setVisible(False)
                self.WIN3_BOX = ''
                self.WIN4_BOX = ''
                self.WIN5_BOX = ''
                self.WIN6_BOX = ''
                self.winHostnameLineEdit1.setText(f"{ self.AWS_HOSTID }HM{ self.AWS_ENV[0] }01") if self.WIN1_BOX == '' else self.win_box1_change()
                self.winHostnameLineEdit2.setText(f"{ self.AWS_HOSTID }INT{ self.AWS_ENV[0] }01") if self.WIN2_BOX == '' else self.win_box2_change()
                self.winHostnameLineEdit3.setText(f"{ self.AWS_HOSTID }RDS{ self.AWS_ENV[0] }01") if self.WIN3_BOX == '' else self.win_box3_change()
                self.winHostnameLineEdit4.setText(f"{ self.AWS_HOSTID }VDA{ self.AWS_ENV[0] }01") if self.WIN4_BOX == '' else self.win_box4_change()
                self.winHostnameLineEdit5.setText(f"{ self.AWS_HOSTID }SQL{ self.AWS_ENV[0] }01") if self.WIN5_BOX == '' else self.win_box5_change()
                self.winHostnameLineEdit6.setText(f"{ self.AWS_HOSTID }VDA{ self.AWS_ENV[0] }01") if self.WIN6_BOX == '' else self.win_box6_change()
                self.winBoxLbl1.setVisible(True)
                self.winBoxLbl2.setVisible(True)
                self.winBoxLbl3.setVisible(False)
                self.winBoxLbl4.setVisible(False)
                self.winBoxLbl5.setVisible(False)
                self.winBoxLbl6.setVisible(False)
                self.winBoxComboBox1.setVisible(True)
                self.winBoxComboBox2.setVisible(True)
                self.winBoxComboBox3.setVisible(False)
                self.winBoxComboBox4.setVisible(False)
                self.winBoxComboBox5.setVisible(False)
                self.winBoxComboBox6.setVisible(False)
                self.winBoxComboBox1.setCurrentText("HANA Management") if self.WIN1_BOX == '' else self.win_box1_change()
                self.winBoxComboBox2.setCurrentText("Integration Server") if self.WIN2_BOX == '' else self.win_box2_change()
                self.winTypeLbl1.setVisible(True)
                self.winTypeLbl2.setVisible(True)
                self.winTypeLbl3.setVisible(False)
                self.winTypeLbl4.setVisible(False)
                self.winTypeLbl5.setVisible(False)
                self.winTypeLbl6.setVisible(False)
                self.winTypeComboBox1.setVisible(True)
                self.winTypeComboBox2.setVisible(True)
                self.winTypeComboBox3.setVisible(False)
                self.winTypeComboBox4.setVisible(False)
                self.winTypeComboBox5.setVisible(False)
                self.winTypeComboBox6.setVisible(False)
                self.winTypeComboBox1.setCurrentText("r5.xlarge") if self.WIN1_BOX == '' else self.win_type1_change()
                self.winTypeComboBox2.setCurrentText("r5.xlarge") if self.WIN2_BOX == '' else self.win_type2_change()
                self.winTypeComboBox3.setCurrentText("r5.xlarge") if self.WIN3_BOX == '' else self.win_type3_change()
                self.winTypeComboBox4.setCurrentText("r5.xlarge") if self.WIN4_BOX == '' else self.win_type4_change()
                self.winTypeComboBox5.setCurrentText("r5.xlarge") if self.WIN5_BOX == '' else self.win_type5_change()
                self.winTypeComboBox6.setCurrentText("r5.xlarge") if self.WIN6_BOX == '' else self.win_type6_change()
                self.winToolBtn1.setVisible(True)
                self.winToolBtn2.setVisible(True)
                self.winToolBtn3.setVisible(False)
                self.winToolBtn4.setVisible(False)
                self.winToolBtn5.setVisible(False)
                self.winToolBtn6.setVisible(False)
            elif self.winComboBox.currentText() == "3":
                self.winHostnameLbl1.setVisible(True)
                self.winHostnameLbl2.setVisible(True)
                self.winHostnameLbl3.setVisible(True)
                self.winHostnameLbl4.setVisible(False)
                self.winHostnameLbl5.setVisible(False)
                self.winHostnameLbl6.setVisible(False)
                self.winHostnameLineEdit1.setVisible(True)
                self.winHostnameLineEdit2.setVisible(True)
                self.winHostnameLineEdit3.setVisible(True)
                self.winHostnameLineEdit4.setVisible(False)
                self.winHostnameLineEdit5.setVisible(False)
                self.winHostnameLineEdit6.setVisible(False)
                self.WIN4_BOX = ''
                self.WIN5_BOX = ''
                self.WIN6_BOX = ''
                self.winHostnameLineEdit1.setText(f"{ self.AWS_HOSTID }HM{ self.AWS_ENV[0] }01") if self.WIN1_BOX == '' else self.win_box1_change()
                self.winHostnameLineEdit2.setText(f"{ self.AWS_HOSTID }INT{ self.AWS_ENV[0] }01") if self.WIN2_BOX == '' else self.win_box2_change()
                self.winHostnameLineEdit3.setText(f"{ self.AWS_HOSTID }RDS{ self.AWS_ENV[0] }01") if self.WIN3_BOX == '' else self.win_box3_change()
                self.winHostnameLineEdit4.setText(f"{ self.AWS_HOSTID }VDA{ self.AWS_ENV[0] }01") if self.WIN4_BOX == '' else self.win_box4_change()
                self.winHostnameLineEdit5.setText(f"{ self.AWS_HOSTID }SQL{ self.AWS_ENV[0] }01") if self.WIN5_BOX == '' else self.win_box5_change()
                self.winHostnameLineEdit6.setText(f"{ self.AWS_HOSTID }VDA{ self.AWS_ENV[0] }01") if self.WIN6_BOX == '' else self.win_box6_change()
                self.winBoxLbl1.setVisible(True)
                self.winBoxLbl2.setVisible(True)
                self.winBoxLbl3.setVisible(True)
                self.winBoxLbl4.setVisible(False)
                self.winBoxLbl5.setVisible(False)
                self.winBoxLbl6.setVisible(False)
                self.winBoxComboBox1.setVisible(True)
                self.winBoxComboBox2.setVisible(True)
                self.winBoxComboBox3.setVisible(True)
                self.winBoxComboBox4.setVisible(False)
                self.winBoxComboBox5.setVisible(False)
                self.winBoxComboBox6.setVisible(False)
                self.winBoxComboBox1.setCurrentText("HANA Management") if self.WIN1_BOX == '' else self.win_box1_change()
                self.winBoxComboBox2.setCurrentText("Integration Server") if self.WIN2_BOX == '' else self.win_box2_change()
                self.winBoxComboBox3.setCurrentText("RDS") if self.WIN3_BOX == '' else self.win_box3_change()
                self.winTypeLbl1.setVisible(True)
                self.winTypeLbl2.setVisible(True)
                self.winTypeLbl3.setVisible(True)
                self.winTypeLbl4.setVisible(False)
                self.winTypeLbl5.setVisible(False)
                self.winTypeLbl6.setVisible(False)
                self.winTypeComboBox1.setVisible(True)
                self.winTypeComboBox2.setVisible(True)
                self.winTypeComboBox3.setVisible(True)
                self.winTypeComboBox4.setVisible(False)
                self.winTypeComboBox5.setVisible(False)
                self.winTypeComboBox6.setVisible(False)
                self.winTypeComboBox1.setCurrentText("r5.xlarge") if self.WIN1_BOX == '' else self.win_type1_change()
                self.winTypeComboBox2.setCurrentText("r5.xlarge") if self.WIN2_BOX == '' else self.win_type2_change()
                self.winTypeComboBox3.setCurrentText("r5.xlarge") if self.WIN3_BOX == '' else self.win_type3_change()
                self.winTypeComboBox4.setCurrentText("r5.xlarge") if self.WIN4_BOX == '' else self.win_type4_change()
                self.winTypeComboBox5.setCurrentText("r5.xlarge") if self.WIN5_BOX == '' else self.win_type5_change()
                self.winTypeComboBox6.setCurrentText("r5.xlarge") if self.WIN6_BOX == '' else self.win_type6_change()
                self.winToolBtn1.setVisible(True)
                self.winToolBtn2.setVisible(True)
                self.winToolBtn3.setVisible(True)
                self.winToolBtn4.setVisible(False)
                self.winToolBtn5.setVisible(False)
                self.winToolBtn6.setVisible(False)
            elif self.winComboBox.currentText() == "4":
                self.winHostnameLbl1.setVisible(True)
                self.winHostnameLbl2.setVisible(True)
                self.winHostnameLbl3.setVisible(True)
                self.winHostnameLbl4.setVisible(True)
                self.winHostnameLbl5.setVisible(False)
                self.winHostnameLbl6.setVisible(False)
                self.winHostnameLineEdit1.setVisible(True)
                self.winHostnameLineEdit2.setVisible(True)
                self.winHostnameLineEdit3.setVisible(True)
                self.winHostnameLineEdit4.setVisible(True)
                self.winHostnameLineEdit5.setVisible(False)
                self.winHostnameLineEdit6.setVisible(False)
                self.WIN5_BOX = ''
                self.WIN6_BOX = ''
                self.winHostnameLineEdit1.setText(f"{ self.AWS_HOSTID }HM{ self.AWS_ENV[0] }01") if self.WIN1_BOX == '' else self.win_box1_change()
                self.winHostnameLineEdit2.setText(f"{ self.AWS_HOSTID }INT{ self.AWS_ENV[0] }01") if self.WIN2_BOX == '' else self.win_box2_change()
                self.winHostnameLineEdit3.setText(f"{ self.AWS_HOSTID }RDS{ self.AWS_ENV[0] }01") if self.WIN3_BOX == '' else self.win_box3_change()
                self.winHostnameLineEdit4.setText(f"{ self.AWS_HOSTID }VDA{ self.AWS_ENV[0] }01") if self.WIN4_BOX == '' else self.win_box4_change()
                self.winHostnameLineEdit5.setText(f"{ self.AWS_HOSTID }SQL{ self.AWS_ENV[0] }01") if self.WIN5_BOX == '' else self.win_box5_change()
                self.winHostnameLineEdit6.setText(f"{ self.AWS_HOSTID }VDA{ self.AWS_ENV[0] }01") if self.WIN6_BOX == '' else self.win_box6_change()
                self.winBoxLbl1.setVisible(True)
                self.winBoxLbl2.setVisible(True)
                self.winBoxLbl3.setVisible(True)
                self.winBoxLbl4.setVisible(True)
                self.winBoxLbl5.setVisible(False)
                self.winBoxLbl6.setVisible(False)
                self.winBoxComboBox1.setVisible(True)
                self.winBoxComboBox2.setVisible(True)
                self.winBoxComboBox3.setVisible(True)
                self.winBoxComboBox4.setVisible(True)
                self.winBoxComboBox5.setVisible(False)
                self.winBoxComboBox6.setVisible(False)
                self.winBoxComboBox1.setCurrentText("HANA Management") if self.WIN1_BOX == '' else self.win_box1_change()
                self.winBoxComboBox2.setCurrentText("Integration Server") if self.WIN2_BOX == '' else self.win_box2_change()
                self.winBoxComboBox3.setCurrentText("RDS") if self.WIN3_BOX == '' else self.win_box3_change()
                self.winBoxComboBox4.setCurrentText("Citrix") if self.WIN4_BOX == '' else self.win_box4_change()
                self.winTypeLbl1.setVisible(True)
                self.winTypeLbl2.setVisible(True)
                self.winTypeLbl3.setVisible(True)
                self.winTypeLbl4.setVisible(True)
                self.winTypeLbl5.setVisible(False)
                self.winTypeLbl6.setVisible(False)
                self.winTypeComboBox1.setVisible(True)
                self.winTypeComboBox2.setVisible(True)
                self.winTypeComboBox3.setVisible(True)
                self.winTypeComboBox4.setVisible(True)
                self.winTypeComboBox5.setVisible(False)
                self.winTypeComboBox6.setVisible(False)
                self.winTypeComboBox1.setCurrentText("r5.xlarge") if self.WIN1_BOX == '' else self.win_type1_change()
                self.winTypeComboBox2.setCurrentText("r5.xlarge") if self.WIN2_BOX == '' else self.win_type2_change()
                self.winTypeComboBox3.setCurrentText("r5.xlarge") if self.WIN3_BOX == '' else self.win_type3_change()
                self.winTypeComboBox4.setCurrentText("r5.xlarge") if self.WIN4_BOX == '' else self.win_type4_change()
                self.winTypeComboBox5.setCurrentText("r5.xlarge") if self.WIN5_BOX == '' else self.win_type5_change()
                self.winTypeComboBox6.setCurrentText("r5.xlarge") if self.WIN6_BOX == '' else self.win_type6_change()
                self.winToolBtn1.setVisible(True)
                self.winToolBtn2.setVisible(True)
                self.winToolBtn3.setVisible(True)
                self.winToolBtn4.setVisible(True)
                self.winToolBtn5.setVisible(False)
                self.winToolBtn6.setVisible(False)
            elif self.winComboBox.currentText() == "5":
                self.winHostnameLbl1.setVisible(True)
                self.winHostnameLbl2.setVisible(True)
                self.winHostnameLbl3.setVisible(True)
                self.winHostnameLbl4.setVisible(True)
                self.winHostnameLbl5.setVisible(True)
                self.winHostnameLbl6.setVisible(False)
                self.winHostnameLineEdit1.setVisible(True)
                self.winHostnameLineEdit2.setVisible(True)
                self.winHostnameLineEdit3.setVisible(True)
                self.winHostnameLineEdit4.setVisible(True)
                self.winHostnameLineEdit5.setVisible(True)
                self.winHostnameLineEdit6.setVisible(False)
                self.WIN6_BOX = ''
                self.winHostnameLineEdit1.setText(f"{ self.AWS_HOSTID }HM{ self.AWS_ENV[0] }01") if self.WIN1_BOX == '' else self.win_box1_change()
                self.winHostnameLineEdit2.setText(f"{ self.AWS_HOSTID }INT{ self.AWS_ENV[0] }01") if self.WIN2_BOX == '' else self.win_box2_change()
                self.winHostnameLineEdit3.setText(f"{ self.AWS_HOSTID }RDS{ self.AWS_ENV[0] }01") if self.WIN3_BOX == '' else self.win_box3_change()
                self.winHostnameLineEdit4.setText(f"{ self.AWS_HOSTID }VDA{ self.AWS_ENV[0] }01") if self.WIN4_BOX == '' else self.win_box4_change()
                self.winHostnameLineEdit5.setText(f"{ self.AWS_HOSTID }SQL{ self.AWS_ENV[0] }01") if self.WIN5_BOX == '' else self.win_box5_change()
                self.winHostnameLineEdit6.setText(f"{ self.AWS_HOSTID }VDA{ self.AWS_ENV[0] }01") if self.WIN6_BOX == '' else self.win_box6_change()
                self.winBoxLbl1.setVisible(True)
                self.winBoxLbl2.setVisible(True)
                self.winBoxLbl3.setVisible(True)
                self.winBoxLbl4.setVisible(True)
                self.winBoxLbl5.setVisible(True)
                self.winBoxLbl6.setVisible(False)
                self.winBoxComboBox1.setVisible(True)
                self.winBoxComboBox2.setVisible(True)
                self.winBoxComboBox3.setVisible(True)
                self.winBoxComboBox4.setVisible(True)
                self.winBoxComboBox5.setVisible(True)
                self.winBoxComboBox6.setVisible(False)
                self.winBoxComboBox1.setCurrentText("HANA Management") if self.WIN1_BOX == '' else self.win_box1_change()
                self.winBoxComboBox2.setCurrentText("Integration Server") if self.WIN2_BOX == '' else self.win_box2_change()
                self.winBoxComboBox3.setCurrentText("RDS") if self.WIN3_BOX == '' else self.win_box3_change()
                self.winBoxComboBox4.setCurrentText("Citrix") if self.WIN4_BOX == '' else self.win_box4_change()
                self.winBoxComboBox5.setCurrentText("SQL") if self.WIN5_BOX == '' else self.win_box5_change()
                self.winTypeLbl1.setVisible(True)
                self.winTypeLbl2.setVisible(True)
                self.winTypeLbl3.setVisible(True)
                self.winTypeLbl4.setVisible(True)
                self.winTypeLbl5.setVisible(True)
                self.winTypeLbl6.setVisible(False)
                self.winTypeComboBox1.setVisible(True)
                self.winTypeComboBox2.setVisible(True)
                self.winTypeComboBox3.setVisible(True)
                self.winTypeComboBox4.setVisible(True)
                self.winTypeComboBox5.setVisible(True)
                self.winTypeComboBox6.setVisible(False)
                self.winTypeComboBox1.setCurrentText("r5.xlarge") if self.WIN1_BOX == '' else self.win_type1_change()
                self.winTypeComboBox2.setCurrentText("r5.xlarge") if self.WIN2_BOX == '' else self.win_type2_change()
                self.winTypeComboBox3.setCurrentText("r5.xlarge") if self.WIN3_BOX == '' else self.win_type3_change()
                self.winTypeComboBox4.setCurrentText("r5.xlarge") if self.WIN4_BOX == '' else self.win_type4_change()
                self.winTypeComboBox5.setCurrentText("r5.xlarge") if self.WIN5_BOX == '' else self.win_type5_change()
                self.winTypeComboBox6.setCurrentText("r5.xlarge") if self.WIN6_BOX == '' else self.win_type6_change()
                self.winToolBtn1.setVisible(True)
                self.winToolBtn2.setVisible(True)
                self.winToolBtn3.setVisible(True)
                self.winToolBtn4.setVisible(True)
                self.winToolBtn5.setVisible(True)
                self.winToolBtn6.setVisible(False)
            else:
                self.winHostnameLbl1.setVisible(True)
                self.winHostnameLbl2.setVisible(True)
                self.winHostnameLbl3.setVisible(True)
                self.winHostnameLbl4.setVisible(True)
                self.winHostnameLbl5.setVisible(True)
                self.winHostnameLbl6.setVisible(True)
                self.winHostnameLineEdit1.setVisible(True)
                self.winHostnameLineEdit2.setVisible(True)
                self.winHostnameLineEdit3.setVisible(True)
                self.winHostnameLineEdit4.setVisible(True)
                self.winHostnameLineEdit5.setVisible(True)
                self.winHostnameLineEdit6.setVisible(True)
                self.winHostnameLineEdit1.setText(f"{ self.AWS_HOSTID }HM{ self.AWS_ENV[0] }01") if self.WIN1_BOX == '' else self.win_box1_change()
                self.winHostnameLineEdit2.setText(f"{ self.AWS_HOSTID }INT{ self.AWS_ENV[0] }01") if self.WIN2_BOX == '' else self.win_box2_change()
                self.winHostnameLineEdit3.setText(f"{ self.AWS_HOSTID }RDS{ self.AWS_ENV[0] }01") if self.WIN3_BOX == '' else self.win_box3_change()
                self.winHostnameLineEdit4.setText(f"{ self.AWS_HOSTID }VDA{ self.AWS_ENV[0] }01") if self.WIN4_BOX == '' else self.win_box4_change()
                self.winHostnameLineEdit5.setText(f"{ self.AWS_HOSTID }SQL{ self.AWS_ENV[0] }01") if self.WIN5_BOX == '' else self.win_box5_change()
                self.winHostnameLineEdit6.setText(f"{ self.AWS_HOSTID }VDA{ self.AWS_ENV[0] }01") if self.WIN6_BOX == '' else self.win_box6_change()
                self.winBoxLbl1.setVisible(True)
                self.winBoxLbl2.setVisible(True)
                self.winBoxLbl3.setVisible(True)
                self.winBoxLbl4.setVisible(True)
                self.winBoxLbl5.setVisible(True)
                self.winBoxLbl6.setVisible(True)
                self.winBoxComboBox1.setVisible(True)
                self.winBoxComboBox2.setVisible(True)
                self.winBoxComboBox3.setVisible(True)
                self.winBoxComboBox4.setVisible(True)
                self.winBoxComboBox5.setVisible(True)
                self.winBoxComboBox6.setVisible(True)
                self.winBoxComboBox1.setCurrentText("HANA Management") if self.WIN1_BOX == '' else self.win_box1_change()
                self.winBoxComboBox2.setCurrentText("Integration Server") if self.WIN2_BOX == '' else self.win_box2_change()
                self.winBoxComboBox3.setCurrentText("RDS") if self.WIN3_BOX == '' else self.win_box3_change()
                self.winBoxComboBox4.setCurrentText("Citrix") if self.WIN4_BOX == '' else self.win_box4_change()
                self.winBoxComboBox5.setCurrentText("SQL") if self.WIN5_BOX == '' else self.win_box5_change()
                self.winBoxComboBox6.setCurrentText("Citrix") if self.WIN6_BOX == '' else self.win_box6_change()
                self.winTypeLbl1.setVisible(True)
                self.winTypeLbl2.setVisible(True)
                self.winTypeLbl3.setVisible(True)
                self.winTypeLbl4.setVisible(True)
                self.winTypeLbl5.setVisible(True)
                self.winTypeLbl6.setVisible(True)
                self.winTypeComboBox1.setVisible(True)
                self.winTypeComboBox2.setVisible(True)
                self.winTypeComboBox3.setVisible(True)
                self.winTypeComboBox4.setVisible(True)
                self.winTypeComboBox5.setVisible(True)
                self.winTypeComboBox6.setVisible(True)
                self.winTypeComboBox1.setCurrentText("r5.xlarge") if self.WIN1_BOX == '' else self.win_type1_change()
                self.winTypeComboBox2.setCurrentText("r5.xlarge") if self.WIN2_BOX == '' else self.win_type2_change()
                self.winTypeComboBox3.setCurrentText("r5.xlarge") if self.WIN3_BOX == '' else self.win_type3_change()
                self.winTypeComboBox4.setCurrentText("r5.xlarge") if self.WIN4_BOX == '' else self.win_type4_change()
                self.winTypeComboBox5.setCurrentText("r5.xlarge") if self.WIN5_BOX == '' else self.win_type5_change()
                self.winTypeComboBox6.setCurrentText("r5.xlarge") if self.WIN6_BOX == '' else self.win_type6_change()
                self.winToolBtn1.setVisible(True)
                self.winToolBtn2.setVisible(True)
                self.winToolBtn3.setVisible(True)
                self.winToolBtn4.setVisible(True)
                self.winToolBtn5.setVisible(True)
                self.winToolBtn6.setVisible(True)

            self.WIN_COUNT = int(self.winComboBox.currentText())
        else:
            self.winHostnameLbl1.setVisible(False)
            self.winHostnameLbl2.setVisible(False)
            self.winHostnameLbl3.setVisible(False)
            self.winHostnameLbl4.setVisible(False)
            self.winHostnameLbl5.setVisible(False)
            self.winHostnameLbl6.setVisible(False)
            self.winHostnameLineEdit1.setVisible(False)
            self.winHostnameLineEdit2.setVisible(False)
            self.winHostnameLineEdit3.setVisible(False)
            self.winHostnameLineEdit4.setVisible(False)
            self.winHostnameLineEdit5.setVisible(False)
            self.winHostnameLineEdit6.setVisible(False)
            self.winBoxLbl1.setVisible(False)
            self.winBoxLbl2.setVisible(False)
            self.winBoxLbl3.setVisible(False)
            self.winBoxLbl4.setVisible(False)
            self.winBoxLbl5.setVisible(False)
            self.winBoxLbl6.setVisible(False)
            self.winBoxComboBox1.setVisible(False)
            self.winBoxComboBox2.setVisible(False)
            self.winBoxComboBox3.setVisible(False)
            self.winBoxComboBox4.setVisible(False)
            self.winBoxComboBox5.setVisible(False)
            self.winBoxComboBox6.setVisible(False)
            self.winTypeLbl1.setVisible(False)
            self.winTypeLbl2.setVisible(False)
            self.winTypeLbl3.setVisible(False)
            self.winTypeLbl4.setVisible(False)
            self.winTypeLbl5.setVisible(False)
            self.winTypeLbl6.setVisible(False)
            self.winTypeComboBox1.setVisible(False)
            self.winTypeComboBox2.setVisible(False)
            self.winTypeComboBox3.setVisible(False)
            self.winTypeComboBox4.setVisible(False)
            self.winTypeComboBox5.setVisible(False)
            self.winTypeComboBox6.setVisible(False)
            self.winToolBtn1.setVisible(False)
            self.winToolBtn2.setVisible(False)
            self.winToolBtn3.setVisible(False)
            self.winToolBtn4.setVisible(False)
            self.winToolBtn5.setVisible(False)
            self.winToolBtn6.setVisible(False)
            self.WIN_COUNT = 0
            self.HANAMGMT_COUNT = 0
            self.IS_COUNT = 0
            self.RDS_COUNT = 0
            self.CITRIX_COUNT = 0
            self.SQL_COUNT = 0
            self.HANAMGMT_LIST = []
            self.IS_LIST = []
            self.RDS_LIST = []
            self.CITRIX_LIST = []
            self.SQL_LIST = []
            self.HANAMGMT_TYPE_LIST = []
            self.IS_TYPE_LIST = []
            self.RDS_TYPE_LIST = []
            self.CITRIX_TYPE_LIST = []
            self.SQL_TYPE_LIST = []
            self.WIN1_TYPE = ''
            self.WIN2_TYPE = ''
            self.WIN3_TYPE = ''
            self.WIN4_TYPE = ''
            self.WIN5_TYPE = ''
            self.WIN6_TYPE = ''
            self.WIN1_BOX = ''
            self.WIN2_BOX = ''
            self.WIN3_BOX = ''
            self.WIN4_BOX = ''
            self.WIN5_BOX = ''
            self.WIN6_BOX = ''

        self.enable_start()

    def dc1_type_change(self):
        self.DC1_TYPE = self.dcTypeComboBox1.currentText()

    def dc2_type_change(self):
        self.DC2_TYPE = self.dcTypeComboBox2.currentText()

    def hana_type_change(self):
        self.HANA_TYPE = self.hanaTypeComboBox.currentText()

    def win_type1_change(self):
        self.WIN1_TYPE = self.winTypeComboBox1.currentText()

    def win_type2_change(self):
        self.WIN2_TYPE = self.winTypeComboBox2.currentText()

    def win_type3_change(self):
        self.WIN3_TYPE = self.winTypeComboBox3.currentText()

    def win_type4_change(self):
        self.WIN4_TYPE = self.winTypeComboBox4.currentText()

    def win_type5_change(self):
        self.WIN5_TYPE = self.winTypeComboBox5.currentText()

    def win_type6_change(self):
        self.WIN6_TYPE = self.winTypeComboBox6.currentText()

    def win_box1_change(self):
        self.WIN1_BOX = self.winBoxComboBox1.currentText()
        winbox_list = [ self.WIN2_BOX, self.WIN3_BOX, self.WIN4_BOX, self.WIN5_BOX, self.WIN6_BOX ]

        tag = 'HM' if self.winBoxComboBox1.currentText() == 'HANA Management' else \
        'INT' if self.winBoxComboBox1.currentText() == 'Integration Server' else \
        'RDS' if self.winBoxComboBox1.currentText() == 'RDS' else \
        'VDA' if self.winBoxComboBox1.currentText() == 'Citrix' else \
        'SQL' if self.winBoxComboBox1.currentText() == 'SQL' else ''

        self.winHostnameLineEdit1.setText(f"{ self.AWS_HOSTID }{ tag }{ self.AWS_ENV[0] }01")

        for idx, box in enumerate(winbox_list):
            if self.winBoxComboBox1.currentText() in box:
                self.logger(f"Match found at index {idx}: {box}", 'a')
                self.logger(f"Get attribute from list: { getattr(self, f"winHostnameLineEdit{ idx + 2 }").text() }", 'a')
                self.winHostnameLineEdit1.setText(f"{ self.AWS_HOSTID }{ tag }{ self.AWS_ENV[0] }0{ self.get_last_digit(getattr(self, f"winHostnameLineEdit{ idx + 2 }").text()) }")

    def win_box2_change(self):
        self.WIN1_BOX = self.winBoxComboBox1.currentText()
        self.WIN2_BOX = self.winBoxComboBox2.currentText()
        winbox_list = [ self.WIN1_BOX, self.WIN3_BOX, self.WIN4_BOX, self.WIN5_BOX, self.WIN6_BOX ]

        tag = 'HM' if self.winBoxComboBox2.currentText() == 'HANA Management' else \
        'INT' if self.winBoxComboBox2.currentText() == 'Integration Server' else \
        'RDS' if self.winBoxComboBox2.currentText() == 'RDS' else \
        'VDA' if self.winBoxComboBox2.currentText() == 'Citrix' else \
        'SQL' if self.winBoxComboBox2.currentText() == 'SQL' else ''

        self.winHostnameLineEdit2.setText(f"{ self.AWS_HOSTID }{ tag }{ self.AWS_ENV[0] }01")

        for idx, box in enumerate(winbox_list):
            if self.winBoxComboBox2.currentText() in box:
                self.logger(f"Match found at index {idx}: {box}", 'a')
                if idx == 0:
                    self.winHostnameLineEdit2.setText(f"{ self.AWS_HOSTID }{ tag }{ self.AWS_ENV[0] }0{ self.get_last_digit(getattr(self, f"winHostnameLineEdit{ idx + 1 }").text()) }")
                else:
                    self.winHostnameLineEdit2.setText(f"{ self.AWS_HOSTID }{ tag }{ self.AWS_ENV[0] }0{ self.get_last_digit(getattr(self, f"winHostnameLineEdit{ idx + 2 }").text()) }")

    def win_box3_change(self):
        self.WIN1_BOX = self.winBoxComboBox1.currentText()
        self.WIN2_BOX = self.winBoxComboBox2.currentText()
        self.WIN3_BOX = self.winBoxComboBox3.currentText()
        winbox_list = [ self.WIN1_BOX, self.WIN2_BOX, self.WIN4_BOX, self.WIN5_BOX, self.WIN6_BOX ]

        tag = 'HM' if self.winBoxComboBox3.currentText() == 'HANA Management' else \
        'INT' if self.winBoxComboBox3.currentText() == 'Integration Server' else \
        'RDS' if self.winBoxComboBox3.currentText() == 'RDS' else \
        'VDA' if self.winBoxComboBox3.currentText() == 'Citrix' else \
        'SQL' if self.winBoxComboBox3.currentText() == 'SQL' else ''

        self.winHostnameLineEdit3.setText(f"{ self.AWS_HOSTID }{ tag }{ self.AWS_ENV[0] }01")

        for idx, box in enumerate(winbox_list):
            if self.winBoxComboBox3.currentText() in box:
                self.logger(f"Match found at index {idx}: {box}", 'a')
                if idx <= 1:
                    self.winHostnameLineEdit3.setText(f"{ self.AWS_HOSTID }{ tag }{ self.AWS_ENV[0] }0{ self.get_last_digit(getattr(self, f"winHostnameLineEdit{ idx + 1 }").text()) }")
                else:
                    self.winHostnameLineEdit3.setText(f"{ self.AWS_HOSTID }{ tag }{ self.AWS_ENV[0] }0{ self.get_last_digit(getattr(self, f"winHostnameLineEdit{ idx + 2 }").text()) }")

    def win_box4_change(self):
        self.WIN1_BOX = self.winBoxComboBox1.currentText()
        self.WIN2_BOX = self.winBoxComboBox2.currentText()
        self.WIN3_BOX = self.winBoxComboBox3.currentText()
        self.WIN4_BOX = self.winBoxComboBox4.currentText()
        winbox_list = [ self.WIN1_BOX, self.WIN2_BOX, self.WIN3_BOX, self.WIN5_BOX, self.WIN6_BOX ]
        
        tag = 'HM' if self.winBoxComboBox4.currentText() == 'HANA Management' else \
        'INT' if self.winBoxComboBox4.currentText() == 'Integration Server' else \
        'RDS' if self.winBoxComboBox4.currentText() == 'RDS' else \
        'VDA' if self.winBoxComboBox4.currentText() == 'Citrix' else \
        'SQL' if self.winBoxComboBox4.currentText() == 'SQL' else ''

        self.winHostnameLineEdit4.setText(f"{ self.AWS_HOSTID }{ tag }{ self.AWS_ENV[0] }01")

        for idx, box in enumerate(winbox_list):
            if self.winBoxComboBox4.currentText() in box:
                self.logger(f"Match found at index {idx}: {box}", 'a')
                if idx <= 2:
                    self.winHostnameLineEdit4.setText(f"{ self.AWS_HOSTID }{ tag }{ self.AWS_ENV[0] }0{ self.get_last_digit(getattr(self, f"winHostnameLineEdit{ idx + 1 }").text()) }")
                else:
                    self.winHostnameLineEdit4.setText(f"{ self.AWS_HOSTID }{ tag }{ self.AWS_ENV[0] }0{ self.get_last_digit(getattr(self, f"winHostnameLineEdit{ idx + 2 }").text()) }")

    def win_box5_change(self):
        self.WIN1_BOX = self.winBoxComboBox1.currentText()
        self.WIN2_BOX = self.winBoxComboBox2.currentText()
        self.WIN3_BOX = self.winBoxComboBox3.currentText()
        self.WIN4_BOX = self.winBoxComboBox4.currentText()
        self.WIN5_BOX = self.winBoxComboBox5.currentText()
        winbox_list = [ self.WIN1_BOX, self.WIN2_BOX, self.WIN3_BOX, self.WIN4_BOX, self.WIN6_BOX ]

        tag = 'HM' if self.winBoxComboBox5.currentText() == 'HANA Management' else \
        'INT' if self.winBoxComboBox5.currentText() == 'Integration Server' else \
        'RDS' if self.winBoxComboBox5.currentText() == 'RDS' else \
        'VDA' if self.winBoxComboBox5.currentText() == 'Citrix' else \
        'SQL' if self.winBoxComboBox5.currentText() == 'SQL' else ''

        self.winHostnameLineEdit5.setText(f"{ self.AWS_HOSTID }{ tag }{ self.AWS_ENV[0] }01")

        for idx, box in enumerate(winbox_list):
            if self.winBoxComboBox5.currentText() in box:
                self.logger(f"Match found at index {idx}: {box}", 'a')
                if idx <= 3:
                    self.winHostnameLineEdit5.setText(f"{ self.AWS_HOSTID }{ tag }{ self.AWS_ENV[0] }0{ self.get_last_digit(getattr(self, f"winHostnameLineEdit{ idx + 1 }").text()) }")
                else:
                    self.winHostnameLineEdit5.setText(f"{ self.AWS_HOSTID }{ tag }{ self.AWS_ENV[0] }0{ self.get_last_digit(getattr(self, f"winHostnameLineEdit{ idx + 2 }").text()) }")

    def win_box6_change(self):
        self.WIN1_BOX = self.winBoxComboBox1.currentText()
        self.WIN2_BOX = self.winBoxComboBox2.currentText()
        self.WIN3_BOX = self.winBoxComboBox3.currentText()
        self.WIN4_BOX = self.winBoxComboBox4.currentText()
        self.WIN5_BOX = self.winBoxComboBox5.currentText()
        self.WIN6_BOX = self.winBoxComboBox6.currentText()
        winbox_list = [ self.WIN1_BOX, self.WIN2_BOX, self.WIN3_BOX, self.WIN4_BOX, self.WIN5_BOX ]

        tag = 'HM' if self.winBoxComboBox6.currentText() == 'HANA Management' else \
        'INT' if self.winBoxComboBox6.currentText() == 'Integration Server' else \
        'RDS' if self.winBoxComboBox6.currentText() == 'RDS' else \
        'VDA' if self.winBoxComboBox6.currentText() == 'Citrix' else \
        'SQL' if self.winBoxComboBox6.currentText() == 'SQL' else ''

        self.winHostnameLineEdit6.setText(f"{ self.AWS_HOSTID }{ tag }{ self.AWS_ENV[0] }01")

        for idx, box in enumerate(winbox_list):
            if self.winBoxComboBox6.currentText() in box:
                self.logger(f"Match found at index {idx}: {box}", 'a')
                self.winHostnameLineEdit6.setText(f"{ self.AWS_HOSTID }{ tag }{ self.AWS_ENV[0] }0{ self.get_last_digit(getattr(self, f"winHostnameLineEdit{ idx + 1 }").text()) }")

    def get_last_digit(self, str):
        digits = [ int(char) for char in str if char.isdigit() ]
        return digits[-1] + 1 if digits else 1

    def hana_rev_change(self):
        self.HANA_REVISION_NAME = self.hanaRevisionComboBox.currentText()

        if self.hanaRevisionComboBox.currentIndex() == 0:
            self.HANA_REVISION = '51058191'
        elif self.hanaRevisionComboBox.currentIndex() == 1:
            self.HANA_REVISION = '51057201'
        elif self.hanaRevisionComboBox.currentIndex() == 2:
            self.HANA_REVISION = '51056351'
        elif self.hanaRevisionComboBox.currentIndex() == 3:
            self.HANA_REVISION = '51055068'
        else:
            self.HANA_REVISION = '51054995'

    def hana_patch_change(self):
        self.HANA_PATCH_NAME = self.hanaClientPkgComboBox.currentText()

        if self.hanaClientPkgComboBox.currentIndex() == 0:
            self.HANA_PATCH = 'B1H1000SP_2411-70004122'
        elif self.hanaClientPkgComboBox.currentIndex() == 1:
            self.HANA_PATCH = 'B1H1000SP_2408-70004122'
        elif self.hanaClientPkgComboBox.currentIndex() == 2:
            self.HANA_PATCH = 'B1H1000_2405-70004122'
        else:
            self.HANA_PATCH = 'B1H1000SP_2402-70004122'

    def hana_cockpit_select(self, state):
        self.HANA_COCKPIT = self.hanaCockpitCheckBox.isChecked() if state !=0 else False

    def hana_demodb_select(self, state):
        self.HANA_DEMO_DB = self.hanaDemoDbCheckBox.isChecked() if state !=0 else False

    def init_account(self):
        try:
            ACCT_NAME = boto3.client('sts').get_caller_identity()['UserId'].split(':')[1]
        except (Exception) as e:
            errorMsg = 'No awsumed account.<br>Please set one now!'
            errorMsg += '<p style=\'text-align: justify; background-color: black\'>&nbsp;awsume&nbsp;&lt;AWS_ACCOUNT_NAME&gt;&nbsp;</p>'
            self.error(errorMsg, 'error', window)
        else:
            try:
                self.AWS_ACCT = boto3.client('sts').get_caller_identity()["Account"]
                # cmd = f". awsume sapphire-payer && aws organizations list-tags-for-resource --resource-id { self.AWS_ACCT } --output json | jq -r 'reduce .Tags[] as $tag ({{}}; if $tag.Key == \"CustomerID\" or $tag.Key == \"Environment\" then .[$tag.Key] = $tag.Value else . end)'"
                cmd = f"awsume sapphire-payer && aws organizations list-tags-for-resource --resource-id { self.AWS_ACCT } --output json"
                result = subprocess.run(f"{ '.' if self.os_name != 'Windows' else '' } { cmd }", shell=True, capture_output=True, text=True)
                # boto3.client('resourcegroupstaggingapi').get_tag_values(Key="CustomerID").get('TagValues', [])[0]
            except (Exception) as e:
                errorMsg = f'[ERROR]: Account ({ ACCT_NAME }) has no tag CustomerID. Please set one now!'
            else:
                # self.AWS_HOSTID = boto3.client('resourcegroupstaggingapi').get_tag_values(Key="CustomerID").get('TagValues', [])[0]
                self.AWS_ALIAS = boto3.client('sts').get_caller_identity()['UserId'].split(':')[1]

                tags = json.loads(result.stdout).get('Tags')
                for obj in tags:
                    if obj.get('Key') == 'CustomerID':
                        self.AWS_HOSTID = obj.get('Value')
                    if obj.get('Key') == 'Environment':
                        self.AWS_ENV = obj.get('Value')

                # self.AWS_HOSTID = json.loads(result.stdout).get('CustomerID')
                # self.AWS_ENV = json.loads(result.stdout).get('Environment')
                self.AWS_RGN = boto3.Session().region_name
                self.AWS_REGNAME = self.get_region_name()

                self.logger(f'\nAccount ID: { self.AWS_ACCT }', 's')
                self.logger(f'\nAccount Name: { self.AWS_ALIAS }', 'b')
                self.logger(f'\nAccount Region: { self.AWS_RGN } ({ self.AWS_REGNAME })', 'b')
                self.logger(f'\nCustomer ID: { self.AWS_HOSTID }', 'b')
                self.logger(f'\nEnvironment: { self.AWS_ENV }', 'b')
                self.logger(f'\nGitHub User: { self.GITHUB_USER } ({ self.GITHUB_EMAIL })', 'b')
                self.logger(f'\nCurrent Branch: { self.GIT_BRANCH }', 'b')
                self.logger(f'\nProject Path: { self.proj_dir }', 'b')

    def get_region_name(self):
        if 'eu-west-2' in self.AWS_RGN:
            return "London"
        elif 'us-east-2' in self.AWS_RGN:
            return 'Ohio'
        else:
            return 'N/A'

    def enable_start(self):
        if self.DC_COUNT or self.HANA_COUNT or self.WIN_COUNT:
            self.startBtn.setDisabled(False)
            # self.startBtn.setStyleSheet(u"background-color: rgb(214, 214, 214);\n""color: rgb(255, 255, 255)")
        else:
            self.startBtn.setDisabled(True) # set disable if no servers provision for now
            # self.startBtn.setStyleSheet(u"background-color: rgb(18, 57, 79);\n""color: rgb(255, 255, 255)")

    def validation(self):
        winbox_list = [ self.WIN1_BOX, self.WIN2_BOX, self.WIN3_BOX, self.WIN4_BOX, self.WIN5_BOX, self.WIN6_BOX ]
        self.HANAMGMT_COUNT = 0
        
        if 'HANA Management' in winbox_list:
            self.HANAMGMT_COUNT += 1

        self.AWS_FINCODE = self.finCodeLineEdit.text()

        try:
            if not self.finCodeLineEdit.text():
                data = 'Finance Code'
                raise ValueError('should not be empty!')
            if not self.finCodeLineEdit.text().isdigit():
                data = 'Finance Code'
                raise ValueError('should be numeric!')
            if int(self.DC_COUNT) != 0:
                if not self.dcHostnameLineEdit1.text():
                    data = 'Domain Controller'
                    raise ValueError('hostname should not be empty!')
                if not self.dcHostnameLineEdit1.text().isalnum():
                    data = 'Domain Controller'
                    raise ValueError('hostname should not contain special characters!')
                if int(self.DC_COUNT) > 1:
                    if not self.dcHostnameLineEdit2.text():
                        data = 'Domain Controller'
                        raise ValueError('hostname should not be empty!')
                    if not self.dcHostnameLineEdit2.text().isalnum():
                        data = 'Domain Controller'
                        raise ValueError('hostname should not contain special characters!')
            if int(self.HANA_COUNT) != 0:
                if not self.hanaHostnameLineEdit.text():
                    data = 'SAP HANA DB'
                    raise ValueError('hostname should not be empty!')
                if not self.hanaHostnameLineEdit.text().isalnum():
                    data = 'SAP HANA DB'
                    raise ValueError('hostname should not contain special characters!')
                if int(self.HANAMGMT_COUNT) == 0:
                    data = 'HANA Management'
                    raise ValueError('instance is required!')
            if int(self.WIN_COUNT) != 0:
                if int(self.HANAMGMT_COUNT) != 0 and int(self.HANA_COUNT) == 0:
                    data = 'SAP HANA DB'
                    raise ValueError('instance is required!')
                if not self.winHostnameLineEdit1.text():
                    data = self.winBoxComboBox1.currentText()
                    raise ValueError('hostname should not be empty!')
                if not self.winHostnameLineEdit1.text().isalnum():
                    data = self.winBoxComboBox1.currentText()
                    raise ValueError('hostname should not contain special characters!')
                if not self.winHostnameLineEdit2.text():
                    data = self.winBoxComboBox2.currentText()
                    raise ValueError('hostname should not be empty!')
                if not self.winHostnameLineEdit2.text().isalnum():
                    data = self.winBoxComboBox2.currentText()
                    raise ValueError('hostname should not contain special characters!')
                if not self.winHostnameLineEdit3.text():
                    data = self.winBoxComboBox3.currentText()
                    raise ValueError('hostname should not be empty!')
                if not self.winHostnameLineEdit3.text().isalnum():
                    data = self.winBoxComboBox3.currentText()
                    raise ValueError('hostname should not contain special characters!')
                if not self.winHostnameLineEdit4.text():
                    data = self.winBoxComboBox4.currentText()
                    raise ValueError('hostname should not be empty!')
                if not self.winHostnameLineEdit4.text().isalnum():
                    data = self.winBoxComboBox4.currentText()
                    raise ValueError('hostname should not contain special characters!')
                if not self.winHostnameLineEdit5.text():
                    data = self.winBoxComboBox5.currentText()
                    raise ValueError('hostname should not be empty!')
                if not self.winHostnameLineEdit5.text().isalnum():
                    data = self.winBoxComboBox5.currentText()
                    raise ValueError('hostname should not contain special characters!')
                if not self.winHostnameLineEdit6.text():
                    data = self.winBoxComboBox6.currentText()
                    raise ValueError('hostname should not be empty!')
                if not self.winHostnameLineEdit6.text().isalnum():
                    data = self.winBoxComboBox6.currentText()
                    raise ValueError('hostname should not contain special characters!')
        except (ValueError) as e:
            errorMsg = f'{ data } { e }'
            self.error(errorMsg, 'validation', window)
        else:
            self.start()

    def start(self):
        self.logger('\nInitializing ...\n', 's')

        self.set_hostname()
        self.DC_COUNT = len(self.DC_LIST)
        self.HANA_COUNT = len(self.HANA_LIST)
        self.HANAMGMT_COUNT = len(self.HANAMGMT_LIST)
        self.IS_COUNT = len(self.IS_LIST)
        self.RDS_COUNT = len(self.RDS_LIST)
        self.CITRIX_COUNT = len(self.CITRIX_LIST)
        self.SQL_COUNT = len(self.SQL_LIST)
        if self.DC_COUNT == 1:
            self.DC_TYPE_LIST.append(self.DC1_TYPE)
        if self.DC_COUNT == 2:
            self.DC_TYPE_LIST.append(self.DC1_TYPE)
            self.DC_TYPE_LIST.append(self.DC2_TYPE)
        self.HANA_TYPE_LIST.append(self.HANA_TYPE)
        self.EC2_APP_LIST = [ item for sublist in [ self.IS_LIST, self.RDS_LIST, self.CITRIX_LIST ] for item in sublist ]
        self.EC2_DATA_LIST = [ item for sublist in [ self.DC_LIST, self.HANA_LIST, self.HANAMGMT_LIST, self.SQL_LIST ] for item in sublist ]
        self.set_wintype_list()

        self.EXPORTED.append("AWS_ALIAS")
        self.VARS.append(self.AWS_ALIAS)

        self.EXPORTED.append("AWS_ACCT")
        self.VARS.append(self.AWS_ACCT)
        
        self.EXPORTED.append("AWS_RGN")
        self.VARS.append(self.AWS_RGN)

        self.EXPORTED.append("AWS_REGNAME")
        self.VARS.append(self.AWS_REGNAME)

        self.EXPORTED.append("AWS_HOSTID")
        self.VARS.append(self.AWS_HOSTID)

        self.EXPORTED.append("AWS_FINCODE")
        self.VARS.append(self.AWS_FINCODE)

        with open(f'{ self.proj_dir }/terraform/template/customer-account/var.base.tpl', 'r', encoding='utf-8') as vars_file:
            lines = vars_file.readlines()

            for i, line in enumerate(lines):
                if 'automation_account_id' in line:
                    for j in range(i + 1, i + 4):
                        if 'default' in lines[j]:
                            self.AWS_AUTOMATIONID = lines[j].split()[2].strip('"')
                            continue
                if 'shared-services_account_id' in line:
                    for j in range(i + 1, i + 4):
                        if 'default' in lines[j]:
                            self.AWS_SHAREDID = lines[j].split()[2].strip('"')
                            break

        self.EXPORTED.append("AWS_AUTOMATIONID")
        self.VARS.append(self.AWS_AUTOMATIONID)

        self.EXPORTED.append("AWS_SHAREDID")
        self.VARS.append(self.AWS_SHAREDID)

        if int(self.DC_COUNT) == 0 and int(self.HANA_COUNT) == 0 and int(self.WIN_COUNT) == 0:            
            self.end(1)

        if int(self.DC_COUNT) != 0:
            self.RUNNER_COUNT += 1
            self.EXPORTED.append("DOMAIN CONTROLLERS")
            self.VARS.append(f'{ str(self.DC_COUNT) }, { str(self.DC_LIST) }, { str(self.DC_TYPE_LIST) }')

        if int(self.HANA_COUNT) != 0:
            self.RUNNER_COUNT += 1
            self.EXPORTED.append("SAP HANA DB")
            self.VARS.append(f'{ str(self.HANA_COUNT) }, { str(self.HANA_LIST) }, { str(self.HANA_TYPE_LIST) }')

            self.EXPORTED.append("SAP HANA REVISION")
            self.VARS.append(str(f'{ self.HANA_REVISION } - { self.HANA_REVISION_NAME }'))

            self.EXPORTED.append("SAP HANA PATCH")
            self.VARS.append(str(f'{ self.HANA_PATCH } - { self.HANA_PATCH_NAME }'))

            self.EXPORTED.append("SAP HANA COCKPIT")
            self.VARS.append(str(f'{ self.HANA_COCKPIT }'))

            self.EXPORTED.append("SAP HANA DEMO DATABASES")
            self.VARS.append(str(f'{ self.HANA_DEMO_DB }'))

        if int(self.HANAMGMT_COUNT) != 0:
            self.EXPORTED.append("HANA MANAGEMENT")
            self.VARS.append(f'{ str(self.HANAMGMT_COUNT) }, { str(self.HANAMGMT_LIST) }, { str(self.HANAMGMT_TYPE_LIST) }')

        if int(self.IS_COUNT) != 0:
            self.EXPORTED.append("INTEGRATION SERVER")
            self.VARS.append(f'{ str(self.IS_COUNT) }, { str(self.IS_LIST) }, { str(self.IS_TYPE_LIST) }')

        if int(self.RDS_COUNT) != 0:
            self.EXPORTED.append("RDS")
            self.VARS.append(f'{ str(self.RDS_COUNT) }, { str(self.RDS_LIST) }, { str(self.RDS_TYPE_LIST) }')

        if int(self.CITRIX_COUNT) != 0:
            self.RUNNER_COUNT += 1
            self.EXPORTED.append("CITRIX")
            self.VARS.append(f'{ str(self.CITRIX_COUNT) }, { str(self.CITRIX_LIST) }, { str(self.CITRIX_TYPE_LIST) }')

        if int(self.SQL_COUNT) != 0:
            self.RUNNER_COUNT += 1
            self.EXPORTED.append("SQL")
            self.VARS.append(f'{ str(self.SQL_COUNT) }, { str(self.SQL_LIST) }, { str(self.SQL_TYPE_LIST) }')

        self.logger('Generating workflow & terraform files from template..' , 't')

        # Remove existing customer folder
        try:
            shutil.rmtree(f'{ self.proj_dir }/terraform/{ self.AWS_ALIAS }')
        except (FileNotFoundError):
            self.logger(f"Folder { self.proj_dir }/terraform/{ self.AWS_ALIAS } does not exist, so it cannot be removed.", 'e')
        except (Exception) as e:
            self.logger(f"An unexpected error occurred: {e}", 'e')
        finally:
            os.makedirs(f'{ self.proj_dir }/terraform/{ self.AWS_ALIAS }')
            self.logger(f"Folder { self.proj_dir }/terraform/{ self.AWS_ALIAS } created.", 'a')

        # Remove existing workflow file
        try:
            os.remove(f'{ self.proj_dir }/.github/workflows/{ self.AWS_ALIAS }.yml')
        except (FileNotFoundError):
            self.logger(f"File { self.proj_dir }/.github/workflows/{ self.AWS_ALIAS }.yml'does not exist, so it cannot be removed.", 'e')
        except (Exception) as e:
            self.logger(f"An unexpected error occurred: {e}", 'e')

        TEMPLATE_FILES = sorted([ f for f in os.listdir(f'{ self.proj_dir }/terraform/template/customer-account') if f.endswith(('.tfvars', '.tf', '.yml', '.tpl', '.py')) ])

        for file in TEMPLATE_FILES:
            if file.endswith('.yml') or file.endswith('.tpl'):
                with open(f'{ self.proj_dir }/terraform/template/customer-account/{ file }', 'r', encoding='utf-8') as template_files:
                    content = template_files.read()
                    content = content.replace('env.AWS_ALIAS', self.AWS_ALIAS)
                    content = content.replace('env.AWS_ACCT', self.AWS_ACCT)
                    content = content.replace('env.AWS_RGN', self.AWS_RGN)
                    content = content.replace('env.AWS_REGNAME', self.AWS_REGNAME)
                    content = content.replace('env.AWS_HOSTID', self.AWS_HOSTID)
                    content = content.replace('env.AWS_FINCODE', self.AWS_FINCODE)
                    content = content.replace('env.AWS_AUTOMATIONID', self.AWS_AUTOMATIONID)
                    content = content.replace('env.AWS_SHAREDID', self.AWS_SHAREDID)
                    content = content.replace('env.HANA_REVISION', self.HANA_REVISION)
                    content = content.replace('env.HANA_PATCH', self.HANA_PATCH)
                    content = content.replace('env.HANA_COCKPIT', str(self.HANA_COCKPIT).lower())
                    content = content.replace('env.HANA_DEMO_DB', str(self.HANA_DEMO_DB).lower())
                    content = content.replace('env.EC2_APP_LIST', str(self.EC2_APP_LIST).replace("'", '"').replace('[', '[ ').replace(']', ' ]'))
                    content = content.replace('env.EC2_DATA_LIST', str(self.EC2_DATA_LIST).replace("'", '"').replace('[', '[ ').replace(']', ' ]'))
                    content = content.replace('env.RUNNER_COUNT', '2' if self.RUNNER_COUNT <= 2 else str(self.RUNNER_COUNT))
                    content = content.replace('env.DC_CONFIG', 'true' if self.DC_COUNT else 'false')
                    content = content.replace('env.HANA_CONFIG', 'true' if self.HANA_COUNT else 'false')
                    content = content.replace('env.CITRIX_CONFIG', 'true' if self.CITRIX_COUNT else 'false')
                    content = content.replace('env.DESTROY_NEEDS',
                        '[ terraform_apply, configure_dc, configure_hana, configure_citrix ]' if self.DC_COUNT and self.HANA_COUNT and self.CITRIX_COUNT else
                        '[ terraform_apply, configure_dc, configure_hana ]' if self.DC_COUNT and self.HANA_COUNT and not self.CITRIX_COUNT else
                        '[ terraform_apply, configure_dc, configure_citrix ]' if self.DC_COUNT and self.CITRIX_COUNT and not self.HANA_COUNT else
                        '[ terraform_apply, configure_hana, configure_citrix ]' if self.HANA_COUNT and self.CITRIX_COUNT and not self.DC_COUNT else
                        '[ terraform_apply, configure_dc ]' if self.DC_COUNT and not self.HANA_COUNT and not self.CITRIX_COUNT else
                        '[ terraform_apply, configure_hana ]' if self.HANA_COUNT and not self.DC_COUNT and not self.CITRIX_COUNT else
                        '[ terraform_apply, configure_citrix ]' if self.CITRIX_COUNT and not self.DC_COUNT and not self.HANA_COUNT else
                        'terraform_apply'
                    )
                    content = content.replace('env.DESTROY_COND',
                        "(needs.terraform_apply.outputs.job-status == 'failure' || needs.configure_dc.outputs.job-status == 'failure' || needs.configure_hana.outputs.job-status == 'failure' || needs.configure_citrix.outputs.job-status == 'failure')" if self.DC_COUNT and self.HANA_COUNT and self.CITRIX_COUNT else
                        "(needs.terraform_apply.outputs.job-status == 'failure' || needs.configure_dc.outputs.job-status == 'failure' || needs.configure_hana.outputs.job-status == 'failure')" if self.DC_COUNT and self.HANA_COUNT and not self.CITRIX_COUNT else
                        "(needs.terraform_apply.outputs.job-status == 'failure' || needs.configure_dc.outputs.job-status == 'failure' || needs.configure_citrix.outputs.job-status == 'failure')" if self.DC_COUNT and self.CITRIX_COUNT and not self.HANA_COUNT else
                        "(needs.terraform_apply.outputs.job-status == 'failure' || needs.configure_hana.outputs.job-status == 'failure' || (needs.configure_citrix.outputs.job-status == 'failure')" if self.HANA_COUNT and self.CITRIX_COUNT and not self.DC_COUNT else
                        "(needs.terraform_apply.outputs.job-status == 'failure' || needs.configure_dc.outputs.job-status == 'failure')" if self.DC_COUNT and not self.HANA_COUNT and not self.CITRIX_COUNT else
                        "(needs.terraform_apply.outputs.job-status == 'failure' || needs.configure_hana.outputs.job-status == 'failure')" if self.HANA_COUNT and not self.DC_COUNT and not self.CITRIX_COUNT else
                        "(needs.terraform_apply.outputs.job-status == 'failure' || needs.configure_citrix.outputs.job-status == 'failure')" if self.CITRIX_COUNT and not self.DC_COUNT and not self.HANA_COUNT else
                        "needs.terraform_apply.outputs.job-status == 'failure'"
                    )
                    content = content.replace('env.DESTROY_RUNNERS',
                        "(needs.terraform_apply.outputs.job-status != 'failure' && needs.configure_dc.outputs.job-status != 'failure' && needs.configure_hana.outputs.job-status != 'failure' && needs.configure_citrix.outputs.job-status != 'failure')" if self.DC_COUNT and self.HANA_COUNT and self.CITRIX_COUNT else
                        "(needs.terraform_apply.outputs.job-status != 'failure' && needs.configure_dc.outputs.job-status != 'failure' && needs.configure_hana.outputs.job-status != 'failure')" if self.DC_COUNT and self.HANA_COUNT and not self.CITRIX_COUNT else
                        "(needs.terraform_apply.outputs.job-status != 'failure' && needs.configure_dc.outputs.job-status != 'failure' && needs.configure_citrix.outputs.job-status != 'failure')" if self.DC_COUNT and self.CITRIX_COUNT and not self.HANA_COUNT else
                        "(needs.terraform_apply.outputs.job-status != 'failure' && needs.configure_hana.outputs.job-status != 'failure' && needs.configure_citrix.outputs.job-status != 'failure')" if self.HANA_COUNT and self.CITRIX_COUNT and not self.DC_COUNT else
                        "(needs.terraform_apply.outputs.job-status != 'failure' && needs.configure_dc.outputs.job-status != 'failure')" if self.DC_COUNT and not self.HANA_COUNT and not self.CITRIX_COUNT else
                        "(needs.terraform_apply.outputs.job-status != 'failure' && needs.configure_hana.outputs.job-status != 'failure')" if self.HANA_COUNT and not self.DC_COUNT and not self.CITRIX_COUNT else
                        "(needs.terraform_apply.outputs.job-status != 'failure' && needs.configure_citrix.outputs.job-status != 'failure')" if self.CITRIX_COUNT and not self.DC_COUNT and not self.HANA_COUNT else
                        "needs.terraform_apply.outputs.job-status != 'failure'"
                    )

                    if int(self.DC_COUNT) != 0:
                        content = content.replace(f'{ self.AWS_HOSTID }DCT0env.DC_COUNT', str(self.DC_LIST).strip("\"'[]").replace("'", '"'))
                        content = content.replace('env.DC_TYPE_LIST', str(self.DC_TYPE_LIST).strip("\"'[]").replace("'", '"'))
                    else:
                        content = content.replace('env.DC_COUNT', str(self.DC_COUNT))
                        content = content.replace('env.DC_TYPE_LIST', str(self.DC_TYPE_LIST))

                    if int(self.HANA_COUNT) != 0:
                        content = content.replace(f'{ self.AWS_HOSTID }HANA0env.HANA_COUNT', str(self.HANA_LIST).strip("\"'[]").replace("'", '"'))
                        content = content.replace('env.HANA_TYPE_LIST', str(self.HANA_TYPE_LIST).strip("\"'[]").replace("'", '"'))
                    else:
                        content = content.replace('env.HANA_COUNT', str(self.HANA_COUNT))
                        content = content.replace('env.HANA_TYPE_LIST', str(self.HANA_TYPE_LIST))

                    if int(self.HANAMGMT_COUNT) != 0:
                        content = content.replace(f'{ self.AWS_HOSTID }APP0env.HANAMGMT_COUNT', str(self.HANAMGMT_LIST).strip("\"'[]").replace("'", '"'))
                        content = content.replace('env.HANAMGMT_TYPE_LIST', str(self.HANAMGMT_TYPE_LIST).strip("\"'[]").replace("'", '"'))
                    else:
                        content = content.replace('env.HANAMGMT_COUNT', str(self.HANAMGMT_COUNT))
                        content = content.replace('env.HANAMGMT_TYPE_LIST', str(self.HANAMGMT_TYPE_LIST))

                    if int(self.IS_COUNT) != 0:
                        content = content.replace(f'{ self.AWS_HOSTID }APP0env.IS_COUNT', str(self.IS_LIST).strip("\"'[]").replace("'", '"'))
                        content = content.replace('env.IS_TYPE_LIST', str(self.IS_TYPE_LIST).strip("\"'[]").replace("'", '"'))
                    else:
                        content = content.replace('env.IS_COUNT', str(self.IS_COUNT))
                        content = content.replace('env.IS_TYPE_LIST', str(self.IS_TYPE_LIST))

                    if int(self.RDS_COUNT) != 0:
                        content = content.replace(f'{ self.AWS_HOSTID }APP0env.RDS_COUNT', str(self.RDS_LIST).strip("\"'[]").replace("'", '"'))
                        content = content.replace('env.RDS_TYPE_LIST', str(self.RDS_TYPE_LIST).strip("\"'[]").replace("'", '"'))
                    else:
                        content = content.replace('env.RDS_COUNT', str(self.RDS_COUNT))
                        content = content.replace('env.RDS_TYPE_LIST', str(self.RDS_TYPE_LIST))

                    if int(self.CITRIX_COUNT) != 0:
                        content = content.replace(f'{ self.AWS_HOSTID }APP0env.CITRIX_COUNT', str(self.CITRIX_LIST).strip("\"'[]").replace("'", '"'))
                        content = content.replace('env.CITRIX_TYPE_LIST', str(self.CITRIX_TYPE_LIST).strip("\"'[]").replace("'", '"'))
                    else:
                        content = content.replace('env.CITRIX_COUNT', str(self.CITRIX_COUNT))
                        content = content.replace('env.CITRIX_TYPE_LIST', str(self.CITRIX_TYPE_LIST))

                    if int(self.SQL_COUNT) != 0:
                        content = content.replace(f'{ self.AWS_HOSTID }APP0env.SQL_COUNT', str(self.SQL_LIST).strip("\"'[]").replace("'", '"'))
                        content = content.replace('env.SQL_TYPE_LIST', str(self.SQL_TYPE_LIST).strip("\"'[]").replace("'", '"'))
                    else:
                        content = content.replace('env.SQL_COUNT', str(self.SQL_COUNT))
                        content = content.replace('env.SQL_TYPE_LIST', str(self.SQL_TYPE_LIST))

                if file.endswith('.yml'):
                    with open(f'{ self.proj_dir }/.github/workflows/{ self.AWS_ALIAS }.yml', 'w', encoding='utf-8') as yml_file:
                        yml_file.write(content)

            if file.endswith('.tpl'):
                if file.startswith('module.'):
                    tf_file = f'{ self.proj_dir }/terraform/{ self.AWS_ALIAS }/main.tf'
                if file.startswith('loc.'):
                    tf_file = f'{ self.proj_dir }/terraform/{ self.AWS_ALIAS }/locals.tf'
                if file.startswith('out.'):
                    tf_file = f'{ self.proj_dir }/terraform/{ self.AWS_ALIAS }/outputs.tf'
                if file.startswith('var.'):
                    tf_file = f'{ self.proj_dir }/terraform/{ self.AWS_ALIAS }/variables.tf'

                with open(tf_file, 'a', encoding='utf-8') as module_file:
                    if file.endswith('.base.tpl'):
                        if file.startswith('loc.'):
                            module_file.write(f'{ content[:-2] }')
                        else:
                            module_file.write(f'\n{ content }')
                    if int(self.DC_COUNT) != 0 and file.endswith('.dc.tpl'):
                        module_file.write(f'\n{ content }')
                    if int(self.HANAMGMT_COUNT) != 0 and file.endswith('.hanamgmt.tpl'):
                        module_file.write(f'\n{ content }')
                    if int(self.IS_COUNT) != 0 and file.endswith('.is.tpl'):
                        module_file.write(f'\n{ content }')
                    if int(self.RDS_COUNT) != 0 and file.endswith('.rds.tpl'):
                        module_file.write(f'\n{ content }')
                    if int(self.CITRIX_COUNT) != 0 and file.endswith('.citrix.tpl'):
                        module_file.write(f'\n{ content }')
                    if int(self.SQL_COUNT) != 0 and file.endswith('.sql.tpl'):
                        module_file.write(f'\n{ content }')
                    # sorted last file name should append "}" close syntax
                    if int(self.HANA_COUNT) != 0 and file.endswith('.suse.tpl'):
                        if file.startswith('loc.'):
                            module_file.write(f'\n{ content }\n{ "}" }')
                        else:
                            module_file.write(f'\n{ content }')
                    if int(self.HANA_COUNT) == 0 and file.endswith('.suse.tpl'):
                        if file.startswith('loc.'):
                            module_file.write(f'\n{ "}" }')

            if file.endswith(('.tfvars', '.tf')):
                source_file = os.path.join(f'{ self.proj_dir }/terraform/template/customer-account', file) 
                target_file = os.path.join(f'{ self.proj_dir }/terraform/{ self.AWS_ALIAS }', file)
                self.copy_file(source_file, target_file)

            if file.endswith('.py'):
                source_file = os.path.join(f'{ self.proj_dir }/terraform/template/customer-account', file) 
                target_file = os.path.join(f'{ self.proj_dir }/terraform/{ self.AWS_ALIAS }', file)
                current_permissions = os.stat(source_file).st_mode
                os.chmod(source_file, current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                self.copy_file(source_file, target_file)

        # Create IAM Role (github-oidc)
        role_name = "github-oidc"
        provider_name = 'token.actions.githubusercontent.com'

        try:
            create_provider_response = boto3.client('iam').create_open_id_connect_provider(
                Url=f'https://{ provider_name }',
                ClientIDList=['sts.amazonaws.com'],
                ThumbprintList=["1c58a3a8518e8759bf075b76b750d4f2df264fcd"]
            )
            provider_arn = create_provider_response['OpenIDConnectProviderArn']
            self.logger(f"OIDC provider { provider_name } created successfully with ARN { provider_arn }.", 'a')
        except boto3.client('iam').exceptions.EntityAlreadyExistsException:
            self.logger(f"OIDC provider { provider_name } already exists.", 'w')
            provider_arn = f'arn:aws:iam::{ self.AWS_ACCT }:oidc-provider/{ provider_name }'
        
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Federated": provider_arn
                    },
                    "Action": "sts:AssumeRoleWithWebIdentity",
                    "Condition": {
                        "StringEquals": {
                            f"{ provider_name }:aud": "sts.amazonaws.com"
                        },
                        "StringLike": {
                            f"{ provider_name }:sub": [
                                "repo:SapphireSystems/customer-onboarding:*",
                                "repo:SapphireSystems/ami-factory:*",
                                "repo:SapphireSystems/customer-onboarding-terraform*",
                                "repo:SapphireSystems/self-hosted-runner*"
                            ]
                        }
                    }
                }
            ]
        }
        
        try:
            boto3.client('iam').create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                MaxSessionDuration=14400
            )
            self.logger(f"Role { role_name } created successfully.", 'a')
        except boto3.client('iam').exceptions.EntityAlreadyExistsException:
            self.logger(f"Role { role_name } already exists.", 'w')
            boto3.client('iam').get_role(RoleName=role_name)

        try:
            boto3.client('iam').update_assume_role_policy(
                RoleName=role_name,
                PolicyDocument=json.dumps(trust_policy)
            )
            self.logger(f"Trust policy for role { role_name } updated successfully.", 'a')
        except (Exception) as e:
            self.logger(f"Error updating trust policy for role: {e}", 'e')
                
        try:
            boto3.client('iam').attach_role_policy(
                RoleName=role_name,
                PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess"
            )
            self.logger(f"Policy AdministratorAccess attached to role { role_name } successfully.", 'a')
        except (Exception) as e:
            self.logger(f"Error updating trust policy for role: { e }", 'e')

        # policy_name = "KMSPermissionsPolicy"

        # kms_policy = {
        #     "Version": "2012-10-17",
        #     "Statement": [
        #         {
        #             "Effect": "Allow",
        #             "Action": [
        #                 "kms:Create*",
        #                 "kms:Describe*",
        #                 "kms:Enable*",
        #                 "kms:List*",
        #                 "kms:Put*",
        #                 "kms:Update*",
        #                 "kms:Revoke*",
        #                 "kms:Disable*",
        #                 "kms:Get*",
        #                 "kms:Delete*",
        #                 "kms:TagResource",
        #                 "kms:UntagResource",
        #                 "kms:ScheduleKeyDeletion",
        #                 "kms:CancelKeyDeletion",
        #                 "kms:Encrypt",
        #                 "kms:Decrypt",
        #                 "kms:ReEncrypt*",
        #                 "kms:Generate*",
        #                 "ssm:Create*",
        #                 "ssm:Describe*",
        #                 "ssm:Put*",
        #                 "ssm:List*",
        #                 "ssm:Update*",
        #                 "ssm:Delete*",
        #                 "ssm:Get*"
        #             ],
        #             "Resource": "*"
        #         }
        #     ]
        # }

        # trust_policy = {
        #     "Version": "2012-10-17",
        #     "Statement": [
        #         {
        #             "Effect": "Allow",
        #             "Principal": {
        #                 "AWS": f"arn:aws:sts::{ self.AWS_ACCT }:assumed-role/github-oidc/actionsrolesession",
        #                 "Service": "ec2.amazonaws.com"
        #             },
        #             "Action": "sts:AssumeRole"
        #         }
        #     ]
        # }

        # policy_arn = None
        # paginator = boto3.client('iam').get_paginator('list_policies')
        # for page in paginator.paginate(Scope='All'):
        #     for policy in page['Policies']:
        #         if policy['PolicyName'] == policy_name:
        #             policy_arn = policy['Arn']
        #             self.logger(f"Policy { policy_name } already exists with ARN: { policy_arn }", 'e)

        # if policy_arn:
        #     try:
        #         boto3.client('iam').create_policy_version(
        #             PolicyArn=policy_arn,
        #             PolicyDocument=json.dumps(kms_policy),
        #             SetAsDefault=True
        #         )
        #         self.logger(f"Policy { policy_name } updated successfully with ARN: { policy_arn }", 'a)
        #     except (Exception) as e:
        #         if e.response['Error']['Code'] == 'LimitExceeded':
        #             try:
        #                 list_policy_response = boto3.client('iam').list_policy_versions(PolicyArn=policy_arn)
        #                 versions = list_policy_response['Versions']

        #                 for version in versions:
        #                     if not version['IsDefaultVersion']:
        #                         version_id = version['VersionId']
        #                         boto3.client('iam').delete_policy_version(PolicyArn=policy_arn, VersionId=version_id)
        #                         self.logger(f"Deleted policy version { version_id }", 'a)
        #             except (Exception) as e:
        #                 self.logger(f"Error creating new policy: { e }", 'e)
                        
        #             try: 
        #                 boto3.client('iam').create_policy_version(
        #                     PolicyArn=policy_arn,
        #                     PolicyDocument=json.dumps(kms_policy),
        #                     SetAsDefault=True
        #                 )
        #                 self.logger(f"Policy { policy_name } updated successfully with ARN: { policy_arn }"), 'a 
        #             except (Exception) as e:
        #                 self.logger(f"Error creating new policy: { e }", 'a)
        #         else:
        #             self.logger(f"Error updating policy: { e }", 'e)
        # else:
        #     try:
        #         create_policy_response = boto3.client('iam').create_policy(
        #             PolicyName=policy_name,
        #             PolicyDocument=json.dumps(kms_policy)
        #         )
        #         policy_arn = create_policy_response['Policy']['Arn']
        #         self.logger(f"Created new policy: { policy_arn }", 'a)
        #     except (Exception) as e:
        #         self.logger(f"Error creating new policy: { e }", 'e)

        # try:
        #     boto3.client('iam').attach_role_policy(
        #         RoleName=role_name,
        #         PolicyArn=policy_arn
        #     )
        #     self.logger(f"Policy { policy_name } attached to role { role_name } successfully.", 'a)
        # except (Exception) as e:
        #     self.logger(f"Error updating trust policy for role: { e }", 'e)

        # try:
        #     boto3.client('iam').update_assume_role_policy(
        #         RoleName=role_name,
        #         PolicyDocument=json.dumps(trust_policy)
        #     )
        #     self.logger(f"Trust policy for role { role_name } updated successfully.", 'a)
        # except (Exception) as e:
        #     self.logger(f"Error updating trust policy for role: {e}", 'e)

        try:
            boto3.client("s3", region_name=self.AWS_RGN).head_bucket(Bucket=f"{ self.AWS_ACCT }-{ self.AWS_ALIAS }-keypairs")
        except (Exception) as e:
            self.logger(f"{ e } \nBucket { self.AWS_ACCT }-{ self.AWS_ALIAS }-keypairs does not exist.", 'e')

            try:
                boto3.client('s3').create_bucket(
                    Bucket=f"{ self.AWS_ACCT }-{ self.AWS_ALIAS }-keypairs", 
                    CreateBucketConfiguration={ 'LocationConstraint': self.AWS_RGN }
                )
                self.logger(f"Bucket { self.AWS_ACCT }-{ self.AWS_ALIAS }-keypairs created successfully.", 'a')
            except (Exception) as e:
                self.logger(f"{ e } \nError creating bucket: { self.AWS_ACCT }-{ self.AWS_ALIAS }-keypairs", 'e')
                self.end(1)

            private_key_file, public_key_file = self.generate_keypairs()
            self.upload_keypairs(private_key_file, public_key_file)

        self.logger(f"Bucket { self.AWS_ACCT }-{ self.AWS_ALIAS }-keypairs already exists. Checking contents...", 'a')

        if len(self.bucket_objects('check')) == 2:
            self.logger(f"Bucket objects already exists. Skipping create keypairs...", 'a')
        else:
            private_key_file, public_key_file = self.generate_keypairs()
            self.upload_keypairs(private_key_file, public_key_file)

        self.end(0)

    def bucket_objects(self, action):
        try:
            response = boto3.client('s3').list_objects_v2(Bucket=f"{ self.AWS_ACCT }-{ self.AWS_ALIAS }-keypairs")
        except (Exception) as e:
            self.logger(f"No objects found in bucket: { e }", 'e')
        
        if 'Contents' in response:
            objects = [{'Key': obj['Key']} for obj in response['Contents']]

            if action == 'check':
                self.logger(objects, 'a')
                return objects

            if action == 'delete':
                boto3.client('s3').delete_objects(
                    Bucket=f"{ self.AWS_ACCT }-{ self.AWS_ALIAS }-keypairs", 
                    Delete={ 'Objects': objects }
                )
                self.logger(f"All objects deleted from bucket { self.AWS_ACCT }-{ self.AWS_ALIAS }-keypairs.", 'a')
        else:
            self.logger(f"Bucket { self.AWS_ACCT }-{ self.AWS_ALIAS }-keypairs is already empty.", 'a')

    def generate_keypairs(self):
            try:
                boto3.client('ec2', region_name=self.AWS_RGN).delete_key_pair(KeyName=self.AWS_ALIAS)
                self.logger(f"Key Pair { self.AWS_ALIAS } deleted successfully.", 'a')
            except (Exception) as e:
                self.logger(f"Error deleting the key pair: { e }", 'e')
                self.end(1)

            key_bits = 2048
            key_path = Path.home().joinpath('.ssh')

            if not os.path.exists(key_path):
                self.logger(f"Creating... { key_path }", 'a')
                key_path.mkdir(parents=True, exist_ok=True)
                os.chmod(key_path, 0o700)
            
            private_key_file = key_path.joinpath(f"{ self.AWS_ALIAS }.ppk")
            public_key_file = key_path.joinpath(f"{ self.AWS_ALIAS }.pub")

            os.path.exists(private_key_file) and os.remove(private_key_file)
            os.path.exists(public_key_file) and os.remove(public_key_file)

            private_key = paramiko.RSAKey.generate(key_bits)
            public_key = f"{ private_key.get_name() } { private_key.get_base64() }"

            private_key.write_private_key_file(private_key_file)
            with open(public_key_file, 'w') as pub_file:
                pub_file.write(public_key)

            self.logger(f"Private key saved to: { private_key_file }", 'a')
            self.logger(f"Public key saved to: { public_key_file }", 'a')

            return private_key_file, public_key_file
    
    def upload_keypairs(self, private_key_file, public_key_file):
        try:
            boto3.client('s3').upload_file(private_key_file, f"{ self.AWS_ACCT }-{ self.AWS_ALIAS }-keypairs", f"{ self.AWS_ALIAS }.ppk")
            self.logger(f"Private key: { private_key_file } uploaded successfully.", 'a')
            boto3.client('s3').upload_file(public_key_file, f"{ self.AWS_ACCT }-{ self.AWS_ALIAS }-keypairs", f"{ self.AWS_ALIAS }.pub")
            self.logger(f"Public key: { public_key_file } uploaded successfully.", 'a')
        except (Exception) as e:
            self.bucket_objects('delete')

            self.logger(f"Deleting local key files: { private_key_file }, { public_key_file }", 'a')
            os.path.exists(private_key_file) and os.remove(private_key_file)
            os.path.exists(public_key_file) and os.remove(public_key_file)

            try:
                boto3.client('s3').delete_bucket(Bucket=f"{ self.AWS_ACCT }-{ self.AWS_ALIAS }-keypairs")
                self.logger(f"Bucket { self.AWS_ACCT }-{ self.AWS_ALIAS }-keypairs deleted successfully.", 'a')
            except (Exception) as e:
                self.logger(f"Error deleting bucket: { e }", 'e')
                self.end(1)

            self.logger(f"Upload to S3 bucket { self.AWS_ACCT }-{ self.AWS_ALIAS }-keypairs failed.", 'e')
            self.end(1)

        try:
            with open(public_key_file, 'r') as file:
                public_key = file.read()

            response = boto3.client('ec2', region_name=self.AWS_RGN).import_key_pair(
                KeyName=self.AWS_ALIAS,
                PublicKeyMaterial=public_key
            )
        except (Exception) as e:
            self.logger(f"Error importing the key pair: { e }", 'e')
            self.end(1)
        else:
            self.logger(f"Key Pair { self.AWS_ALIAS } imported successfully.", 'a')
            self.logger(f"Key Pair ID: { response['KeyPairId'] }", 'a')

        self.end(0)

    def end(self, exit_code):
        if exit_code == 0:
            banner = 'Setting up environment'
            message = 'D O N E !!!'
        else:
            banner = 'No servers to provision'
            message = f"Exited with non-zero error status ({ exit_code })."

        self.logger(f'\n{"-":>12}----------------------------------', 'b')
        self.logger(f'{"-":>17} { banner } -', 'b')
        self.logger(f'{"-":>12}----------------------------------\n', 'b')

        for item in self.EXPORTED:
            os.environ[item] = self.VARS[self.EXPORTED.index(item)]
        
        for i in range(len(self.VARS)):
            self.logger(f"{self.EXPORTED[i]:>25}: {self.VARS[i]}", 'b')

        self.logger(f'\n{"-":>12}----------------------------------', 'b')
        self.logger(f'\n{ message }', 'b')

        self.logger('\n...Closing application', 'b')
        for i in range(5, 0, -1):
            self.logger(f'... { i }', 'b')
            time.sleep(1)

        time.sleep(1)
        os._exit(exit_code)

    def set_hostname(self):
        if int(self.DC_COUNT) != 0:
            self.DC_LIST.append(self.dcHostnameLineEdit1.text())
            if int(self.DC_COUNT) > 1:
                self.DC_LIST.append(self.dcHostnameLineEdit2.text())

        if int(self.HANA_COUNT) != 0:
            self.HANA_LIST.append(self.hanaHostnameLineEdit.text())
            # if int(self.HANA_COUNT) > 1:
            #     self.HANA_LIST.append(self.hanaHostnameLineEdit2.text())

        if int(self.WIN_COUNT) != 0:
            if self.WIN1_BOX == "HANA Management":
                self.HANAMGMT_LIST.append(self.winHostnameLineEdit1.text())
            if self.WIN1_BOX == "Integration Server":
                self.IS_LIST.append(self.winHostnameLineEdit1.text())
            if self.WIN1_BOX == "RDS":
                self.RDS_LIST.append(self.winHostnameLineEdit1.text())
            if self.WIN1_BOX == "Citrix":
                self.CITRIX_LIST.append(self.winHostnameLineEdit1.text())
            if self.WIN1_BOX == "SQL":
                self.SQL_LIST.append(self.winHostnameLineEdit1.text())
            if int(self.WIN_COUNT) > 1:
                if self.WIN2_BOX == "HANA Management":
                    self.HANAMGMT_LIST.append(self.winHostnameLineEdit2.text())
                if self.WIN2_BOX == "Integration Server":
                    self.IS_LIST.append(self.winHostnameLineEdit2.text())
                if self.WIN2_BOX == "RDS":
                    self.RDS_LIST.append(self.winHostnameLineEdit2.text())
                if self.WIN2_BOX == "Citrix":
                    self.CITRIX_LIST.append(self.winHostnameLineEdit2.text())
                if self.WIN2_BOX == "SQL":
                    self.SQL_LIST.append(self.winHostnameLineEdit2.text())
                if int(self.WIN_COUNT) > 2:
                    if self.WIN3_BOX == "HANA Management":
                        self.HANAMGMT_LIST.append(self.winHostnameLineEdit3.text())
                    if self.WIN3_BOX == "Integration Server":
                        self.IS_LIST.append(self.winHostnameLineEdit3.text())
                    if self.WIN3_BOX == "RDS":
                        self.RDS_LIST.append(self.winHostnameLineEdit3.text())
                    if self.WIN3_BOX == "Citrix":
                        self.CITRIX_LIST.append(self.winHostnameLineEdit3.text())
                    if self.WIN3_BOX == "SQL":
                        self.SQL_LIST.append(self.winHostnameLineEdit3.text())
                    if int(self.WIN_COUNT) > 3:
                        if self.WIN4_BOX == "HANA Management":
                            self.HANAMGMT_LIST.append(self.winHostnameLineEdit4.text())
                        if self.WIN4_BOX == "Integration Server":
                            self.IS_LIST.append(self.winHostnameLineEdit4.text())
                        if self.WIN4_BOX == "RDS":
                            self.RDS_LIST.append(self.winHostnameLineEdit4.text())
                        if self.WIN4_BOX == "Citrix":
                            self.CITRIX_LIST.append(self.winHostnameLineEdit4.text())
                        if self.WIN4_BOX == "SQL":
                            self.SQL_LIST.append(self.winHostnameLineEdit4.text())
                        if int(self.WIN_COUNT) > 4:
                            if self.WIN5_BOX == "HANA Management":
                                self.HANAMGMT_LIST.append(self.winHostnameLineEdit5.text())
                            if self.WIN5_BOX == "Integration Server":
                                self.IS_LIST.append(self.winHostnameLineEdit5.text())
                            if self.WIN5_BOX == "RDS":
                                self.RDS_LIST.append(self.winHostnameLineEdit5.text())
                            if self.WIN5_BOX == "Citrix":
                                self.CITRIX_LIST.append(self.winHostnameLineEdit5.text())
                            if self.WIN5_BOX == "SQL":
                                self.SQL_LIST.append(self.winHostnameLineEdit5.text())
                            if int(self.WIN_COUNT) > 5:
                                if self.WIN6_BOX == "HANA Management":
                                    self.HANAMGMT_LIST.append(self.winHostnameLineEdit6.text())
                                if self.WIN6_BOX == "Integration Server":
                                    self.IS_LIST.append(self.winHostnameLineEdit6.text())
                                if self.WIN6_BOX == "RDS":
                                    self.RDS_LIST.append(self.winHostnameLineEdit6.text())
                                if self.WIN6_BOX == "Citrix":
                                    self.CITRIX_LIST.append(self.winHostnameLineEdit6.text())
                                if self.WIN6_BOX == "SQL":
                                    self.SQL_LIST.append(self.winHostnameLineEdit6.text())

    def set_wintype_list(self):
        if int(self.WIN_COUNT) != 0:
            if self.WIN1_BOX == "HANA Management":
                self.HANAMGMT_TYPE_LIST.append(self.WIN1_TYPE)
            if self.WIN1_BOX == "Integration Server":
                self.IS_TYPE_LIST.append(self.WIN1_TYPE)
            if self.WIN1_BOX == "RDS":
                self.RDS_TYPE_LIST.append(self.WIN1_TYPE)
            if self.WIN1_BOX == "Citrix":
                self.CITRIX_TYPE_LIST.append(self.WIN1_TYPE)
            if self.WIN1_BOX == "SQL":
                self.SQL_TYPE_LIST.append(self.WIN1_TYPE)
            if int(self.WIN_COUNT) > 1:
                if self.WIN2_BOX == "HANA Management":
                    self.HANAMGMT_TYPE_LIST.append(self.WIN2_TYPE)
                if self.WIN2_BOX == "Integration Server":
                    self.IS_TYPE_LIST.append(self.WIN2_TYPE)
                if self.WIN2_BOX == "RDS":
                    self.RDS_TYPE_LIST.append(self.WIN2_TYPE)
                if self.WIN2_BOX == "Citrix":
                    self.CITRIX_TYPE_LIST.append(self.WIN2_TYPE)
                if self.WIN2_BOX == "SQL":
                    self.SQL_TYPE_LIST.append(self.WIN2_TYPE)
                if int(self.WIN_COUNT) > 2:
                    if self.WIN3_BOX == "HANA Management":
                        self.HANAMGMT_TYPE_LIST.append(self.WIN3_TYPE)
                    if self.WIN3_BOX == "Integration Server":
                        self.IS_TYPE_LIST.append(self.WIN3_TYPE)
                    if self.WIN3_BOX == "RDS":
                        self.RDS_TYPE_LIST.append(self.WIN3_TYPE)
                    if self.WIN3_BOX == "Citrix":
                        self.CITRIX_TYPE_LIST.append(self.WIN3_TYPE)
                    if self.WIN3_BOX == "SQL":
                        self.SQL_TYPE_LIST.append(self.WIN3_TYPE)
                    if int(self.WIN_COUNT) > 3:
                        if self.WIN4_BOX == "HANA Management":
                            self.HANAMGMT_TYPE_LIST.append(self.WIN4_TYPE)
                        if self.WIN4_BOX == "Integration Server":
                            self.IS_TYPE_LIST.append(self.WIN4_TYPE)
                        if self.WIN4_BOX == "RDS":
                            self.RDS_TYPE_LIST.append(self.WIN4_TYPE)
                        if self.WIN4_BOX == "Citrix":
                            self.CITRIX_TYPE_LIST.append(self.WIN4_TYPE)
                        if self.WIN4_BOX == "SQL":
                            self.SQL_TYPE_LIST.append(self.WIN4_TYPE)
                        if int(self.WIN_COUNT) > 4:
                            if self.WIN5_BOX == "HANA Management":
                                self.HANAMGMT_TYPE_LIST.append(self.WIN5_TYPE)
                            if self.WIN5_BOX == "Integration Server":
                                self.IS_TYPE_LIST.append(self.WIN5_TYPE)
                            if self.WIN5_BOX == "RDS":
                                self.RDS_TYPE_LIST.append(self.WIN5_TYPE)
                            if self.WIN5_BOX == "Citrix":
                                self.CITRIX_TYPE_LIST.append(self.WIN5_TYPE)
                            if self.WIN5_BOX == "SQL":
                                self.SQL_TYPE_LIST.append(self.WIN5_TYPE)
                            if int(self.WIN_COUNT) > 5:
                                if self.WIN6_BOX == "HANA Management":
                                    self.HANAMGMT_TYPE_LIST.append(self.WIN6_TYPE)
                                if self.WIN6_BOX == "Integration Server":
                                    self.IS_TYPE_LIST.append(self.WIN6_TYPE)
                                if self.WIN6_BOX == "RDS":
                                    self.RDS_TYPE_LIST.append(self.WIN6_TYPE)
                                if self.WIN6_BOX == "Citrix":
                                    self.CITRIX_TYPE_LIST.append(self.WIN6_TYPE)
                                if self.WIN6_BOX == "SQL":
                                    self.SQL_TYPE_LIST.append(self.WIN6_TYPE)

    def copy_file(self, src, dest):
        try:
            shutil.copy(src, dest)
            self.logger(f"Copied { src } to { dest }", 'a')
        except (Exception) as e:
            self.logger(f"Failed to copy { src }: {e}", 'e')

    def logger(self, msg, action):
        if action == 'a':
            self.consoleLog.append(f'\t>> { msg }')
        elif action == 't':
            self.consoleLog.append(f'[*] - { msg }\n')
        elif action == 'w':
            self.consoleLog.append(f'[WARN] - { msg }')
        elif action == 'e':
            self.consoleLog.append(f'[ERR] - { msg }')
        elif action == 'b':
            self.consoleLog.append(msg)
        else:
            self.consoleLog.setText(msg)

        QApplication.processEvents()    # Forces the UI to update

    def error(self, msg, type, parent=None):
        _errorMsg = QMessageBox(parent)
        _errorMsg.setWindowIcon(QIcon('./img/icon.ico'))
        _errorMsg.setWindowTitle('Error !' if type == 'error' else 'Validation Error !')
        _errorMsg.setIcon(QMessageBox.Critical if type == 'error' else QMessageBox.Warning)
        # _errorMsg.setInformativeText(f'<p style=\'text-align: center\'>{ '[ERROR]: ' if type == 'error' else '[VALIDATION ERROR]: <br>' }{ msg }</p>')
        error_prefix = '[ERROR]: ' if type == 'error' else '[VALIDATION ERROR]: <br>'
        _errorMsg.setInformativeText(f'<p style="text-align: center">{error_prefix}{msg}</p>')
        # _errorMsg.setStandardButtons(QMessageBox.text('Okay'))
        # _errorMsg.setDefaultButton(QMessageBox::Ok)
        _errorMsg.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        # center error box
        box_geometry = _errorMsg.geometry()
        x = (screen_geometry.width() - box_geometry.width()) * 0.4
        y = (screen_geometry.height() - box_geometry.height()) * 0.4
        _errorMsg.move(int(x), int(y))
        _errorMsg.exec()

        self.end(1) if type == 'error' else _errorMsg.closeEvent


if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()
    ui = GenerateTemplate()
    # center window
    screen = app.primaryScreen()
    screen_geometry = screen.geometry()
    window_geometry = window.geometry()
    x = (screen_geometry.width() - window_geometry.width()) * 0.5
    y = (screen_geometry.height() - window_geometry.height()) * 0.5
    window.move(int(x), int(y))
    ui.setupUi(window)
    window.show()
    app.exec()
    