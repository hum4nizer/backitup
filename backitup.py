#/usr/bin/env python3
# -*- coding: utf-8 -*-
# BackItUp by Johnny Norberg (2020 - 2024)
# Version: 2.0 Beta

import os
import time
import shutil
import pathlib
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
#job_name = 'Selected'
job_name = 'Test'

# Linux backup location if no input argument is given
#backup_location = '/mnt/backup/'
backup_location = '/tmp/btest'

# Windows backup location if no input argument is given
# backup_location = 'c:\\temp\\Backups\\'

# Linux backup list file if no input argument is given
list_file = './backup_list_file'
# Windows backup list file if no input argument is given
# list_file = 'c:\\temp\\backup_list_file'

# Linux log file with full path
#log_file = '/var/log/backitup.log'
log_file = '/tmp/btest/backitup.log'
# Windows log file with full path
# log_file = 'c:\\temp\\backitup.log'

# Backup rotation count. Keeps the specified amount of
# backups. Set this option to 0 to disable rotation
backup_count = 5

# True of False
terminal_output = False

# If backup should write to log file or not
# True of False
backup_log = True

# Backup type
# full or inceremental
backup_type = 'incremental'

# Placeholder for action parameter
action = ''

# Placeholder for unpack_location parameter
user_home = pathlib.Path.home()
unpack_location = str(user_home) + '/backitup'
###################################################


# Read user argments and format variables
def SetUserArguments(backup_location, list_file, log_file, job_name, backup_count, terminal_output, backup_log, backup_type, action, unpack_location):
    bad_chars = ["'", ",", "[", "]"]

    if sys.argv[1:]:
            argument = sys.argv[1]
            if argument == '-h' or argument == '-help' or argument == '--help':
                PrintHelp()

    location = [arg for arg in sys.argv if 'location' in arg]
    if len(location) != 0:
        location = ''.join(char for char in location if not char in bad_chars)
        location = str(location).split('=')
        backup_location = location[1]
        
        if platform.system() == 'Windows':
            if backup_location[-1] != '\\':
                backup_location = backup_location + '\\'
        else:
            if backup_location[-1] != '/':
                backup_location = backup_location + '/'
    else:
        if platform.system() == 'Windows':
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

    backuptype = [arg for arg in sys.argv if 'backup_type' in arg]
    if len(backuptype) != 0:
        backuptype = ''.join(char for char in backuptype if not char in bad_chars)
        backuptype = str(backuptype).split('=')
        backuptype = backuptype[1]
        backup_type = backuptype

    action = [arg for arg in sys.argv if 'action' in arg]
    if len(action) != 0:
        action = ''.join(char for char in action if not char in bad_chars)
        action = str(action).split('=')
        action = action[1]

    unpack_loc = [arg for arg in sys.argv if 'unpack_loc' in arg]
    if len(unpack_loc) != 0:
        unpack_loc = ''.join(char for char in unpack_loc if not char in bad_chars)
        unpack_loc = str(unpack_loc).split('=')
        unpack_location = unpack_loc[1]

    return backup_location, list_file, log_file, job_name, backup_count, terminal_output, backup_log, backup_type, action, unpack_location


