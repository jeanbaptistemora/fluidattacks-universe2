using System;

public class ExampleClass
{
    public void ExampleMethod()
    {
        AppContext.SetSwitch("Switch.System.ServiceModel.DisableUsingServicePointManagerSecurityProtocols", true);
    }
}
