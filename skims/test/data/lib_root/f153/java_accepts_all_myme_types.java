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

  // Line 29 should be marked
  public HttpRequest headerUse(String url) throws IOException {
    HttpRequest request = HttpRequest.post(url);
    request.header("Accept","*/*");
    return request;
  }

  // Line 37 should be marked
  public HttpRequest chainOfMethods(String url) throws IOException {
    HttpRequest request = HttpRequest.newBuilder()
      .setHeader("X-Our-Header-1", "value1")
      .setHeader("Accept","*/*")
      .uri(new URI(url)).build();
    return request;
  }

  // line 46 should be marked
  public HttpRequest chainOfMethodsII(String url) throws IOException {
    HttpRequest request = HttpRequest.post(url)
      .header("X-Our-Header-1", "value1")
      .header("Accept","*/*")
      .uri(new URI(url)).build();
    return request;
  }
}
