using System;
using System.Security.Cryptography;

public class GenericExceptionsClose
{
  public static void Main()
  {
    try
    {
      int[] a = new int[7];
      a[4]=30/0;
      Console.WriteLine("First print statement in try block");
      if (a > 5) {
        Console.WriteLine("Big num")
      } else {
        Console.WriteLine("Small num")
      }
    }

    catch(ArithmeticException e)
    {
      Console.WriteLine("Warning: ArithmeticException");
    }

    catch(IndexOutOfRangeException e)
    {
      Console.WriteLine("Warning: ArrayIndexOutOfBoundsException");
    }
/*
    try
    {
      Console.WriteLine("Out of try-catch block...");
      if (a > 5) {
        Debug.WriteLine("Big num")
      }
      MD5 md5 = System.Security.Cryptography.MD5.Create();
      byte[] inputBytes = System.Text.Encoding.ASCII.GetBytes(input);
      byte[] hash = md5.ComputeHash(inputBytes);

      MD5CryptoServiceProvider md5Hasher = new MD5CryptoServiceProvider();
      byte[] data = md5Hasher.ComputeHash(Encoding.Default.GetBytes(input));

      SHA1 shaM = new SHA1Managed();
      result = shaM.ComputeHash(data);
    }

    catch(Exception e)
    {
      Console.WriteLine("Warning: Some Other exception");
    }
*/
  }
}