# Prints the help section
def PrintHelp():
    myname = os.path.basename(__file__)
    print('\nBackItUp v.3.0 (Beta) by Johnny Norberg \n'
          '------------------------------\n'
          'A backup utility that reads an input file of what to include and\n'
          'then pack the files in a zip file and saves it to a specified location.\n'
          'Usage: py ' + myname + ' (uses values set inside backitup.py)\n'
          'You can set all values staticly in the code of' + myname + ' or pass\n'
          'one or more values as arguments to the program. Arguments is always\n'
          'prioritised.\n\n'
          'Accepted arguments are:\n'
          'jobname\t\tThe name of the backup instance. Ex. jobname=MyHomeDir\n'
          'listfile\tThe list file that specifies what to backup. Ex. listfile=/etc/backup_list_file \n'
          'logfile\t\tThe log file to write log to. Ex. logfile=/var/log/backup.log \n'
          'location\tWhere backups should be saved. Ex. location=/opt/backup/\n'
          'rotation\tHow many historical backups should be saved. Ex. rotation=7 \n'
          'logging\t\tEnable or disable logging to file. Values 0 or 1. Ex. logging=1\n'
          'output\t\tEnable or disable screen output. Values 0 or 1. Ex. output=0\n'
          'backup_type\t\tBackup type- full or incremental are valid commands'
          'unpack_loc\tSpecifies the destination of the action: unpack\n\n'
          'action is a parameter to trigger a merge, unpack or reset\n'
          'action=unpack \t - Unpacks all incremental files to a specified directory\n' 
          'action=merge\t - Merges all inceremental files to a new intital backup file\n'
          'action=reset\t - Resets the backup, deletes all files and creates a new initial file\n'
          'Example of action trigger: action=unpack unpack_loc=/tmp/my_backup\n\n'
          'You can also use the exclude parameter in the backup list file to exclude\n'
          'files or directories. Example exclude:/home/user/.bashrc\n'
          )
       
    quit()


# Formats the date
def TimeDate():
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return str(date_time)


# Function for text output to log file and terminal
def WriteToLog(log_file, log_message):
    if backup_log == True:
        if os.path.isfile(log_file):
            log = open(log_file, "a")
            log.write(TimeDate() + ": " + str(log_message) + "\n")
            log.close()
        else:
            log = open(log_file, "w")
            log.write(TimeDate() + ": " + str(log_message) + "\n")
            log.close()
        
    if terminal_output == True:
        print(log_message.strip())


# Write header status to terminal output and log file
def WriteStats(log_file, backupfile, backup_location, list_file, backup_type):
    WriteToLog(log_file, '-' * 45)
    row = format('Time:', '15'), format(TimeDate(), '40')
    WriteToLog(log_file, ''.join(row))
    
    row = format('System:', '15'), format(platform.system(), '40')
    WriteToLog(log_file, ''.join(row))
    
    row = format('Backup file:', '15'), format(backupfile, '70')
    WriteToLog(log_file, ''.join(row))

    row = format('Backup type:', '15'), format(backup_type, '70')
    WriteToLog(log_file, ''.join(row))

    row = format('Location:', '15'), format(backup_location, '70')
    WriteToLog(log_file, ''.join(row))

    row = format('Using:', '15'), format(list_file.replace('\n','').strip(), '70')
    WriteToLog(log_file, ''.join(row))

    WriteToLog(log_file, '-' * 45)


def excludecheck(excludes, row):
    for item in excludes:
        if item in row:
            return True

        else:           
            return False


def BackupRotate(backup_location, backup_count):
    filelist = []
    filelist_with_date = []
    
    for filename in glob.glob(os.path.join(backup_location + socket.gethostname() + '_' + job_name +'*.zip')):
        filelist.append(filename)

    WriteToLog(log_file, '-' * 45)
    WriteToLog(log_file, 'Backup rotate: Searching for backups')
    
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
                WriteToLog(log_file, 'Deleting backup: ' + file[1])
    
            except:
                WriteToLog(log_file, 'Error deleting backup: '+ file[1])
        WriteToLog(log_file, '')
    
    else:
        WriteToLog(log_file, 'No backups to delete')
        WriteToLog(log_file, '-' * 45)


