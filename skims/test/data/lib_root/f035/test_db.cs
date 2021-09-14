namespace Controllers
{
    public class DBaccess
    {
        public void dbauth()
        {
            DbContextOptionsBuilder optionsBuilder = new DbContextOptionsBuilder();
            con_str = "Server=myServerAddress;Database=myDataBase;User Id=myUsername;Password=";
            optionsBuilder.UseSqlServer(con_str);

            DbContextOptionsBuilder optionsBuilder2 = new DbContextOptionsBuilder();
            optionsBuilder2.UseSqlServer("Server=myServerAddress;Database=myDataBase;User Id=myUsername;Password=");
        }
    }
}
