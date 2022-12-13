using System;
class cipher{

   public void Encrypt()
	{
      var insecure_rsa = new RSACryptoServiceProvider();
      var secure_rsa = new RSACryptoServiceProvider(2048);

		var insecure_dsa = new DSACng(1024);
      var secure_dsa = new DSACng();
      var secure_dsa2 = new DSACng(2048);

      var insecure_rsa = new RSACng(1024);
      int key = 1024;
      var insecure_rsa2 = new RSACng(key);
      var secure_rsa = new RSACng();
      int secure_key = 2048;
      var secure_rsa2 = new RSACng(secure_key);
	}
}
