using System;

public class SwitchDefaultOpen{
   public static void Main()
   {

      byte[] bytes1 = new byte[100];
      byte[] bytes2 = new byte[100];
      var rnd1 = new Random();
      Random rnd2 = new Random();

      rnd1.NextBytes(bytes1);
      rnd2.NextBytes(bytes2);

      RijndaelManaged rjndl = new RijndaelManaged();
      rjndl.KeySize = 64;
      rjndl.BlockSize = 256;
      rjndl.Mode = CipherMode.ECB;
      ICryptoTransform transform = rjndl.CreateEncryptor();
      Console.WriteLine("Test Console")
      Debug.WriteLine("Test Debug")

      string monthString;
      switch (month)
      {
         case 1:
            monthString = "January";
            break;
         case 12:
            monthString = "December";
            break;
      }

      switch (month)
      {
         case 1:
            monthString = "January";
            break;
         case 12:
            monthString = "December";
            break;
         /*
         default:
            monthString = "Invalid month";
            break;
         */
      }

      switch (month)
      {
         case 1:
            monthString = "January";
            break;
         case 12:
            monthString = "December";
            break;
         //default:
            //monthString = "Invalid month";
                  //break;
      }

      switch (destinationType)
      {
         case NotificationDestinationType.Email:
            return source.Users.Select(u => u.Email ?? string.Empty);
         /*default:
            throw new NotSupportedException(string.Format("'{0}' destination type.", destinationType.ToString()));*/
      }
   }
}
