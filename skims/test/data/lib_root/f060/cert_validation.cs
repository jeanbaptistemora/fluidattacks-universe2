using System;
using System.IO;
using System.Security.Cryptography;
class Test {

  public static void unsafe1() {
    //There is an option in the callback method that sets all certificates to true
    ServicePointManager.ServerCertificateValidationCallback += (sender, certificate, chain, errors) => {return true;};
  }

  public static void unsafe2() {
    // Directly setting the validation to all true
    ServicePointManager.ServerCertificateValidationCallback = (sender, certificate, chain, errors) => true;
  }

  public static void safe() {
    // Trust only some certificates
    ServicePointManager.ServerCertificateValidationCallback +=
    (sender, certificate, chain, errors) =>
    {
        if (development) return true; // for development, trust all certificates
        return errors == SslPolicyErrors.None && validCerts.Contains(certificate.GetCertHashString());
    };
  }
}
