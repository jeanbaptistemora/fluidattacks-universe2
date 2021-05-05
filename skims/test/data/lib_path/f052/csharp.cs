using System.Security.Cryptography;

namespace Cypher_Example
{
    class CypherExample
    {
        public static void Main()
        {
            MD5 myAes = MD5.Create();
            SHA1 myAes = SHA1.Create();
            HMACMD5 myAes = HMACMD5.Create();
            DES myAes = DES.Create();
            TripleDES myAes = TripleDES.Create();
            var hashProvider3 = new SHA1Managed();
            var hashProvider3 = new RC2CryptoServiceProvider();
        }
    }
}
