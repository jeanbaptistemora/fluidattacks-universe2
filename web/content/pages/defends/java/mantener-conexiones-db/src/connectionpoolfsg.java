import java.io.*;
import java.sql.*;
import javax.servlet.*;
import javax.servlet.http.*;
import org.apache.tomcat.jdbc.pool.*;

public class ConnectionPoolFSG extends HttpServlet {
  private Connection con = null;

  public void init(ServletConfig config) throws ServletException {
      super.init(config);
      try {
      PoolProperties pool = new PoolProperties();
      pool.setDriverClassName("com.mysql.jdbc.Driver");
      pool.setUrl("jdbc:mysql://localhost:3306/fluid");
      pool.setUsername("fsg");
      pool.setPassword("fsg-test-2011");
      pool.setInitialSize(10);
      pool.setMaxActive(100);
      DataSource dataSource = new DataSource();
      dataSource.setPoolProperties(pool);
      con = dataSource.getConnection();
    }
      catch (SQLException e) {
        throw new ServletException(e);
      }
  }

  public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
       response.setContentType("text/html");
       HtmlSQLResult result = new HtmlSQLResult("SELECT id, name, password FROM users",con);
       PrintWriter out = response.getWriter();
       out.println(result);
  }

  public void destroy() {
      try {
        if (con != null) {
          con.close();
      }
    }
    catch (SQLException e) {
      // Silently ignore -- there's nothing to be done.
    }
}
