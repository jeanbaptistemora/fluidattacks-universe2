using System.Security.Cryptography.X509Certificates;
using System.Net;

public class MyPolicy : ICertificatePolicy {
  public bool CheckValidationResult(ServicePoint srvPoint,
    X509Certificate certificate, WebRequest request,
    int certificateProblem) {
      return true;
    }
}
