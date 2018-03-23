using System;
using System.Net;
using System.Net.Mail;

namespace LineaBase {
  class Program {
    static void Main(string[] args) {
      try {
        var direccionOrigen = new MailAddress("origen@gmail.com", "Remitente de prueba");
        var direccionDestino = new MailAddress("destino@gmail.com", "Destinatario de prueba");
        const string clave = "miclave";
        const string asunto = "Asunto de prueba";
        string cuerpo = @"
        Bienvenido/a al sistema, usuario <nombre_de_usuario>.
        Para poder acceder a su nueva cuenta debe verificar su correo
        haciendo click en el siguiente enlace:
        http://www.pagina.com/ID=" + System.Guid.NewGuid().ToString();
        using (MailMessage mensaje = new MailMessage(direccionOrigen, direccionDestino) {
          Subject = asunto,
          Body = cuerpo
        }) {
          using (var smtp = new SmtpClient() {
            Host = "smtp.gmail.com",
            Port = 587,
            EnableSsl = true,
            DeliveryMethod = SmtpDeliveryMethod.Network,
            Credentials = new NetworkCredential(direccionOrigen.Address, clave),
            Timeout = 18000
          }) {
            smtp.Send(mensaje);
          }
        }
      } catch (SmtpException) {
        Console.WriteLine("El mensaje no ha podido ser enviado");
      }
    }
  }
}
