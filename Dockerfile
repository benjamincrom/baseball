FROM nginx:latest

WORKDIR /

RUN apt-get update && apt-get install -y python3 python3-pip
COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt
RUN mkdir /code
COPY site-files/wrapper.py code/
COPY site-files/sweeper.py code/
COPY site-files/clean_delay.py code/
COPY baseball/ code/baseball/

RUN apt-get -y install liblmdb-dev nginx

WORKDIR /code
RUN mkdir -p /var/www
RUN mkdir -p /mnt/delay
RUN ln -s /usr/share/nginx/html /var/www
RUN python3 clean_delay.py
RUN python3 wrapper.py

EXPOSE 80
