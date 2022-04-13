using System;

namespace API
{
    public class Program
    {
        public static void Main()
        {
            BuildWebHost();
        }

        public static IWebHost BuildWebHost() =>
            WebHost.CreateDefaultBuilder()
                   .UseSetting(WebHostDefaults.DetailedErrorsKey, "true")
                   .Build();
    }
}
