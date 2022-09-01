#!/bin/bash
echo "adding host to known host"
mkdir -p ~/.ssh
touch ~/.ssh/known_hosts
ssh-keyscan sftp >> ~/.ssh/known_hosts
echo "run command on remote server"

sshpass -p pass sftp foo@sftp << EOF
    ls
    pwd
EOF
