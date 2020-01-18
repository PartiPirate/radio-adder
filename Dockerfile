FROM python:3
LABEL maintainer="contact@partipirate.org"
WORKDIR /usr/src/python-audio

COPY requirements.txt ./
RUN apt update && apt install -y libtag1-dev ffmpeg
#libchromaprint-tools 
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./your-daemon-or-script.py" ]
