using System.Net.Http;

class ExampleClass
{
    void ExampleMethod()
    {
        WinHttpHandler winHttpHandler = new WinHttpHandler();
        winHttpHandler.CheckCertificateRevocationList = false;
        HttpClient httpClient = new HttpClient(winHttpHandler);
    }
}