def ArchiveWorker(unpack_location, location, backupfile, state):
    filelist = []
    filelist_with_date = []
    
    if state == 'unpack' or state == 'merge' or state == 'reset':
        if state == 'unpack':
            WriteToLog(log_file, 'Unpack command executed with destination directory ' + unpack_location)
        
        elif state == 'merge':
            WriteToLog(log_file, 'Merge command executed')

        for filename in glob.glob(os.path.join(backup_location + socket.gethostname() + '_' + job_name + '*.zip')):
            filelist.append(filename)
        
        for file in filelist:
                mtime = time.strftime('%Y%m%d%H%M%S', time.gmtime(os.path.getmtime(file)))
                filelist_with_date.append(str(mtime) + '#' + file)
                filelist_with_date.sort(reverse=False)
        
        filelist.sort()
        
        for file in filelist:
            with zipfile.ZipFile(file) as zf:
                if state == 'unpack':
                    zf.extractall(unpack_location)         
                    WriteToLog(log_file, 'Extracting: ' + file)

                if state == 'merge':
                    zf.extractall(location)
                    WriteToLog(log_file, 'Merging: ' + file)

        if state == 'unpack':
            WriteToLog(log_file, 'Unpack finished') 
        
    if state == 'merge':
        DeleteFilesAtMerge(filelist, 'before_merge')
        content_file_list = CreateMergeArchive(backupfile, location)
        master_file_list = CreateMasterFileAfterMerge(content_file_list)
        SaveFile(backup_location + '.masterfile', master_file_list)
        DeleteFilesAtMerge(filelist, 'after_merge')
        WriteToLog(log_file, 'Merge finished')

    if state == 'reset':
        DeleteFilesAtMerge(filelist, 'before_merge')
        DeleteFilesAtMerge(filelist, 'after_merge')
        WriteToLog(log_file, 'Reset command executed. Rebuildning backup')

def  DeleteFilesAtMerge(filelist, state):
    if state == 'before_merge':
        for file in filelist:
            os.remove(file)

        if os.path.isfile(backup_location + '.masterfile'):
            os.remove(backup_location + '.masterfile')
        
        if os.path.isfile(backup_location + '.contentfile'):
            os.remove(backup_location + '.contentfile')

    if state == 'after_merge':
        if os.path.isdir(str(user_home) + '/tmp/backitup'):
            shutil.rmtree(str(user_home) + '/tmp/backitup')


def CreateMergeArchive(backupfile, location):
    content_file_list = []
    backupobject = ZipFile(backup_location + backupfile, 'w', zipfile.ZIP_DEFLATED)
    w = os.walk(location)
    
    for (dirpath, dirnames, filenames) in w:
        for filename in filenames:
            file = os.path.join(dirpath, filename)
            content_file_list.append(file.replace(str(user_home) + '/tmp/backitup', ''))
            backupobject.write(file, arcname=file.split(str(user_home) + '/tmp/backitup')[1], compress_type=zipfile.ZIP_DEFLATED)

    backupobject.close()

    WriteContentFile(content_file_list, backupfile)
    return content_file_list


def CreateMasterFileAfterMerge(content_file_list):
    file_list = []
    for file in content_file_list:
        if os.path.isfile(file) == True:
            m_time = os.path.getmtime(file)
            dt_m = datetime.fromtimestamp(m_time)
            file_list.append(os.path.join(file + '#:#' + str(dt_m))) 
        else:
            file_list.append(os.path.join(file + '#:#' + '1900-01-01 00:00:00'))
    
    return file_list


def ReadListFile(list_file):
    dirs = []
    files = []
    excludes = []
    thelist = list(open(list_file, encoding='utf-8'))

    for entry in thelist:
        entry = entry.replace('\n', '') 
          
        if 'exclude:' in entry:
            entry = entry.lstrip('exclude:')
            excludes.append(entry)
        
        elif os.path.isdir(entry):
            dirs.append(entry)

        elif os.path.isfile(entry):
            files.append(entry)

    return dirs, files, excludes


def CreateMasterFile(dirs, files, excludes):
    tmp_files = []
    file_list = []

    for dir in dirs:
        w = os.walk(dir)
    
        for (dirpath, dirnames, filenames) in w:
            for filename in filenames:
                filename = os.path.join(dirpath, filename)
                tmp_files.append(os.path.join(filename))
    
    tmp_files += files

    for file in tmp_files:
        is_excluded = False

        for exclude in excludes:

            if file.__contains__(exclude):
                is_excluded = True                

        if is_excluded == False and os.path.isfile(file) == True:
            m_time = os.path.getmtime(file)
            dt_m = datetime.fromtimestamp(m_time)
            file_list.append(os.path.join(file + '#:#' + str(dt_m)))        
   
    return file_list


