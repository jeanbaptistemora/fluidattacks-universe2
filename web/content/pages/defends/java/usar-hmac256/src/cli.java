import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.Mac;

class CLI {
  public static void main(String[] args) throws Exception {
    String algorithm = "HmacSHA256";
    KeyGenerator kg = KeyGenerator.getInstance(algorithm);
    SecretKey key = kg.generateKey();
    Mac mac = Mac.getInstance(algorithm);
    mac.init(key);
    String message = "This is the message";
    byte[] tag = mac.doFinal(message.getBytes());
    System.out.println("Text: " + message);
    String encodedTag = javax.xml.bind.DatatypeConverter.printBase64Binary(tag);
    System.out.println(algorithm + ": " + encodedTag);
  }
}
