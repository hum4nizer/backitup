# backitup
The repository of BackItUp

A backup utility that reads an input file of what to include and then pack the files in a zip file and saves it to a specified location. Usage: py backitup.py (reads standard backup_list_file). You can set all values staticly in the code of backitup.py or pass one or more values as arguments at execution time. Arguments is always prioritised.

Accepted arguements are:
jobname   The name of the backup instance. Ex. jobname=MyHomeDir\n'
listfile  The list file the specifies what to backup. Ex. listfile=/etc/backup_list_file \n'
logfile   The log file to write log to. Ex. logfile=/var/log/backup.log \n'
location  Where backups should be saved. Ex. location=/opt/backup/\n'
rotation  How many historical backups should be saved. Ex. rotation=7 \n'
logging   Enable or disable logging to file. Values 0 or 1. Ex. logging=1\n'
output    Enable or disable screen output. Values 0 or 1. Ex. output=0')
