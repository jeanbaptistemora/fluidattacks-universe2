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

            if (!whiteList.Contains(url))
            {
                return BadRequest();
            }
            //secure
            WebRequest request = WebRequest.Create(url);
        }
    }
}
