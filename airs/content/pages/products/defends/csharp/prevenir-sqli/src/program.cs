using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Data;
using System.Data.SqlClient;

namespace FluidCode1{
  class Program{
    static void Main(string[] args){
      int Identificador = 1337;
      String DataConnectionString = "Server=localhost;Database=Fluidtest;User Id=fluidsignal;Password=V0mSeBaGgzF4_F7Xt6TWZ;";

        using (SqlConnection connection = new SqlConnection(DataConnectionString)){
          DataSet userDataset = new DataSet();
          SqlDataAdapter myCommand = new SqlDataAdapter("SELECT nombre, apellido FROM Autores WHERE au_id = @au_id", connection);
          myCommand.SelectCommand.Parameters.Add("@au_id", SqlDbType.VarChar, 11);
          myCommand.SelectCommand.Parameters["@au_id"].Value = Identificador;
          myDataAdapter.Fill(userDataset);
        }
    }
  }
}
