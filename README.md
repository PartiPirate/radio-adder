# radio-adder

## Dependance

### [pytaglib](https://pypi.org/project/pytaglib/)

to read and write the audio tags (mp3, flac, ...)

#### Instal
	
`pip3 install pytaglib`
or
`apt install python3-pip`

### [pyacoustid](https://pypi.org/project/pyacoustid/)

to identify musics.

#### Install

`pip3 install pyacoustid`

### [MySQL connector](https://dev.mysql.com/doc/connector-python/en/)

#### Install (debian)

download the [deb](https://dev.mysql.com/downloads/connector/python/) file.

`dpkg -i {file}.deb`

## Use

`./TagsScript.py [Directory]`

`[Directory]` : the music directory 

## Settings

create a `settings.py` file with this variables : 

```python

display = "short" # all - short - error - none
tagVersion = "1.3"

acoustIDToken = ""

webServiceURL = "https://127.0.0.1/"
webServiceRacinePath = "/var/www/html/"

bddHost 	= "127.0.0.1"
bdduser 	= "user"
bddPassword = "password"
bddName 	= "name"

```

### display

Is the detail level on the displaying information.

- **none** : no display
- **error** : just error
- **short** : just one line for each music file + error
- **all** : all details.

### tagVersion

The tag version, if you change this value, all old files are re tag.

### acoustIDToken

the token of the acoustid API, you can create our own on [Acoustid web site](https://acoustid.org/), just folow "Register your application" link.

### webServiceURL

### webServiceRacinePath

### bddHost

the address of your MySQL service.

### bdduser

the user of your MySQL service.

### bddPassword

the password of your MySQL service.

### bddName

the name of your MySQL database.