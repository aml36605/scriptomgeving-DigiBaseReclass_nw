import sqlite3 as db3


def digiBaseReclassConnect(path):
    conn = db3.connect(path)
    return conn

def digiBaseReclassAddtable(connectie, table):

    if table == 'devices':
        sql = 'create table if not exists ' + table + '''(
            driveletter 		TEXT,
            volume_label 		TEXT,
            device_size 		TEXT,
            device_sn 			TEXT,
            physicaldrive 		TEXT,
            device_vendor		TEXT,
            devicetype		TEXT,
            partitioncount		TEXT
            );'''
    elif table == 'indigolog':
        sql = 'create table if not exists ' + table + '''(
            datetime			TEXT,
            message			TEXT
            );'''
    elif table == 'case':
        sql = 'create table if not exists ' + table + '''(
            zaaknaam			TEXT,
            zaaknummer			NUMERIC,
            verbalisant		    TEXT,
            datum               TEXT,
            adres	            TEXT,
            huisnr			    NUMERIC,
            postcode			TEXT,
            plaats          TEXT,
            hovj			TEXT,
            casedir         TEXT
            );'''

    elif table == 'currentdevice' :
        sql = 'create table if not exists ' + table + '''(
            driveletter 		TEXT,
            volume_label 		TEXT,
            device_size 		TEXT,
            device_sn 			TEXT,
            physicaldrive 		TEXT,
            device_vendor		TEXT,
            devicetype		TEXT,
            partitioncount		TEXT,
            image_type     TEXT
            );'''

    elif table == 'match':
        sql = 'create table if not exists ' + table + '''(

            pic                 BINARY,
            crc                 TEXT,
            md5                 TEXT,
            key                 TEXT,
            test                TEXT,
            cdate               TEXT
            );'''



    elif table == 'keyword' or table == 'hash':
        sql = 'create table if not exists ' + table + '''(
            progress			TEXT
            );'''

    connectie.execute(sql)

def checkTable(connectie, tableName):
    cur = connectie.cursor()
    cur.execute(""" SELECT COUNT(*) FROM sqlite_master WHERE name = ?  """, (tableName, ))
    res = cur.fetchone()
    if bool(res[0]): # True if exists
        return True
    else:
        return False

def digiBaseReclassDropTable(connectie, table):
    connectie.executescript('drop table if exists ' + table)

def digiBaseReclassInsertTable(connectie, table, column):

    cur = connectie.cursor()

    if table == 'devices':
        insertsql = [(column[0], column[1], column[2], column[3], column[4], column[5], column[6], column[7])]
        cur.executemany('Insert into ' + table + ' values (?,?,?,?,?,?,?,?)', insertsql)
    elif table == 'case':
        insertsql = [(column[0], column[1], column[2], column[3], column[4], column[5], column[6], column[7], column[8], column[9])]
        cur.executemany('Insert into ' + table + ' values (?,?,?,?,?,?,?,?,?,?)', insertsql)
    elif table == 'currentdevice':
        insertsql = [(column[0], column[1], column[2], column[3], column[4], column[5], column[6], column[7], column[8])]
        cur.executemany('Insert into ' + table + ' values (?,?,?,?,?,?,?,?,?)', insertsql)
    elif table == 'match' :
        insertsql = [(column[0], column[1], column[2], column[3], column[4], column[5])]
        cur.executemany('Insert into ' + table + ' values (?,?,?,?,?,?)', insertsql)


    elif table == 'keyword' or table =='hash':
        insertsql = [(column[0])]
        cur.execute('Insert into ' + table + '(progress) values (?)', insertsql)

    connectie.commit()
    cur.close()