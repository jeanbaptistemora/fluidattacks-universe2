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
            SqlDataReader dr = command.ExecuteReader();
            string data = dr.GetString(1);
            string[] names = data.Split('-');
            badSqlCommand.CommandText += "update users set hitcount=hitcount+1 where name='" + names[i] + "';";
            var affectedRows = badSqlCommand.ExecuteNonQuery();
        }
    }
}
