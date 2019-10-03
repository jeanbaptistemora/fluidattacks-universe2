public class API {
  public static void ControlMethod() {
    SecurityManager securityManager = System.getSecurityManager();
    if (securityManager != null) {
      securityManager.checkPermission(new CustomPermission("permission"));
    }
    System.out.println("Method was executing satisfly");
  }
}
