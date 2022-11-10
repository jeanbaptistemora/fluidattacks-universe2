using System;
using System.IO;
using System.Security.Cryptography;
class Test {
   public static void insecure() {
      AesManaged aes_insecure = new AesManaged
      {
         KeySize = 128,
         BlockSize = 128,
         Mode = CipherMode.CBC,
         Padding = PaddingMode.PKCS7
      };

      var cipher_mode = CipherMode.OFB;

      AesManaged aes_insecure1 = new AesManaged
      {
         KeySize = 128,
         BlockSize = 128,
         Mode = cipher_mode,
         Padding = PaddingMode.PKCS7
      };

      AesManaged aes_insecure2 = new AesManaged();
      aes_insecure2.BlockSize = 128;
      aes_insecure2.KeySize = 128;
      aes_insecure2.Mode = cipher_mode;

   }

   public static void secure() {
      AesManaged aes_secure = new AesManaged
      {
         KeySize = 128,
         BlockSize = 128,
         Mode = CipherMode.CTS,
         Padding = PaddingMode.PKCS7
      };
   }
}
