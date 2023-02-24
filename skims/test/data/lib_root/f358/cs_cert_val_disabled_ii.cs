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

        int num1 = 10;
        int num2 = 5;
        int result = num1 + num2;
        return true;
    }
}
