FROM ubuntu

RUN mkdir /code
ADD . /code

RUN apt update && \
    apt install -y cron wget python3 python3-pip zip nginx && \
    pip3 install python-dateutil pytz requests && \
    rm /var/www/html/index.nginx-debian.html && \
    mkdir /baseball_files && \
    wget -P /var/www/html https://spaces-host.nyc3.digitaloceanspaces.com/livebaseballscorecards-artifacts/baseball-fairy-161.png && \
    wget -P /var/www/html https://spaces-host.nyc3.digitaloceanspaces.com/livebaseballscorecards-artifacts/baseball-fairy-bat-250.png && \
    wget -P /var/www/html https://spaces-host.nyc3.digitaloceanspaces.com/livebaseballscorecards-artifacts/index.html && \
    wget -P / https://spaces-host.nyc3.digitaloceanspaces.com/livebaseballscorecards-artifacts/baseball_files_2008-2017.zip && \
    wget -P / https://spaces-host.nyc3.digitaloceanspaces.com/livebaseballscorecards-artifacts/baseball_files_2018.zip && \
    unzip /baseball_files_2008-2017.zip -d /baseball_files && \
    unzip /baseball_files_2018.zip -d /baseball_files && \
    python3 /code/generate_svg.py files 2008-01-01 2018-12-31 /var/www/html /baseball_files/ && \
    rm -r /baseball_files* && \
    wget -P / https://spaces-host.nyc3.digitaloceanspaces.com/livebaseballscorecards-artifacts/default && \
    mv /default /etc/nginx/sites-enabled/default && \
    touch /current_cron && \
    echo "* * * * * python3 /code/get_today_games.py /var/www/html" >> /current_cron && \
    echo "* * * * * sleep 20; python3 /code/get_today_games.py /var/www/html" >> /current_cron && \
    echo "* * * * * sleep 40; python3 /code/get_today_games.py /var/www/html" >> /current_cron && \
    crontab /current_cron && \
    rm /current_cron 

EXPOSE 80
CMD /usr/sbin/cron && nginx -g "daemon off;"
