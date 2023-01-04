using System;

class cipher{

  public void Encrypt(byte[] key, byte[] data, MemoryStream target)
	{
    byte[] initializationVector = new byte[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16 };
		using var aes = new AesCryptoServiceProvider();
		var encryptor = aes.CreateEncryptor(key, initializationVector);

  }

  public override void Bad(HttpRequest req, HttpResponse resp)
  {
    string data;
    string[] names = data.Split('-');
    int successCount = 0;
    if (data != null)
    {
      try
      {
        using (SqlConnection dbConnection = IO.GetDBConnection())
        {
          badSqlCommand.Connection = dbConnection;

          if (existingStudent != null)
          {
              existingStudent.FirstName = student.FirstName;
              existingStudent.LastName = student.LastName;

              ctx.SaveChanges();
          }
          else
          {
              return NotFound();
          }

          for (int i = 0; i < names.Length; i++)
          {
              /* POTENTIAL FLAW: data concatenated into SQL statement used in CommandText, which could result in SQL Injection */
              badSqlCommand.CommandText += "update users set hitcount=hitcount+1 where name='" + names[i] + "';";
          }
          successCount += affectedRows;
          IO.WriteLine("Succeeded in " + successCount + " out of " + names.Length + " queries.");
        }
      }
      catch (SqlException exceptSql)
      {
        IO.Logger.Log(NLog.LogLevel.Warn, "Error getting database connection", exceptSql);
      }
      finally
      {
        IO.Logger.Log(NLog.LogLevel.Warn, "Error disposing SqlCommand", exceptSql);
      }
    }
  }
}

public class Test {

  public static void main(String[ ] args) {

    while(counter < 5) {
        System.out.println("Truck number: " + counter);
        counter++;
        for(int i=1; i<=5; i++){
          System.out.println("Truck Number: " + i + ", " + counter);
          if (counter % 2 == 0){
            break;
          }else{
            continue;
          }
          System.out.println("Truck Number: " + i + ", " + counter);
      }
      if (counter > 4){
        break;
      }
      System.out.println("Finish");
    }
    switch (age) {
        case 1:  System.out.println("You are one yr old");
                 break;
        case 2:  {
                 System.out.println("You are two yr old");
                 for(int i=1; i<=5; i++){
                  System.out.println("number :" + i);
                  if (i > 3){
                    break;
                    }
                 }
                 System.out.println("Finish");
              break;
            }
        case 3:  System.out.println("You are three yr old");
                 break;
        default: System.out.println("You are more than three yr old");
                 break;
    }

    int counter = 0;
    do {
        System.out.println("Inside the while loop, counting: " + counter);
        counter++;
        for(int i=1; i<=5; i++){
          System.out.println("number :" + i);
            for(int j=1; j<=5; j++){
              int counter = 0;
              while(counter < 5) {
                if(counter==3)
                {
                  System.out.println("Breaking the for loop.");
                  break;
                }
                  System.out.println("Inside the while loop, counting: " + counter);
                  counter++;
                if (counter == 4){
                  continue;
                }
              }
              System.out.println("number :" + j);
            }
        }
    } while(counter < 5);
	}
}
