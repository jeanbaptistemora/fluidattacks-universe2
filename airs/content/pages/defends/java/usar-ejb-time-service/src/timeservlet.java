package fsg;

import java.io.IOException;
import javax.ejb.EJB;
import javax.ejb.EJBs;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/Time")
public class TimeServlet extends HttpServlet {
  private static final long serialVersionUID = 1L;

  @EJB
  private TimeService timerEJB;
  public TimeServlet() {
    super();
  }

  protected void doGet(HttpServletRequest request, HttpServletResponse response) throws
     ServletException, IOException {
       response.setContentType("text/html;charset=UTF-8");
       java.io.PrintWriter out = response.getWriter();
       timerEJB.startTimer();
       out.println("Processing the request at: " + new java.util.Date());
       out.close();
    }
}
