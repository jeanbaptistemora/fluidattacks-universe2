import java.util.Random;

public class test112 extends HttpServlet {

  // line 11 should be marked
	private HttpRequest urlConnectionTest(String url) throws IOException {
    HttpClient httpClient = HttpClient.newHttpClient();

    HttpRequest request = HttpRequest.newBuilder(url)
      .header("X-Our-Header-1", "value1")
      .header("Accept", "*/*")
      .header("X-Our-Header-2", "value2")
      .uri(new URI(url)).build();

    return httpClient.send(request, HttpResponse.BodyHandlers.ofString());
  }

  // line 23 should be marked
  private HttpRequest urlConnectionTestII(String url) throws IOException {
    HttpClient httpClient = HttpClient.newHttpClient();

    HttpRequest request = HttpRequest.newBuilder(url)
      .setHeader("Accept", "*/*")
      .setHeader("X-Our-Header-1", "value1")
      .setHeader("X-Our-Header-2", "value2")
      .uri(new URI(url)).build();

    return httpClient.send(request, HttpResponse.BodyHandlers.ofString());
  }

  // line 36 should be marked
  private HttpRequest urlConnectionTestIII(String url) throws IOException {
    HttpClient httpClient = HttpClient.newHttpClient();

    HttpRequest request = HttpRequest.newBuilder(url)
      .setHeader("Accept", "*/*")
      .uri(new URI(url)).build();

    return httpClient.send(request, HttpResponse.BodyHandlers.ofString());
  }

  // Headers method - line 47 should be marked
  private HttpRequest urlConnectionTestIII(String url) throws IOException {
    HttpClient httpClient = HttpClient.newHttpClient();

    HttpRequest request = HttpRequest.newBuilder(url)
      .headers("Accept", "*/*", "X-Our-Header-1", "value1", "X-Our-Header-2", "value2")
      .uri(new URI(url)).build();

    return httpClient.send(request, HttpResponse.BodyHandlers.ofString());
  }

  // Headers method II -  line 47 should be marked
  private HttpRequest urlConnectionTestIII(String url) throws IOException {
    HttpClient httpClient = HttpClient.newHttpClient();

    HttpRequest request = HttpRequest.newBuilder(url)
      .headers("X-Our-Header-1", "value1", "Accept", "*/*",  "X-Our-Header-2", "value2")
      .uri(new URI(url)).build();

    return httpClient.send(request, HttpResponse.BodyHandlers.ofString());
  }

  // No line should be marked
  private HttpRequest urlConnectionTestSafe(String url) throws IOException {
    HttpClient httpClient = HttpClient.newHttpClient();

    HttpRequest request = HttpRequest.newBuilder(url)
      .setHeader("Accept","text/html")
      .setHeader("Custom-Header", "*/*")
      .uri(new URI(url)).build();

    return httpClient.send(request, HttpResponse.BodyHandlers.ofString());
  }

  // Headers method Safe-  No line should be marked
  private HttpRequest urlConnectionTestIII(String url) throws IOException {
    HttpClient httpClient = HttpClient.newHttpClient();

    HttpRequest request = HttpRequest.newBuilder(url)
      .headers("Accept","text/html", "X-Our-Header-1", "value1", "X-Our-Header-2", "value2")
      .uri(new URI(url)).build();

    return httpClient.send(request, HttpResponse.BodyHandlers.ofString());
  }
}
