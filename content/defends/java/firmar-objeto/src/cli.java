import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.Signature;
import java.security.SignedObject;
import java.io.IOException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.SignatureException;

class CLI {
  public static void main(String[] args) throws Exception,
    NoSuchAlgorithmException, SignatureException, InvalidKeyException,
      IOException, ClassNotFoundException {
        PublicKey publicKey = null;
        PrivateKey privateKey = null;
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("DSA");
        keyGen.initialize(1024);
        KeyPair keypair = keyGen.genKeyPair();
        privateKey = keypair.getPrivate();
        publicKey = keypair.getPublic();
        String data = "object signed";
        Signature signature = Signature.getInstance(privateKey.getAlgorithm());
        Signature sigs = Signature.getInstance(publicKey.getAlgorithm());
        boolean b = so.verify(publicKey, sigs);
        String os = (String) so.getObject();
        System.out.println("object signed: " + os);
        System.out.println("Signature Verification: " + b);
   }
}
