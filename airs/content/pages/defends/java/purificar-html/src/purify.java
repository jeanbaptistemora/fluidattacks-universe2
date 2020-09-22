import java.io.*;
import java.util.*;
import javax.servlet.*;
import javax.servlet.http.*;
import org.jsoup.*;
import org.jsoup.safety.*;

public class Purify extends HttpServlet
{
  public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
  {
    PrintWriter out = response.getWriter();
    String unsafe = request.getParameter("content");
    Whitelist basicWithImages = Whitelist.basic().addTags(new String[] { "img" })
      .addAttributes("img", new String[] { "align", "alt", "height", "src", "title", "width" })
        .addProtocols("img", "src", new String[] { "http", "https" });
    String safe = Jsoup.clean(unsafe, basicWithImages);
    response.setContentType("text/html");
    out.println(safe);
  }
}
