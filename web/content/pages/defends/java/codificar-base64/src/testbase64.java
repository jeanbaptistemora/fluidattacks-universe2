import org.apache.commons.codec.binary.Base64;
import java.nio.charset.Charset;
import java.util.Arrays;

public class TestBase64 {
  public static void main (String... args) throws java.io.UnsupportedEncodingException {

   // Se define texto plano y codificado originales

   String originalExamplePlain = "Texto de ejemplo incluyendo caracteres como
      A-Z, a-z, 0-9, = y /.";
   String originalExampleBase64 =
       "VGV4dG8gZGUgZWplbXBsbyBpbmNsdXllbmRvIGNhcmFjdGVyZXMgY29tbyBBLVosIGEteiwgMC05LCA9IHkgLy4=";

   /* Se obtiene la representacion en bytes de los datos originales asumiendo que su
     codificación es ASCII*/

   byte[] bytesExamplePlain = originalExamplePlain.getBytes("US-ASCII");
   byte[] bytesExampleBase64 = originalExampleBase64.getBytes("US-ASCII");

   // Se comprueba que en realidad los datos originales sí estuvieran en ASCII

   String examplePlain = new String(bytesExamplePlain, Charset.forName("USASCII"));
   String exampleBase64 = new String(bytesExampleBase64, Charset.forName("USASCII"));
   assert examplePlain.equals(originalExamplePlain);
   assert exampleBase64.equals(originalExampleBase64);

   // Se obtiene la conversión a texto plano de la representación base64 original

   byte[] convertedToPlain = Base64.decodeBase64(exampleBase64);

   /* Se comprueba que la conversión corresponda a los bytes originales del
      texto plano*/

   assert Arrays.equals(convertedToPlain, bytesExamplePlain);

   // Se obtiene la conversión a base64 del texto plano original

   String convertedToBase64 = Base64.encodeBase64String(bytesExamplePlain);

   // Se comprueba que la conversión corresponda al texto plano original

   assert convertedToBase64.equals(exampleBase64);

   // Se muestra por salida estandar el resultado de la conversion

   System.out.format("%s\n", new String(convertedToPlain, "US-ASCII"));
   System.out.format("%s\n", convertedToBase64);
  }
}
