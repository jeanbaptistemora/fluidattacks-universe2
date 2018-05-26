#!/bin/bash

echo 'TORUS_TOKEN_ID='"$TORUS_TOKEN_ID" > /root/mycron
echo 'TORUS_TOKEN_SECRET='"$TORUS_TOKEN_SECRET" >> /root/mycron

crontab -l >> /root/mycron
sed -i 's#/usr/bin#torus\ run\ --\ /usr/bin#g' /root/mycron

crontab /root/mycron
service cron start
rm /root/mycron
