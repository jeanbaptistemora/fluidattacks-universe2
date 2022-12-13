using System.Net;
using System;
namespace testmod
{
    public class Controllers
    {
        public void Configure(IApplicationBuilder app)
        {
            // Should report

            var corsBuilder = new CorsPolicyBuilder();
            corsBuilder.AllowAnyHeader();
            corsBuilder.AllowAnyMethod();
            corsBuilder.AllowAnyOrigin();

            var policyBuilder = new CorsPolicyBuilder();
            var policy = policyBuilder
                .AllowAnyOrigin()
                .AllowAnyHeader()
                .AllowAnyMethod()
                .Build();

            app.UseCors(Microsoft.Owin.Cors.CorsOptions.AllowAll);

            app.UseCors( cors => cors
                .AllowAnyMethod()
                .AllowAnyOrigin());


            // Should not report
            var SecCorsBuilder = new CorsPolicyBuilder();
            SecCorsBuilder.AllowAnyHeader();
            SecCorsBuilder.AllowAnyMethod();

            var SecPolicyBuilder = new CorsPolicyBuilder();
            var SecPolicy = SecPolicyBuilder
                .AllowAnyHeader()
                .AllowAnyMethod()
                .Build();

            app.UseCors( x => x
                .AllowAnyMethod()
                .AllowAnyHeader());
        }
    }
}
