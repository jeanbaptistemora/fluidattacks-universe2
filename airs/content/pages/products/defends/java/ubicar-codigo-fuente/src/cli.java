import java.security.Policy;
import java.security.Permission;
import java.security.ProtectionDomain;
import java.security.PermissionCollection;
import java.security.CodeSource;
import java.security.cert.Certificate;
import java.net.URL;

class CLI {
  public static void main(String[] args) {
    ProtectionDomain protectionDomain = CLI.class.getProtectionDomain();
    CodeSource codeSource = protectionDomain.getCodeSource();
    URL codebase = codeSource.getLocation();
    System.out.println(codebase);
    Certificate[] certificates = codeSource.getCertificates();
    if (certificates == null) {
      System.out.println("ProtectionDomain sin certificados");
    }
    else {
      for (int i=0; i<certificates.length; i++) {
        System.out.println(certificates[i]);
      }
    }
  }
}
