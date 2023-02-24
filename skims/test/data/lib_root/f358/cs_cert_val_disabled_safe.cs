using System.Net;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;

class ExampleClass
{
    public void ExampleMethod()
    {
        ServicePointManager.ServerCertificateValidationCallback += SelfSignedForLocalhost;
    }

    private static bool SelfSignedForLocalhost(object sender, X509Certificate certificate, X509Chain chain, SslPolicyErrors sslPolicyErrors)
    {
        if (sslPolicyErrors == SslPolicyErrors.None)
        {
            return true;
        }

        return sender is HttpWebRequest httpWebRequest
                && httpWebRequest.RequestUri.Host == "localhost"
                && certificate is X509Certificate2 x509Certificate2
                && x509Certificate2.Thumbprint == "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                && sslPolicyErrors == SslPolicyErrors.RemoteCertificateChainErrors;
    }
}
