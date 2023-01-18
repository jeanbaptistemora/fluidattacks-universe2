using System.Text.RegularExpressions;
namespace Controllers
{
    public class Controller : Controller
    {
        public IActionResult Validate(HttpRequest req, string regex)
        {
            string input = req.QueryString["command"];
            var pattern = @"^(([a-z])+.)+[A-Z]([a-z])+$";

            Regex myreg = new Regex(pattern, RegexOptions.IgnoreCase);
            bool unsafe = myreg.IsMatch(input);

            bool unsafe2 = myreg.Matches(input, pattern);
            bool unsafe3 = myreg.Match(input, @"^(([a-z])+.)+");

            bool safe = myreg.IsMatch("mystring", pattern);

            string safeInput = reg.Escape(pattern);
            bool safe2 = myreg.IsMatch(input, safeInput);

            bool safe3 = myreg.IsMatch(input, pattern, RegexOptions.IgnoreCase, TimeSpan.FromSeconds(1));

            Regex myreg2 = new Regex(pattern, RegexOptions.IgnoreCase, TimeSpan.FromSeconds(1));
            bool safe4 = myreg2.IsMatch(input);
        }
    }
}
