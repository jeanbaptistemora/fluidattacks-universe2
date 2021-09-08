using System.Text.RegularExpressions;
namespace Controllers
{
    public class Controller : Controller
    {
        public IActionResult Validate(string regex, string input)
        {
            var expreg = @"\b(?<word>\w+)\s+(\k<word>)\b";

            Regex reg = new Regex(pat, RegexOptions.IgnoreCase);

            bool match = reg.IsMatch("testing", @"\b(?<word>\w+)\s+(\k<word>)\b");
            bool match2 = reg.IsMatch(input, expreg);
            bool match3 = reg.IsMatch(input, reg.Escape(regex));
        }
    }
}
