# Configura la BD de exams
ansible-playbook servers/host/scripts/dumpbd.yml -e @servers/host/vars/vars.yml --vault-password-file ~/.vault.txt
