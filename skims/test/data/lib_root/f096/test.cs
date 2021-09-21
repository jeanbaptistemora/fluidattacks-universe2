using System.Runtime.Serialization.Formatters.Binary;
using System.Web.UI;
namespace Controllers
{
    public class Encrypt
    {
        public static void Process(string secret)
        {
            var mac_false = false;
            var mac_true = true;
            BinaryFormatter formatter_vuln1 = new BinaryFormatter();
            LosFormatter formatter_secure1 = new LosFormatter(true, secret);
            LosFormatter formatter_vuln2 = new LosFormatter(false, secret);
            LosFormatter formatter_secure2 = new LosFormatter(mac_true, secret);
            LosFormatter formatter_vuln3 = new LosFormatter(mac_false, secret);

        }
    }
}
