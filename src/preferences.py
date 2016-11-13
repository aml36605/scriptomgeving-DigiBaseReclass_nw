from PySide.QtCore import *
from PySide.QtGui import *
from src.iniConfig import *
from view.py_files import pyPreferences
from configparser import ConfigParser
import os


appDataPath = AppPath()
appDataPathRes = AppPathRes(appDataPath)
inifile = AppPathIni(appDataPath)


class Preferences(QDialog, pyPreferences.Ui_Dialog):


    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)
        self.setupUi(self)

        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "DigiBaseReclass", "DigiBaseReclass")

        self.btnAddOpslaglokatieZaken.clicked.connect(self.showDialog)

        # instantiate
        config = ConfigParser()


        # parse existing file
        config.read(inifile)
        self.leOpslaglokatieZaken.setText(os.path.abspath(config.get("General", "zaakmap")))
        self.leOpslaglokatieCRC.setText(os.path.abspath(config.get('General','crchash')))
        self.leOpslaglokatieMD5.setText(os.path.abspath(config.get('General', 'MD5hash')))
        self.leOpslaglokatieKeywords.setText(os.path.abspath(config.get('General', 'Keyword')))
        self.leOpslaglokatieIncludes.setText(os.path.abspath(config.get('General', 'Includes')))
        self.leOpslaglokatieExludes.setText(os.path.abspath(config.get('General', 'Excludes')))


    def showDialog(self):

        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly)

        dir = dialog.getExistingDirectory(self, 'Kies map', os.path.curdir)

        self.zaak = self.leOpslaglokatieZaken.setText(dir)
        self.zaakmap = os.path.abspath(self.leOpslaglokatieZaken.text())
        self.settings.setValue("zaakmap", self.zaakmap)

    def CasePath(inifile): # Path according to inifile "zaakmap"
        # instantiate
        config = ConfigParser()
        config.read(inifile)

        casePath = os.path.abspath(config.get('General','zaakmap'))

        return casePath

    def CRChashPath(inifile):
         # instantiate
        config = ConfigParser()
        config.read(inifile)

        crchashPath = os.path.abspath(config.get('General','crchash'))

        return crchashPath

    def MD5hashPath(inifile):
        # instantiate
        config = ConfigParser()
        config.read(inifile)

        md5hashPath = os.path.abspath(config.get('General','MD5hash'))

        return md5hashPath

    def KeyWordPath(inifile):
             # instantiate
        config = ConfigParser()
        config.read(inifile)

        keywordPath = os.path.abspath(config.get('General','keyword'))

        return keywordPath

    def IncludesPath(inifile):
             # instantiate
        config = ConfigParser()
        config.read(inifile)

        includesPath = os.path.abspath(config.get('General','Includes'))

        return includesPath

    def ExcludesPath(inifile):
             # instantiate
        config = ConfigParser()
        config.read(inifile)

        excludesPath = os.path.abspath(config.get('General','Excludes'))

        return excludesPath