using TestCaseSupport;
using System;
using System.Data.SqlClient;
using System.Data;
using System.Web;


namespace testcase
{
    class testcasef001
    {
        public override void Bad(HttpRequest req, HttpResponse resp)
        {
            string data = req.QueryString["id"];
            string root = "path/";
            if (File.Exists(root + data))
            {
                IO.WriteLine(sr.ReadLine());
            }
        }
    }
}
