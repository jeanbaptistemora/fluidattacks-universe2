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
        }
    }
}
