#/bin/bash
cd /tmp/
sudo docker-compose -f docker-compose.yml up -d
sudo mv docker_pull.sh /usr/local/bin/docker_pull.sh
sudo mv login.sh /usr/local/bin/login.sh
sudo crontab -l > mycron
sudo cat cronjob >> mycron
sudo crontab mycron
