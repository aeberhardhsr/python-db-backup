###########################################################
#
# This python script is used for mysql database backup
# using mysqldump and tar utility.
#
# Written by : Andreas Eberhard
# Created date: Dec 25, 2022
# Last modified: Aug 25, 2022 
# Tested with : Python 3.10
# Script Revision: 1.0
#
##########################################################
 
# Import required python libraries
 
import os
import time
import datetime
import pipes
import dropbox
 
# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databases names one on each line and assigned to DB_NAME variable.
 
DB_HOST = 'localhost' 
DB_USER = 'newuser'
DB_USER_PASSWORD = 'password'
DB_NAME = 'coiffeur_royal'
BACKUP_PATH = 'backups'
 
# Getting current DateTime to create the separate backup folder like "20180817-123433".
DATETIME = time.strftime('%Y%m%d-%H%M%S')
TODAYBACKUPPATH = BACKUP_PATH

# Access Token to login at Dropbox App
access_token = 'sl.BVsJ8jdNOmiuYODDO95bMurrVCqW60ckeuiHh7UG4Fbbra39utNAQNg47ec3bqeoDAQLfYjVXSjOQ0nEYBH3_P3DM53K_TXokYH-ky7QFA29kXOIOhQ8n50BUoW9_pyr4I6ZfQxWk2WN'
 
def backup_database():
    # Checking if backup folder already exists or not. If not exists will create it.
    try:
        os.stat(TODAYBACKUPPATH)
    except:
        os.mkdir(TODAYBACKUPPATH)
    
    # Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
    print ("checking for databases names file.")
    if os.path.exists(DB_NAME):
        file1 = open(DB_NAME)
        multi = 1
        print ("Databases file found...")
        print ("Starting backup of all dbs listed in file " + DB_NAME)
    else:
        print ("Databases file not found...")
        print ("Starting backup of database " + DB_NAME)
        multi = 0
    
    # Starting actual database backup process.
    if multi:
        in_file = open(DB_NAME,"r")
        flength = len(in_file.readlines())
        in_file.close()
        p = 1
        dbfile = open(DB_NAME,"r")
    
        while p <= flength:
            db = dbfile.readline()   # reading database name from file
            db = db[:-1]         # deletes extra line
            dumpcmd = "C:/xampp/mysql/bin/mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + "_" + DATETIME + ".sql"
            os.system(dumpcmd)
            p = p + 1
        dbfile.close()
    else:
        db = DB_NAME
        dumpcmd = "C:/xampp/mysql/bin/mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + "_" + DATETIME + ".sql"
        os.system(dumpcmd)
    
    print ("")
    print ("Backup script completed")
    print ("Your backups have been created in '" + TODAYBACKUPPATH + "' directory")

"""
def upload_backup():
    latest_file = max('backups/*', key=os.path.getctime)
    dbx = dropbox.Dropbox(access_token)
    f = open(latest_file, 'rb')
    dbx.files_upload(f.read(), '/Data/' + latest_file)
""" 
    
    
if __name__ == "__main__":
    backup_database()
    #upload_backup()