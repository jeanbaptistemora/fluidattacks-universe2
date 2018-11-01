import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.Signature;
import java.security.NoSuchAlgorithmException;
import java.security.SignatureException;
import java.security.InvalidKeyException;

class CLI {
  public static void main(String[] args) throws Exception,
    NoSuchAlgorithmException, SignatureException, InvalidKeyException {
      KeyPairGenerator keyGen = KeyPairGenerator.getInstance("DSA");
      KeyGen.initialize(1024);
      KeyPair keypair = keyGen.genKeyPair();
      PrivateKey privateKey = keypair.getPrivate();
      PublicKey publicKey = keypair.getPublic();
      byte buffer[] = "Hello World".getBytes();
      Signature signature = Signature.getInstance(privateKey.getAlgorithm());
      signature.initSign(privateKey);
      signature.update(buffer, 0, buffer.length);
      byte[] signBytes = signature.sign();
      signature.initVerify(publicKey);
      signature.update(buffer, 0, buffer.length);
      boolean validBuffer = signature.verify(signBytes);
      sun.misc.BASE64Encoder encoder = new sun.misc.BASE64Encoder();
      System.out.println("DSA-1024 PrivateKey = " + privateKey);
      System.out.println("DSA-1024 PublicKey = " + publicKey);
      System.out.println("buffer: " + new String(buffer));
      System.out.println("Signature: " + encoder.encode(signBytes));
      System.out.println("Verification: " + validBuffer);
    }
}
