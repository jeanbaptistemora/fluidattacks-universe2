# Configura la BD de exams
ansible-playbook servers/rds/scripts/dumpbd.yml -e @servers/rds/vars/vars.yml --vault-password-file ~/.vault.txt
