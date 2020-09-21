import java.io.*;
import java.net.*;
import java.util.*;
import javax.servlet.*;
import javax.servlet.http.*;

public class HPP2 extends HttpServlet
{
  public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
  {
    PrintWriter out = response.getWriter();
    String amount = URLEncoder.encode(request.getParameter("amount"), "UTF-8");
    String beneficiary = URLEncoder.encode(request.getParameter("recipient"), "UTF-8");
    URL url = new URL("http://ejemplo.com/");
    out.println(httpRequest(url, "action=transfer&amount=" + amount + "&recipient=" + beneficiary));
  }

  public String httpRequest(URL url, String post)
  {
    String data = "";
    try
    {
      URLConnection conn = url.openConnection();
      conn.setDoOutput(true);
      OutputStreamWriter wr = new OutputStreamWriter(conn.getOutputStream());
      wr.write(post);
      wr.flush();
      BufferedReader rd = new BufferedReader(new
      InputStreamReader(conn.getInputStream()));
      String line = "";
      while ((line = rd.readLine()) != null)
      {
        data += line;
      }
      wr.close();
      rd.close();
    }
    catch (IOException e) {}
    finally
    {
      return data;
    }
  }
}
