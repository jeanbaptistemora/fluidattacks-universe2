using Newtonsoft.Json;

public class ExampleClass
{

    public void ExampleClass()
    {
        var Settings = new JsonSerializerSettings();
        Settings.TypeNameHandling = TypeNameHandling.All;
    }
}
