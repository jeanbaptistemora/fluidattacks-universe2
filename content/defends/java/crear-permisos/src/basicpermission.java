import java.security.BasicPermission;

public class CustomPermission extends BasicPermission {
  public CustomPermission(String perm) {
    super(perm);
  }
}
