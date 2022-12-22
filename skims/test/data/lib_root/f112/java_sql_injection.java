import java.util.Random;

public class test112 extends HttpServlet {

	public void doPost(HttpServletRequest request, HttpServletResponse response) {

		param = request.getHeader("search");
		String sql = "{call " + param + "}";
		java.sql.Connection connection = org.owasp.benchmark.helpers.DatabaseHelper.getSqlConnection();
		java.sql.CallableStatement statement = connection.prepareCall( sql );
		java.sql.ResultSet rs = statement.executeQuery();

	}

}
