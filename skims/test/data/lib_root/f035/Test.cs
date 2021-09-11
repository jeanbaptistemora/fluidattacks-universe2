public class Startup
{
    public void start(IServiceCollection services)
    {
        services.Configure<IdentityOptions>( options =>
        {
            options.Password.RequireDigit = true;
            options.Password.RequireDigit = false;
            options.Password.RequiredLength = 8;
            options.Password.RequireNonAlphanumeric = true;
            options.Password.RequireUppercase = true;
            options.Password.RequireLowercase = true;
            options.Password.RequiredUniqueChars = 5;
        });
    }
}
