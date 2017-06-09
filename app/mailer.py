"""
    Modulo creado para enviar correos de notificacion
    a traves de Integrates y Amazon
"""

import smtplib
from datetime import datetime


class Mailer(object):
    """Clase para enviar mensajes con Amazon."""

    username = "integrates@mailgun.fluid.la"
    password = "yI1ZcNljI4UAp72YF7vvJ460166T2t"
    server_port = "587"
    server_name = "smtp.mailgun.org"
    timeout = 10
    default_to = "engineering@fluid.la"
    default_to_new_user = "aroldan@fluid.la, glopez@fluid.la, \
projects@fluid.la, production@fluid.la, technology@fluid.la"
    default_from = "FLUID<noreply@fluid.la>"
    server = None

    def __init__(self):
        self.server = smtplib.SMTP(
            host=self.server_name,
            port=self.server_port,
            timeout=self.timeout
        )

    def __tpl_new_user(self):
        """Funcion que retorna el formato HTML del correo
            que se envia cuando un usuario nuevo trata de ingresar."""
        return """From: :from\r\nTo: :to\r\nSubject: :subject\r\n\
MIME-Version: 1.0\r\nContent-type: text/html\r\n
            <style>
            table{ border: 1px solid black; }
            table td { border: 1px solid black; }
            table.no-spacing {
              border-spacing:0;
              border-collapse: collapse;
            }
            </style>
            <center>
                <img style="display:block;margin-left:\
auto;margin-right:auto" src="https://ci6.googleusercontent.com/proxy/\
HJaEHh-IlU0dbE9CAWZM3HEw2VbTv3pwU6iexhsj2xVXA52mdscUyw7uOazWCLj0uIgL18f\
0sMBb6Fb3J4vog_r40RZmQJE7mMwgWFKoOtifj7SboWOF2w9ajySTF5XO9eHjrcw=s0-d-\
e1-ft#https://s3.amazonaws.com/files.formstack.com/public/600135/\
image_customLogo.png" alt="customLogo.png" class="CToWUd">
                <hr/>
                <div style="text-align: left;">
                    La persona <b>:first_name :last_name</b> con correo\
                    <b>:email</b> ha solicitado acceso.<br>
                </div>
            </center>

            <center>
                <hr/>
                <p>Enviado a traves de <b>FLUIDIntegrates </b> :time </p>
            </center>
        """

    def __tpl_delete_finding(self):
        """Funcion que retorna el formato HTML del correo
            que se envia al eliminar un hallazgo."""
        return """From: :from\r\nTo: :to\r\nSubject: :subject\r\n\
MIME-Version: 1.0\r\nContent-type: text/html\r\n
            <style>
            table{ border: 1px solid black; }
            table td { border: 1px solid black; }
            table.no-spacing {
              border-spacing:0;
              border-collapse: collapse;
            }
            </style>
            <center>
                <img style="display:block;margin-left:\
auto;margin-right:auto" src="https://ci6.googleusercontent.com/proxy/\
HJaEHh-IlU0dbE9CAWZM3HEw2VbTv3pwU6iexhsj2xVXA52mdscUyw7uOazWCLj0uIgL18f\
0sMBb6Fb3J4vog_r40RZmQJE7mMwgWFKoOtifj7SboWOF2w9ajySTF5XO9eHjrcw=s0-d-\
e1-ft#https://s3.amazonaws.com/files.formstack.com/public/600135/\
image_customLogo.png" alt="customLogo.png" class="CToWUd">
                <hr/>
                <div style="text-align: left;">
                    <b>Analista: </b> :analista <br>
                    <b>Hallazgo: </b> :hallazgo <br>
                    <b>ID: </b> :id <br>
                    <b>Justificacion: </b> :justificacion <br>
                </div>
            </center>

            <center>
                <hr/>
                <p>Enviado a traves de <b>FLUIDIntegrates </b> :time </p>
            </center>
        """

    def send_delete_finding(self, finding_id, finding, analyst, justify):
        """Funcion que envia un email cuando se elimina un hallazgo."""
        title_mail = "El hallazgo #:id ha sido eliminado"
        title_mail = title_mail.replace(":id", finding_id)
        tpl_mail = self.__tpl_delete_finding()
        tpl_mail = tpl_mail.replace(":subject", title_mail)
        tpl_mail = tpl_mail.replace(":from", self.default_from)
        tpl_mail = tpl_mail.replace(":to", self.default_to)
        tpl_mail = tpl_mail.replace(":analista", analyst)
        tpl_mail = tpl_mail.replace(":hallazgo", finding)
        tpl_mail = tpl_mail.replace(":justificacion", justify)
        tpl_mail = tpl_mail.replace(":id", finding_id)
        tpl_mail = tpl_mail.replace(":time", str(datetime.now()))
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.username, self.password)
        self.server.sendmail(self.default_from, self.default_to, tpl_mail)

    def send_new_user(self, first_name, last_name, email):
        """Funcion que envia un email cuando se elimina un hallazgo."""
        title_mail = "Nueva solicitud de acceso por :email para \
FLUIDIntegrates"
        title_mail = title_mail.replace(":email", email)
        tpl_mail = self.__tpl_new_user()
        tpl_mail = tpl_mail.replace(":subject", title_mail)
        tpl_mail = tpl_mail.replace(":from", self.default_from)
        tpl_mail = tpl_mail.replace(":to", self.default_to_new_user)
        tpl_mail = tpl_mail.replace(":first_name",
                        first_name.encode('ascii',
                                    'ignore').decode('ascii'))
        tpl_mail = tpl_mail.replace(":last_name",
                        last_name.encode('ascii',
                                    'ignore').decode('ascii'))
        tpl_mail = tpl_mail.replace(":email", email)
        tpl_mail = tpl_mail.replace(":time", str(datetime.now()))
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.username, self.password)
        self.server.sendmail(self.default_from, self.default_to, tpl_mail)

    def close(self):
        """Funcion para cerrar la conexion ocn el servidor SMTP."""
        self.server.quit()
