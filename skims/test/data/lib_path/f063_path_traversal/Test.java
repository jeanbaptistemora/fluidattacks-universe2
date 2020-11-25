import java.io.File;

public class Test {
  @Override
  public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    // some code
    response.setContentType("text/html;charset=UTF-8");

    // Vuln
    javax.servlet.http.Cookie[] theCookies = request.getCookies();
    String param = java.net.URLDecoder.decode(theCookie.getValue(), "UTF-8");
    String fileName = org.owasp.benchmark.helpers.Utils.testfileDir + param;
    java.io.FileInputStream fis = new java.io.FileInputStream(new java.io.File(fileName));
  }
}
