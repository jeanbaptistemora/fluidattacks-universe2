using System;

namespace AspNet5SQLite
{
    public class Startup
    {

        public void ConfigureServices(IServiceCollection services)
        {
            services.AddCors();

            var policy = new Microsoft.AspNetCore.Cors.Infrastructure.CorsPolicy();

            policy.Headers.Add("*");
            policy.Methods.Add("*");
            policy.Origins.Add("*");
            policy.SupportsCredentials = true;

            services.AddCors(x => x.AddPolicy("corsGlobalPolicy", policy));

        }
    }
}
