using System.Net;
using System;
namespace cookies
{

    public class CookieExample
    {
        public static void Main(string[] args)
        {
            var test = true;
            var secure_cookie = new HttpCookie(key , value);
            secure_cookie.Expires = DateTime.Now.AddDays(expireDay);
            secure_cookie.HttpOnly = true;
            secure_cookie.Secure = true;

            var insecure_cookie = new HttpCookie(key , value);
            insecure_cookie.Expires = DateTime.Now.AddDays(expireDay);
            insecure_cookie.HttpOnly = true;

            var insecure = new HttpCookie(key , value);

            var secure_cookie2 = new HttpCookie(key , value);
            secure_cookie2.Expires = DateTime.Now.AddDays(expireDay);
            secure_cookie2.HttpOnly = test;
            secure_cookie2.Secure = test;

            var insecure_cookie2 = new HttpCookie(key , value);
            insecure_cookie2.Expires = DateTime.Now.AddDays(expireDay);
            insecure_cookie2.HttpOnly = test;

            var insecure2 = new HttpCookie(key , value);
            insecure2.Expires = DateTime.Now.AddDays(expireDay);
        }
    }
}
