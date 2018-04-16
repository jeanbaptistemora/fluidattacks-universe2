import java.io.File;
import javax.security.auth.Subject;
import javax.security.auth.callback.Callback;
import javax.security.auth.callback.CallbackHandler;
import javax.security.auth.login.LoginContext;
import javax.security.auth.login.LoginException;

public class CountFiles {
  static class NullCallbackHandler implements CallbackHandler {
    public void handle(Callback[] cb) {
      throw new IllegalArgumentException("Not implemented yet");
    }
  }
  static LoginContext lc = null;

  public static void main(String[] args) {
    try {
      lc = new LoginContext("CountFiles", new NullCallbackHandler());
    }
    catch (LoginException le) {
      le.printStackTrace();
      System.exit(-1);
    }
    try {
      lc.login();
    }
    catch (Exception e) {
      System.out.println("Login failed: " + e);
      System.exit(-1);
    }
    System.out.println("logged as " + lc.getSubject());
    Object o;
    String tmpDir = File.separator + "tmp";
    o = Subject.doAs(lc.getSubject(), new CountFilesAction(tmpDir));
    System.out.println("user found " + o + " files in " + tmpDir);
    String etcDir = File.separator + "etc";
    o = Subject.doAs(lc.getSubject(), new CountFilesAction(etcDir));
    System.out.println("user found " + o + " files in " + etcDir);
    System.exit(0);
  }
}
