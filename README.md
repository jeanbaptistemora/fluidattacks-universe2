FLUID SERVES - Infraestructura Inmutable
============

Repositorio de código para almacenar la definición de la infraestructura de FLUID.

La definición de la infraestrucura se realizó utilizando Terraform y Docker.

Servidores en Producción:
------------

  * ALG: Servidor Apache para realizar proxy reverso para los diferentes recursos web con los que cuenta FLUID.
  * Exams: Plataforma online para la realización de cursos y examenes. Su uso principal es la realización del examen de conocimientos en el proceso de selección.
  * Integrates: Servidor para la publicación del servicio FLUID integrates.
  * Host: Servidor base instalado en nube de Amazon.

Requisitos para lanzar el ambiente:
------------

  * Terraform
  * AWS cli
  * Clave privada .pem en infrastructure/vars
  * Archivo con credenciales de AWS y ejecucion de login de docker en la ruta infrastucture/vars/aws.tfvars

  Ejemplo:
  ----
  acc_key = "YOUR KEY"
  sec_key = "YOUR SECRET KEY"
  docker = "sudo docker login URL -u USER -p PASSWORD"
  start_all = "sudo docker-compose -f /tmp/docker-compose.yml up -d"
  ----

Instrucciones para lanzar el ambiente:
------------
  * cd infrastructure
  * terraform init
  * terraform apply -var-file="vars/aws.tfvars"

Cosas por hacer:
------------

  * Cambiar en innodb de la base de datos MySQL del servidor exams a Barracuda, para mejor soporte con Moodle.
  * Mantener sincronizada la db en algun repositorio, para nuevas implementaciones.
  * Probar soporte CI 2.0.
