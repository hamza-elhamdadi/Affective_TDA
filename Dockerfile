FROM ubuntu

RUN apt-get -y update && apt-get install -y python3
RUN apt-get install -y python3-pip

RUN pip3 install flask
RUN pip3 install sklearn
RUN pip3 install Cython
RUN pip3 install ripser
RUN pip3 install matplotlib

RUN mkdir /opt/source-code

COPY . /opt/source-code

RUN cd /opt/source-code

ENTRYPOINT FLASK_APP=/opt/source-code/serve.py flask run