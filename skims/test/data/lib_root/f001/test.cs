using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WebApplication1.Controllers;

namespace WebApplicationDotNetCore.Controllers
{
    public class RSPEC3649SQLiNoncompliant
    {
        public IActionResult Authenticate(UserAccountContext context, string user)
        {
            string insecure_query = "SELECT * FROM Users WHERE Username = '" + user + "'";

            insecure_obj = new SqlCommand(insecure_query);

            insecure_methd = sqcontext.Database.ExecuteSqlCommand(insecure_query);

            string secure_query = "UPDATE Sales.Store SET Demographics = @demographics " + "WHERE CustomerID = @ID;";

            secure_obj = new SqlCommand(secure_query);

            secure_methd = sqcontext.Database.ExecuteSqlCommand(secure_query);
        }
    }
}
