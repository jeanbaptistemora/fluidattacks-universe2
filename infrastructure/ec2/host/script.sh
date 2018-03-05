#/bin/bash
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common python-pip direnv
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian jessie stable"
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y docker-ce
sudo pip install docker-compose
