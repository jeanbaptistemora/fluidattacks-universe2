using System;
class TestClass
{
    public void TestMethod(Rfc2898DeriveBytes rfc2898DeriveBytes, string algname, string alghashname, int keySize, byte[] rgbIV)
    {
        System.Security.Cryptography.rfc2898DeriveBytes.CryptDeriveKey(algname, alghashname, keySize, rgbIV);

        byte[] pwd = Encoding.Unicode.GetBytes(Console.ReadLine());

        byte[] salt = CreateRandomSalt(7);

        PasswordDeriveBytes pdb = new PasswordDeriveBytes(pwd, salt);
    }
}
