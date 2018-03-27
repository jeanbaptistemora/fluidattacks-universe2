package test;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/TestRemoteUserData")

public class TestRemoteUserData extends HttpServlet {
  public TestRemoteUserData() {
    super();
  }
  protected void doGet(HttpServletRequest request, HttpServletResponse response)
    throws ServletException, IOException {
      response.setContentType("text/html;charset=UTF-8");
      PrintWriter out = response.getWriter();
    java.security.Principal principal = null;
      String remoteUser = null;
    try {
      out.println("<h2>Antes de hacer login:</h2>");
      out.println("IsUserInRole rol1: " + request.isUserInRole("rol1") + "<br>");
      out.println("getRemoteUser: " + request.getRemoteUser() + "<br>");
      principal = request.getUserPrincipal();
      if( principal != null )
        remoteUser = principal.getName();
      out.println("getUserPrincipal.getName: " + remoteUser + "<br>");
      out.println("getAuthType: " + request.getAuthType() + "<br><br>");NONE.
    try {
        request.login("usuario1", "clave1"); //manda cookie
      }
      catch(ServletException ex) {
        out.println("No se completó el login. <br>");
        return;
      }
      out.println("<h2>Despues de hacer <strong>login</strong>:</h2>");
      out.println("IsUserInRole rol1: " + request.isUserInRole("rol1") + "<br>");
      out.println("getRemoteUser: " + request.getRemoteUser() + "<br>");
      principal = request.getUserPrincipal();
      remoteUser = null;
      if( principal != null )
        remoteUser = principal.getName();
      out.println("getUserPrincipal.getName: " + remoteUser + "<br>");
      out.println("getAuthType: " + request.getAuthType() + "<br><br>");
    request.logout();
      out.println("<h2>Despues de hacer <strong>logout</strong>:</h2>");
      out.println("IsUserInRole rol1: " + request.isUserInRole("rol1") + "<br>");
      out.println("getRemoteUser: " + request.getRemoteUser() + "<br>");
      principal = request.getUserPrincipal();
      remoteUser = null;
      if( principal != null )
          remoteUser = principal.getName();
      out.println("getUserPrincipal.getName: " + remoteUser + "<br>");
      out.println("getAuthType: " + request.getAuthType() + "<br><br>");
       }
       finally {
       out.close();
       }
   }
}
