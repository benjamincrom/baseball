#!/bin/bash
printf -v yesterday $(date -d "1 day ago" '+%Y-%m-%d').html; find /var/www/html -name $yesterday -exec sed -i 's/<div id="delay-header" style="width:100%;/<div id="delay-header" style="visibility: hidden; width:100%;/g' {} \;
