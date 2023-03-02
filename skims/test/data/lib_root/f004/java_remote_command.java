import java.io.IOException;
import javax.servlet.http.HttpServletRequest;

public class test extends HttpServlet {

  public void runUnsafe(HttpServletRequest request, HttpServletResponse response) throws IOException {

    param = request.getHeader("someheader");
    ProcessBuilder pb = new ProcessBuilder();
    pb.command(param);
    try {
			Process p = pb.start();
			org.owasp.benchmark.helpers.Utils.printOSCommandResults(p, response);
		} catch (IOException e) {
			System.out.println("Problem executing cmdi - java.lang.ProcessBuilder(java.util.List) Test Case");
            throw new ServletException(e);
		}
  }

}
