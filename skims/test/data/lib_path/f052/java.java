import org.springframework.security.crypto.password.NoOpPasswordEncoder;
public class Main {
    public static void main(String[] args) {
        MessageDigest md = MessageDigest.getInstance("ShA-256");
        MessageDigest md = MessageDigest.getInstance("ShA-1", provider);
        MessageDigest md = MessageDigest.getInstance("mD5");
        MessageDigest md = MessageDigest.getInstance("Md2");
        DigestUtils.sha3_256("test");
        DigestUtils.sha1Hex("test");
        Hashing.md5().hashString(password,StandardCharsets.UTF_8).toString();
        Hashing.sha256().hashString(password,StandardCharsets.UTF_8).toString();
        Cipher c = Cipher.getInstance("AES");
        Cipher c = Cipher.getInstance("DES");
        Cipher c = Cipher.getInstance("DESede");
        Cipher c = Cipher.getInstance("RSA");
        Cipher c = Cipher.getInstance("AES/CBC/PKCS5Padding");
        Cipher c = Cipher.getInstance("AES/CBC/NoPadding");
        Cipher c = Cipher.getInstance("AES/ECB/NoPadding");
        Cipher c = Cipher.getInstance("AES/ECB/PKCS5Padding");
        Cipher c = Cipher.getInstance("DES/CBC/NoPadding");
        Cipher c = Cipher.getInstance("DES/CBC/PKCS5Padding");
        Cipher c = Cipher.getInstance("DES/ECB/NoPadding");
        Cipher c = Cipher.getInstance("DES/ECB/PKCS5Padding");
        Cipher c = Cipher.getInstance("DESede/CBC/NoPadding");
        Cipher c = Cipher.getInstance("DESede/CBC/PKCS5Padding");
        Cipher c = Cipher.getInstance("DESede/ECB/NoPadding");
        Cipher c = Cipher.getInstance("DESede/ECB/PKCS5Padding");
        Cipher c = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        Cipher c = Cipher.getInstance("RSA/ECB/OAEPWithSHA-1AndMGF1Padding");
        Cipher c = Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding");
        SSLContext.getInstance("SSLv3");
        SSLContext.getInstance("TLSv1.2");
        new RSAKeyGenParameterSpec(2048, RSAKeyGenParameterSpec.F4);
        new RSAKeyGenParameterSpec(2047, RSAKeyGenParameterSpec.F4);
        new ECGenParameterSpec("secp521r1");
        new ECGenParameterSpec("c2pnb208w1");
        javax.crypto.KeyGenerator.getInstance("DES").generateKey();
        javax.crypto.KeyGenerator.getInstance("HmacSHA256").generateKey();
        javax.crypto.KeyGenerator.getInstance("AES").generateKey();
        ShaPasswordEncoder encoder = new ShaPasswordEncoder(12);
    }
  }
