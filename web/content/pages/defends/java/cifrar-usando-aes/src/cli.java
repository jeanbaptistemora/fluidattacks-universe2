import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import javax.crypto.BadPaddingException;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;

class CLI {
  public static void main(String args[])
    throws NoSuchAlgorithmException, NoSuchPaddingException,
      BadPaddingException, InvalidKeyException, IllegalBlockSizeException {
        String plainText = "This is just an example";
        String algorithm = "AES";
        Cipher cipher = Cipher.getInstance(algorithm);
        KeyGenerator keyGenerator = KeyGenerator.getInstance(algorithm);
        KeyGenerator.init(256);
        SecretKey secretKey = keyGenerator.generateKey();
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        byte[] encrypText = cipher.doFinal(plainText.getBytes());
        cipher.init(Cipher.DECRYPT_MODE, secretKey);
        byte[] decrypText = cipher.doFinal(encrypText);
        String encodedEncText =
        javax.xml.bind.DatatypeConverter.printBase64Binary(encrypText);
        System.out.println("Encrypted text: " + new String(encrypText));
        System.out.println("Encrypted and encoded text: " + encodedEncText);
        System.out.println("Decrypted text: " + new String(decrypText));
   }
}
