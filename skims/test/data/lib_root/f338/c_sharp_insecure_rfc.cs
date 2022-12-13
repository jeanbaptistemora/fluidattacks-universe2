namespace Controllers
{
    public class Encrypt
    {
        public static void Process(string password)
        {
            var salt = Encoding.UTF8.GetBytes("salt");
            var fromHardcoded = new Rfc2898DeriveBytes(password, salt);

            var fromPassword = new Rfc2898DeriveBytes(password, Encoding.UTF8.GetBytes("test"));

            var fromUnicode = new Rfc2898DeriveBytes(password, Encoding.Unicode.GetBytes("test"));
        }
    }
}
