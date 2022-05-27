using System;
using System.Web.Configuration;

class TestClass
{
    public void TestMethod()
    {
        HttpRuntimeSection httpRuntimeSection = new HttpRuntimeSection();
        httpRuntimeSection.EnableHeaderChecking = false;
    }
}
