package test;

import java.io.IOException;
import java.io.PrintWriter;
import avax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/TestLogin")

public class TestLogin extends HttpServlet {
  public TestLogin() {
    super();
  }

  protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    PrintWriter out = response.getWriter();
    response.setContentType("text/html;charset=UTF-8");
  String user = request.getParameter("user");
  String pass = request.getParameter("pass");
  try {
     request.login(user, pass);
     out.println("Login exitoso");
    }
    catch (Exception e) {
      //throw new ServletException(e);
      out.println("Login fallido");
    }
    finally {
      request.logout();
      out.close();
    }
  }
}
