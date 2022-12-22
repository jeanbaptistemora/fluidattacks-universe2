import java.io.IOException;
import javax.servlet.http.HttpServletRequest;

public class test08 extends HttpServlet {

  public void runUnsafe(HttpServletRequest request, HttpServletResponse response) throws IOException {

    param = request.getHeader("someheader");
    response.setHeader("X-XSS-Protection", "0");
    response.getWriter().format(param);

  }

}
