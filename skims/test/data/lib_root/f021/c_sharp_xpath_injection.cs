using System;
using System.Xml.XPath;

public partial class WebForm : System.Web.UI.Page
{

    protected void Page_Load()
    {
        string operation = Request.Form["operation"];
        XPathNavigator AuthorizedOperations  = new XPathNavigator();
        // Must report
        XPathNavigator node = AuthorizedOperations.SelectSingleNode(operation);
    }
}
