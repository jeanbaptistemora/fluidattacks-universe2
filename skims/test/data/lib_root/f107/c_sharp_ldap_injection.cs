using System;
using System.DirectoryServices;

public partial class WebForm : System.Web.UI.Page
{
    protected void Page_Load(HttpRequest Request)
    {
        string userName = Request.Params["user"];
        string filter = "(uid=" + userName + ")";
        DirectorySearcher searcher = new DirectorySearcher(filter);
        SearchResultCollection results = searcher.FindAll();
    }
}
