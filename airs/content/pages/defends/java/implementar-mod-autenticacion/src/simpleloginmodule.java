import java.util.Map;
import javax.security.auth.Subject;
import javax.security.auth.callback.CallbackHandler;
import javax.security.auth.login.LoginException;
import javax.security.auth.spi.LoginModule;

public class SimpleLoginModule implements LoginModule {
  private Subject subject;
  private CallbackHandler callbackHandler;
  private SimplePrincipal principal;
  private boolean debug;
  private String userName = null;
  private boolean succeeded = false;
  private boolean commitSucceeded = false;

  public void initialize(Subject s, CallbackHandler cb, Map sharedMap, Map options) {
    if (debug)
      System.err.println("SimpleLoginModule: initialize");
    subject = s;
    callbackHandler = cb;
    debug = "true".equalsIgnoreCase((String) options.get("debug"));
  }

  public boolean login() throws LoginException {
    if (debug)
      System.err.println("SimpleLoginModule: login");
    userName = "defaultUser";
    succeeded = true;
    return true;
  }

  public boolean commit() throws LoginException {
    if (debug)
      System.err.println("SimpleLoginModule: commit");
    if (!succeeded) {
      userName = null;
      return false;
    }
    principal = new SimplePrincipal(userName);
    if (!subject.getPrincipals().contains(principal)) {
      subject.getPrincipals().add(principal);
    }
    userName = null;
    commitSucceeded = true;
    return true;
  }

  public boolean abort() throws LoginException {
    if (debug)
      System.err.println("SimpleLoginModule: abort");
    if (succeeded == false)
      return false;
    else if (succeeded == true && commitSucceeded == true) {
      logout();
    }
    else {
      succeeded = false;
    }
    return true;
  }

  public boolean logout() throws LoginException {
    if (debug)
      System.err.println("SimpleLoginModule: logout");
    subject.getPrincipals().remove(principal);
    principal = null;
    userName = null;
    succeeded = commitSucceeded = false;
    return true;
  }
}
