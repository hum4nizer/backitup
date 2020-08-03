#/usr/bin/env python3
# -*- coding: utf-8 -*-
# BackItUp by Johnny Norberg (2020)
# Version: 2.0 Beta

import os
import time
import glob
import sys
import socket
import re
import platform
import zipfile
from zipfile import ZipFile
from datetime import datetime

## Editable variables ############################
# Name of this backup instance
job_name = 'Full'

# Windows backup location if no input argument is given
backup_location = '/home/humanizer/Backup/'
# Windows backup location if no input argument is given
# backup_location = 'c:\\temp\\Backups\\'

# Linux backup list file if no input argument is given
list_file = '/home/humanizer/tmp/backup_list_file'
# Windows backup list file if no input argument is given
# list_file = 'c:\\temp\\backup_list_file'

# Linux log file with full path
log_file = '/home/humanizer/tmp/backitup.log'
# Windows log file with full path
# log_file = 'c:\\temp\\backitup.log'

# Backup rotation count. Keeps the specified amount of
# backups. Set this option to 0 to disable rotation
backup_count = 7

# True of False
terminal_output = True

# If backup should write to log file or not
# True of False
backup_log = True
###################################################
dateandtime = datetime.now()
hostname = socket.gethostname()
system = platform.system()
timestamp = dateandtime.strftime('%Y_%m_%d__%H_%M_%S')
backupfile = ''
file_count = 0
dir_count = 0
myname = os.path.basename(__file__)

# Read user argments and format variables
def SetUserArguments():
    global backup_location
    global backupfile
    global list_file
    global backupobject
    global job_name
    global log_file
    global backup_count
    global terminal_output
    global backup_log

    bad_chars = ["'", ",", "[", "]"]

    if sys.argv[1:]:
            argument = sys.argv[1]
            if argument == '-h' or argument == '-help' or argument == '--help':
                PrintHelp()


    location = [arg for arg in sys.argv if 'location' in arg]
    if len(location) != 0:
        location = ''.join(char for char in location if not char in bad_chars)
        location = str(location).split('=')
        location = location[1]
        backup_location = location
        if system == 'Windows':
            if backup_location[-1] != '\\':
                backup_location = backup_location + '\\'
        else:
            if backup_location[-1] != '/':
                backup_location = backup_location + '/'
    else:
        if system == 'Windows':
            if backup_location[-1] != '\\':
                backup_location = backup_location + '\\'
        else:
            if backup_location[-1] != '/':
                backup_location = backup_location + '/'


    listfile = [arg for arg in sys.argv if 'listfile' in arg]
    if len(listfile) != 0:
        listfile = ''.join(char for char in listfile if not char in bad_chars)
        listfile = str(listfile).split('=')
        listfile = listfile[1]
        list_file = listfile

    jobname = [arg for arg in sys.argv if 'jobname' in arg]
    if len(jobname) != 0:
        jobname = ''.join(char for char in jobname if not char in bad_chars)
        jobname = str(jobname).split('=')
        jobname = jobname[1]
        job_name = jobname


    logfile = [arg for arg in sys.argv if 'logfile' in arg]
    if len(logfile) != 0:
        logfile = ''.join(char for char in logfile if not char in bad_chars)
        logfile = str(logfile).split('=')
        logfile = logfile[1]
        log_file = logfile

    rotation = [arg for arg in sys.argv if 'rotation' in arg]
    if len(rotation) != 0:
        rotation = ''.join(char for char in rotation if not char in bad_chars)
        rotation = str(rotation).split('=')
        rotation = rotation[1]
        backup_count = int(rotation)

    output = [arg for arg in sys.argv if 'output' in arg]
    if len(output) != 0:
        output = ''.join(char for char in output if not char in bad_chars)
        output = str(output).split('=')
        output = int(output[1])
        if output == 0:
            terminal_output = bool(False)
        elif output == 1:
            terminal_output = bool(True)

    logging = [arg for arg in sys.argv if 'logging' in arg]
    if len(logging) != 0:
        logging = ''.join(char for char in logging if not char in bad_chars)
        logging = str(logging).split('=')
        logging = int(logging[1])
        if logging == 0:
            backup_log = bool(False)
        elif logging == 1:
            backup_log = bool(True)

# Prints the help section
def PrintHelp():
    print('\nBackItUp v.2.0 (Beta) by Johnny Norberg \n'
          '------------------------------\n'
          'A backup utility that reads an input file of what to include and\n'
          'then pack the files in a zip file and saves it to a specified location.\n'
          'Usage: py ' + myname + ' (uses values set inside backitup.py)\n'
          'You can set all values staticly in the code of' + myname + ' or pass\n'
          'one or more values as arguments to the program. Arguments is always\n'
          'prioritised.\n\n'
          'Accepted arguments are:\n'
          'jobname\t\tThe name of the backup instance. Ex. jobname=MyHomeDir\n'
          'listfile\tThe list file the specifies what to backup. Ex. listfile=/etc/backup_list_file \n'
          'logfile\t\tThe log file to write log to. Ex. logfile=/var/log/backup.log \n'
          'location\tWhere backups should be saved. Ex. location=/opt/backup/\n'
          'rotation\tHow many historical backups should be saved. Ex. rotation=7 \n'
          'logging\t\tEnable or disable logging to file. Values 0 or 1. Ex. logging=1\n'
          'output\t\tEnable or disable screen output. Values 0 or 1. Ex. output=0')
    quit()

