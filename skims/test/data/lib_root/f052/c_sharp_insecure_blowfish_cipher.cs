using System;
using System.Security.Cryptography;

namespace BlowfishExample
{
    class Program
    {
        static void Main(string[] args)
        {
            string original = "This is the original message";
            string password = "secret password";

            // Encrypt the message
            byte[] encrypted = Encrypt(original, password);
            Console.WriteLine("Encrypted message: " + Convert.ToBase64String(encrypted));

            // Decrypt the message
            string decrypted = Decrypt(encrypted, password);
            Console.WriteLine("Decrypted message: " + decrypted);
        }

        public static byte[] Encrypt(string original, string password)
        {
            using (Blowfish blowfish = new Blowfish(password))
            {
                return blowfish.Encrypt(System.Text.Encoding.UTF8.GetBytes(original));
            }
        }

        public static string Decrypt(byte[] encrypted, string password)
        {
            using (Blowfish blowfish = new Blowfish(password))
            {
                return System.Text.Encoding.UTF8.GetString(blowfish.Decrypt(encrypted));
            }
        }
    }
}
