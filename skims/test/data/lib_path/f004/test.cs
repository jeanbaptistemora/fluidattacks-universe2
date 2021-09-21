using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;

namespace WebApplicationDotNetCore.Controllers
{
    public class RSPEC2076OSCommandInjectionNoncompliantController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }

        public IActionResult Run(HttpRequest binary)
        {
            Process p = new Process();
            p.StartInfo.FileName = binary;
            p.StartInfo.RedirectStandardOutput = true;
            p.Start();
            string output = p.StandardOutput.ReadToEnd();
            p.Dispose();

            return View();
        }
    }
}
