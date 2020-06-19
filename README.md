# Remote Printer

This is a remote printer controlling project based on `Python3`, `Django` and `SumatraPDF`

```text
+-----------+     +-------------+      +-----------+
|           +---->+             +----->+           |
|    PC     |     |     LAN     |      |    PC     |
|           +<----+             +<-----+           |
+-----------+     +-------------+      +-----------+
    |   ^
    |   |
    v   |
+-----------+
|           |
|  Printer  |
|           |
+-----------+
```



## Features

- Upload any format file and no need to bring your USB stick all the time (default folder is the `upload` folder)
- Upload PDF and duplex print
- Upload PDF and print with user-designed settings (Thanks to `SumatraPDF`)



## Installation

1. Install , you can find a release [Here](https://www.sumatrapdfreader.org/)
2. Install `Django` library (we develop this project with Django 3.0 and Python 3.7, but you could use a lower Django edition and Python >= 3.6 with almost no changes)

```bash
pip install django
```

3. change directory and create database: `cd src`

```bash
python manage.py makemigrations user
python manage.py makemigrations
python manage.py migrate user
python manage.py migrate
```

4. create superuser

```
python manage.py createsuperuser
```

5. change settings in `remoteprinter/settings.py`

```python
# upload directory
UPLOAD_DIR = os.path.join(BASE_DIR, 'upload')
# sumatrapdf execution file
SUMATRAPDF_PATH = 'D:\SumatraPDF\SumatraPDF.exe'
# printer name
PRINTER_NAME = 'Brother DCP-7180DN Printer'
```



## Quick Start

```bash
cd src
python manage.py runserver 0:8000
```

- Open admin page：http://ipaddress:port/admin/
- Start to print：http://ipaddress:port/user/index/

