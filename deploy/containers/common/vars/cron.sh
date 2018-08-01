#!/bin/bash

crontab -l >> /root/mycron
sed -i 's#/usr/bin#vaultenv\ /usr/bin#g' /root/mycron

crontab /root/mycron
service cron start
rm /root/mycron
