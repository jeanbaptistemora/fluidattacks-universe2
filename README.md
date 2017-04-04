FLUID SERVES - Infraestructura Inmutable
============

Repositorio de código para almacenar la definición de la infraestructura de FLUID.

La definición de la infraestrucura se realizó utilizando Ansible sobre Docker.

Servidores en Producción:
------------

  * ALG: Servidor Apache para realizar proxy reverso para los diferentes recursos web con los que cuenta FLUID.
  * Exams: Plataforma online para la realización de cursos y examenes. Su uso principal es la realización del examen de conocimientos en el proceso de selección.
  * Integrates: Servidor para la publicación del servicio FLUID integrates.
  * Host: Servidor base instalado en nube de Amazon.

Requisitos para lanzar el ambiente:
------------

  * Python
  * Boto3

Instrucciones para lanzar el ambiente:
------------
  * Configurar el cliente Boto3 con las credenciales de acceso a AWS.
  * Ejecutar el script launch_prd.sh

Cosas por hacer:
------------

  * Cambiar en innodb de la base de datos MySQL del servidor exams a Barracuda, para mejor soporte con Moodle.
  * Mantener sincronizada la db en algun repositorio, para nuevas implementaciones.
