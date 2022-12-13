using System.Web.Script.Serialization;

public class ExampleClass
{
    public T Deserialize<T>(string str)
    {
        JavaScriptSerializer s = new JavaScriptSerializer(new SimpleTypeResolver());
        return s.Deserialize<T>(str);
    }
}
