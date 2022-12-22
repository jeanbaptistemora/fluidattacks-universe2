import java.io.IOException;
import javax.servlet.http.HttpServletRequest;

public class test extends HttpServlet {

  public void runUnsafe(HttpServletRequest request, HttpServletResponse response) throws IOException {

    param = request.getHeader("someheader");
    ProcessBuilder pb = new ProcessBuilder();
    pb.command(param);

  }

}
