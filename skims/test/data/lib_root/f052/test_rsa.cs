using System;
class jwtbuild {

   public static void Main() {

	   RSACryptoServiceProvider RSA2 = new RSACryptoServiceProvider();
	   encryptedData = RSA2.Encrypt(dataToEncrypt, true);

	   RSACryptoServiceProvider RSA3 = new RSACryptoServiceProvider();
	   enc = RSA3.Encrypt(dataToEncrypt, false);
   }
}
