FROM ubuntu

RUN mkdir /code
ADD . /code

RUN apt update && \
    apt install -y python3 python3-pip && \
    pip3 install riak
