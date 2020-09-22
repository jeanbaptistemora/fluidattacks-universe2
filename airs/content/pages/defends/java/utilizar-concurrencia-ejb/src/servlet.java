import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;

public class Servlet extends HttpServlet {

    public void doGet(HttpServletRequest request, HttpServletResponse response)
    throws IOException, ServletException
    {
        response.setContentType("text/html; charset=ISO-8859-1");

        PrintWriter out = response.getWriter();
        //se instancia la clase Cliente que es la que se comunica con el EJB.
        Cliente cl = new Cliente();
        out.println("iniciaProceso");
        cl.Inicio();
        out.close();
    }
}
