public class test extends HttpServlet {

  // lines 7 and 10 should be marked
	private HttpGet urlConnection(String url) throws IOException {
    URL uc = new URL(url);
    HttpGet req = new HttpGet(uc);
    req.setHeader("Accept","*/*");

    HttpUriRequest reqII = new HttpUriRequest(uc);
    reqII.addHeader("Accept","*/*");

    return req;
  }

  // line 20 should be marked
  public HttpHeaders getMultipartHeaders(String paramOrFileName) {
    String contentType = getMultipartContentType(paramOrFileName);
    if (contentType != null) {
      HttpHeaders headers = new HttpHeaders();
      headers.add("Accept","*/*");
      return headers;
    }
    else {
      return null;
    }
  }

  // Safe implementations, no lines should be marked
	private HttpGet urlConnection(String url) throws IOException {
    URL uc = new URL(url);
    HttpGet req = new HttpGet(uc);
    req.setHeader("Custom","*/*");

    HttpUriRequest reqII = new HttpUriRequest(uc);
    reqII.addHeader("X-Our-Header-1", "value1");

    return req;
  }
}
