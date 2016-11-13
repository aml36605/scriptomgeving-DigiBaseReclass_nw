from PySide.QtCore import *
from PySide.QtGui import *
from configparser import ConfigParser
import os

       

def AppPath():
    appDataPath = os.environ['APPDATA'] + "\\DigiBaseReclass\\"

    if not os.path.exists(appDataPath):
        try:
            os.makedirs(appDataPath)
        except ValueError:
            appDataPath = os.getcwd()

    return appDataPath

def AppPathRes(appDataPath):

    appDataPathRes = appDataPath + "Resources"

    if not os.path.exists(appDataPathRes):
        try:
            os.makedirs(appDataPath  + "Resources")
        except ValueError:
            AppPathRes = os.getcwd()


    appDataPathResCrc = appDataPathRes + "\\crchash\\"

    if not os.path.exists(appDataPathResCrc):
        try:
            os.makedirs(appDataPathResCrc)
        except ValueError:
            AppPathRes = os.getcwd()

    appDataPathResMD5 = appDataPathRes + "\\MD5hash\\"

    if not os.path.exists(appDataPathResMD5):
        try:
            os.makedirs(appDataPathResMD5)
        except ValueError:
            AppPathRes = os.getcwd()

    appDataPathResKeyword = appDataPathRes + "\\keyword\\"

    if not os.path.exists(appDataPathResKeyword):
        try:
            os.makedirs(appDataPathResKeyword)
        except ValueError:
            AppPathRes = os.getcwd()

    appDataPathResIncl = appDataPathRes + "\\includes\\"

    if not os.path.exists(appDataPathResIncl):
        try:
            os.makedirs(appDataPathResIncl)
        except ValueError:
            AppPathRes = os.getcwd()


    appDataPathResExcl = appDataPathRes + "\\excludes\\"

    if not os.path.exists(appDataPathResExcl):
        try:
            os.makedirs(appDataPathResExcl)
        except ValueError:
            AppPathRes = os.getcwd()

    return appDataPathRes, appDataPathResCrc, appDataPathResMD5, appDataPathResKeyword, appDataPathResIncl, appDataPathResExcl


def AppPathIni(appDataPath):

    pathVar  = AppPathRes(appDataPath)
    appDataPathIni = appDataPath + "\\DigiBaseReclass.ini"

    # create ini locations if not exsists
    if not os.path.exists(appDataPathIni):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "DigiBaseReclass", "DigiBaseReclass")
        settings.setPath(QSettings.IniFormat, QSettings.UserScope, os.path.abspath(appDataPathIni))
        settings.setValue("zaakmap", "")
        settings.setValue("crchash", pathVar[1])
        settings.setValue("MD5hash", pathVar[2])
        settings.setValue("keyword", pathVar[3])
        settings.setValue("Includes", pathVar[4])
        settings.setValue("Excludes", pathVar[5])

    return appDataPathIni

