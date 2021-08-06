using System.Net;
using System;
namespace cookies
{

    public class CookieExample
    {
        public static void Main(string[] args)
        {
            var secure_cookie = new HttpCookie(key , value);
            secure_cookie .Expires = DateTime.Now.AddDays(expireDay);
            secure_cookie .HttpOnly = true;
            secure_cookie .Secure = true;

            var insecure_cookie = new HttpCookie(key , value);
            insecure_cookie .Expires = DateTime.Now.AddDays(expireDay);
            insecure_cookie .HttpOnly = true;

            var insecure = new HttpCookie(key , value);
        }
    }
}
