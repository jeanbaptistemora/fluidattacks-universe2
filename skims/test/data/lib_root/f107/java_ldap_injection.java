import java.util.Random;

public class test107 extends HttpServlet {

	public void doPost(HttpServletRequest request, HttpServletResponse response) {

		java.util.Enumeration<String> headers = request.getHeaders("BenchmarkTest00012");

		if (headers != null && headers.hasMoreElements()) {
			param = headers.nextElement();
		}

		String filter = "(&(objectclass=person))(|(uid="+param+")(street={0}))";
		javax.naming.NamingEnumeration results = idc.search(base, filter);

	}

}