def CreateArchive(file_list, backupfile):
    file_count = 0
    if len(file_list) > 0:
        backupobject = ZipFile(backup_location + backupfile, 'w', zipfile.ZIP_DEFLATED)

        for file in file_list:
            file = file.split('#:#')
            file = file[0]
            backupobject.write(file, compress_type=zipfile.ZIP_DEFLATED)
            if terminal_output == True:
                WriteToLog(log_file, 'Backup: ' + file)
            
            file_count += 1
        
        backupobject.close()
        
    return file_count
    

def SaveFile(reqfile, file_list):
    file_list = '\n'.join(file_list) 
    with open(reqfile, "w") as data:
        data.write(file_list)


def ReadFile(reqfile):
    with open(reqfile) as f:
        data = f.read()

    return data


def ReadFileToList(reqfile):
    list = []
    with open(reqfile) as f:
        data = f.read()

    for row in data.splitlines():
        list.append(row)

    return list


def CompareFiles(master_file, file_list):
    diff = []

    for entry in file_list:
        if entry not in master_file:
            diff.append(entry)
    
    return diff


def WriteContentFile(content, file):
        content_file = backup_location + '.contentfile'
        if type(content) == list:
            content = '\n'.join(content)
        
        with open(content_file, "a") as content_file:
            content_to_file = 'Date: ' + TimeDate() + '\n' \
            + 'File: ' + file + '\n' \
            + 'Content: \n' \
            + content + '\n' \
            + '-' * 60 + '\n\n'
                        
            content_file.write(content_to_file)    


def StripToContentFile(file_list):
    tmp_list = []

    for line in file_list:
        line = line.split('#:#')
        tmp_list.append(line[0])
        
    return tmp_list


def WriteFooter(file_count):
        WriteToLog(log_file, '-' * 45)
        WriteToLog(log_file, str(file_count) + ' files backed up')


def main():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_count = 0
    backupfile = socket.gethostname() + '_' + job_name + '_' + timestamp + '.zip'
        
    if action == 'unpack':
        ArchiveWorker(unpack_location, str(user_home) + '/tmp/backitup', backupfile, 'unpack')
        quit()

    if action == 'merge':
        ArchiveWorker(unpack_location, str(user_home) + '/tmp/backitup', backupfile, 'merge')
        quit()

    if action == 'reset':
        ArchiveWorker(unpack_location, str(user_home) + '/tmp/backitup', backupfile, 'reset')
        
    if os.path.exists(list_file):
        WriteStats(log_file, backupfile, backup_location, list_file, backup_type)
        
        dirs, files, excludes = ReadListFile(list_file)
        file_list = CreateMasterFile(dirs, files, excludes)

        if not os.path.isfile(backup_location + '.masterfile') or backup_type == 'full':
            SaveFile(backup_location + '.masterfile', file_list)
            file_count = CreateArchive(file_list, backupfile)
            file_list = StripToContentFile(file_list)
            WriteContentFile(file_list, backupfile)
        
        else:
            master_file = ReadFileToList(backup_location + '.masterfile')
            diff = CompareFiles(master_file, file_list)
            if len(diff) != 0:
                file_count = CreateArchive(diff, backupfile)
                SaveFile(backup_location + '.masterfile', file_list)
                diff = StripToContentFile(diff)
                WriteContentFile(diff, backupfile)

            else:
                if terminal_output == True:
                    print('No change on monitored targets')

        WriteFooter(file_count)

               
        if backup_count > 0 and backup_type == 'full':
            BackupRotate(backup_location, backup_count)
    
        else:
            if backup_type == 'incremental':
                WriteToLog(log_file, 'Backup rotation is disabled because of incremental backup')
            else:
                WriteToLog(log_file, 'Backup rotation is disabled')
    
    else:
        WriteToLog(log_file, 'No backup_list_file found')


if __name__ == '__main__':
    backup_location, list_file, log_file, job_name, backup_count, terminal_output, backup_log, backup_type, action, unpack_location = SetUserArguments(backup_location, list_file, log_file, job_name, backup_count, terminal_output, backup_log, backup_type, action, unpack_location)
    main()
