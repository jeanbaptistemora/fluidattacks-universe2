// Source: https://docs.microsoft.com/en-us/aspnet/web-api/overview/security/enabling-cross-origin-requests-in-web-api
using System;

namespace AspNet5SQLite
{
    public class Startup
    {
        // Setting an insecure cors policy attribute
        public void ConfigureServices(IServiceCollection services)
        {
            var policy = new Microsoft.AspNetCore.Cors.Infrastructure.CorsPolicy();
            policy.Headers.Add("*");
            policy.Origins.Add("*");
            policy.SupportsCredentials = true;

        }
    }

    public class Startup2
    {
        //Setting the insecure cors policy directly
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddCors(options =>
            {
                options.AddPolicy(name: "corsGlobalPolicy",
                    builder =>
                    {
                        builder.WithOrigins(Configuration["Origins:localdev"])
                            .AllowAnyOrigin()
                            .AllowAnyMethod();
                    });
            });
        }

        public void ConfigureServices(IServiceCollection services)
        {
            services.AddCors(c =>
            {
                c.AddPolicy("AllowOrigin", options => options.AllowAnyMethod().AllowAnyHeader().AllowAnyOrigin());
            });
        }
    }

    //Enabling insecure cors policy via attribute
    [EnableCors(origins: "*", headers: "*", methods: "*")]
    public class ItemsController : ApiController
    {
        public HttpResponseMessage GetAll() {}
    }
}
