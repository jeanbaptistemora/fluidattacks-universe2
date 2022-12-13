using System.Text.RegularExpressions;
namespace Controllers
{
    public class Controller : Controller
    {
        public IActionResult Validate(string regex, string input)
        {
            Regex myreg = new Regex(regex, RegexOptions.IgnoreCase);
            bool unsafe = myreg.IsMatch("testing");

            bool unsafe2 = myreg.Matches("testing", regex);

            var expreg = @"^(([a-z])+.)+[A-Z]([a-z])+$";
            bool unsafe3 = myreg.Match("testing", expreg);

            Regex anotherDangerous = new Regex(expreg, RegexOptions.IgnoreCase);
            bool unsafe4 = anotherDangerous.Match("testing");

            bool safe = myreg.IsMatch("testing", reg.Escape(expreg));

            string safeInput = reg.Escape(expreg);
            bool safe2 = myreg.IsMatch(input, safeInput);

            bool safe3 = myreg.IsMatch("testing", expreg, RegexOptions.IgnoreCase, TimeSpan.FromSeconds(1));

            Regex myreg2 = new Regex(regex, RegexOptions.IgnoreCase, TimeSpan.FromSeconds(1));
            bool safe4 = myreg2.IsMatch(input, regex);
        }
    }
}
