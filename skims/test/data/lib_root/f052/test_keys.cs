using System;
class cipher{

   public void Encrypt()
	{
      var rsa1 = new RSACryptoServiceProvider();
		var dsa1 = new DSACng();
      var dsa2 = new DSACng(2048);
		var dsa3 = new DSACng(1024);
      var rsa1 = new RSACryptoServiceProvider(2048);
      var rsa2 = new RSACng();
      var rsa2 = new RSACng(1024);
	}
}
