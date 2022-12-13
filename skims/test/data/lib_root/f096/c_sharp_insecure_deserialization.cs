using System.Runtime.Serialization.Formatters.Binary;
using System.Runtime.Serialization.IFormatter;
namespace Controllers
{
    public class Encrypt
    {
        public static void Process(string secret)
        {
            BinaryFormatter formatter = new BinaryFormatter();
            LosFormatter formatter2 = new LosFormatter();
            SoapFormatter formatter3 = new SoapFormatter();
            NetDataContractSerializer formatter4  = new NetDataContractSerializer();
        }
    }
}
