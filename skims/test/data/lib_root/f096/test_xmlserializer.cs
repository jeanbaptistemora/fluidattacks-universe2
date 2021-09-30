public class XmlSerializerTestCase : Controller
{
    public ActionResult unsecuredeserialization(HttpRequest typeName)
    {
        //insecure
        Tpe t = Type.GetType(typeName);
        XmlSerializer serializer = new XmlSerializer(t);

        //insecure
        XmlSerializer serializer = new XmlSerializer(Type.GetType(typeName));

        //secure
        ExpectedType obj = null;
        XmlSerializer serializer = new XmlSerializer(typeof(ExpectedType));
    }
}
