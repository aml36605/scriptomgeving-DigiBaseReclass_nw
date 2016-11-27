import sys
import time
import datetime
import os
import wmi
from os.path import join, expanduser
from ui_files import pyMainWindow
from PySide.QtCore import *
from PySide.QtGui import *
from py_files.convert import *
from py_files.pySQL import *


DB_PATH = "C:\\users\\aml36\\Desktop\\digibasereclass.db"


        # TODO: imports
        #       win32 importeren in venv

        # TODO: general
        # create QTablewidget button frame

class Window(QMainWindow, pyMainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        self.create_case()

        self.leFilePath.setText(expanduser('~\\DigiBaseReclass_Zaken\\'))

        self.stackedWidget.setCurrentIndex(0)
        self.lblCasedetails.setText('case details')
        self.tbGoTo.setText('go to evidence sources')
        self.tbGoTo.clicked.connect(self.evidence_sources)

        self.tbProcessing.clicked.connect(self.processing_details)
        self.tbCaseDetails.clicked.connect(self.case_details)
        self.tbAddKeywordToSearch.clicked.connect(self.add_keywords_to_search)
        self.tbAddKey.clicked.connect(self.add_keywords_to_search)
        self.tbAddHash.clicked.connect(self.add_hash_to_Search)
        self.tbAddHashFilesToSearch.clicked.connect(self.add_hash_to_Search)
        self.tbIgnoreFolders.clicked.connect(self.ignore_folders)
        self.tbIgnoreFolders_2.clicked.connect(self.ignore_folders)
        self.tbEvidenceSources.clicked.connect(self.evidence_sources)
        self.tbLoad.clicked.connect(self.load_evidence)
        self.tbLoadEvidence.clicked.connect(self.load_evidence)
        #self.tbBrowsePath.clicked.connect(self.create_filepath)
        self.tbAcquire.clicked.connect(self.select_device)
        self.tbAcquireEvidence.clicked.connect(self.select_device)
        self.createWMI()

    def case_details(self):
        self.stackedWidget.setCurrentIndex(0)
        self.lblCasedetails.setText('case details')
        self.tbGoTo.setText('go to evidence sources')
        #self.tbGoTo.clicked.connect(self.create_case_db)
        self.tbGoTo.clicked.connect(self.evidence_sources)
        self.stackedWidget.show()

    def load_evidence(self):
        self.stackedWidget.setCurrentIndex(1)
        self.lblCasedetails.setText('load evidence')
        self.lblSelect_devices.setText('select device')
        self.lblLoadEvidence.setText('select an evidence source')
        self.tbGoTo.setText('go to processing details')
        self.tbGoTo.clicked.connect(self.processing_details)
        self.stackedWidget.show()

    def add_keywords_to_search(self):
        self.stackedWidget.setCurrentIndex(2)
        self.lblCasedetails.setText('add keywords to search')
        self.tbGoTo.setText('go to add hash files')
        self.tbGoTo.clicked.connect(self.add_hash_to_Search)
        self.stackedWidget.show()

    def processing_details(self):
        self.stackedWidget.setCurrentIndex(3)
        self.lblCasedetails.setText('processing details')
        self.tbGoTo.setText('go to analyze evidence')
        #self.tbGoTo.clicked.connect(self.analyze_evidence)
        self.stackedWidget.show()

    def add_hash_to_Search(self):
        self.stackedWidget.setCurrentIndex(4)
        self.lblCasedetails.setText('add hash files to search')
        self.tbGoTo.setText('go to ignore folder(s)')
        self.tbGoTo.clicked.connect(self.ignore_folders)
        self.stackedWidget.show()

    def ignore_folders(self):
        self.stackedWidget.setCurrentIndex(5)
        self.lblCasedetails.setText('ignore folders to search')
        self.tbGoTo.setText('go to analyze evidence')
        # self.tbGoTo.clicked.connect(self.analyze_evidence)
        self.stackedWidget.show()

    def evidence_sources(self):
        self.stackedWidget.setCurrentIndex(6)
        self.lblCasedetails.setText('evidence sources')
        self.tbGoTo.setText('go to processing details')
        self.tbGoTo.clicked.connect(self.processing_details)
        self.stackedWidget.show()

    def select_device(self):
        self.stackedWidget.setCurrentIndex(7)
        self.lblCasedetails.setText('acquire evidence')
        self.lblSelect_devices.setText('select device')
        self.tbGoTo.setText('go to load evidence')
        self.tbGoTo.clicked.connect(self.load_evidence)
        self.stackedWidget.show()

    def create_case(self):

        # verify casefolder
        casePath = expanduser("~\\DigiBaseReclass_Zaken\\")

        if not os.path.exists(casePath):
            try:
                os.makedirs(casePath)
            except ValueError:
                dialog = QFileDialog()
                dialog.setFileMode(QFileDialog.Directory)
                dialog.setOption(QFileDialog.ShowDirsOnly)
                dir = dialog.getExistingDirectory(self, 'Kies map', QFileDialog.ShowDirsOnly)

                filepath = self.leFilePath.text()



        self.leCaseName.textChanged[str].connect(self.onChanged)

    def onChanged(self):
        filepath = self.leFilePath.text()

        text = self.leCaseName.text()
        filepath = filepath + text
        self.leFilePath.setText(filepath)




    def createWMI(self):
        # Connect to sqlite
        dbConn = digiBaseReclassConnect(DB_PATH)
        self.dbCursor = dbConn.cursor()
        checkTable(dbConn, 'devices')
        digiBaseReclassDropTable(dbConn, 'devices')
        digiBaseReclassAddtable(dbConn, 'devices')
        checkTable(dbConn, 'currentdevice')
        digiBaseReclassAddtable(dbConn, 'currentdevice')

        # Create WMI objects
        c = wmi.WMI()
        # loop trough objects
        for physical_disk in c.Win32_DiskDrive():
            for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
                for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                    disk_model = physical_disk.model
                    drive_letter = logical_disk.Caption + "\\"
                    drive_volume_name = logical_disk.VolumeName
                    p_drive = physical_disk.DeviceID
                    part_count = physical_disk.partitions
                    p_disk_sn = physical_disk.Serialnumber
                    p_disk_size = convert_bytes(physical_disk.size)
                    interface = physical_disk.interfacetype

                    # fill devices as dictionairy

                    devices = [drive_letter, drive_volume_name, p_disk_size, p_disk_sn, p_drive, disk_model, interface,
                                    part_count]

                    # insert dictionary in indigodevices_temp table
                    digiBaseReclassInsertTable(dbConn, 'devices', devices)

        self.dbCursor.execute("""SELECT * FROM devices ORDER BY driveletter ASC""")
        allRows = self.dbCursor.fetchall()
        print(allRows)

        # self.twSelectDevices.setHorizontalHeaderLabels(
        #     str("Schijfletter:;Volume naam:;Grootte:;Serienummer:;Fysieke schijf:;Merk:;Type:;Aantal partities:;Akties:; Toevoegen aan Zaak").split(";"))
        self.twSelectDevices.verticalHeader().setVisible(False)
        self.twSelectDevices.horizontalHeader().setVisible(False)
        self.twSelectDevices.resizeColumnsToContents()

        for row in allRows:
            inx = allRows.index(row)
            self.twSelectDevices.insertRow(inx)
            self.twSelectDevices.setItem(inx, 0, QTableWidgetItem(row[0]))

            self.twSelectDevices.setColumnWidth(0, 90)
            self.twSelectDevices.setItem(inx, 1, QTableWidgetItem(row[1]))
            self.twSelectDevices.setColumnWidth(1, 150)
            self.twSelectDevices.setItem(inx, 2, QTableWidgetItem(row[2]))
            self.twSelectDevices.setColumnWidth(2, 150)
            self.twSelectDevices.setItem(inx, 3, QTableWidgetItem(row[3]))
            self.twSelectDevices.setColumnWidth(3, 170)
            self.twSelectDevices.setItem(inx, 4, QTableWidgetItem(row[4]))
            self.twSelectDevices.setColumnWidth(4, 170)
            self.twSelectDevices.setItem(inx, 5, QTableWidgetItem(row[5]))
            self.twSelectDevices.setColumnWidth(5, 250)
            self.twSelectDevices.setItem(inx, 6, QTableWidgetItem(row[6]))
            self.twSelectDevices.setColumnWidth(6, 60)
            self.twSelectDevices.setItem(inx, 7, QTableWidgetItem(row[7]))
            self.twSelectDevices.setColumnWidth(7, 120)
            # add label and combo to qtablewidget
            combolabel = QLabel()
            combolabel.setText('Image type:')
            self.twSelectDevices.setCellWidget(inx, 8, combolabel)
            combo = QComboBox()
            combo.addItem('keyword search')
            combo.addItem('crc_hash search')
            combo.addItem('md5_hash search')
            combo.addItem('keyword_crc_hash search')
            combo.addItem('keyword_md5_hash search')
            combo.addItem('full search')
            self.twSelectDevices.setCellWidget(inx, 9, combo)
            # add button
            button = QToolButton()
            button.setStyleSheet('margin-left: 10px; text-transform: uppercase; font: 10pt "Arial Rounded MT Bold";border-style: solid;border-width: 2px;	color: rgb(0,102,255)')
            button.setText('add to case')

            self.twSelectDevices.setCellWidget(inx, 10, button)
            button.clicked.connect(self.handleButtonClicked)
            self.twSelectDevices.resizeRowsToContents()
            self.twSelectDevices.resizeColumnsToContents()



    def handleButtonClicked(self):

        dbConn = digiBaseReclassConnect(DB_PATH)
        cursor = dbConn.cursor()
        # catch button signal and position
        button = self.sender()
        index = self.twSelectDevices.indexAt(button.pos())
        # verify index
        if index.isValid():
            row = index.row()
        # catch combobox current displayed item
        drl = self.twSelectDevices.item(row,0)
        voln = self.twSelectDevices.item(row,1)
        size = self.twSelectDevices.item(row,2)
        sn = self.twSelectDevices.item(row,3)
        fd = self.twSelectDevices.item(row,4)
        ven = self.twSelectDevices.item(row,5)
        type = self.twSelectDevices.item(row,6)
        pcount = self.twSelectDevices.item(row,7)
        image_optie = self.twSelectDevices.cellWidget(row,9)

        # TODO: add to case button
        # insert sql voor selected case in current_devices
        # qtablewidget remove row
        # call sources_to_process()


        currentdevice = [drl.text(), voln.text(), size.text(), sn.text(), fd.text(), ven.text(), type.text(), pcount.text(), image_optie.currentText()]
        print(currentdevice)
        if checkTable(dbConn, 'currentdevice') == False:
            digiBaseReclassAddtable(dbConn, 'currentdevice')

        digiBaseReclassInsertTable(dbConn, 'currentdevice', currentdevice)
        self.twSelectDevices.removeRow(row)
        self.sources_to_process()

    def sources_to_process(self):

        # TODO: sources_to_process
        # fill qtablewidget with current_devices
        # from table current_devices

        dbConn = digiBaseReclassConnect(DB_PATH)
        self.dbCursor.execute("""SELECT * FROM currentdevice ORDER BY driveletter ASC""")
        allRows = self.dbCursor.fetchall()
        self.twSources.verticalHeader().setVisible(False)
        self.twSources.horizontalHeader().setVisible(False)
        self.twSources.resizeColumnsToContents()

        for row in allRows:
            inx = allRows.index(row)
            self.twSources.insertRow(inx)
            self.twSources.setItem(inx, 0, QTableWidgetItem(row[0]))

            self.twSources.setColumnWidth(0, 90)
            self.twSources.setItem(inx, 1, QTableWidgetItem(row[1]))
            self.twSources.setColumnWidth(1, 150)
            self.twSources.setItem(inx, 2, QTableWidgetItem(row[2]))
            self.twSources.setColumnWidth(2, 150)
            self.twSources.setItem(inx, 3, QTableWidgetItem(row[3]))
            self.twSources.setColumnWidth(3, 170)
            self.twSources.setItem(inx, 4, QTableWidgetItem(row[4]))
            self.twSources.setColumnWidth(4, 170)
            self.twSources.setItem(inx, 5, QTableWidgetItem(row[5]))
            self.twSources.setColumnWidth(5, 250)
            self.twSources.setItem(inx, 6, QTableWidgetItem(row[6]))
            self.twSources.setColumnWidth(6, 60)
            self.twSources.setItem(inx, 7, QTableWidgetItem(row[7]))
            self.twSources.setColumnWidth(7, 120)
            # add button
            trash = QToolButton()
            trash.setStyleSheet(
                'margin-left: 10px; text-transform: uppercase; font: 10pt "Arial Rounded MT Bold";border-style: solid;border-width: 2px;	color: rgb(0,102,255)')
            trash.setText('trashcan')

            self.twSources.setCellWidget(inx, 8, trash)
            trash.clicked.connect(self.del_sources_to_process)
            self.twSources.resizeRowsToContents()
            self.twSources.resizeColumnsToContents()


    def del_sources_to_process(self):
        pass
        # TODO: del_sources_to_process
        # del row from qtablewidget -- trashcan
        # refresh createWMI







def conv_to_epoch():
    now = datetime.datetime.now()
    # convert date/time to epoch
    date_time = now.strftime("%d.%m.%Y %H:%M:%S")
    pattern = '%d.%m.%Y %H:%M:%S'
    epoch = int(time.mktime(time.strptime(date_time, pattern)))
    return str(epoch)


    # TODO: main
    # create splashscreen
    # at startup verify :
    #     - create local folder cases
    #     - create db in local folder if not exists
    #     - call createWMI()
    #

def main():
    QCoreApplication.setApplicationName("DigiBaseReclass")
    QCoreApplication.setApplicationVersion("0.1")
    QCoreApplication.setOrganizationName("DigiBaseReclass")
    QCoreApplication.setOrganizationDomain("DigiBaseReclass.com")


    app = QApplication(sys.argv)

    # Create en show splashscreen
    file_name = "DigiBaseReclass_logo.png"
    path = os.path.abspath(os.path.join("resources", file_name))
    splash_pic = QPixmap(path)
    splash = QSplashScreen(splash_pic, Qt.WindowStaysOnTopHint)
    # adding progressbar
    progressBar = QProgressBar(splash)
    # time.sleep(1)
    progressBar.setGeometry(0, 103, 1100, 7)
    splash.setMask(splash_pic.mask())
    splash.show()

    for i in range(0, 100):
        progressBar.setValue(i)
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()

    form = Window()
    form.showMaximized()
    splash.finish(form)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
