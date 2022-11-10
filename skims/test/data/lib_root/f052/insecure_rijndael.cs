using System;
using System.IO;
using System.Security.Cryptography;

class Test {
   public static void Main() {
      RijndaelManaged aes_insecure3 = new RijndaelManaged
      {
         KeySize = 128,
         BlockSize = 128,
         Mode = CipherMode.CTS,
         Padding = PaddingMode.PKCS7
      };
   }
}
