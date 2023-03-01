import java.util.Random;

public class test112 extends HttpServlet {

  // line 11 should be marked
	private HttpURLConnection urlConnectionNcnp(String url) throws IOException {
    URL uc = new URL(url);
    HttpURLConnection huc = (HttpURLConnection) uc.openConnection();
    huc.setRequestMethod("GET");
    huc.setRequestProperty(GITLAB_PRIVATE_TOKEN, configProperties.getRepository());
    huc.setRequestProperty("Accept","*/*");
    return huc;
  }

  // Line 19 should be marked
  private URLConnection urlConnection(String url) throws IOException {
    URLConnection connection = new URL(url).openConnection();
    connection.setDoOutput(true);
    connection.setRequestProperty("Accept","*/*");
    return connection;
  }

  // Line 26 should be marked
  public HttpRequest headerUse(String url) throws IOException {
    HttpRequest request = HttpRequest.post(url);
    request.header("Accept","*/*");
    return request;
  }

  // No line of following function should be marked (SAFE)
  private HttpURLConnection urlConnectionNcnpII(String url) throws IOException {
    URL uc = new URL(url);
    HttpURLConnection huc = (HttpURLConnection) uc.openConnection();
    huc.setRequestMethod("GET");
    huc.setRequestProperty(GITLAB_PRIVATE_TOKEN, configProperties.getRepository());
    huc.setRequestProperty("Accept","text/html");
    huc.setRequestProperty("Custom","*/*");
    return huc;
  }

}
