import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.security.KeyStore;
import javax.net.SocketFactory;
import javax.net.ssl.KeyManagerFactory;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocket;
import javax.net.ssl.TrustManagerFactory;

public class Client
{
 public static void main(String[] args) throws Exception
 {
   String host = "localhost";
   int port = 3333;
   String KEYSTORE = "cacerts";

   // ¿dónde tenemos las claves?

   KeyStore keystore = KeyStore.getInstance("JKS");
   keystore.load(new FileInputStream(KEYSTORE), null);

   // ¿quién nos las va a administrar?

   KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
   kmf.init(keystore, null);

   // ¿quién nos va a verificar las claves?

   TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
   tmf.init(keystore);

   // ¿cómo nos van a cifrar la conexion?

   SSLContext sslc = SSLContext.getInstance("SSLv3");
   sslc.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);

   // ¿quién nos va a cifrar la conexion?

   SocketFactory sf = sslc.getSocketFactory();
   SSLSocket client = (SSLSocket) sf.createSocket(host, port);

   // leer

   BufferedInputStream inputStream = new BufferedInputStream(client.getInputStream());
   byte[] message = new byte[64];
   inputStream.read(message);
   System.out.println("Cliente: mensaje: " + new String(message));

   // cerrar

   client.close();
  }
}
