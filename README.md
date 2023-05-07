## Task

A program that synchronizes two folders: source and replica. The
program should maintain a full, identical copy of source folder at replica folder.

Programming language: Python

- Synchronization is one-way: after the synchronization content of the
  replica folder is modified to exactly match content of the source
  folder;
- Synchronization is performed periodically.
- File creation/copying/removal operations are logged to a file and to the
  console output;
- Folder paths, synchronization interval and log file path are provided
  using the command line arguments

## How to run the program

### Command

`python sync.py --source /sample/source/path --replica /sample/replica/path --interval 5 --log_file sync.log`

- --source: Path to the source folder
- --replica: Path to the replica folder. If path is not present, it creates new folder.
- --interval: Interval time in minutes to sync source and replica folders.
- --log_file: Log file name to log all the synchronizing changes.
