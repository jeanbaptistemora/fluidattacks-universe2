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

Requisitos para lanzar el ambiente desde maquina local:
------------

  * Terraform
  * AWS cli
  * Clave privada FLUID_Serves.pem en infrastructure/vars
  * Archivos XML de los SSO para admin (SSO.xml) y finance (SSOFinance.xml) en infrastucture/vars
  * Archivo con credenciales de AWS y ejecucion de login de docker en la ruta infrastucture/vars/aws.tfvars

  Ejemplo aws.tfvars:
  ```
  ciIP = "IP_CI"
  db_user="DB_USER"
  db_pass="DB_PASS"
  db_name = "DB_NAME"
  engine_ver = "0.0.0"
  acc_key ="YOUR_KEY"
  sec_key = "YOUR_SECRET"

  ```

  * Agregar variables de los buckets persistente, web e integrates y el arn del snapshot de la base de datos

  Ejemplo variables a agregar en terraform.tfvars:
  ```
  bucket = "PERSISTENT_BUCKET_NAME"
  webBucket="WEB_BUCKET_NAME"
  fiBucket="INTEGRATES_BUCKET_NAME"
  db_id = "ARN"

  ```

  * Agregar la siguiente linea con las credenciales del registry de gitlab en infrastructure/ec2/host/script.sh

  ```
  sudo docker login registry.gitlab.com -u USER -p PASSWD

  ```

Instrucciones para lanzar el ambiente desde maquina local:
------------
  * ```cd infrastructure```
  * ```terraform init```
  * ```terraform apply -var-file="vars/aws.tfvars"```


Requisitos para lanzar el ambiente desde GitlabCI:
------------

  * Variables de grupo AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY con credenciales administrativas de AWS
  * Variables globales BUCKET_NAME, FW_S3_BUCKET_NAME y FW_S3_BUCKET_NAME con nombres unicos
  * Variables globales de credenciales de AWS para web e integrates (FI_AWS_S3_ACCESS_KEY, FI_AWS_CLOUDWATCH_ACCESS_KEY, FI_AWS_DYNAMODB_ACCESS_KEY, FW_AWS_ACCESS_KEY_ID, FI_AWS_S3_SECRET_KEY, FI_AWS_CLOUDWATCH_SECRET_KEY, FI_AWS_DYNAMODB_SECRET_KEY, FW_AWS_SECRET_ACCESS_KEY). Estas seran cambiadas por el integrador
  * Variable de serves GL_GROUP con el nombre del grupo de Gitlab donde estan los proyectos y variables globales antes mencionadas
  * Variable en serves FI_SSH_KEY de prueba, solo se necesita para realizar el test de terraform
  * Variables de serves DOCKER_PASS y DOCKER_USER con credenciales para el registry de Gitlab
  * Variables del texto de los archivos XML de los SSO para admin (SSO_XML) y finance (SSO_FINANCE_XML)
  * ARN del snapshot de la base de datos en la variable de serves SNAP_ID


Instrucciones para migrar el ambiente (Gitlab CI):
------------

  1. Cambiar las variables de grupo AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY a las nuevas credenciales
  2. Crear un snapshot de la BD de exams (RDS) y compartirlo con la nueva cuenta de AWS (Desde la consola)
  3. Cambiar la variable de serves SNAP_ID por el ARN del snapshot creado en el paso anterior
  4. Cambiar las variables globales FW_S3_BUCKET_NAME y FW_S3_BUCKET_NAME por nuevos nombres unicos
  5. Cambiar el nombre de la variable global BUCKET_NAME a uno nuevo unico
  6. Ejecutar el pipeline de Gitlab

Cosas por hacer:
------------

  * Cambiar en innodb de la base de datos MySQL del servidor exams a Barracuda, para mejor soporte con Moodle.
