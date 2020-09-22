import java.io.*;
import java.net.*;
import java.util.*;
import javax.servlet.*;
import javax.servlet.http.*;

public class HPP extends HttpServlet
{
  public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
  {
    String queryString = request.getQueryString();
    PrintWriter out = response.getWriter();
    if (checkPollution(queryString))
    {
       out.println("HTTP Parameter Pollution detected.");
    }
    else
    {
      out.println("HTTP Parameter Pollution not detected.");
    }
  }

  private boolean checkPollution(String queryString) throws UnsupportedEncodingException
  {
     if (queryString != null)
     {
        ArrayList<String> keys = new ArrayList<String>();
        String urlDecoded = URLDecoder.decode(queryString, "UTF-8");
        String[] key;
        for (String param : urlDecoded.split("&"))
        {
        String key = param.split("=");
        if (key.length > 0)
        {
            if (keys.contains(key[0]))
              return true;
            else
            keys.add(key[0]);
          }
       }
     }
     return false;
  }
}
