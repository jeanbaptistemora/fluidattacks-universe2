import java.security.MessageDigest;
import javax.xml.bind.DatatypeConverter;
import java.security.SecureRandom;
import java.security.NoSuchAlgorithmException;
import java.io.UnsupportedEncodingException;

class CLI
{
  public static void main(String[] args) throws Exception
  {
    String data = "hola";
    MessageDigest md = MessageDigest.getInstance("SHA-256");
    //byte[] seed = generateSeed();
    //md.update(seed);
    byte[] digest = md.digest(data.getBytes("UTF-8"));
    System.out.println("data: " + data);
    //String encodedSeedBase64 = DatatypeConverter.printBase64Binary(seed);
    //System.out.println("Seed: " + encodedSeedBase64);
    String encodedDigestBase64 = DatatypeConverter.printBase64Binary(digest);
    System.out.println("Digest (base 64): " + encodedDigestBase64);
  }

  private static byte[] generateSeed()
  {
    byte[] seed = new byte[32];
    SecureRandom random = new SecureRandom();
    random.nextBytes(seed);
    return seed;
  }
}
