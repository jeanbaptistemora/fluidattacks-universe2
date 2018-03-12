using System.Security.Cryptography;

public static string Encrypt(string plainText, string passPhrase, string saltValue, string hashAlgorithm, int passwordIterations, string initVector, int keySize)
  byte[] initVectorBytes = Encoding.ASCII.GetBytes(initVector);
  byte[] saltValueBytes  = Encoding.ASCII.GetBytes(saltValue);
  byte[] plainTextBytes  = Encoding.UTF8.GetBytes(plainText);
  PasswordDeriveBytes password = new PasswordDeriveBytes(passPhrase,saltValueBytes,hashAlgorithm,passwordIterations);
  byte[] keyBytes = password.GetBytes(keySize / 8);
  RijndaelManaged symmetricKey = new RijndaelManaged();
  symmetricKey.Mode = CipherMode.CBC;
  ICryptoTransform encryptor = symmetricKey.CreateEncryptor(keyBytes, initVectorBytes);
  MemoryStream memoryStream = new MemoryStream();
  CryptoStream cryptoStream = new CryptoStream(memoryStream, encryptor, CryptoStreamMode.Write);
  cryptoStream.Write(plainTextBytes, 0, plainTextBytes.Length);
  cryptoStream.FlushFinalBlock();
  byte[] cipherTextBytes = memoryStream.ToArray();
  memoryStream.Close();
  cryptoStream.Close();
  string cipherText = Convert.ToBase64String(cipherTextBytes);
  return cipherText;
}
