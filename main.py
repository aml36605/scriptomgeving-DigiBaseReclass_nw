import sys
import os
from os.path import join, expanduser
from ui_files import pyMainWindow
from PySide.QtCore import *
from PySide.QtGui import *
from py_files.convert import *
from py_files.pySQL import *
from datetime import datetime



        # TODO:
        #       win32 importeren in venv


class Window(QMainWindow, pyMainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setupUi(self)

        #self.leFilePath.setText(expanduser('~\\DigiBaseReclass_Zaken\\'))

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
        self.tbLoadEvidence.clicked.connect(self.load_evidence)
        self.tbLoadEvidence.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.tbLoad.clicked.connect(self.load_evidence)
        self.tbBrowsePath.clicked.connect(self.create_case)

    def processing_details(self):
        self.stackedWidget.setCurrentIndex(3)
        self.lblCasedetails.setText('processing details')
        self.tbGoTo.setText('go to analyze evidence')
        #self.tbGoTo.clicked.connect(self.analyze_evidence)
        self.stackedWidget.show()

    def case_details(self):
        self.stackedWidget.setCurrentIndex(0)
        self.lblCasedetails.setText('case details')
        self.tbGoTo.setText('go to evidence sources')
        self.tbGoTo.clicked.connect(self.create_case_db)
        self.tbGoTo.clicked.connect(self.evidence_sources)
        self.stackedWidget.show()

    def add_keywords_to_search(self):
        self.stackedWidget.setCurrentIndex(2)
        self.lblCasedetails.setText('add keywords to search')
        self.tbGoTo.setText('go to add hash files')
        self.tbGoTo.clicked.connect(self.add_hash_to_Search)
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

    def load_evidence(self):
        self.stackedWidget.setCurrentIndex(1)
        self.lblCasedetails.setText('load evidence')
        self.lblLoadEvidence.setText('select an evidence source')
        self.tbGoTo.setText('go to processing details')
        self.tbGoTo.clicked.connect(self.processing_details)
        self.stackedWidget.show()

    def create_casenumber(self):
        pass

    def create_casename(self):
        pass

    def ceate_date_created(self):
        pass


    def create_case(self):

        z = datetime.now()
        casename = self.leCaseName.text()
        casenumber = self.leCaseNumber.text()
        examiner = self.leExaminer.text()
        description = self.plainTextEdit.toPlainText()
        self.lblDateCreated.setText(z)
        datecreated = self.lblDateCreated.text()

        data = [casename, casenumber, datecreated, examiner, description]
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly)

        dir = dialog.getExistingDirectory(self, 'Kies map')


        self.leFilePath.setText(dir + "\\" + casename)

        case = self.leFilePath.text()
        print(case)
        if not os.path.exists(case):
            try:
                os.makedirs(case)
            except ValueError:
                case = os.getcwd()



        dbconn = digiBaseReclassConnect(case + "\\DigiBaseReclass.db")
        digiBaseReclassAddTtable(dbconn, "indigodevices")
        digiBaseReclassAddTtable(dbconn, "indigocase")
        digiBaseReclassInsertTable(dbconn, "indigocase", data)


















        #  TODO:
        #        bekijken of def CreateWMI class moet worden
        #
        #  TODO:
        #        database implementeren
        #







    # def CreateWMI(self):
    #     # Connect to sqlite
    #     dbConn = digiBaseReclassConnect(self.tmpdbPath)
    #     self.dbCursor = dbConn.cursor()
    #     # Create WMI objects
    #     c = wmi.WMI()
    #     # loop trough objects
    #     for physical_disk in c.Win32_DiskDrive():
    #         for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
    #             for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
    #                 disk_model = physical_disk.model
    #                 drive_letter = logical_disk.Caption + "\\"
    #                 drive_volume_name = logical_disk.VolumeName
    #                 p_drive = physical_disk.DeviceID
    #                 part_count = physical_disk.partitions
    #                 p_disk_sn = physical_disk.Serialnumber
    #                 p_disk_size = convert_bytes(physical_disk.size)
    #                 interface = physical_disk.interfacetype
    #                 # fill devices as dictionairy
    #                 self.devices = [drive_letter, drive_volume_name, p_disk_size, p_disk_sn, p_drive, disk_model, interface,
    #                                 part_count]
    #                 # insert dictionary in indigodevices_temp table
    #                 digiBaseReclassInsertTable(dbConn, 'indigodevices', self.devices)
    #
    #     self.dbCursor.execute("""SELECT * FROM indigodevices ORDER BY driveletter ASC""")
    #     allRows = self.dbCursor.fetchall()
    #     print(allRows)
    #     self.tableWidgetItem.setHorizontalHeaderLabels(
    #         str("Schijfletter:;Volume naam:;Grootte:;Serienummer:;Fysieke schijf:;Merk:;Type:;Aantal partities").split(";"))
    #
    #     for row in allRows:
    #         inx = allRows.index(row)
    #         self.tableWidgetItem.insertRow(inx)
    #         self.tableWidgetItem.setItem(inx, 0, QTableWidgetItem(row[0]))
    #
    #         self.tableWidgetItem.setColumnWidth(0, 90)
    #         self.tableWidgetItem.setItem(inx, 1, QTableWidgetItem(row[1]))
    #         self.tableWidgetItem.setColumnWidth(1, 150)
    #         self.tableWidgetItem.setItem(inx, 2, QTableWidgetItem(row[2]))
    #         self.tableWidgetItem.setColumnWidth(2, 150)
    #         self.tableWidgetItem.setItem(inx, 3, QTableWidgetItem(row[3]))
    #         self.tableWidgetItem.setColumnWidth(3, 170)
    #         self.tableWidgetItem.setItem(inx, 4, QTableWidgetItem(row[4]))
    #         self.tableWidgetItem.setColumnWidth(4, 170)
    #         self.tableWidgetItem.setItem(inx, 5, QTableWidgetItem(row[5]))
    #         self.tableWidgetItem.setColumnWidth(5, 250)
    #         self.tableWidgetItem.setItem(inx, 6, QTableWidgetItem(row[6]))
    #         self.tableWidgetItem.setColumnWidth(6, 60)
    #         self.tableWidgetItem.setItem(inx, 7, QTableWidgetItem(row[7]))
    #         self.tableWidgetItem.setColumnWidth(7, 120)
    #
    #     self.tableWidgetItem.doubleClicked.connect(self.item_nieuw)
    #
    #     return self.devices

    def conv_to_epoch():
        now = datetime.datetime.now()
        # convert date/time to epoch
        date_time = now.strftime("%d.%m.%Y %H:%M:%S")
        pattern = '%d.%m.%Y %H:%M:%S'
        epoch = int(time.mktime(time.strptime(date_time, pattern)))
        return str(epoch)


def main():
    QCoreApplication.setApplicationName("DigiBaseReclass")
    QCoreApplication.setApplicationVersion("0.1")
    QCoreApplication.setOrganizationName("DigiBaseReclass")
    QCoreApplication.setOrganizationDomain("DigiBaseReclass.com")

    app = QApplication(sys.argv)

    form = Window()
    form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
