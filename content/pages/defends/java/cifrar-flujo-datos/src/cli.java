import java.io.IOException;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import javax.crypto.Cipher;
import javax.crypto.CipherInputStream;
import javax.crypto.CipherOutputStream;
import javax.crypto.BadPaddingException;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;

class CLI {
  public static void main(String args[]) throws NoSuchAlgorithmException,
    NoSuchPaddingException, BadPaddingException, InvalidKeyException,
      IllegalBlockSizeException, IOException {
        String filename = "./CLI.java";
        String algorithm = "AES";
        KeyGenerator keyGenerator = KeyGenerator.getInstance(algorithm);
        keyGenerator.init(256);
        SecretKey secretKey = keyGenerator.generateKey();
        Cipher encrypter = Cipher.getInstance(algorithm);
        encrypter.init(Cipher.ENCRYPT_MODE, secretKey);
        FileInputStream fis = new FileInputStream(filename);
        FileOutputStream fos = new FileOutputStream(filename + ".crypted");
        CipherOutputStream cos = new CipherOutputStream(fos, encrypter);
        byte[] b = new byte[8];
        int i = fis.read(b);
        while (i != -1) {
          cos.write(b, 0, i);
          i = fis.read(b);
        }
        cos.close();
        Cipher decrypter = Cipher.getInstance(algorithm);
        decrypter.init(Cipher.DECRYPT_MODE, secretKey);
        CipherInputStream cis;
        fis = new FileInputStream(filename + ".crypted");
        cis = new CipherInputStream(fis, decrypter);
        fos = new FileOutputStream(filename + ".decrypted");
        b = new byte[8];
        i = cis.read(b);
        while (i != -1) {
          fos.write(b, 0, i);
          i = cis.read(b);
        }
        cis.close();
   }
}
