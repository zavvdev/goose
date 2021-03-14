# Goose v0.0.1
#### _CLI Ftp-client. Transfer files with your ftp-server via simple command prompt interface._
&nbsp;

> Note: You dont need to use double or single quotes to create/delete/upload/download file or directory with spaces in name. For example, you should use: `dir new dir` instead `dir "new dir"`.

&nbsp;
## Commands:
&nbsp;
### ✔ rush
Connect to remote ftp server.
```sh
rush example.ftp.com
```
&nbsp;

### ✔ drop
Upload file or directory to remote ftp server.
You can provide relative path as well.
Note, that "drop" action uploads data to where you are at the moment in the remote server.
```sh
drop /local/path/to/data
```
&nbsp;

### ✔ take
Download file or directory from remote ftp server.
You can provide relative path as well.
Note, that "take" action downloads data to where you are at the moment in the local server.
```sh
take /remote/path/to/data
```
&nbsp;

### ✔ jump
Change current environment.
```sh
jump local
```
```sh
jump remote
```
&nbsp;

### ✔ dir
Create directory.
You can provide relative path as well.
```sh
dir /path/to/new/dir
```
&nbsp;

### ✔ del
Delete file or directory.
You can provide relative path as well.
```sh
del /path/to/data
```
&nbsp;

### ✔ cd
Change directory.
You can provide relative path as well.
```sh
cd /path/to/dir
```
&nbsp;

### ✔ ls
Print list of content in current directory.
```sh
ls
```
&nbsp;

### ✔ ls
Print list of content in current directory.
```sh
ls
```
&nbsp;

### ✔ whereami (pwd)
Print current path.
```sh
whereami
```
```sh
pwd
```
&nbsp;

### ✔ whoami
Print your user name.
```sh
whoami
```
&nbsp;

### ✔ help (h)
 Print all available commands.
```sh
help
```
```sh
h
```
&nbsp;

### ✔ exit (x)
 Terminate program.
```sh
exit
```
```sh
x
```
&nbsp;

