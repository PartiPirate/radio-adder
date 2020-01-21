# radio-adder

## Dependance

### [pytaglib](https://pypi.org/project/pytaglib/)

to read and write the audio tags (mp3, flac, ...)

#### Instal (debian / ubuntu)

`apt install python3-dev libtag1-dev`

`pip3 install pytaglib`

### [pyacoustid](https://pypi.org/project/pyacoustid/)

to identify musics.

#### Install

`pip3 install pyacoustid`

### [ffmpeg](https://ffmpeg.org/)

used by pyacoustid

#### Install (debian / ubuntu)

`apt install ffmpeg`

### [MySQL connector](https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html)

#### Install

`pip3 install mysql-connector-python`

### [filetype](https://pypi.org/project/filetype/)

to get the type of the files, and check if is a music file.

#### Install

`pip3 install filetype`

## Use

`./radio-adder.py [Directory]`

`[Directory]` : the music directory 

## Settings

create a `settings.py` file with this variables : 

```python

display = "short" # all - short - error - none

acoustIDToken = ""

webServiceURL = "https://127.0.0.1/"
webServiceRacinePath = "/var/www/html/"

bddHost 	= "127.0.0.1"
bdduser 	= "user"
bddPassword = "password"
bddName 	= "name"

sortFile = True
removeUselessFileAndFolder = True

```

### display

Is the detail level on the displaying information.

- **none** : no display
- **error** : just error
- **short** : just short info for each music file (tag state, db state) + error
- **all** : all details.

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

### sortFile

Active the auto sorting tool.
move the file in `Artist/Album/Disc.TrackNumber - Title.mp3`

### removeUselessFileAndFolder

Active the "remove useless" option
Remove empty folders and non-music files.