# Formats the date
def TimeDate():
    dateandtime = datetime.now()
    date_time = dateandtime.strftime('%Y-%m-%d %H:%M:%S')
    return str(date_time)

# Function for text output to log file and terminal
def WriteToLog(log_message):
    if backup_log == True:
        log = open(log_file, "a")
        log.write(TimeDate() + ": " + str(log_message) + "\n")
        log.close()
    if terminal_output == True:
        print(log_message)


# Write header status to terminal output and log file
def WriteStats():
    WriteToLog('-' * 45)
    row = format('Time:', '15'), format(timestamp, '40')
    row = (''.join(row))
    WriteToLog(row)
    
    row = format('System:', '15'), format(system, '40')
    row = (''.join(row))
    WriteToLog(row)
    
    row = format('Backup file:', '15'), format(backupfile, '70')
    row = (''.join(row))
    WriteToLog(row)

    row = format('Location:', '15'), format(backup_location, '70')
    row = (''.join(row))
    WriteToLog(row)

    row = format('Using:', '15'), format(list_file, '70')
    row = (''.join(row))
    WriteToLog(row)

    WriteToLog('-' * 45)
    WriteToLog('Opening: ' + list_file)


def AddDirectory(file_name):
    global dir_count
    global file_count

    try:
        if file_name[-1] == '\n':
            file_name = file_name[:-1]
        if file_name[-1] != '\\' and system == 'Windows':
            file_name = file_name + '\\'
        elif file_name[-1] != '/':
            file_name = file_name + '/'
        WriteToLog('Processing directory: ' + file_name)
        for foldername, subfolders, filenames in os.walk(file_name):
            for directories in subfolders:
                dir_count = dir_count + 1

            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                linkcheck = os.path.islink(filepath)
                if linkcheck == False:
                    WriteToLog(filepath)
                    backupobject.write(filepath, compress_type=zipfile.ZIP_DEFLATED)
                    file_count = file_count + 1
                else:
                    WriteToLog('Excluding link: ' + filepath)
    except os.error as err:
        WriteToLog('Directory: An error has occurred: ' + str(err) + ' ' + file_name)
    else:
        dir_count = dir_count + 1


def AddFile(file_name):
    global file_count

    try:
        if file_name[-1] == '\n':
            backupobject.write(file_name[:-1])
        else:
            backupobject.write(file_name, compress_type=zipfile.ZIP_DEFLATED)
    except os.error as err:
        WriteToLog('File: An error has occurred: ' + str(err) + ' ' + file_name)
    else:
        file_count = file_count + 1
        WriteToLog('Processing file: ' + str(file_name[:-1]))


def BackupRotate(backup_location, backup_count):
    filelist = []
    filelist_with_date = []
    for filename in glob.glob(os.path.join(backup_location + hostname + '_' + job_name +'*.zip')):
        filelist.append(filename)

    WriteToLog('-' * 45)
    WriteToLog('Backup rotate: Searching for backups')
    if len(filelist) >  backup_count:
        for file in filelist:
            mtime = time.strftime('%Y%m%d%H%M%S', time.gmtime(os.path.getmtime(file)))
            filelist_with_date.append(str(mtime) + '#' + file)
        filelist_with_date.sort(reverse=True)
        filelist_with_date = filelist_with_date[backup_count:]
        for file in filelist_with_date:
            file = file.split('#')
            try:
                os.remove(file[1])
                WriteToLog('Deleting backup: ' + file[1])
            except:
                WriteToLog('Error deleting backup: '+ file[1])
        WriteToLog('')
    else:
        WriteToLog('No backups to delete')
        WriteToLog('')


def main():
    global list_file
    global backup_location
    global backupobject
    global backupfile

    if os.path.exists(list_file):
        backupfile = hostname + '_' + job_name + '_' + timestamp + '.zip'
        backupobject = ZipFile(backup_location + backupfile, 'w', zipfile.ZIP_DEFLATED)
        WriteStats()
        reader = list(open(list_file, encoding='utf-8'))
        for row in reader:
            filecheck = os.path.isfile(row[:-1])
            if filecheck == True:
                AddFile(row)
            else:
                AddDirectory(row)
        backupobject.close()

        WriteToLog('-' * 45)
        WriteToLog(str(file_count) + ' files and ' + str(dir_count) + ' directories backed up')
        
        if backup_count > 0:
            BackupRotate(backup_location, backup_count)
        else:
            WriteToLog('Backup rotation is disabled')
    else:
        WriteToLog('No backup_list_file found')


if __name__ == '__main__':
    SetUserArguments()
    main()
