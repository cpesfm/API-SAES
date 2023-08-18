FROM  python:slim-bullseye

COPY . /home/app 

WORKDIR /home/app

RUN apt-get update
RUN apt-get -y install  firefox-esr wget

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz   
RUN tar -xvzf geckodriver-v0.33.0-linux64.tar.gz
RUN mv geckodriver /usr/local/bin/

RUN pip  install --upgrade pip

RUN pip3 install -r requirements.txt




EXPOSE 6969

CMD ["python","server.py"]
