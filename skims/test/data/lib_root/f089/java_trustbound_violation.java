import java.io.IOException;
import javax.servlet.http.HttpServletRequest;

public class test89 extends HttpServlet {

  public void runUnsafe(HttpServletRequest request, HttpServletResponse response) throws IOException {

    param = request.getHeader("someheader");
    request.getSession().setAttribute( param, "10340");

  }

}
