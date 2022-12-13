import java.util.Random;

public class BenchmarkTest00167 extends HttpServlet {
	@Override
	public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		long l = new java.util.Random().nextLong();
		String rememberMeKey = Long.toString(l);
		String cookieName = "rememberMe";
    request.getSession().setAttribute(cookieName, rememberMeKey);
	}
}
