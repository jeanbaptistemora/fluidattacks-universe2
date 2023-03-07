public class TestHttpAccept
{

	public HttpClientMustFail()
	{
		HttpClient = new HttpClient();
		HttpClient.DefaultRequestHeaders.Add("Accept", "*/*");
	}

  public HttpClientMustFailII()
	{
		HttpClientII = new HttpClient();
		HttpClientII.DefaultRequestHeaders.Accept.Clear();
    HttpClientII.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("*/*"));
	}
  public RequestMessageMustFail()
	{
		HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Get, "https://www.example.com");
    request.Headers.Accept.Clear();
    request.Headers.Accept.Add(new MediaTypeWithQualityHeaderValue("*/*"));

	}
  public RequestMessageMustFailII()
	{
		HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Get, "https://www.example.com");
    request.Headers.Accept.Clear();
    request.Headers.Accept.Add(new MediaTypeWithQualityHeaderValue("*/*"));

	}

	public WebClientMustFail()
	{
		WebClient client = new WebClient();
		client.Headers.Clear();
		client.Headers.Add("Accept", "*/*");

	}
}
