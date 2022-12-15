namespace Controllers
{
    public class Calculate
    {
        public static void ProcessRequest(HttpRequest req, HttpResponse res)
        {
            string name = req.QueryString["name"];
            res.Write("Hello " + name);

            string value = req.QueryString["value"];
            res.AddHeader("X-Header", value);
        }
    }
}
