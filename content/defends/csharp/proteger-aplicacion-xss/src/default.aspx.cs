using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using Microsoft.Security.Application;

namespace WebApplication2
{
    public partial class _Default : Page
    {
        public string out_Name;
        protected void Page_Load(object sender, EventArgs e)
        {
            out_Name = Encoder.HtmlEncode(Request.QueryString["name"]);
        }
    }
}
