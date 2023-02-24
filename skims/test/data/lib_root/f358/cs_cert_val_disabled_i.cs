using System.Net;

class ExampleClass
{
    public void ExampleMethod()
    {
        ServicePointManager.ServerCertificateValidationCallback += (sender, cert, chain, error) => { return true; };
    }
}
