namespace Controllers
{
    public class DBaccess
    {
        public void dbauth()
        {
            DbContextOptionsBuilder optionsBuilder = new DbContextOptionsBuilder();
            //insecure
            var con_str = "Server=myServerAddress;Database=myDataBase;User Id=myUsername;Password=";
            optionsBuilder.UseSqlServer(con_str);


            DbContextOptionsBuilder optionsBuilder2 = new DbContextOptionsBuilder();
            //insecure
            optionsBuilder2.UseSqlServer("Server=myServerAddress;Database=myDataBase;User Id=myUsername;Password=");

            DbContextOptionsBuilder optionsBuilder3 = new DbContextOptionsBuilder();
            //secure
            var con_str2 = "Server=myServerAddress;Database=myDataBase;User Id=myUsername;Password=5674_H5lloW0rld";
            optionsBuilder3.UseSqlServer(con_str2);
        }
    }
}
