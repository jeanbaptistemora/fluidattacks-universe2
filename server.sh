#!/bin/bash

# Script para preparar el server host, diseñado para server Ubuntu.

# Instalar Docker Engine en Ubuntu.
apt-get update
sudo apt-get install apt-transport-https ca-certificatessudo linux-image-extra-$(uname -r) linux-image-extra-virtual -y
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-get install docker-engine
sudo service docker start

# Instalar Ansible en Ubuntu.
sudo apt-get install software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible
