using System;
using System.IO;
using System.Security.Cryptography;
class ManagedAesSample {

   public static void Main() {
      var cipher_mode = CipherMode.OFB;

      AesManaged aes_secure = new AesManaged
      {
         KeySize = 128,
         BlockSize = 128,
         Mode = CipherMode.CBC,
         Padding = PaddingMode.PKCS7
      };

      AesManaged aes_secure2 = new AesManaged
      {
         KeySize = 128,
         BlockSize = 128,
         Mode = CipherMode.CTS,
         Padding = PaddingMode.PKCS7
      };

      AesManaged aes_insecure = new AesManaged
      {
         KeySize = 128,
         BlockSize = 128,
         Mode = CipherMode.ECB,
         Padding = PaddingMode.PKCS7
      };

      AesManaged aes_insecure2 = new AesManaged
      {
         KeySize = 128,
         BlockSize = 128,
         Mode = CipherMode.CFB,
         Padding = PaddingMode.PKCS7
      };

      AesManaged aes_insecure3 = new AesManaged
      {
         KeySize = 128,
         BlockSize = 128,
         Mode = CipherMode.OFB,
         Padding = PaddingMode.PKCS7
      };

      AesManaged aes_insecure4 = new AesManaged
      {
         KeySize = 128,
         BlockSize = 128,
         Mode = cipher_mode,
         Padding = PaddingMode.PKCS7
      };

      AesManaged aes_insecure5 = new AesManaged();
      aes_insecure5.BlockSize = 128;
      aes_insecure5.KeySize = 128;
      aes_insecure5.Mode = cipher_mode;
   }
}
