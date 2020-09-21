import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.security.KeyStore;
import javax.net.ServerSocketFactory;
import javax.net.ssl.KeyManagerFactory;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLServerSocket;
import javax.net.ssl.SSLSocket;
import javax.net.ssl.TrustManagerFactory;

public class Server {
  public static void main(String[] args) throws Exception {
    int port = 3333;
    String KEYSTORE = "certs";
    char[] KEYSTOREPW = "storepass".toCharArray();
    char[] KEYPW = "keypass".toCharArray();

    // ¿dónde tenemos las claves?

    KeyStore keystore = KeyStore.getInstance("JKS");
    keystore.load(new FileInputStream(KEYSTORE), KEYSTOREPW);

    // ¿quién nos las va a administrar?

    KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
    vkmf.init(keystore, KEYPW);

    // ¿quién nos va a verificar las claves?
    // (no se requiere si no se realiza autenticacion de cliente)

    TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
    tmf.init(keystore);

    // ¿cómo nos van a cifrar la conexión?

    SSLContext sslc = SSLContext.getInstance("SSLv3");
    sslc.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);

  // ¿quién nos va a cifrar la conexión?

    ServerSocketFactory ssf = sslc.getServerSocketFactory();
    SSLServerSocket server = (SSLServerSocket) ssf.createServerSocket(port);
    server.setNeedClientAuth(false);

  // recibir conexión

    SSLSocket client = (SSLSocket) server.accept();

  // leer

    BufferedOutputStream outputStream = new BufferedOutputStream(client.getOutputStream());
    outputStream.write("Este es el mensaje enviado".getBytes());
    outputStream.flush();
    System.out.println("Servidor: mensaje enviado.");

  // cerrar

  client.close();
    server.close();
  }
}
