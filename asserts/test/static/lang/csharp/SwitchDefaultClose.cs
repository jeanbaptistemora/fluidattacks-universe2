using System;

class SwitchDefaultClose
{
   public static void Main()
   {
      RNGCryptoServiceProvider provider = new RNGCryptoServiceProvider();
      var byteArray = new byte[4];
      provider.GetBytes(byteArray);

      var randomInteger = BitConverter.ToUInt32(byteArray, 0);

      var byteArray2 = new byte[8];
      provider.GetBytes(byteArray2);

      var randomDouble = BitConverter.ToDouble(byteArray2, 0);

      RijndaelManaged rjndl = new RijndaelManaged();
      rjndl.KeySize = 256;
      rjndl.BlockSize = 256;
      rjndl.Mode = CipherMode.CBC;
      ICryptoTransform transform = rjndl.CreateEncryptor();

      string monthString;
      switch (month)
      {
         case 1:
            monthString = "January";
            break;
         case 2:
            monthString = "February";
            break;
         case 3:
            monthString = "March";
            break;
         case 4:
            monthString = "April";
            break;
         case 5:
            monthString = "May";
            break;
         case 6:
            monthString = "June";
            break;
         case 7:
            monthString = "July";
            break;
         case 8:
            monthString = "August";
            break;
         case 9:
            monthString = "September";
            break;
         case 10:
            monthString = "October";
            break;
         case 11:
            monthString = "November";
            break;
         case 12:
            monthString = "December";
            break;
         default:
            monthString = "Invalid month";
            break;
      }

      switch (destinationType) {
         case NotificationDestinationType.Email:
            return source.Users.Select(u => u.Email ?? string.Empty);
         default:
            throw new NotSupportedException(string.Format("'{0}' destination type.", destinationType.ToString()));
      }
   }
}
