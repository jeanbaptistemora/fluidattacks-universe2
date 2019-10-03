using System;
using System.Collections.Generic;
using System.Web;
using System.Web.Security;

namespace Core {
  public class SessionManagerModule :IHttpModule {
    public SortedDictionary<string, SessionContext> ASPNETContext { get; set; }
    #region IHttpModule Members
      public void Init(HttpApplication context) {
        // Initializes the Application variable
        if (context.Application["sessionSortedList"] == null) {
          ASPNETContext = new System.Collections.Generic.SortedDictionary<string, SessionContext>();
          context.Application["sessionSortedList"] = ASPNETContext;
        }
        context.PostAcquireRequestState += new EventHandler(context_PostAcquireRequestState);
      }
      void context_PostAcquireRequestState(object sender, EventArgs e) {
        HttpApplication application = (HttpApplication)sender;
        // Get the Application Context variable
        var ASPNETContext = (SortedDictionary<string, SessionContext>)application.Application["sessionSortedList"];
        HttpContext context = application.Context;
        string filePath = context.Request.FilePath;
        string fileExtension = VirtualPathUtility.GetExtension(filePath);

        if (fileExtension.Equals(".aspx")) {
          if (application.Context.Session != null) {
            // Get the User Name
            string userName = (application.Session != null) ? (string)application.Session["userName"] : string.Empty;
            userName = userName ?? string.Empty;
            //Try to get the current session
            SessionContext currentSessionContext = null;
            ASPNETContext.TryGetValue(userName, out currentSessionContext);

            if (currentSessionContext != null) {
              // Validates old sessions
              bool session = currentSessionContext.SessionID == application.Session.SessionID;
              if (!session) {
                // Sing out
                FormsAuthentication.SignOut();
                // Remove from Session
                application.Session.Clear();
                application.Session.Abandon();
                application.Context.Response.Cookies["ASP.NET_SessionId"].Value = "";
                // Redirect
                FormsAuthentication.RedirectToLoginPage();
              }
            }
          }
        }
      }
    public void Dispose() { }
    #endregion
  }
}
