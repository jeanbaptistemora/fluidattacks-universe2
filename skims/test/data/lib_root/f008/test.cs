namespace Controllers
{
    public class Calculate
    {
        public static void ProcessRequest(HttpRequest req, HttpResponse res)
        {
            string name = req.QueryString["name"];
            res.Write("Hello " + name);

            string value = req.QueryString["value"];
            if (value == null || !Regex.IsMatch(value, "^[a-zA-Z0-9]+$"))
            {
              throw new InvalidOperationException("Invalid value");
            }
            res.AddHeader("X-Header", value);
        }
    }
}
