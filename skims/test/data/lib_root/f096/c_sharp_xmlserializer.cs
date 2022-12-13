public class XmlSerializerTestCase : Controller
{
    public ActionResult unsecuredeserialization(HttpRequest typeName)
    {
        //insecure
        Tpe t = Type.GetType(typeName);
        XmlSerializer insec_serial = new XmlSerializer(t);

        //insecure
        XmlSerializer insec_serial2 = new XmlSerializer(Type.GetType(typeName));

        //secure
        ExpectedType obj = null;
        XmlSerializer sec_serial = new XmlSerializer(typeof(HttpRequest));

        //insecure
        var req = new HttpRequest();
        var t2 = Type.GetType(req);
        XmlSerializer insec_serial3 = new XmlSerializer(t2);

        //secure
        string greeting = "hello";
        XmlSerializer sec_serial2 = new XmlSerializer(Type.GetType(greeting));
    }
}
