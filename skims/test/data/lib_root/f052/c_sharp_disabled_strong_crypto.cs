using System;

public class ExampleClass
{
    public void ExampleMethod()
    {
        AppContext.SetSwitch("Switch.System.Net.DontEnableSchUseStrongCrypto", true);
    }
}
