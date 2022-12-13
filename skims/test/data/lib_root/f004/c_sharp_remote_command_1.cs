using System.Diagnostics;

namespace Application
{
    public class Executor
    {

        public bool Execute(HttpRequest req)
        {
            string command = req.QueryString["command"];
            var p = Diagnostics.Process.Start(command);
            var executor = new Executor();
            var result = executor.Execute(command);
        }
    }
}
