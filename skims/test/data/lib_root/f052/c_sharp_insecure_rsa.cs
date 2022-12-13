using System;
class jwtbuild {

   public static void Main() {

	   RSACryptoServiceProvider RSA2 = new RSACryptoServiceProvider();
	   var secure_enc = RSA2.Encrypt(dataToEncrypt, true);

	   RSACryptoServiceProvider RSA3 = new RSACryptoServiceProvider();
	   var insecure_enc = RSA3.Encrypt(dataToEncrypt, false);

		 bool key_eval = false;
		 var insecure_enc2 = RSA3.Encrypt(dataToEncrypt, key_eval);
   }
}
