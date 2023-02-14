import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Base64;

public class PasswordExample {
  public static void main(String[] args) throws NoSuchAlgorithmException {
    String password = "myPassword";
    String salt = generateSalt();
    String saltedHash = hashPassword(password, salt);
    System.out.println("Salted Hash: " + saltedHash);
  }

  private static String generateSalt() throws NoSuchAlgorithmException {
    SecureRandom sr = SecureRandom.getInstanceStrong();
    byte[] salt = new byte[16];
    sr.nextBytes(salt);
    return Base64.getEncoder().encodeToString(salt);
  }

  private static String hashPassword(String password, String salt) throws NoSuchAlgorithmException {
    MessageDigest md = MessageDigest.getInstance("SHA-256");
    md.update(salt.getBytes());
    byte[] hashedPassword = md.digest(password.getBytes());
    return Base64.getEncoder().encodeToString(hashedPassword);
  }
}

public class PasswordExampleNotSafe {
  private static final String SALT = "HARDCODED_SALT";

  public static void main(String[] args) throws NoSuchAlgorithmException {
    String password = "myPassword";
    String saltedHash = hashPassword(password);
    System.out.println("Salted Hash: " + saltedHash);
  }

  private static String hashPassword(String password) throws NoSuchAlgorithmException {
    MessageDigest md = MessageDigest.getInstance("SHA-256");
    md.update(SALT.getBytes());
    byte[] hashedPassword = md.digest(password.getBytes());
    return Base64.getEncoder().encodeToString(hashedPassword);
  }
}
