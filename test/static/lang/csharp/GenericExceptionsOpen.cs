using System;
using System.Security.Cryptography;

public class GenericExceptionsOpen
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
      }
      MD5 md5 = System.Security.Cryptography.MD5.Create();
      byte[] inputBytes = System.Text.Encoding.ASCII.GetBytes(input);
      byte[] hash = md5.ComputeHash(inputBytes);

      byte[] data = new byte[DATA_SIZE];
      byte[] result;

      MD5CryptoServiceProvider md5Hasher = new MD5CryptoServiceProvider();
      byte[] data = md5Hasher.ComputeHash(Encoding.Default.GetBytes(input));

      SHA1 shaM = new SHA1Managed();
      result = shaM.ComputeHash(data);

      SHA1CryptoServiceProvider sha1Hasher = new SHA1CryptoServiceProvider();
      byte[] data = sha1Hasher.ComputeHash(Encoding.Default.GetBytes(input));

    }

    catch(ArithmeticException e)
    {
      Console.WriteLine("Warning: ArithmeticException");
    }

    catch(IndexOutOfRangeException e)
    {
      Console.WriteLine("Warning: ArrayIndexOutOfBoundsException");
    }

    catch(Exception e)
    {
      Console.WriteLine("Warning: Some Other exception");
    }

    try
    {
      Console.WriteLine("Out of try-catch block...");
    }
    catch
    {
      Console.WriteLine(e);
    }
    catch(Exception)
    {
      Console.WriteLine(e);
    }
    catch(NullReferenceException e)
    {
      Console.WriteLine(e);
    }
  }
}
