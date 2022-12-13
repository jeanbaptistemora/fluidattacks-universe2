using System.Net;
using System;
namespace testmod
{

    public class Controllers
    {
        public void ReadContentOfURL(HttpRequest url)
        {
            //insecure
            WebRequest req = WebRequest.Create(url);

            //secure
            string staticUrl = "https://someurl.com";
            WebRequest request = WebRequest.Create(staticUrl);
        }
    }
}
