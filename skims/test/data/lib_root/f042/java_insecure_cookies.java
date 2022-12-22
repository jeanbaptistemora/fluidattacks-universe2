import java.util.Random;

public class test42 extends HttpServlet {

	public void doPost(HttpServletRequest request, HttpServletResponse response) {

		cookie.setSecure(false);
		cookie.setHttpOnly(true);
		response.addCookie(cookie);

	}

}
