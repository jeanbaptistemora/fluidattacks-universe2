using System;
using System.Text.RegularExpressions;

public partial class WebForm : System.Web.UI.Page
{

    protected void Page_Load(object sender, EventArgs e)
    {
        string findTerm = Request.Form["findTerm"];
        Match m = Regex.Match(SearchableText, "^term=" + findTerm);
    }
}
