# BackItUp
The repository of BackItUp

A cross platform backup utility that reads an input file of what to include and then pack the files in a zip file and saves it to a specified location.

Because of its dynamic way of handeling arguments you can run it from crontab, Windows scheduler, scripts or manually. You can also setup different jobs on the same machine, separating them with unique job names and locations.

Usage: python backitup.py (uses values set inside backitup.py). You can set all values staticly in the code of backitup.py or pass one or more values as arguments at execution time. Arguments is always prioritised.
 
Accepted arguments are:
* **jobname**   The name of the backup instance. Ex. jobname=MyHomeDir

* **listfile**  The list file the specifies what to backup. Ex. listfile=/etc/backup_list_file

* **logfile**   The log file to write log to. Ex. logfile=/var/log/backup.log

* **location**  Where backups should be saved. Ex. location=/opt/backup/

* **rotation**  How many historical backups should be saved. Ex. rotation=7 

* **logging**   Enable or disable logging to file. Values 0 or 1. Ex. logging=1

* **output**    Enable or disable screen output. Values 0 or 1. Ex. output=0

Please give me some feedback if you find this useful. Please, report any bugs and contribute with feature requests if you have specific needs. I will review the requests and add them if I find the feature suiting for the project. The project follows the unix philosophy *Do one thing and do it well.*
